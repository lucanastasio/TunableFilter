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

from enum import Enum
from warnings import warn


class Channel:
	# bit mask for reading the channel number
	DAC_READ_BITS = 0x30
	# number of right shifts to read the channel number in decimal
	DAC_READ_SHIFT = 4
	# this bit is set to 1 when reading from EEPROM or 0 when reading from registers
	EEPROM_READ_BIT = 0x08
	# DAC binary code least significant bits mask
	CODE_LSBITS_MASK = 0x0F
	# byte order used with the DAC binary code
	ORD = 'big'
	# first element of a list is considered most significant byte in 'big' ordering
	MSB = 0
	LSB = 1

	CMD_FAST_WR = 0x00

	class VrefSel(Enum):
		VDD = 0x0
		INT = 0x1
		MASK = 0x80

	class GainSel(Enum):
		X1 = 0x0
		X2 = 0x1
		MASK = 0x10

	class PowerSel(Enum):
		ON = 0x0
		DOWN_1K = 0x1
		DOWN_100K = 0x2
		DOWN_500K = 0x3
		MASK = 0x60

	def __init__(self, channelSel=0x00, parentDac=None):
		"""
		:param channelSel: channel number selection
		:type channelSel: int
		:param parentDac: MCP4728 DAC the channel belongs to
		:type parentDac: MCP4728.MCP4728
		"""
		self.vout = 0.0
		self.code = 0
		self.step = 2.048 / 4096
		self.channelSel = channelSel
		self.vref = 2.048
		self.vrefSel = self.VrefSel.INT.value
		self.gainSel = self.GainSel.X1.value
		self.powerSel = self.PowerSel.ON.value
		self.parentDac = parentDac

	def getVrefIndex(self):
		if self.vrefSel == self.VrefSel.VDD.value:
			return 2
		if self.gainSel == self.GainSel.X2.value:
			return 1
		return 0

	def setVref(self, newVal):
		if (newVal > 5.5) or (newVal < 2.7) and newVal != 2.048:
			warn('Vref outside of Vdd range, are you sure?')
		self.vref = newVal
		self.step = newVal / 4096
		self.vout = self.code * self.step
		self.vrefSel = self.VrefSel.INT.value if (newVal == 2.048 or newVal == 4.096) else self.VrefSel.VDD.value
		self.gainSel = self.GainSel.X2.value if (newVal == 4.096) else self.GainSel.X1.value
		if self.parentDac:
			self.parentDac.WriteGain()
			self.parentDac.WriteVref()

	def setVout(self, newVal):
		if (newVal > self.vref) or (newVal < 0):
			raise AttributeError('Voltage outside of Vref range')
		self.vout = newVal
		self.code = int(newVal / self.step)
		if self.parentDac:
			self.parentDac.MultiWrite([self.channelSel])

	def setCode(self, newVal):
		if (newVal > 4095) or (newVal < 0):
			raise AttributeError('DAC code outside of 0-4095 range')
		self.code = int(newVal)
		self.vout = newVal * self.step
		if self.parentDac:
			self.parentDac.MultiWrite([self.channelSel])

	def setStep(self, newVal):
		if (newVal > 5.5 / 4096) or (newVal < 2.048 / 4096):
			warn('Step outside of allowable range, are you sure?')
		self.setVref(newVal * 4096)

	def setPower(self, newVal):
		if isinstance(newVal, self.PowerSel):
			self.powerSel = newVal.value
		elif isinstance(newVal, (str, int)):
			self.powerSel = self.PowerSel[newVal].value
		else:
			raise TypeError
		if self.parentDac:
			self.parentDac.WritePower()

	def EncodeFast(self):
		"""
		Encode into binary data for the FastWrite method
		:return: encoded channel data
		"""
		code = self.code.to_bytes(2, self.ORD)
		data = [(self.CMD_FAST_WR | self.powerSel << 4 | code[self.MSB]), code[self.LSB]]
		return data

	def Encode(self):
		"""
		Encode into binary data for transmission
		:return: encoded channel data
		"""
		code = self.code.to_bytes(2, self.ORD)
		data = [(self.vrefSel << 7 | self.powerSel << 5 | self.gainSel << 4 | code[self.MSB]), code[self.LSB]]
		return data

	def Decode(self, data):
		"""
		Decode binary data read form the IC into readable format
		:param data: binary data to be decoded
		:type data: byte list of length 3
		:return: the new Channel instance
		"""
		self.channelSel = (data[0] & self.DAC_READ_BITS) >> self.DAC_READ_SHIFT
		self.vrefSel = int(bool(data[1] & self.VrefSel.MASK.value))
		self.powerSel = int(bool(data[1] & self.PowerSel.MASK.value))
		self.gainSel = int(bool(data[1] & self.GainSel.MASK.value))
		self.code = int.from_bytes([(data[1] & self.CODE_LSBITS_MASK), data[2]], 'big')
		vref = [2.048, 4.096, 0.0]
		self.setVref(vref[self.getVrefIndex()])
