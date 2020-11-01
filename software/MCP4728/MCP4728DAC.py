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


class DAC:
	from .MCP4728Channel import Channel

	def __init__(self, parentDac=None):
		"""
		:type parentDac: MCP4728.MCP4728
		"""
		self.A = self.Channel(0x0, parentDac)
		self.B = self.Channel(0x1, parentDac)
		self.C = self.Channel(0x2, parentDac)
		self.D = self.Channel(0x3, parentDac)
		#TODO: change usage of __dict__ to list
		#self.channel = [self.A, self.B, self.C, self.D]

	def __iter__(self):
		for i in 'ABCD':
			yield self[i]

	def __getitem__(self, item):
		if isinstance(item, str):
			return self.__dict__[item]
		elif isinstance(item, int):
			return self.__dict__[chr(item + ord('A'))]

	def __setitem__(self, key, value):
		if isinstance(key, str):
			self.__dict__[key] = value
		elif isinstance(key, int):
			self.__dict__[chr(key + ord('A'))] = value

	def __setattr__(self, key, value):
		if key is 'all':
			for i in 'ABCD':
				self.__setattr__(i, value)
		elif isinstance(value, float):
			self.__dict__[key].setVout(value)
		elif isinstance(value, int):
			self.__dict__[key].setCode(value)
		else:
			self.__dict__[key] = value
