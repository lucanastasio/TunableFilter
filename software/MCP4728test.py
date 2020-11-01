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

from MCP4728 import MCP4728
from MCP4728Channel import Channel as ch
from glob import glob

bus = glob('/dev/i2c*')

dac = MCP4728(bus=bus[0], update=True)

dac.channel.A.setVref(2.048)
dac.channel.A.setVout(1.024)
