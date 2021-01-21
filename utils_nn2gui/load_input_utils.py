from PyQt5.QtWidgets import QFileDialog

def get_file(input_type):
    if input_type == "Image":
        options     = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self,"Choose The Image","","Image (*.jpg *.png);;All Files (*)", options=options)
        return fileName

    elif input_type == "Tabular":
        options     = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self,"Choose The Data","","Tabular (*.txt *.csv);;All Files (*)", options=options)
        return fileName

    elif input_type == "Text":
        options     = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self,"Choose The Text","","Text (*.txt);;All Files (*)", options=options)
        return fileName

    elif input_type == "Other":
        options     = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self,"Choose The Data","","Data (*)", options=options)
        return fileName