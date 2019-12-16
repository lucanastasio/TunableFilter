"""
MCP4728 PyQt5 GUI
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

from PyQt5 import QtWidgets, QtCore
from MainWindow import Ui_MainWindow
import sys, glob
from MCP4728 import MCP4728, Channel


class Application(QtWidgets.QMainWindow):

	def __init__(self):
		super(Application, self).__init__()
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)

		self.FillComboBoxBus()
		self.dac = MCP4728(self.ui.ComboBoxBus.currentText(), self.ui.SpinBoxAddress.value())
		#self.dac.channel['A'].

		# ------- signals -------
		#self.Vref = Vref(self.ui.SpinBoxVdd.value())
		#self.ui.SpinBoxVdd.valueChanged['double'].connect(self.Vref.Vdd)
		self.ui.SliderChannelA.valueChanged.connect(self.setSpinBoxChannelA)
		self.ui.SpinBoxChannelA.valueChanged.connect(self.setSliderChannelA)

		self.ui.ComboBoxBus.Popup.connect(self.FillComboBoxBus)
		self.ui.ComboBoxBus.activated['QString'].connect(self.BusChanged)

		# ------- setup -------

		self.ui.statusbar.showMessage("Ready")

	def FillComboBoxBus(self):
		bus = glob.glob('/dev/i2c*')
		bus.sort(reverse=False)
		self.ui.ComboBoxBus.clear()
		self.ui.ComboBoxBus.addItems(bus)

	def BusChanged(self, bus):
		self.dac.i2c.close()
		self.dac.i2c.open(bus)

	def setSpinBoxChannelA(self, value):
		self.A = value
		self.ui.SpinBoxChannelA.setValue(value)

	def setSliderChannelA(self, value):
		self.A = value
		self.ui.SliderChannelA.setValue(value)

app = QtWidgets.QApplication([])
application = Application()
application.show()
sys.exit(app.exec())
