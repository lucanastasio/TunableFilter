"""
MCP4728 Python Library
Copyright (C) 2019 Luca Anastasio
<anastasio.lu@gmail.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from smbus2 import SMBus, i2c_msg
from enum import Enum


class MCP4728:
	class Cmd(Enum):
		FAST_WR = 0x00
		MULT_WR = 0x40
		SING_WR = 0x58
		SEQ_WR = 0x50
		SEL_VREF = 0x80
		SEL_GAIN = 0xC0
		SEL_PWR = 0xA0
		GEN_RST = 0x06
		GEN_WAKE = 0x09
		GEN_UPD = 0x08
		GEN_ADDR = 0x0C

	from .MCP4728DAC import DAC

	# first element = select bit value, second = binary value of the bit in position
	BIT = 0
	VAL = 1

	DEV_CODE = 0x60  # or base address
	RDY_BIT = 0x80
	POR_BIT = 0x40
	ADDR_BITS = 0x07
	# this bit is set to 1 when reading from EEPROM or 0 when reading from registers
	EEPROM_READ_BIT = 0x08

	def __init__(self, bus=None, address=DEV_CODE, addrBits=0x00, update=None):
		self.address = address | addrBits
		if isinstance(bus, str):
			bus = None if len(bus) == 0 else bus
		self.i2c = SMBus(bus)
		self.channel = self.DAC(parentDac=self)
		self.EEPROMready = None
		self.VddGood = None
		self.update = update

	def SetBus(self, bus):
		if self.i2c.fd is not None:
			self.i2c.close()
		self.i2c.open(bus)

	def SetAddressBits(self, addrBits):
		self.address = self.DEV_CODE | addrBits

	def FastWrite(self, update=None):
		"""
		Writes all 4 channels' input data and power down registers (EEPROM not affected)
		NOTE: Doesn't update Vout (output data registers), use LDAC pin or GeneralCallSoftwareUpdate()
		:param update: force (enable or disable) writing registers, defaults to self.update if None
		:type update: bool
		"""
		if self.trigger(update):
			data = []
			for channel in self.channel:
				data.extend(channel.EncodeFast())
			msg = i2c_msg.write(self.address, data)
			self.i2c.i2c_rdwr(msg)

	def MultiWrite(self, channelList, update=None):
		"""
		Writes the selected channel(s) register(s) (EEPROM not affected)
		(including: data input register, gain, power down, Vref)
		Also determines if Vout gets updated or not
		:param channelList: the channel(s) to write (e.g. 'AB...' or (0,1,...))
		:type channelList: str or list of int
		:param update: trigger an update of Vout if True, else just write register, defaults to self.update
		:type update: bool
		"""
		trig = self.triggerBit(update)
		data = []
		for c in channelList:
			channel = self.channel[c]
			data.append(self.Cmd.MULT_WR.value | (channel.channelSel << 1) | trig)
			data.extend(channel.Encode())
		msg = i2c_msg.write(self.address, data)
		self.i2c.i2c_rdwr(msg)

	def SequentialWrite(self, start='A', update=None):
		"""
		Writes registers and EEPROM starting from the given channel to channel D
		:param start: the starting channel (e.g. 'A' (default) or B,C,D; 0 or 1,2,3 etc...)
		:type start: str or int
		:param update: trigger an update of Vout if True, else just write registers and EEPROM
		:type update: bool
		"""
		trig = self.triggerBit(update)
		start = int(ord(start) - ord('A')) if isinstance(start, str) else start
		data = [(self.Cmd.SEQ_WR.value | self.channel[start].channelSel << 1 | trig)]
		for c in range(start, 4):
			data.extend(self.channel[c].Encode())
		msg = i2c_msg.write(self.address, data)
		self.i2c.i2c_rdwr(msg)

	def SingleWrite(self, channel, update=None):
		"""
		Writes registers and EEPROM only for the given channel
		:param channel: channel to write (e.g. 'A' or 'B' or 'C' or 'D')
		:type channel: str
		:param update: trigger an update of Vout if True, else just write registers and EEPROM
		:type update: bool
		"""
		trig = self.triggerBit(update)
		channel = self.channel[channel]
		data = [(self.Cmd.SING_WR.value | channel.channelSel << 1 | trig), channel.Encode()]
		msg = i2c_msg.write(self.address, data)
		self.i2c.i2c_rdwr(msg)

	def WriteAddressBits(self, newaddr):
		"""
		Unimplemented, requires dedicated pin
		"""
		pass

	def WriteVref(self, update=None):
		"""
		Writes Vref selection bits, does not affect EEPROM
		:param update: force (enable or disable) an update, defaults to self.update if None
		:type update: bool
		"""
		if self.trigger(update):
			data = self.Cmd.SEL_VREF.value >> 4
			for channel in self.channel:
				data <<= 1
				data |= channel.vrefSel
			self.i2c.write_byte(self.address, data)

	def WriteGain(self, update=None):
		"""
		Writes Gain selection bits, does not affect EEPROM
		:param update: force (enable or disable) an update, defaults to self.update if None
		:type update: bool
		"""
		if self.trigger(update):
			data = self.Cmd.SEL_GAIN.value >> 4
			for channel in self.channel:
				data <<= 1
				data |= channel.gainSel
			self.i2c.write_byte(self.address, data)

	def WritePower(self, update=None):
		"""
		Writes Power selection bits, does not affect EEPROM
		:param update: force (enable or disable) an update, defaults to self.update if None
		:type update: bool
		"""
		if self.trigger(update):
			data = self.Cmd.SEL_PWR.value >> 4
			for channel in self.channel:
				data <<= 2
				data |= channel.powerSel
			data <<= 4
			msg = i2c_msg.write(self.address, list(data.to_bytes(2, 'big')))
			self.i2c.i2c_rdwr(msg)

	def ReadAll(self, restore=None):
		"""
		Reads registers or EEPROM contents and optionally saves values in current instance
		:param restore: which contents to restore, either None (default), 'R' or 0 for registers and 'E' or 1 for EEPROM
		:type restore: str
		:return: list of DAC objects [registers, EEPROM]
		"""
		msg = i2c_msg.read(self.address, 24)
		self.i2c.i2c_rdwr(msg)
		msg = bytes(msg)
		self.ReadStatus(msg[0])
		reg = self.DAC()
		eep = self.DAC()

		for i in range(0, 24, 3):
			channel = self.DAC.Channel(parentDac=self)
			channel.Decode(msg[i:i + 3])
			if bool(msg[i] & self.EEPROM_READ_BIT) is True:
				eep[channel.channelSel] = channel
			else:
				reg[channel.channelSel] = channel

		if restore == 'R' or 0:
			self.channel = reg
		elif restore == 'E' or 1:
			self.channel = eep
		return [reg, eep]

	def ReadStatus(self, sByte=None):
		"""
		Quickly reads status bits only and saves values in the current instance
		(updates EEPROMready and VddGood fields)
		:param sByte: optional (default None) for internal reading
		:type sByte: byte
		"""
		if sByte is None:
			sByte = self.i2c.read_byte(self.address)
		self.EEPROMready = bool(sByte & MCP4728.RDY_BIT)
		self.VddGood = bool(sByte & MCP4728.POR_BIT)

	@staticmethod
	def DecodeStatus(statusByte):
		return {'RDY': bool(statusByte & MCP4728.RDY_BIT),
				'POR': bool(statusByte & MCP4728.POR_BIT),
				'addrBits': statusByte & MCP4728.ADDR_BITS}


	def GeneralCallReset(self):
		"""
		Resets devices on bus, devices load EEPROM values afeter reset
		"""
		#self.i2c.write_byte(i2c_addr=0x00, value=self.Cmd.GEN_RST.value)
		pass

	def GeneralCallWakeUp(self):
		"""
		Resets power down bits for all channels to 00
		"""
		#self.i2c.write_byte(i2c_addr=0x00, value=self.Cmd.GEN_WAKE.value)
		pass

	def GeneralCallSoftwareUpdate(self):
		"""
		Updates all channels' outputs simultaneously
		"""
		#self.i2c.write_byte(i2c_addr=0x00, value=self.Cmd.GEN_UPD.value)
		pass

	@staticmethod
	def GeneralCallReadAddress():
		"""
		Unimplemented, requires dedicated pin
		"""
		pass

	def trigger(self, update):
		return update if (update is not None) else self.update

	def triggerBit(self, update):
		return int(not (update if (update is not None) else self.update))
