from PyQt5 import QtWidgets, QtCore


class ComboBox(QtWidgets.QComboBox):
    Popup = QtCore.pyqtSignal()

    def showPopup(self):
        self.Popup.emit()
        super(ComboBox, self).showPopup()