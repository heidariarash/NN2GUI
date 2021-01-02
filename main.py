from mainPageUi      import Ui_NN2GUI
from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow, qApp, QDockWidget, QFileDialog
from PyQt5           import QtWidgets, QtGui

import sys

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent=parent)
        self.ui = Ui_NN2GUI()
        self.ui.setupUi(self)
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