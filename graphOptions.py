"""
generic header
"""
import os

from .resources import *

from PyQt5 import uic
from PyQt5.QtWidgets import QDialog
from PyQt5.QtGui import QIcon


FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'graphOptions.ui'))

class GraphOptionsWindow(QDialog, FORM_CLASS):
    """
    generic docstring
    """
    def __init__(self, parent=None):
        super(GraphOptionsWindow, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("Graph Options")
        self.iconPath = ":/plugins/FS3/FS3Icon.png"
        self.setWindowIcon(QIcon(self.iconPath))

        transforms = ['None', 'Log']
        self.dataTransformBox.insertItems(0, transforms)

        sorts = ['None', 'Ascending', 'Descending']
        self.dataSortingBox.insertItems(0, sorts)

        self.xAxisDefaultBox.insertItem(0, 'None')
