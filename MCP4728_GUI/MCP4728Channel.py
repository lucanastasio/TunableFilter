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


class Channel:

	from MCP4728 import Cmd

	# first element = select bit
	# second element = binary value of the bit in position

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

	LSBITS = 0x0F

	def __init__(self, dacSel=0x00, parent=None):
		"""
		:param dacSel: channel number selection
		:type dacSel: int
		:param parent: MCP4728 DAC the channel belongs to
		:type parent: MCP4728.MCP4728
		"""
		self.voltage = 0.0
		self.code = 0
		self.step = 0.0
		self.dacSel = dacSel
		self.Vref = 0.0
		self.vrefSel = self.vrefSel.INT
		self.gainSel = self.GainSel.X1
		self.powerSel = self.PowerSel.ON
		self.parent = parent

	def __setattr__(self, key, value):
		if key is 'Vref':
			if (value > 5.5) or (value < 2.7):
				raise AttributeError('Vref outside of Vdd range')
			self.__dict__['Vref'] = value
			self.__dict__['step'] = value / 4096.0
			self.__dict__['voltage'] = self.code * self.step
			self.__dict__['VrefSel'] = self.vrefSel.INT if value is 2.048 or 4.096 else self.vrefSel.VDD
			self.__dict__['gainSel'] = self.GainSel.X2 if value is 4.096 else self.GainSel.X1
			self.parent.WriteGain()
			self.parent.WriteVref()
		elif key is 'voltage':
			if (value > self.Vref) or (value < 0):
				raise AttributeError('Voltage outside of Vref range')
			self.__dict__['voltage'] = value
			self.__dict__['code'] = value / self.step
			if self.parent.update:
				self.parent.MultiWrite([self.dacSel])
		elif key is 'code':
			if (value > 4095) or (value < 0):
				raise AttributeError('DAC code outside of 0-4095 range')
			self.__dict__['code'] = value
			self.__dict__['voltage'] = value * self.step
			if self.parent.update:
				self.parent.MultiWrite([self.dacSel])
		elif key is 'power':

			pass
		else:
			self.__dict__[key] = value

	def EncodeFast(self):
		"""
		Encode into binary data for the FastWrite method
		:return: encoded channel data
		"""
		code = self.code.to_bytes(2, 'big')
		data = list(self.Cmd.FAST_WR.value | (self.powerSel[1] >> 1) | code[0])
		data.append(code[1])
		return data

	def Encode(self):
		"""
		Encode into binary data for transmission
		:return: encoded channel data
		"""
		code = self.code.to_bytes(2, 'big')
		data = list(self.vrefSel[1] | self.powerSel[1] | self.gainSel[1] | code[0])
		data.append(code[1])
		return data
