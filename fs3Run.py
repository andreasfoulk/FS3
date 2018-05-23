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
        self.percentile25.clicked.connect(self.percentile25Update)
        self.percentile10.clicked.connect(self.percentile10Update)
        self.percentile5.clicked.connect(self.percentile5Update)
        self.percentileHighEnd.clicked.connect(self.percentileHighEndUpdate)

        ### Layer Combo Box
        self.refreshLayers()
        self.refreshFields()
        self.selectLayerComboBox.currentIndexChanged.connect(self.refreshFields)
        #layers = fieldGetterInst.get_vector_layers()
        #self.selectLayerComboBox.insertItems(0, layers)

        #field = (fieldGetterInst
        #    .get_single_layer(self.selectLayerComboBox.currentText()))
        #self.selectFieldComboBox.insertItems(self, field)

    """
    Fill LineEdit with percentile numbers when the buttons are pressed
    """
    @pyqtSlot()
    def percentile25Update(self):
        self.percentilesLineEdit.setText("25, 50, 75, 100")

    @pyqtSlot()
    def percentile10Update(self):
        percentile10Str = ", ".join(str(x * 10) for x in range(1, 11))
        self.percentilesLineEdit.setText(percentile10Str)

    @pyqtSlot()
    def percentile5Update(self):
        percentile5Str = ", ".join(str(x * 5) for x in range(1, 21))
        self.percentilesLineEdit.setText(percentile5Str)

    @pyqtSlot()
    def percentileHighEndUpdate(self):
        self.percentilesLineEdit.setText("50, 80, 95")

    def refreshLayers(self):
        """
        Reload the layers coboBox with the current content of the layers list
        """
        self.selectLayerComboBox.clear()
        fieldGetterInst = LayerFieldGetter()
        layers = fieldGetterInst.get_vector_layers()
        self.selectLayerComboBox.insertItems(0, layers)

    def refreshFields(self):
        """
        Reload the fields coboBox with the current content of the field lists
        """
        self.selectFieldComboBox.clear()

        fieldGetterInst = LayerFieldGetter()
        layer = fieldGetterInst.get_single_layer \
                (self.selectLayerComboBox.currentText())
        if layer != None:
            self.selectFieldComboBox.insertItems \
            (1, fieldGetterInst.get_all_fields(layer))
