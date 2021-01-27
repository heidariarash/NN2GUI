from PyQt5.QtWidgets        import QFileDialog
from PIL                    import Image
from torchvision.transforms import ToTensor, Compose

import pandas     as pd
import numpy      as np
import tensorflow as tf
import torch

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


def preprocess_file(data, input_type, framework):
    if input_type == "Image":
        data = Image.open(data)
        if framework == "PyTorch":
            transform = Compose([ToTensor()])
            data = transform(data)
            data = torch.unsqueeze(data, 0)
            return data
        if framework == "TensorFlow":
            data = tf.keras.preprocessing.image.img_to_array(data)
            return np.expand_dims(data, 0)

    elif input_type == "Tabular":
        data = pd.read_csv(data, header=None)
        if framework == "PyTorch":
            data = torch.Tensor(data.values)
        elif framework == "TensorFlow":
            data = data.values
        return data