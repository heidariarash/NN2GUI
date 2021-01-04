from mainPageUi      import Ui_NN2GUI
from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow, qApp, QDockWidget, QFileDialog
from PyQt5           import QtWidgets, QtGui, QtCore

import sys
import importlib.util

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent=parent)
        self.ui = Ui_NN2GUI()
        self.ui.setupUi(self)
        #correcting the stylesheets of comboboxes
        QtCore.QTimer.singleShot(100, lambda: self.ui.input_type.setStyleSheet(self.ui.input_type.styleSheet()))
        QtCore.QTimer.singleShot(100, lambda: self.ui.framework_type.setStyleSheet(self.ui.framework_type.styleSheet()))
        QtCore.QTimer.singleShot(100, lambda: self.ui.output_type.setStyleSheet(self.ui.output_type.styleSheet()))
        #setting parts of the GUI in hidden mode
        self.ui.predictions_info.setHidden(True)
        self.ui.predictions.setHidden(True)
        self.ui.input_input.setHidden(True)
        self.ui.load_preprocess_error.setHidden(True)
        #connecting different signals to slots
        self.ui.output_type.currentTextChanged.connect(self.output_type_change)
        self.ui.load_preprocess.clicked.connect(self.load_preprocess_clicked)

    def output_type_change(self, value):
        if(value == "Regression"):
            self.ui.output_classes.setHidden(True)
            self.ui.output_classes_label.setHidden(True)
        else:
            self.ui.output_classes_label.setHidden(False)
            self.ui.output_classes.setHidden(False)

    def load_preprocess_clicked(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self,"Choose Preprocess File","","Python Files (*.py)", options=options)
        try:
            spec = importlib.util.spec_from_file_location("preprocess", fileName)
            self.preprocess = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(self.preprocess)
            if "preprocess" not in dir(self.preprocess):
                self.ui.load_preprocess_error.setText("* The module does not contain preprocess function.")
                self.ui.load_preprocess_error.setHidden(False)
            else:
                self.ui.load_preprocess_error.setHidden(True)
        except:
            self.ui.load_preprocess_error.setText("* Something went wrong. Please try again.")
            self.ui.load_preprocess_error.setHidden(False)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("fusion")
    app.setWindowIcon(QtGui.QIcon('gallery/icon.jpg'))
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())