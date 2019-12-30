"""
MCP4728 GUI
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

from PyQt5 import QtWidgets
from MainWindow import Ui_MainWindow
import glob
from MCP4728 import MCP4728


class MCP4728App(QtWidgets.QMainWindow):

	def __init__(self):
		super(MCP4728App, self).__init__()
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)

		self.FillComboBoxBus()
		self.dac = MCP4728(self.ui.ComboBoxBus.currentText(), self.ui.SpinBoxAddress.value())
		# self.dac.channel['A'].

		# ------- signals -------
		# self.Vref = self.ui.SpinBoxVdd.value()
		# self.ui.SpinBoxVdd.valueChanged['double'].connect(self.Vref.Vdd)
		self.ui.SliderChannelA.valueChanged.connect(self.SliderChannelAChanged)
		self.ui.SpinBoxChannelA.valueChanged.connect(self.SpinBoxChannelAChanged)

		self.ui.ComboBoxBus.Popup.connect(self.FillComboBoxBus)
		self.ui.ComboBoxBus.activated['QString'].connect(self.BusChanged)

		# ------- setup -------

		self.showMessage("Ready")

	def showMessage(self, msg, msgType=None):
		style = 'color:black'
		if msgType is 'wrn':
			style = 'color:orange'
		elif msgType is 'err':
			style = 'color:red'
		self.ui.statusbar.setStyleSheet(style)
		self.ui.statusbar.showMessage(msg)

	def FillComboBoxBus(self):
		bus = glob.glob('/dev/i2c*')
		self.ui.ComboBoxBus.clear()
		self.ui.ComboBoxBus.addItems(bus)

	def BusChanged(self, bus):
		self.dac.SetBus(bus)

	def SliderChannelAChanged(self, value: int):
		self.dac.channel.A.setCode(value)
		self.ui.SpinBoxChannelA.setValue(self.dac.channel.A.vout)

	def SliderChannelBChanged(self, value: int):
		self.dac.channel.B.setCode(value)
		self.ui.SpinBoxChannelB.setValue(self.dac.channel.B.vout)

	def SliderChannelCChanged(self, value: int):
		self.dac.channel.C.setCode(value)
		self.ui.SpinBoxChannelC.setValue(self.dac.channel.C.vout)

	def SliderChannelDChanged(self, value: int):
		self.dac.channel.D.setCode(value)
		self.ui.SpinBoxChannelD.setValue(self.dac.channel.D.vout)

	def SpinBoxChannelAChanged(self, value: float):
		self.dac.channel.A.setVout(value)
		self.ui.SliderChannelA.setValue(self.dac.channel.A.code)

	def SpinBoxChannelBChanged(self, value: float):
		self.dac.channel.B.setVout(value)
		self.ui.SliderChannelB.setValue(self.dac.channel.B.code)

	def SpinBoxChannelCChanged(self, value: float):
		self.dac.channel.C.setVout(value)
		self.ui.SliderChannelC.setValue(self.dac.channel.C.code)

	def SpinBoxChannelDChanged(self, value: float):
		self.dac.channel.D.setVout(value)
		self.ui.SliderChannelD.setValue(self.dac.channel.D.code)

	def excepthook(self, exc_type, exc_value, exc_tb):
		if isinstance(exc_type, (Exception, BaseException)):
			self.showMessage(str(exc_value), 'err')
		else:
			self.showMessage(str(exc_value), 'wrn')
