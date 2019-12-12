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
