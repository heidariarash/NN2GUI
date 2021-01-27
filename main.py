from UIs.mainPageUi      import Ui_NN2GUI
from UIs.changeClassesUi import Ui_ChangeClasses
from PyQt5.QtWidgets     import QDialog, QApplication, QMainWindow, qApp, QDockWidget, QFileDialog
from PyQt5               import QtWidgets, QtGui, QtCore
from utils_nn2gui        import size_utils, load_input_utils

import sys
import os
import importlib.util
import torch
import tensorflow as tf
import pandas     as pd
import numpy      as np

class ChangeClass(QMainWindow):
    def __init__(self, parent = None):
        super(ChangeClass, self).__init__(parent = parent)
        self.ui = Ui_ChangeClasses()
        self.ui.setupUi(self)
        #correcting the stylesheets of comboboxes
        QtCore.QTimer.singleShot(100, lambda: self.ui.scrollArea.setStyleSheet(self.ui.scrollArea.styleSheet()))
        #initializing variables
        self.classes     = []
        self.num_classes = 2
        #disabling some elements
        self.ui.delete_class.setDisabled(True)
        #connecting different signals to slots
        self.ui.cancel.clicked.connect(self.cancle_button_clicked)
        self.ui.ok.clicked.connect(self.ok_button_clicked)
        self.ui.add_class.clicked.connect(self.add_class_button_clicked)
        self.ui.delete_class.clicked.connect(self.delete_class_button_clicked)

    def cancle_button_clicked(self):
        self.close()

    def set_classes(self, classes):
        self.classes      = classes
        number_of_classes = len(classes) - 2
        for _ in range(number_of_classes):
            self.add_class_button_clicked()
            eval("self.ui.class" + str(self.num_classes -1) + "_name.setText(self.classes[self.num_classes-1])")
        self.ui.class0_name.setText(self.classes[0])
        self.ui.class1_name.setText(self.classes[1])

    def ok_button_clicked(self):
        self.classes = []
        for class_num in range(self.num_classes):
            self.classes.append(eval("self.ui.class"+str(class_num)+"_name.text()"))
        self.parent().classes = self.classes
        self.close()

    def add_class_button_clicked(self):
        #adding another class
        exec("self.ui.class"+str(self.num_classes)+" = QtWidgets.QLabel(self.ui.scrollAreaWidgetContents)")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(30)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(eval("self.ui.class"+str(self.num_classes)+".sizePolicy().hasHeightForWidth()"))
        eval("self.ui.class"+str(self.num_classes)+".setSizePolicy(sizePolicy)")
        eval("self.ui.class"+str(self.num_classes)+".setMinimumSize(QtCore.QSize(50, 50))")
        eval("self.ui.class"+str(self.num_classes)+".setMaximumSize(QtCore.QSize(50, 50))")
        font = QtGui.QFont()
        font.setFamily("MV Boli")
        font.setPointSize(10)
        eval("self.ui.class"+str(self.num_classes)+".setFont(font)")
        eval("self.ui.class"+str(self.num_classes)+".setStyleSheet('color: #F5F3F4;')")
        eval("self.ui.class"+str(self.num_classes)+".setAlignment(QtCore.Qt.AlignCenter)")
        eval("self.ui.class"+str(self.num_classes)+".setObjectName('class" + str(self.num_classes) + "')")
        self.ui.gridLayout_3.addWidget(eval("self.ui.class"+str(self.num_classes)), self.num_classes + 1, 0, 1, 1)
        eval("self.ui.class"+str(self.num_classes)+".setText('"+ str(self.num_classes) +"')")
        #adding the textbox
        exec("self.ui.class"+str(self.num_classes)+"_name = QtWidgets.QLineEdit(self.ui.scrollAreaWidgetContents)")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(50)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(eval("self.ui.class" + str(self.num_classes) + "_name.sizePolicy().hasHeightForWidth()"))
        eval("self.ui.class"+str(self.num_classes)+"_name.setSizePolicy(sizePolicy)")
        eval("self.ui.class"+str(self.num_classes)+"_name.setMinimumSize(QtCore.QSize(100, 50))")
        eval("self.ui.class"+str(self.num_classes)+"_name.setMaximumSize(QtCore.QSize(100, 50))")
        font = QtGui.QFont()
        font.setFamily("Arial Narrow")
        font.setPointSize(11)
        font.setUnderline(False)
        eval("self.ui.class"+str(self.num_classes)+"_name.setFont(font)")
        eval("self.ui.class"+str(self.num_classes)+"_name.setStyleSheet('border: 0px;color: #F5F3F4;')")
        eval("self.ui.class"+str(self.num_classes)+"_name.setAlignment(QtCore.Qt.AlignCenter)")
        eval("self.ui.class"+str(self.num_classes)+".setObjectName('class" + str(self.num_classes) + "_name')")
        self.ui.gridLayout_3.addWidget(eval("self.ui.class" + str(self.num_classes) + "_name"), self.num_classes + 1, 1, 1, 1)
        eval("self.ui.class"+str(self.num_classes)+"_name.setText('Class "+ str(self.num_classes) +"')")
        self.num_classes += 1
        self.ui.delete_class.setDisabled(False)

    def delete_class_button_clicked(self):
        self.ui.gridLayout_3.removeWidget(eval("self.ui.class" + str(self.num_classes - 1) + "_name"))
        self.ui.gridLayout_3.removeWidget(eval("self.ui.class" + str(self.num_classes - 1)))
        exec("del self.ui.class"+ str(self.num_classes - 1))
        exec("del self.ui.class"+ str(self.num_classes - 1)+ "_name")
        self.num_classes -= 1
        if self.num_classes == 2:
            self.ui.delete_class.setDisabled(True)


class MainWindow(QMainWindow):
    def __init__(self, parent = None):
        super(MainWindow, self).__init__(parent=parent)
        self.ui = Ui_NN2GUI()
        self.ui.setupUi(self)
        #initializing variables
        self.valid_prep  = False
        self.valid_model = False
        self.model       = None
        self.preprocess  = None
        self.framework   = "TensorFlow"
        self.classes     = ["Class 0", "Class 1"]
        #correcting the stylesheets of comboboxes
        QtCore.QTimer.singleShot(100, lambda: self.ui.input_type.setStyleSheet(self.ui.input_type.styleSheet()))
        QtCore.QTimer.singleShot(100, lambda: self.ui.framework_type.setStyleSheet(self.ui.framework_type.styleSheet()))
        QtCore.QTimer.singleShot(100, lambda: self.ui.output_type.setStyleSheet(self.ui.output_type.styleSheet()))
        #setting parts of the GUI in hidden mode
        self.ui.predictions_info.setHidden(True)
        self.ui.input_input.setHidden(True)
        self.ui.load_preprocess_error.setHidden(True)
        self.ui.model_spec.setHidden(True)
        self.ui.enter_input.setHidden(True)
        #disabling some buttons and inputs
        self.ui.input_input.setDisabled(True)
        self.ui.load_input.setDisabled(True)
        self.ui.enter_input.setDisabled(True)
        #connecting different signals to slots
        self.ui.output_type.currentTextChanged.connect(self.output_type_changed)
        self.ui.load_preprocess.clicked.connect(self.load_preprocess_clicked)
        self.ui.input_type.currentTextChanged.connect(self.input_type_changed)
        self.ui.output_classes.clicked.connect(self.output_classes_clicked)
        self.ui.load_model.clicked.connect(self.load_model_clicked)
        self.ui.load_input.clicked.connect(self.load_input_clicked)
        self.ui.enter_input.clicked.connect(self.enter_input_clicked)

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
            options     = QFileDialog.Options()
            fileName, _ = QFileDialog.getOpenFileName(self,"Choose Preprocess File","","Python Files (*.py)", options=options)
            try:
                spec            = importlib.util.spec_from_file_location("preprocess", fileName)
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
            self.ui.enter_input.setHidden(False)
        else:
            self.ui.input_input.setHidden(True)
            self.ui.enter_input.setHidden(True)

    def output_classes_clicked(self):
        #opening the new window
        window = ChangeClass(parent = self)
        window.setWindowModality(True)
        window.set_classes(self.classes)
        window.show()

    def load_model_clicked(self):
        if not self.valid_model:
            self.framework = self.ui.framework_type.currentText()

            #PyTorch Case
            if self.framework == "PyTorch":
                options     = QFileDialog.Options()
                fileName, _ = QFileDialog.getOpenFileName(self,"Choose The Model","","PyTorch Model (*.pt *.pth);;All Files (*)", options=options)
                if not fileName:
                    return

                try:
                    self.model       = torch.load(fileName)
                    self.model.eval()
                    self.valid_model = True
                    self.ui.input_input.setDisabled(False)
                    self.ui.load_input.setDisabled(False)
                    self.ui.enter_input.setDisabled(False)
                    self.ui.load_model.setText("Remove Model")
                    self.ui.model_info.setText("PyTorch Model Loaded Successfully")
                    self.ui.predictions_info.setHidden(False)
                    self.ui.model_spec.setHidden(False)
                    self.ui.model_spec.setText("Model Size:  " + str(round(os.stat(fileName).st_size/(1024*1024),2)) + " MB")
                    self.ui.predictions.setStyleSheet("color: #F5F3F4")
                    self.ui.predictions.setText("Ready for Inputs")
                    self.ui.framework_type.setDisabled(True)
                except:
                    self.ui.predictions.setStyleSheet("color: #BA181B")
                    self.ui.predictions.setText("* Something went wrong.")

            #TensorFlow Case
            elif self.framework == "TensorFlow":
                options     = QFileDialog.Options()
                fileName, _ = QFileDialog.getOpenFileName(self,"Choose The Model","","TensorFlow Model (*.pb);;Keras Model (*.h5);;All Files (*)", options=options)
                if not fileName:
                    return

                if fileName.endswith(".pb"):
                    fileName = "/".join(fileName.split("/")[:-1])
                    size = size_utils.get_size(fileName)
                else:
                    size = os.stat(fileName).st_size

                try:
                    self.model = tf.keras.models.load_model(fileName)
                    self.valid_model = True
                    self.ui.input_input.setDisabled(False)
                    self.ui.load_input.setDisabled(False)
                    self.ui.enter_input.setDisabled(False)
                    self.ui.load_model.setText("Remove Model")
                    self.ui.model_info.setText("TensorFlow Model Loaded Successfully")
                    self.ui.predictions_info.setHidden(False)
                    self.ui.model_spec.setHidden(False)
                    self.ui.model_spec.setText("Model Size:  " + str(round(size/(1024*1024),2)) + " MB")
                    self.ui.predictions.setStyleSheet("color: #F5F3F4")
                    self.ui.predictions.setText("Ready for Inputs")
                    self.ui.framework_type.setDisabled(True)
                except:
                    self.ui.predictions.setStyleSheet("color: #BA181B")
                    self.ui.predictions.setText("* Something went wrong.")

        #Remove Model Case
        else:
            self.valid_model = False
            self.model       = None
            self.ui.load_model.setText("Load Model")
            self.ui.predictions.setText("")
            self.ui.model_info.setText("Waiting passionately for a model!")
            self.ui.model_spec.setHidden(True)
            self.ui.input_input.setDisabled(True)
            self.ui.load_input.setDisabled(True)
            self.ui.enter_input.setDisabled(True)
            self.ui.predictions_info.setHidden(True)
            self.ui.framework_type.setDisabled(False)

    def load_input_clicked(self):
        input_type = self.ui.input_type.currentText()
        data       = load_input_utils.get_file(input_type, self)
        if not data:
            return
        
        if self.valid_prep:
            try:
                data = self.preprocess.preprocess(data, True)
            except:
                self.ui.predictions.setText("* Something went wrong with the preprocess file. There might be a bug.")
                self.ui.predictions.setStyleSheet("color: #BA181B")
                return
        else:
            if input_type == "Other" or input_type == "Text":
                self.ui.predictions.setText("* For other  and text data types you must provide a preprocess file.")
                self.ui.predictions.setStyleSheet("color: #BA181B")
                return
            data = load_input_utils.preprocess_file(data, input_type, self.framework)

        if self.framework == "PyTorch":
            # try:
            prediction = self.model(data)
            # except:
            #     self.ui.predictions.setText("* Something went wrong when predicting. It might be an inconsistency between your input data and your model input. Or there is something wrong in your model.")
            #     self.ui.predictions.setStyleSheet("color: #BA181B")
            #     return
        elif self.framework == "TensorFlow":
            try:
                prediction = self.model.predict(data)
            except:
                self.ui.predictions.setText("* Something went wrong when predicting. It might be an inconsistency between your input data and your model input. Or there is something wrong in your model.")
                self.ui.predictions.setStyleSheet("color: #BA181B")
                return

        output_type = self.ui.output_type.currentText()
        self.ui.predictions.setText("Predictions are as follows: \n")
        if self.framework == "PyTorch":
            prediction = prediction.detach().numpy()
        self.ui.predictions.setStyleSheet("color: #F5F3F4")
        if output_type == "Regression":
            for index, pred in enumerate(prediction):
                self.ui.predictions.setText(self.ui.predictions.text() + "Output for instance " + str(index) + ": " + str(pred).lstrip("[").rstrip(']') + "\n")
        elif output_type == "Classification":
            for index, pred in enumerate(prediction):
                try:
                    self.ui.predictions.setText(self.ui.predictions.text() + "Output for instance " + str(index) + ": " + self.classes[np.argmax(pred)] + "\n")
                except:
                    self.ui.predictions.setText(self.ui.predictions.text() + "Output for instance " + str(index) + ": Class " + str(np.argmax(pred)) + "\n")

    def enter_input_clicked(self):
        input_type = self.ui.input_type.currentText()
        data       = self.ui.input_input.toPlainText()
        if self.valid_prep:
            try:
                data = self.preprocess.preprocess(data, False)
            except:
                self.ui.predictions.setText("* Something went wrong with the preprocess file. There might be a bug.")
                self.ui.predictions.setStyleSheet("color: #BA181B")
                return
        else:
            self.ui.predictions.setText("* You must provide a preprocess file, in case you want to enter the input manually.")
            self.ui.predictions.setStyleSheet("color: #BA181B")
            return

        if self.framework == "PyTorch":
            try:
                prediction = self.model(data)
            except:
                self.ui.predictions.setText("* Something went wrong when predicting. It might be an inconsistency between your input data and your model input. Or there is something wrong in your model.")
                self.ui.predictions.setStyleSheet("color: #BA181B")
                return
        elif self.framework == "TensorFlow":
            try:
                prediction = self.model.predict(data)
            except:
                self.ui.predictions.setText("* Something went wrong when predicting. It might be an inconsistency between your input data and your model input. Or there is something wrong in your model.")
                self.ui.predictions.setStyleSheet("color: #BA181B")
                return
            
        output_type = self.ui.output_type.currentText()
        self.ui.predictions.setText("Predictions are as follows: \n")
        if self.framework == "PyTorch":
            prediction = prediction.item()
        self.ui.predictions.setStyleSheet("color: #F5F3F4")
        if output_type == "Regression":
            for index, pred in enumerate(prediction):
                self.ui.predictions.setText(self.ui.predictions.text() + "Output for instance " + str(index) + ": " + str(pred).lstrip("[").rstrip(']') + "\n")
        elif output_type == "Classification":
            for index, pred in enumerate(prediction):
                try:
                    self.ui.predictions.setText(self.ui.predictions.text() + "Output for instance " + str(index) + ": " + self.classes[np.argmax(pred)] + "\n")
                except:
                    self.ui.predictions.setText(self.ui.predictions.text() + "Output for instance " + str(index) + ": Class " + str(np.argmax(pred)) + "\n")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("fusion")
    app.setWindowIcon(QtGui.QIcon('gallery/icon.jpg'))
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())