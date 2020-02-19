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
from .MainWindow import Ui_MainWindow
import glob
import sys
import warnings
from MCP4728.MCP4728 import MCP4728


class MCP4728App(QtWidgets.QMainWindow):

	def __init__(self):
		super(MCP4728App, self).__init__()
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)
		self.Slider = [self.ui.SliderA, self.ui.SliderB, self.ui.SliderC, self.ui.SliderD]
		self.SpinBox = [self.ui.SpinBoxA, self.ui.SpinBoxB, self.ui.SpinBoxC, self.ui.SpinBoxD]
		self.Vref = [self.ui.VrefA, self.ui.VrefB, self.ui.VrefC, self.ui.VrefD]
		self.FillComboBoxBus()
		self.dac = MCP4728(bus=self.ui.ComboBoxBus.currentText(), address=self.ui.SpinBoxAddress.value(), update=False)
		self.connectSignals()
		sys.excepthook = self.excepthook
		warnings.showwarning = self.showwarning
		self.showMessage("Licensed under GPL3, Copyright © 2019 Luca Anastasio anastasio.lu@gmail.com", timeout=15000)

	def connectSignals(self):
		self.ui.SpinBoxVdd.valueChanged.connect(self.SpinBoxVddChanged)
		self.ui.SpinBoxAddress.valueChanged.connect(self.AddressChanged)
		self.ui.CheckBoxUpdate.stateChanged.connect(self.UpdateModeChanged)
		self.ui.ComboBoxBus.Popup.connect(self.FillComboBoxBus)
		self.ui.ComboBoxBus.activated.connect(self.BusChanged)  # ['QString']
		self.ui.PushButtonWrite.clicked.connect(self.WriteValues)
		self.ui.PushButtonRead.clicked.connect(self.ReadValues)
		self.ui.PushButtonLoad.clicked.connect(self.LoadEEPROM)
		self.ui.PushButtonSave.clicked.connect(self.SaveEEPROM)
		for i in range(0, 4):
			self.Slider[i].valueChanged.connect(lambda value, num=i: self.SliderChanged(newVal=value, chNum=num))
			self.SpinBox[i].valueChanged.connect(lambda value, num=i: self.SpinBoxChanged(newVal=value, chNum=num))
			self.Vref[i].activated.connect(lambda index, num=i: self.VrefChanged(newIndex=index, chNum=num))  # ['int']

	def showMessage(self, msg, msgType=None, timeout=2000):
		style = 'color:black'
		if msgType is 'wrn':
			style = 'color:orange'
		elif msgType is 'err':
			style = 'color:red'
		self.ui.statusbar.setStyleSheet(style)
		self.ui.statusbar.showMessage(msg, timeout)

	def FillComboBoxBus(self):
		bus = glob.glob('/dev/i2c*')
		self.ui.ComboBoxBus.clear()
		self.ui.ComboBoxBus.addItems(bus)
		self.showMessage('i2c bus list updated')

	def BusChanged(self, newBus: str):
		self.dac.SetBus(newBus)

	def AddressChanged(self, newAddr: int):
		self.dac.address = newAddr

	def UpdateModeChanged(self, newMode: bool):
		self.dac.update = newMode
		#text = 'enabled' if newMode is True else 'disabled'
		#self.showMessage('Continuous update mode ' + text)

	def WriteValues(self):
		self.dac.MultiWrite('ABCD', True)
		self.showMessage('DAC registers written')

	def ReadValues(self):
		self.dac.ReadAll('R')
		self.restore()
		self.showMessage('DAC registers loaded')

	def SaveEEPROM(self):
		self.dac.SequentialWrite(0, True)
		self.showMessage('EEPROM written')

	def LoadEEPROM(self):
		self.dac.ReadAll('E')
		self.restore()
		self.showMessage('EEPROM loaded')

	def restore(self):
		for i in range(0, 4):
			vrefInd = self.dac.channel[i].getVrefIndex()
			intVref = [2.048, 4.096, self.ui.SpinBoxVdd.value()]
			self.dac.channel[i].setVref(intVref[vrefInd])
			self.Vref[i].setCurrentIndex(vrefInd)
			self.Slider[i].setValue(self.dac.channel[i].code)
			self.SpinBox[i].setValue(self.dac.channel[i].vout)

	def SpinBoxVddChanged(self, newVal):
		for i in range(0, 4):
			if self.Vref[i].currentIndex() == 2:
				self.VrefChanged(2, i)

	def SliderChanged(self, newVal: int, chNum: int):
		self.dac.channel[chNum].setCode(newVal)
		self.SpinBox[chNum].setValue(self.dac.channel[chNum].vout)

	def SpinBoxChanged(self, newVal: float, chNum: int):
		self.dac.channel[chNum].setVout(newVal)
		self.Slider[chNum].setValue(self.dac.channel[chNum].code)

	def VrefChanged(self, newIndex: int, chNum: int):
		intVref = [2.048, 4.096, self.ui.SpinBoxVdd.value()]
		vref = intVref[newIndex]
		self.dac.channel[chNum].setVref(vref)
		if vref > self.SpinBox[chNum].maximum():
			self.SpinBox[chNum].setMaximum(vref * 0.999755859)
			self.SpinBox[chNum].setValue(self.dac.channel[chNum].vout)
		else:
			self.SpinBox[chNum].setValue(self.dac.channel[chNum].vout)
			self.SpinBox[chNum].setMaximum(vref * 0.999755859)
		self.SpinBox[chNum].setSingleStep(self.dac.channel[chNum].step)

	def excepthook(self, exc_type, exc_value, exc_tb):
		self.showMessage(exc_type.__name__ + ': ' + str(exc_value), 'err')

	def showwarning(self, message, category, filename, lineno, file=None, line=None):
		self.showMessage(category.__name__ + ': ' + str(message), 'wrn')
