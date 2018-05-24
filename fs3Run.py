# -*- coding: utf-8 -*-
"""
Created on Tue May 15 11:12:02 2018

@author: Tanner Lee
"""

import os
from PyQt5 import uic
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QTableWidget, QTableWidgetItem

from .layerFieldGetter import LayerFieldGetter
from .fs3Stats import FS3NumericalStatistics

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

        self.fieldGetterInst = LayerFieldGetter()
        self.currentLayer = None

        ### Tabs
        # Data Table
        self.dataTableLayout = QVBoxLayout()
        self.tableWidget = QTableWidget()

        ### Buttons
        # Percentile
        self.percentile25.clicked.connect(self.percentile25Update)
        self.percentile10.clicked.connect(self.percentile10Update)
        self.percentile5.clicked.connect(self.percentile5Update)
        self.percentileHighEnd.clicked.connect(self.percentileHighEndUpdate)

        # Next/Prev
        self.nextButton.clicked.connect(self.setNextField)
        self.previousButton.clicked.connect(self.setPrevField)

        ### Layer Combo Box
        self.selectLayerComboBox.currentIndexChanged \
                        .connect(self.refreshFields)

        self.refresh()

    def refresh(self):
        """
        Reload data
        """
        self.refreshLayers()
        self.refreshFields()
        self.refreshTable()

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

    """
    Next/Previous
    """
    @pyqtSlot()
    def setNextField(self):
        index = self.selectFieldComboBox.currentIndex()
        index = (index + 1) % self.selectFieldComboBox.count()
        self.selectFieldComboBox.setCurrentIndex(index)

    @pyqtSlot()
    def setPrevField(self):
        index = self.selectFieldComboBox.currentIndex()
        index = (index - 1) % self.selectFieldComboBox.count()
        self.selectFieldComboBox.setCurrentIndex(index)

    def refreshLayers(self):
        """
        Reload the layers coboBox with the current content of the layers list
        """
        self.selectLayerComboBox.clear()

        layers = self.fieldGetterInst.get_vector_layers()
        self.selectLayerComboBox.insertItems(0, layers)

    @pyqtSlot()
    def refreshFields(self):
        """
        Reload the fields coboBox with the current content of the field lists
        """
        self.selectFieldComboBox.clear()

        layer = self.fieldGetterInst.get_single_layer \
                (self.selectLayerComboBox.currentText())
        if layer != None:
            self.currentLayer = layer
            self.selectFieldComboBox.insertItem(0, "All")
            self.selectFieldComboBox.insertItems \
                (1, self.fieldGetterInst.get_all_fields(layer))

    def refreshTable(self):
        """
        docstring
        """
        self.tableWidget.clear()

        if self.currentLayer:

            # Should add a default to fieldsComboBox, all where all the layer data can be displayed... and ability to select multiple...

            features = self.currentLayer.getFeatures()
            # Determine length
            total = 0
            for x in features:
                total += 1

            self.tableWidget.setRowCount(total)

            row = 0
            names = []
            features = self.currentLayer.getFeatures()

            # for each row
            for feature in features:
                attributes = feature.attributes()
                self.tableWidget.setColumnCount(len(attributes)) # Not loading in the data yet.... not sure where it will be loaded from or how we want to process it either
                col = 0

                # for each column value
                for attribute in attributes:
                    self.tableWidget.setItem(row, col, QTableWidgetItem(str(attribute)))
                    col += 1

                row += 1

                try:
                    # Not all data has a "name"
                    # TODO look through other datasets and find what else this might be called
                    names.append(feature["name"])
                except KeyError:
                    names.append(str(row))

            fields = self.fieldGetterInst.get_all_fields(self.currentLayer)
            self.tableWidget.setHorizontalHeaderLabels(fields)
            self.tableWidget.setVerticalHeaderLabels(names)

        else:
            # TODO display this in the gui or a pop up
            print("Please select a layer to look at it's data")

        self.tableWidget.move(0,0)

        self.dataTableLayout.addWidget(self.tableWidget)

        self.dataTab.setLayout(self.dataTableLayout)
        
    def createStatistics(self, inputArray):
        """
        createStatistics
        Methods that instantiates both Statistics classes and initializes them
        """
        self.numericalStatistics = FS3NumericalStatistics()
        self.numericalStatistics.initialize(inputArray)
        
