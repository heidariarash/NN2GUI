from PyQt5.QtWidgets import QFileDialog
from PIL             import Image

import pandas as pd

def get_file(input_type, parent):
    if input_type == "Image":
        options     = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(parent,"Choose The Image","","Image (*.jpg *.png);;All Files (*)", options=options)
        return fileName

    elif input_type == "Tabular":
        options     = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(parent,"Choose The Data","","Tabular (*.txt *.csv);;All Files (*)", options=options)
        return fileName

    elif input_type == "Text":
        options     = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(parent,"Choose The Text","","Text (*.txt);;All Files (*)", options=options)
        return fileName

    elif input_type == "Other":
        options     = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(parent,"Choose The Data","","Data (*)", options=options)
        return fileName


def preprocess_file(data, input_type):
    if input_type == "Image":
        data = Image.open(data)
        # converting to tensor here
        return data

    elif input_type == "Tabular":
        data = pd.read_csv(data)
        #convert to tensor here
        return data

    elif input_type == "Text":
        with open(data) as f:
            data = f.read()
        #convert to tensor here
        return data