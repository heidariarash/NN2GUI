from mainPageUi      import Ui_NN2GUI
from changeClassesUi import Ui_ChangeClasses
from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow, qApp, QDockWidget, QFileDialog
from PyQt5           import QtWidgets, QtGui, QtCore

import sys
import importlib.util

class ChangeClass(QMainWindow):
    def __init__(self, parent = None):
        super(ChangeClass, self).__init__(parent = parent)
        self.ui = Ui_ChangeClasses()
        self.ui.setupUi(self)
        #connecting different signals to slots
        self.ui.cancel.clicked.connect(self.cancle_button_clicked)

    def cancle_button_clicked(self):
        self.close()


class MainWindow(QMainWindow):
    def __init__(self, parent = None):
        super(MainWindow, self).__init__(parent=parent)
        self.ui = Ui_NN2GUI()
        self.ui.setupUi(self)
        #initializing variables
        self.valid_prep  = False
        self.valid_model = False
        #correcting the stylesheets of comboboxes
        QtCore.QTimer.singleShot(100, lambda: self.ui.input_type.setStyleSheet(self.ui.input_type.styleSheet()))
        QtCore.QTimer.singleShot(100, lambda: self.ui.framework_type.setStyleSheet(self.ui.framework_type.styleSheet()))
        QtCore.QTimer.singleShot(100, lambda: self.ui.output_type.setStyleSheet(self.ui.output_type.styleSheet()))
        #setting parts of the GUI in hidden mode
        self.ui.predictions_info.setHidden(True)
        self.ui.predictions.setHidden(True)
        self.ui.input_input.setHidden(True)
        self.ui.load_preprocess_error.setHidden(True)
        #disabling some buttons and inputs
        self.ui.input_input.setDisabled(True)
        self.ui.load_input.setDisabled(True)
        #connecting different signals to slots
        self.ui.output_type.currentTextChanged.connect(self.output_type_changed)
        self.ui.load_preprocess.clicked.connect(self.load_preprocess_clicked)
        self.ui.input_type.currentTextChanged.connect(self.input_type_changed)
        self.ui.output_classes.clicked.connect(self.output_classes_clicked)

    def output_type_changed(self, value):
        #hiding the output classes if the output type is regression.
        if(value == "Regression"):
            self.ui.output_classes.setHidden(True)
            self.ui.output_classes_label.setHidden(True)
        else:
            self.ui.output_classes_label.setHidden(False)
            self.ui.output_classes.setHidden(False)

    def load_preprocess_clicked(self):
        #checking if there already a preprocess file exists
        if(not self.valid_prep):
            options = QFileDialog.Options()
            fileName, _ = QFileDialog.getOpenFileName(self,"Choose Preprocess File","","Python Files (*.py)", options=options)
            try:
                spec = importlib.util.spec_from_file_location("preprocess", fileName)
                self.preprocess = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(self.preprocess)
                #when preprocess file is a valid python file but there is no preprocess funtion.
                if "preprocess" not in dir(self.preprocess):
                    self.ui.load_preprocess_error.setText("* The module does not contain preprocess function.")
                    self.ui.load_preprocess_error.setStyleSheet("color: #BA181B")
                    self.ui.load_preprocess_error.setHidden(False)
                #when everything is ok.
                else:
                    self.ui.load_preprocess_error.setText("* Preprocess File Accepted")
                    self.ui.load_preprocess_error.setStyleSheet("color: #F5F3F4")
                    self.ui.load_preprocess_error.setHidden(False)
                    self.valid_prep = True
                    self.ui.load_preprocess.setText("Remove Preprocess")
            #when the file is not a valid python file.
            except:
                self.ui.load_preprocess_error.setText("* Something went wrong. Please try again.")
                self.ui.load_preprocess_error.setStyleSheet("color: #BA181B")
                self.ui.load_preprocess_error.setHidden(False)
        #changing the functionality to removing preprocess file when one already exists.
        else:
            self.valid_prep = False
            self.ui.load_preprocess_error.setHidden(True)
            self.ui.load_preprocess.setText("Load Preprocess")

    def input_type_changed(self, value):
        #setting input_input to visible if the type is text and vice versa.
        if value == "Text" or value == "Tabular":
            self.ui.input_input.setHidden(False)
        else:
            self.ui.input_input.setHidden(True)

    def output_classes_clicked(self):
        #opening the new window
        window = ChangeClass(parent = self)
        window.setWindowModality(True)
        window.show()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("fusion")
    app.setWindowIcon(QtGui.QIcon('gallery/icon.jpg'))
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())