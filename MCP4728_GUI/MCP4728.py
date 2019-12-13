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


class Channel:
	VREF_VDD = 0x0
	VREF_INT = 0x1
	VREF_INT_BIT = 0x80
	GAIN_X2_BIT = 0x10
	GAIN_X1 = 0x0
	GAIN_X2 = 0x1
	PWR = {
		'POWER_ON': 0x0,
		'DOWN_1K': 0x1,
		'DOWN_100K': 0x2,
		'DOWN_500K': 0x3
	}
	PWR_MSK = 0x60
	PWR_BITS = {
		'POWER_ON': 0x00,
		'DOWN_1K': 0x20,
		'DOWN_100K': 0x40,
		'DOWN_500K': 0x60
	}
	LSBITS = 0x0F

	def __init__(self, dacSel, dac=None):
		self.voltage = 0.0
		self.code = 0
		self.codeChanged = False
		self.step = 0.0
		self.dacSel = dacSel
		self.vrefValue = 0.0
		self.vrefSel = None
		self.gainSel = None
		self.powerDownSel = None
		self.vrefChanged = False
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
		data = list(MCP4728.cmd['FAST_WR'] | (self.powerDownSel >> 1) | code[0])
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

	@staticmethod
	def Decode(data):
		"""
		Decode binary data read form the IC into readable format
		:param data: binary data to be decoded
		:type data: byte list of length 3
		:return: the new Channel instance
		"""
		if bool(data[0] & MCP4728.ZERO_BIT):
			raise IOError('Unexpected value')
		ch = Channel((data[0] & MCP4728.DAC_BITS) >> 4)
		ch.vrefSel = data[1] & Channel.VREF_INT_BIT
		ch.powerDownSel = data[1] & Channel.PWR_MSK
		ch.gainSel = data[1] & Channel.GAIN_X2_BIT
		ch.code = int.from_bytes([(data[1] & Channel.LSBITS), data[2]], 'big')
		return ch


class Channels:
	def __init__(self, dac):
		self.ch = [
			Channel(0x0, dac),
			Channel(0x1, dac),
			Channel(0x2, dac),
			Channel(0x3, dac)
		]
		self.A = Channel(0x0, dac)
		self.B = Channel(0x1, dac)
		self.C = Channel(0x2, dac)
		self.D = Channel(0x3, dac)
	def __iter__(self):
		self.i = 0
		return self
	#def __next__(self):
	#	if self.i == 0:


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
	cmd = {
		'FAST_WR': 0x00,
		'MULT_WR': 0x40,
		'SING_WR': 0x58,
		'SEQ_WR': 0x50,
		'SEL_VREF': 0x80,
		'SEL_GAIN': 0xC0,
		'SEL_PWR': 0xA0,
		'GEN_RST': 0x06,
		'GEN_WAKE': 0x09,
		'GEN_UPD': 0x08,
		'GEN_ADDR': 0x0C
	}
	DEV_CODE = 0x60  # or base address
	RDY_BIT = 0x80
	POR_BIT = 0x40
	ADDR_BITS = 0x07
	DAC_BITS = 0x30
	ZERO_BIT = 0x08

	def __init__(self, bus=None, address=DEV_CODE, addrBits=None):
		self.address = address | addrBits
		self.i2c = SMBus(bus)
		self.channel = {'A': Channel(0x0, self),
						'B': Channel(0x1, self),
						'C': Channel(0x2, self),
						'D': Channel(0x3, self)}
		self.Channels = Channels(self)
		self.EEPROMready = None
		self.VddGood = None

	def SetBus(self, bus):
		pass

	def SetAddress(self, address):
		pass

	def FastWrite(self):
		"""
		Writes all 4 channels' input data and power down registers (EEPROM not affected)
		NOTE: Doesn't update Vout (output data registers), use LDAC pin or GeneralCallSoftwareUpdate()
		"""
		data = []
		for c in 'ABCD':
			data.extend(self.channel[c].EncodeFast())
		msg = i2c_msg.write(self.address, data)
		self.i2c.i2c_rdwr(msg)

	def MultiWrite(self, channels='ABCD', update=True):
		"""
		Writes the selected channel(s) register(s) (EEPROM not affected)
		(including: data input register, gain, power down, Vref)
		Also determines if Vout gets updated or not
		:param channels: the channel(s) to write (e.g. 'ABCD' (default) or 'ABC' or 'CD' or 'B' and combinations)
		:type channels: str
		:param update: trigger an update of Vout if True, else just write register
		:type update: bool
		"""
		data = []
		for c in channels:
			ch = self.channel[c]
			data.append(MCP4728.cmd['MULT_WR'] | (ch.dacSel << 1) | int(not update))
			data.extend(ch.Encode())
		msg = i2c_msg.write(self.address, data)
		self.i2c.i2c_rdwr(msg)

	def SequentialWrite(self, start='A', update=True):
		"""
		Writes registers and EEPROM starting from the given channel to channel D
		:param start: the starting channel (e.g. 'A' (default) or 'B' or 'C' or 'D')
		:type start: str
		:param update: trigger an update of Vout if True, else just write registers and EEPROM
		:type update: bool
		"""
		data = [(MCP4728.cmd['SEQ_WR'] | self.channel[start].dacSel << 1 | int(not update))]
		for c in range(ord(start), ord('D')+1):
			data.extend(self.channel[chr(c)].Encode())
		msg = i2c_msg.write(self.address, data)
		self.i2c.i2c_rdwr(msg)

	def SingleWrite(self, channel, update=True):
		"""
		Writes registers and EEPROM only for the given channel
		:param channel: channel to write (e.g. 'A' or 'B' or 'C' or 'D')
		:type channel: str
		:param update: trigger an update of Vout if True, else just write registers and EEPROM
		:type update: bool
		"""
		ch = self.channel[channel]
		data = [(MCP4728.cmd['SING_WR'] | ch.dacSel << 1 | int(not update))]
		code = ch.code.to_bytes(2, 'big')
		data.append(ch.vrefSel | ch.powerDownSel | ch.gainSel | code[0])
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
		data = MCP4728.Cmd.SEL_VREF
		pass

	def WriteGain(self):
		"""
		Writes Gain selection bits, does not affect EEPROM
		"""
		pass

	def WritePower(self):
		"""
		Writes Power selection bits, does not affect EEPROM
		"""
		pass

	def ReadAll(self, Restore=None):
		"""
		Reads registers or EEPROM contents and optionally saves values in current instance
		:param Restore: which contents to restore, either None (default), 'registers' or 'EEPROM'
		:type Restore: str
		:return: dict of channels ('registers' and 'EEPROM' keys)
		"""
		msg = i2c_msg.read(self.address, 24)
		# in case it doesn't work, try to split in messages of 3 bytes each
		self.i2c.i2c_rdwr(msg)
		msg = bytes(msg)
		self.ReadStatus(msg[0])
		ch = []
		for i in range(0, 23, 3):
			ch.append(Channel.Decode(msg[i:i+3]))
		ret = {}
		for c in range(0, 3):
			ret['registers'][chr(ord('A') + c)] = ch[2*c]
			ret['EEPROM'][chr(ord('A') + c)] = ch[(2*c)+1]
		if Restore:
			self.channel = ret[Restore]
		return ret

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

	@staticmethod
	def GeneralCallReset():
		"""

		"""
		pass

	@staticmethod
	def GeneralCallWakeUp():
		"""

		"""
		pass

	@staticmethod
	def GeneralCallSoftwareUpdate():
		"""

		"""
		pass

	@staticmethod
	def GeneralCallReadAddress():
		"""
		Unimplemented, requires dedicated pin
		"""
		pass
