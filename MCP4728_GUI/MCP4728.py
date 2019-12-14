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

	DEV_CODE = 0x60  # or base address
	RDY_BIT = 0x80
	POR_BIT = 0x40
	ADDR_BITS = 0x07
	DAC_BITS = 0x30
	ZERO_BIT = 0x08

	def __init__(self, bus=None, address=DEV_CODE, addrBits=0x00, update=True):
		self.address = address | addrBits
		self.i2c = SMBus(bus)
		self.Channels = MCP4728.DAC(dac=self)
		self.EEPROMready = None
		self.VddGood = None
		self.update = update

	def SetBus(self, bus):
		if self.i2c.fd is not None:
			self.i2c.close()
		self.i2c.open(bus)

	def SetAddress(self, address):
		self.address = address

	def SetAddressBits(self, addrBits):
		self.address = self.DEV_CODE | addrBits

	def FastWrite(self):
		"""
		Writes all 4 channels' input data and power down registers (EEPROM not affected)
		NOTE: Doesn't update Vout (output data registers), use LDAC pin or GeneralCallSoftwareUpdate()
		"""
		data = []
		for channel in self.Channels:
			data.extend(channel.EncodeFast())
		msg = i2c_msg.write(self.address, data)
		self.i2c.i2c_rdwr(msg)

	def MultiWrite(self, channelList='ABCD', update=None):
		"""
		Writes the selected channel(s) register(s) (EEPROM not affected)
		(including: data input register, gain, power down, Vref)
		Also determines if Vout gets updated or not
		:param channelList: the channel(s) to write (e.g. 'ABCD' (default) or 'ABC' or 'CD' or 'B' and combinations)
		:type channelList: str
		:param update: trigger an update of Vout if True, else just write register, defaults to self.update
		:type update: bool
		"""
		update = int(not (update if update is not None else self.update))
		data = []
		for c in channelList:
			channel = self.Channels[c]
			data.append(MCP4728.Cmd.MULT_WR.value | (channel.dacSel << 1) | update)
			data.extend(channel.Encode())
		msg = i2c_msg.write(self.address, data)
		self.i2c.i2c_rdwr(msg)

	def SequentialWrite(self, start='A', update=None):
		"""
		Writes registers and EEPROM starting from the given channel to channel D
		:param start: the starting channel (e.g. 'A' (default) or 'B' or 'C' or 'D')
		:type start: str
		:param update: trigger an update of Vout if True, else just write registers and EEPROM
		:type update: bool
		"""
		update = int(not (update if update is not None else self.update))
		data = [(MCP4728.Cmd.SEQ_WR.value | self.Channels[start].dacSel << 1 | update)]
		for c in range(ord(start), ord('D')+1):
			data.extend(self.Channels[chr(c)].Encode())
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
		update = int(not (update if update is not None else self.update))
		channel = self.Channels[channel]
		data = [(MCP4728.Cmd.SING_WR.value | channel.dacSel << 1 | update)]
		code = channel.code.to_bytes(2, 'big')
		data.append(channel.vrefSel | channel.powerDownSel | channel.gainSel | code[0])
		data.append(code[1])
		msg = i2c_msg.write(self.address, data)
		self.i2c.i2c_rdwr(msg)

	def WriteAddressBits(self, newaddr):
		"""
		Unimplemented, requires dedicated pin
		"""
		pass

	def WriteVref(self):
		"""
		Writes Vref selection bits, does not affect EEPROM
		"""
		data = MCP4728.Cmd.SEL_VREF.value >> 3
		for channel in self.Channels:
			data = (data | channel.vrefSel) << 1
		self.i2c.write_byte(self.address, data)

	def WriteGain(self):
		"""
		Writes Gain selection bits, does not affect EEPROM
		"""
		data = MCP4728.Cmd.SEL_GAIN.value >> 3
		for channel in self.Channels:
			data = (data | channel.gainSel) << 1
		self.i2c.write_byte(self.address, data)
		pass

	def WritePower(self):
		"""
		Writes Power selection bits, does not affect EEPROM
		"""
		data = MCP4728.Cmd.SEL_PWR.value | (self.Channels.A.powerDownSel << 2) | self.Channels.B.powerDownSel
		data[1] = (self.Channels.C.powerDownSel <<  6) | (self.Channels.D.powerDownSel << 4)
		pass

	def ReadAll(self, Restore=None):
		"""
		Reads registers or EEPROM contents and optionally saves values in current instance
		:param Restore: which contents to restore, either None (default), 'R' or 0 for registers and 'E' or 1 for EEPROM
		:type Restore: str
		:return: list of DAC objects [registers. EEPROM]
		"""
		msg = i2c_msg.read(self.address, 24)
		# TODO: in case it doesn't work, try to split in messages of 3 bytes each
		self.i2c.i2c_rdwr(msg)
		msg = bytes(msg)
		self.ReadStatus(msg[0])
		reg = MCP4728.DAC()
		eep = MCP4728.DAC()
		for i in range(0, 23, 6):
			reg.Decode(msg[i:i+3])
			eep.Decode(msg[i+3:i+6])
		if Restore is 'R' or 0:
			self.Channels = reg
		elif Restore is 'E' or 1:
			self.Channels = eep
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
		self.i2c.write_byte(i2c_addr=0x00, value=MCP4728.Cmd.GEN_RST.value)

	def GeneralCallWakeUp(self):
		"""
		Resets power down bits for all channels to 00
		"""
		self.i2c.write_byte(i2c_addr=0x00, value=MCP4728.Cmd.GEN_WAKE.value)

	def GeneralCallSoftwareUpdate(self):
		"""
		Updates all channels' outputs simultaneously
		"""
		self.i2c.write_byte(i2c_addr=0x00, value=MCP4728.Cmd.GEN_UPD.value)

	@staticmethod
	def GeneralCallReadAddress():
		"""
		Unimplemented, requires dedicated pin
		"""
		pass

	class DAC:

		def __init__(self, dac=None):
			self.A = self.Channel(0x0, dac)
			self.B = self.Channel(0x1, dac)
			self.C = self.Channel(0x2, dac)
			self.D = self.Channel(0x3, dac)

		def __iter__(self):
			for i in 'ABCD':
				yield self[i]

		def __getitem__(self, item):
			if isinstance(item, str):
				return self.__dict__[item]
			elif isinstance(item, int):
				return self.__dict__[chr(item + ord('a'))]

		def __setitem__(self, key, value):
			if isinstance(key, str):
				self.__dict__[key] = value
			elif isinstance(key, int):
				self.__dict__[chr(key + ord('a'))] = value

		def Decode(self, data):
			"""
			Decode binary data read form the IC into readable format
			:param data: binary data to be decoded
			:type data: byte list of length 3
			:return: the new Channel instance
			"""
			if (data[0] & MCP4728.ZERO_BIT) is not 0:
				raise IOError('Unexpected value')
			dacSel = (data[0] & MCP4728.DAC_BITS) >> 4
			channel = self.Channel(dacSel)
			channel.vrefSel = data[1] & self.Channel.VREF_INT_BIT
			channel.powerDownSel = data[1] & self.Channel.PWR_MSK
			channel.gainSel = data[1] & self.Channel.GAIN_X2_BIT
			channel.code = int.from_bytes([(data[1] & self.Channel.LSBITS), data[2]], 'big')
			self[dacSel] = channel

		class Channel:
			VREF_VDD = 0x0
			VREF_INT = 0x1
			VREF_INT_BIT = 0x80
			GAIN_X2_BIT = 0x10
			GAIN_X1 = 0x0
			GAIN_X2 = 0x1
			PWR = {
				'POWER_ON' : 0x0,
				'DOWN_1K'  : 0x1,
				'DOWN_100K': 0x2,
				'DOWN_500K': 0x3
			}
			PWR_MSK = 0x60
			PWR_BITS = {
				'POWER_ON' : 0x00,
				'DOWN_1K'  : 0x20,
				'DOWN_100K': 0x40,
				'DOWN_500K': 0x60
			}
			LSBITS = 0x0F

			def __init__(self, dacSel=0x00, dac=None):
				self.voltage = 0.0
				self.code = 0
				self.step = 0.0
				self.dacSel = dacSel
				self.vrefValue = 0.0
				self.vrefSel = None
				self.vrefBit = None
				self.gainSel = None
				self.gainBit = None
				self.powerDownSel = None
				self.powerDownBits = None
				self.dac = dac

			def Vref(self, value, update):
				pass

			def Vref2048(self, update):
				self.vrefValue = 2.048
				self.step = 0.0005
				self.voltage = self.code * self.step
				if update:
					self.dac.Vref2048(self.dacSel)

			def Vref4096(self, update):
				self.vrefValue = 4.096
				self.step = 0.001
				self.voltage = self.code * self.step
				if update:
					self.dac.Vref4096(self.dacSel)

			def VrefVdd(self, vdd, update):

				self.vrefValue = vdd
				self.step = vdd / 4096
				self.voltage = self.code * self.step
				if update:
					self.dac.VrefVdd(self.dacSel)

			def EncodeFast(self):
				"""
				Encode into binary data for the FastWrite method
				:return: encoded channel data
				"""
				code = self.code.to_bytes(2, 'big')
				data = list(MCP4728.Cmd.FAST_WR.value | (self.powerDownSel >> 1) | code[0])
				data.append(code[1])
				return data

			def Encode(self):
				"""
				Encode into binary data for transmission
				:return: encoded channel data
				"""
				code = self.code.to_bytes(2, 'big')
				data = list(self.vrefSel | self.powerDownSel | self.gainSel | code[0])
				data.append(code[1])
				return data
