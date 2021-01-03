from mainPageUi      import Ui_NN2GUI
from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow, qApp, QDockWidget, QFileDialog
from PyQt5           import QtWidgets, QtGui, QtCore

import sys

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent=parent)
        self.ui = Ui_NN2GUI()
        self.ui.setupUi(self)
        QtCore.QTimer.singleShot(100, lambda: self.ui.input_type.setStyleSheet(self.ui.input_type.styleSheet()))
        QtCore.QTimer.singleShot(100, lambda: self.ui.framework_type.setStyleSheet(self.ui.framework_type.styleSheet()))
        QtCore.QTimer.singleShot(100, lambda: self.ui.output_type.setStyleSheet(self.ui.output_type.styleSheet()))
        self.ui.predictions_info.setHidden(True)
        self.ui.predictions.setHidden(True)
        self.ui.input_input.setHidden(True)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("fusion")
    app.setWindowIcon(QtGui.QIcon('gallery/icon.jpg'))
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())