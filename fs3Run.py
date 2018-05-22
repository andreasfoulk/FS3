# -*- coding: utf-8 -*-
"""
Created on Tue May 15 11:12:02 2018

@author: Tanner Lee
"""

import os
from PyQt5 import uic
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtWidgets import QApplication, QMainWindow

from .layerFieldGetter import LayerFieldGetter

QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'fs3.ui'))

class FS3MainWindow(QMainWindow, FORM_CLASS):
    """
    FS3MainWindow
    Handles the creation and display of the window.
    Makes use of the fs3.ui QT ui file.
    """
    def __init__(self, parent=None):
        super(FS3MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.mainWindowSplitter.setStretchFactor(1, 10)
        self.setWindowTitle('FS3 -- FieldStats3')

        ### Buttons
        # Percentile
        self.percentile25.clicked.connect(self.percentile25_update)
        self.percentile10.clicked.connect(self.percentile10_update)
        self.percentile5.clicked.connect(self.percentile5_update)
        self.percentileHighEnd.clicked.connect(self.percentileHighEnd_update)
        
        ### Layer Combo Box
        #Create the getter
        fieldGetterInst = LayerFieldGetter()
        layers = fieldGetterInst.get_vector_layers()
        self.selectLayerComboBox.insertItems(0, layers)

    @pyqtSlot()
    def percentile25_update(self):
        self.percentilesLineEdit.setText("25, 50, 75, 100")

    @pyqtSlot()
    def percentile10_update(self):
        percentile10_str = ", ".join(str(x * 10) for x in range(1,11))
        self.percentilesLineEdit.setText(percentile10_str)

    @pyqtSlot()
    def percentile5_update(self):
        percentile5_str = ", ".join(str(x * 5) for x in range(1,21))
        self.percentilesLineEdit.setText(percentile5_str)

    @pyqtSlot()
    def percentileHighEnd_update(self):
        self.percentilesLineEdit.setText("50, 80, 95")
