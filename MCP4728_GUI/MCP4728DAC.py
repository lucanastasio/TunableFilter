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

class DAC:
	# bit mask for reading the channel number
	DAC_READ_BITS = 0x30
	# number of right shifts to read the channel number in decimal
	DAC_READ_SHIFT = 4
	# this bit is set to 1 when reading from EEPROM or 0 when reading from registers
	EEPROM_READ_BIT = 0x08
	# DAC binary code least significant bits mask
	CODE_LSBITS_MASK = 0x0F

	from MCP4728Channel import Channel

	def __init__(self, parent=None):
		"""

		:type parent: MCP4728.MCP4728
		"""
		self.A = self.Channel(0x0, parent)
		self.B = self.Channel(0x1, parent)
		self.C = self.Channel(0x2, parent)
		self.D = self.Channel(0x3, parent)

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

	def __setattr__(self, key, value):
		if key is 'all':
			for i in 'ABCD':
				self[i] = value
		elif isinstance(value, float):
			self.__dict__[key].voltage = value
		elif isinstance(value, int):
			self.__dict__[key].code = value
		else:
			self.__dict__[key] = value

	def Decode(self, data):
		"""
		Decode binary data read form the IC into readable format
		:param data: binary data to be decoded
		:type data: byte list of length 3
		:return: the new Channel instance
		"""
		dacSel = (data[0] & self.DAC_READ_BITS) >> self.DAC_READ_SHIFT
		channel = self.Channel(dacSel)
		channel.vrefSel = data[1] & self.Channel.VrefSel.MASK.value
		channel.powerSel = data[1] & self.Channel.PowerSel.MASK.value
		channel.gainSel = data[1] & self.Channel.GainSel.MASK.value
		channel.code = int.from_bytes([(data[1] & self.CODE_LSBITS_MASK), data[2]], 'big')
		self[dacSel] = channel
