#  Copyright (c) 2019 Luca Anastasio
#  anastasio.lu(at)gmail.com
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
# TODO: correct usage of channel configuration bits
from enum import Enum
from warnings import warn


class Channel:

	from MCP4728 import Cmd

	# first element = select bit value, second element = binary value of the bit in position
	BIT = 0
	VAL = 1
	# byte order used with the DAC binary code
	ORD = 'big'
	# first element of a list is considered most significant byte in 'big' ordering
	MSB = 0
	LSB = 1

	class ChannelSel(Enum):
		A = [0x0, 0x00]
		B = [0x1, 0x02]
		C = [0x2, 0x04]
		D = [0x3, 0x06]
		MASK = 0x06

	class VrefSel(Enum):
		VDD = [0x0, 0x00]
		INT = [0x1, 0x80]
		MASK = 0x80

	class GainSel(Enum):
		X1 = [0x0, 0x00]
		X2 = [0x1, 0x10]
		MASK = 0x10

	class PowerSel(Enum):
		ON = [0x0, 0x00]
		DOWN_1K = [0x1, 0x20]
		DOWN_100K = [0x2, 0x40]
		DOWN_500K = [0x3, 0x60]
		MASK = 0x60

	def __init__(self, channelSel=0x00, parent=None):
		"""
		:param channelSel: channel number selection
		:type channelSel: int
		:param parent: MCP4728 DAC the channel belongs to
		:type parent: MCP4728.MCP4728
		"""
		self.vout = 0.0
		self.code = 0
		self.step = 0.0
		self.channelSel = channelSel
		self.vref = 0.0
		self.vrefSel = self.vrefSel.INT.value
		self.gainSel = self.GainSel.X1.value
		self.powerSel = self.PowerSel.ON.value
		self.parent = parent

	def setVref(self, newVal):
		if (newVal > 5.5) or ((newVal < 2.7) and newVal is not 2.048):
			warn('Vref outside of Vdd range, are you sure?')
		self.__dict__['vref'] = newVal
		self.__dict__['step'] = newVal / 4096
		self.__dict__['vout'] = self.code * self.step
		self.__dict__['vrefSel'] = self.vrefSel.INT.value if newVal is 2.048 or 4.096 else self.vrefSel.VDD.value
		self.__dict__['gainSel'] = self.GainSel.X2.value if newVal is 4.096 else self.GainSel.X1.value
		self.parent.WriteGain()
		self.parent.WriteVref()

	def setVout(self, newVal):
		if (newVal > self.vref) or (newVal < 0):
			raise AttributeError('Voltage outside of Vref range')
		self.__dict__['vout'] = newVal
		self.__dict__['code'] = newVal / self.step
		if self.parent.update:
			self.parent.MultiWrite([self.channelSel])

	def setCode(self, newVal):
		if (newVal > 4095) or (newVal < 0):
			raise AttributeError('DAC code outside of 0-4095 range')
		self.__dict__['code'] = newVal
		self.__dict__['vout'] = newVal * self.step
		if self.parent.update:
			self.parent.MultiWrite([self.channelSel])

	def setStep(self, newVal):
		if (newVal > 5.5 / 4096) or (newVal < 2.048 / 4096):
			warn('Step outside of allowable range, are you sure?')
		self.setVref(newVal * 4096)

	def setPower(self, newVal):
		if isinstance(newVal, self.PowerSel):
			self.__dict__['powerSel'] = newVal.value
		elif isinstance(newVal, str):
			self.__dict__['powerSel'] = self.PowerSel[newVal].value

	def __setattr__(self, key, value):
		if key is 'Vref':
			self.setVref(value)
		elif key is 'vout':
			self.setVout(value)
		elif key is 'code':
			self.setCode(value)
		elif key is 'step':
			self.setStep(value)
		elif key is 'power':
			self.setPower(value)
		else:
			self.__dict__[key] = value

	def getVref(self, bitOrVal):
		return self.__dict__['vrefSel'][bitOrVal]

	def __getattr__(self, item):
		if item is 'vrefBit':
			return self.getVref(self.BIT)
		elif item is 'vrefVal':
			return self.getVref(self.VAL)
		elif item is 'vrefBit':
			return self.__dict__['vrefSel'][self.BIT]
		elif item is 'vrefVal':
			return self.__dict__['vrefSel'][self.VAL]
		else:
			return self.__dict__[item]

	def EncodeFast(self):
		"""
		Encode into binary data for the FastWrite method
		:return: encoded channel data
		"""
		code = self.code.to_bytes(2, self.ORD)
		data = list(self.Cmd.FAST_WR.value | (self.powerSel[self.VAL] >> 1) | code[self.MSB])
		data.append(code[self.LSB])
		return data

	def Encode(self):
		"""
		Encode into binary data for transmission
		:return: encoded channel data
		"""
		code = self.code.to_bytes(2, self.ORD)
		data = list(self.vrefSel[self.VAL] | self.powerSel[self.VAL] | self.gainSel[self.VAL] | code[self.MSB])
		data.append(code[self.LSB])
		return data
