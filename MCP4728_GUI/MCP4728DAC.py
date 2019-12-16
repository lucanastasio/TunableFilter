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
	DAC_BITS = 0x30
	ZERO_BIT = 0x08

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
		if (data[0] & DAC.ZERO_BIT) is not 0:
			raise IOError('Unexpected value')
		dacSel = (data[0] & DAC.DAC_BITS) >> 4
		channel = self.Channel(dacSel)
		channel.vrefSel = data[1] & self.Channel.VREF_INT_BIT
		channel.powerDownSel = data[1] & self.Channel.PWR_MSK
		channel.gainSel = data[1] & self.Channel.GAIN_X2_BIT
		channel.code = int.from_bytes([(data[1] & self.Channel.LSBITS), data[2]], 'big')
		self[dacSel] = channel