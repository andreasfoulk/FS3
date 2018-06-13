"""
    fs3.py 
           -- For more information see : https://github.com/andreasfoulk/FS3
           
    Copyright (c) 2018 Orden Aitchedji, McKenna Duzac, Andreas Foulk, Tanner Lee
    
    This software may be modified and distributed under the terms
    of the MIT license.  See the LICENSE file for details.
"""

import os

from .resources import *

from PyQt5 import uic
from PyQt5.QtWidgets import QDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QCoreApplication

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

        transforms = [QCoreApplication.translate("GraphOptionsWindow", "None"),
                QCoreApplication.translate("GraphOptionsWindow", "Log")]
        self.dataTransformBox.insertItems(0, transforms)

        sorts = [QCoreApplication.translate("GraphOptionsWindow", "None"),
                QCoreApplication.translate("GraphOptionsWindow", "Ascending"),
                QCoreApplication.translate("GraphOptionsWindow", "Descending")]
        self.dataSortingBox.insertItems(0, sorts)

        self.xAxisDefaultBox.insertItem(0, QCoreApplication.translate("GraphOptionsWindow", "None"))
