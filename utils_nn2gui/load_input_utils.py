from PIL             import Image
from PyQt5.QtWidgets import QFileDialog

import torch
# import tensorflow as tf

def get_file(input_type, framework, valid_prep, prep):
    if input_type == "Image":
        options     = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self,"Choose The Model","","Image (*.jpg *.png);;All Files (*)", options=options)
        if not fileName:
            return

        if valid_prep:
            return prep(fileName)
        returned_file = torch.Image.open(fileName)



    elif input_type == "Tabular":
        pass
    elif input_type == "Text":
        pass
    elif input_type == "Video":
        pass
    elif input_type == "3D Image":
        pass