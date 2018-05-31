# -*- coding: utf-8 -*-
"""
Created on Tue May 15 11:12:02 2018

@author: Tanner Lee
"""
from __future__ import print_function

import os
from qgis.core import QgsProject
from PyQt5 import uic
from PyQt5.QtCore import Qt, pyqtSlot, QUrl
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QTableWidget, QTableWidgetItem
from PyQt5.QtWebKit import *
from PyQt5.QtWebKitWidgets import *

from .layerFieldGetter import LayerFieldGetter
from .fs3Stats import FS3NumericalStatistics, FS3CharacterStatistics
from .fs3Stats import removeEmptyCells
from .fs3Graphs import test
from .roundFunc import decimalRound

# pylint: disable=fixme

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
        self.setWindowTitle('FS3 -- FieldStats3 -- Field Statistics 3')

        self.fieldGetterInst = LayerFieldGetter()
        self.currentProject = QgsProject.instance()
        self.currentLayer = None
        self.allFields = None

        self.percentile25Update()
        self.currentDecimalPrecision = 0

        ### Tabs
        self.dataTableLayout = QVBoxLayout()
        self.tableWidget = QTableWidget()
        self.statisticLayout = QVBoxLayout()
        self.statisticTable = QTableWidget()
        self.graphLayout = QVBoxLayout()
        self.graphView = QWebView()

        #Refresh for the connecters
        self.refresh()

        ###pyqtSlot connectors (PROJECT)
        self.currentProject.layersAdded.connect(self.refresh)
        self.currentProject.layersRemoved.connect(self.refresh)

        ### pyqtSlot connectors (BUTTONS)
        # Percentile
        self.percentile25.clicked.connect(self.percentile25Update)
        self.percentile10.clicked.connect(self.percentile10Update)
        self.percentile5.clicked.connect(self.percentile5Update)
        self.percentileHighEnd.clicked.connect(self.percentileHighEndUpdate)
        self.percentilesLineEdit.textChanged.connect(self.percentileTextChanged)
        # Limit to Selected
        self.limitToSelected.stateChanged.connect(self.handleLimitSelected)
        # Decimal Selector
        self.numberOfDecimalsBox.valueChanged.connect(self.handleDecimalChanged)
        # Next/Prev
        self.nextButton.clicked.connect(self.setNextField)
        self.previousButton.clicked.connect(self.setPrevField)

        ### Layer Combo Box and Field List Widget
        self.selectLayerComboBox.currentIndexChanged \
                        .connect(self.refreshFields)
        self.selectFieldListWidget.itemSelectionChanged \
                        .connect(self.refreshTable)


    def refresh(self):
        """
        Reload data
        """
        self.refreshLayers()
        self.refreshFields()
        self.refreshTable()
        self.refreshGraph()


    ### Fill LineEdit with percentile numbers when the buttons are pressed
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

    @pyqtSlot()
    def percentileTextChanged(self):
        try:
            percentileList = self.percentilesLineEdit.text().split(', ')
            for percentile in percentileList:
                # Ensure the user has entered a valid percentile
                if float(percentile) < 0 or float(percentile) > 100:
                    return
            self.refreshTable()
        except ValueError:
            # The user is either still entering text
            # Or has entered an invalid input
            return


    ### Limit to Selected Checkbox
    @pyqtSlot()
    def handleLimitSelected(self):
        #If there are selected layers in QGIS
        if not self.currentLayer.getSelectedFeatures().isClosed():
            #Update the table
            self.refreshTable()

    ### Update on new selection
      # TODO: CHECK TO SEE IF THIS CAN BE REPLACED WITH refreshTable()
    @pyqtSlot()
    def handleSelectionChanged(self):
        #If there are selected layers in QGIS
        if not self.currentLayer.getSelectedFeatures().isClosed():
            print('Layers Selected')
        self.refreshTable()

    ### Decimal Selection Box
    @pyqtSlot()
    def handleDecimalChanged(self):
        self.currentDecimalPrecision = self.numberOfDecimalsBox.value()
        self.refreshTable()


    ### Next/Previous
    @pyqtSlot()
    def setNextField(self):
        """
        Method implements next field when Next button is clicked
        """
        pass
        # index = self.selectFieldComboBox.currentIndex()
        # try:
        #     index = (index + 1) % self.selectFieldComboBox.count()
        # except ZeroDivisionError:
        #     # TODO not sure what it should do here...
        #     index = 0
        # self.selectFieldComboBox.setCurrentIndex(index)

    @pyqtSlot()
    def setPrevField(self):
        """
        Method implements pevious field when Previous button is clicked
        """
        pass
        # index = self.selectFieldComboBox.currentIndex()
        # try:
        #     index = (index - 1) % self.selectFieldComboBox.count()
        # except ZeroDivisionError:
        #     index = 0
        # self.selectFieldComboBox.setCurrentIndex(index)

    def refreshLayers(self):
        """
        Reload the layers coboBox with the current content of the layers list
        """
        self.selectLayerComboBox.clear()

        layers = self.fieldGetterInst.getVectorLayers()
        self.selectLayerComboBox.insertItems(0, layers)


    @pyqtSlot()
    def refreshFields(self):
        """
        Reload the fields coboBox with the current content of the field lists
        """
        self.selectFieldListWidget.clear()

        layer = self.fieldGetterInst.getSingleLayer \
                (self.selectLayerComboBox.currentText())
        if layer != None:
            self.currentLayer = layer
            self.allFields = self.currentLayer.fields()
            self.selectFieldListWidget.insertItem(0, "All")
            self.selectFieldListWidget.insertItems \
                (1, self.fieldGetterInst.getAllFields(layer))

            # 3 is Extended, 2 is Multi, check the documentation
            self.selectFieldListWidget.setSelectionMode(3)

            # Connect the current layer to a pyqtSlot
            self.currentLayer.selectionChanged.connect(self.handleSelectionChanged)


    @pyqtSlot()
    def refreshTable(self):
        """
        Refresh the table content with coresponding Layer & field selection
        """
        self.tableWidget.setSortingEnabled(False)
        self.tableWidget.clear()

        # Get selected fields
        fields = []
        selectedFields = self.selectFieldListWidget.selectedItems()
        for field in selectedFields:
            fields.append(field.text())

        # If the field is not set yet (Layer was swapped)
        # Return until the refresh is ready
        if len(fields) is 0:
            return

        if self.limitToSelected.isChecked():
            if not self.currentLayer.getSelectedFeatures().isClosed():
                # If there are features selected, get them
                features = self.currentLayer.getSelectedFeatures()
            else:
                # Else get all features
                features = self.currentLayer.getFeatures()
        else:
            features = self.currentLayer.getFeatures()

        # Determine length
        total = 0
        for feature in features:
            total += 1
        self.tableWidget.setRowCount(total)

        if self.limitToSelected.isChecked():
            if not self.currentLayer.getSelectedFeatures().isClosed():
                # If there are features selected, get them
                features = self.currentLayer.getSelectedFeatures()
            else:
                # Else get all features
                features = self.currentLayer.getFeatures()
        else:
            features = self.currentLayer.getFeatures()

        # Data to pass to statistical calculations
        statValues = []
        for i in range(len(fields)):
            statValues.append([])

        # for each row
        row = 0
        for feature in features:
            if 'All' in fields:
                attributes = feature.attributes()
                self.tableWidget.setColumnCount(len(attributes))

                col = 0
                # for each column value
                for attribute in attributes:
                    #Set the precision of numeric fields
                    if isinstance(attribute, float):
                        attribute = decimalRound(attribute,
                                                 self.currentDecimalPrecision)
                    self.tableWidget.setItem(row, col, MyTableWidgetItem(str(attribute)))
                    col += 1

            else:
                self.tableWidget.setColumnCount(len(fields))

                col = 0
                for field in fields:
                    fieldIndex = feature.fieldNameIndex(field)
                    attribute = feature.attributes()[fieldIndex]
                    if isinstance(attribute, float):
                        attribute = decimalRound(attribute,
                                                     self.currentDecimalPrecision)
                    statValues[col].append(attribute)
                    self.tableWidget.setItem(row, col, MyTableWidgetItem(str(attribute)))
                    col += 1

            row += 1
            featureInst = feature


        if 'All' in fields:
            fields = self.fieldGetterInst.getAllFields(self.currentLayer)
            self.tableWidget.setHorizontalHeaderLabels(fields)
        else:
            self.tableWidget.setHorizontalHeaderLabels(fields)

            statistics = []
            for i in range(len(fields)):
                fieldIndex = featureInst.fieldNameIndex(fields[i])
                if self.allFields.at(fieldIndex).isNumeric():
                    #Generate numeric statistics
                    statistics.append(self.createNumericalStatistics(statValues[i]))
                else:
                    #Generate character statistics
                    statistics.append(self.createCharacterStatistics(statValues[i]))

            self.refreshStatistics(fields, statistics)

        self.dataTableLayout.addWidget(self.tableWidget)
        self.dataTab.setLayout(self.dataTableLayout)
        self.tableWidget.setSortingEnabled(True)


    def createNumericalStatistics(self, inputArray):
        """
        createNumericalStatistics
        Methods that instantiates Numerical Statistics and initializes them
        """
        percentileArray = []
        try:
            percentileArray = self.percentilesLineEdit.text().split(', ')
            for percentile in percentileArray:
                if float(percentile) < 0 or float(percentile) > 100:
                    raise ValueError
        except ValueError:
            # TODO: Prompt this in a dialouge
            print('Invalid Value for Percentile Detected!')
            percentileArray = []
        emptyCellsRemoved = removeEmptyCells(inputArray)
        numericalStatistics = FS3NumericalStatistics()
        numericalStatistics.initialize(emptyCellsRemoved, percentileArray)
        numericalStatistics.roundNumericStatistics(self.currentDecimalPrecision)
        return numericalStatistics


    def createCharacterStatistics(self, inputArray):
        """
        createNumericalStatistics
        Methods that instantiates Numerical Statistics and initializes them
        """
        percentileArray = []
        try:
            percentileArray = self.percentilesLineEdit.text().split(', ')
            for percentile in percentileArray:
                if float(percentile) < 0 or float(percentile) > 100:
                    raise ValueError
        except ValueError:
            # TODO: Prompt this in a dialouge
            print('Invalid Value for Percentile Detected!')
            percentileArray = []
        emptyCellsRemoved = removeEmptyCells(inputArray)
        characterStatistics = FS3CharacterStatistics()
        characterStatistics.initialize(emptyCellsRemoved, percentileArray)
        characterStatistics.roundCharacterStatistics(self.currentDecimalPrecision)
        return characterStatistics


    def refreshStatistics(self, fields, stats):
        """
        refreshStatistics
        Method that updates the statistic table
        """
        numAndCharStats = False
        verticalHeaders = stats[0].statName
        for i in range(len(stats)):
            for j in range(len(stats)):
                if isinstance(stats[i], FS3NumericalStatistics):
                    if isinstance(stats[j], FS3CharacterStatistics):
                        numAndCharStats = True
                        verticalHeaders = stats[i].statName + stats[j].statName
                        break

        self.statisticTable.clear()
        self.statisticTable.setRowCount(stats[0].statCount + stats[0].statCount * numAndCharStats)
        self.statisticTable.setColumnCount(len(fields))
        self.statisticTable.setVerticalHeaderLabels(verticalHeaders)
        self.statisticTable.setHorizontalHeaderLabels(fields)

        col = 0
        for stat in stats:
            #See if the field is numeric
            if isinstance(stat, FS3NumericalStatistics):
                row = 0
                self.statisticTable.setItem(row, col,
                                            QTableWidgetItem(str(stat.itemCount)))
                row += 1
                self.statisticTable.setItem(row, col,
                                            QTableWidgetItem(str(stat.maxValue)))
                row += 1
                self.statisticTable.setItem(row, col,
                                            QTableWidgetItem(str(stat.minValue)))
                row += 1
                self.statisticTable.setItem(row, col,
                                            QTableWidgetItem(str(stat.meanValue)))
                row += 1
                self.statisticTable.setItem(row, col,
                                            QTableWidgetItem(str(stat.medianValue)))
                row += 1
                self.statisticTable.setItem(row, col,
                                            QTableWidgetItem(str(stat.sumValue)))
                row += 1
                self.statisticTable.setItem(row, col,
                                            QTableWidgetItem(str(stat.stdDevValue)))
                row += 1
                self.statisticTable.setItem(row, col,
                                            QTableWidgetItem(str(stat.coeffVarValue)))
                row += 1
                for percentile in stat.percentiles:
                    self.statisticTable.setItem(row, col,
                                                QTableWidgetItem(str(percentile)))
                    row += 1
            else:
                # is character statistics
                row = 0
                if numAndCharStats:
                    row = stat.statCount

                self.statisticTable.setItem(row, col,
                                            QTableWidgetItem(str(stat.itemCount)))
                row += 1
                self.statisticTable.setItem(row, col,
                                            QTableWidgetItem(str(stat.maxLength)))
                row += 1
                self.statisticTable.setItem(row, col,
                                            QTableWidgetItem(str(stat.minLength)))
                row += 1
                self.statisticTable.setItem(row, col,
                                            QTableWidgetItem(str(stat.meanLength)))
                row += 1
                self.statisticTable.setItem(row, col,
                                            QTableWidgetItem(str(stat.medianLength)))
                row += 1
                self.statisticTable.setItem(row, col,
                                            QTableWidgetItem(str(stat.sumLength)))
                row += 1
                self.statisticTable.setItem(row, col,
                                            QTableWidgetItem(str(stat.stdDevLength)))
                row += 1
                self.statisticTable.setItem(row, col,
                                            QTableWidgetItem(str(stat.coeffVarLength)))
                row += 1
                for percentile in stat.percentiles:
                    self.statisticTable.setItem(row, col,
                                                QTableWidgetItem(str(percentile)))
                    row += 1
            col += 1

        self.statisticLayout.addWidget(self.statisticTable)
        self.statisticsTab.setLayout(self.statisticLayout)

    def refreshGraph(self):
        plot_path = test() # Get graph from fs3Graphs
        self.graphView.load(QUrl.fromLocalFile(plot_path))
        self.graphView.show()
        self.graphLayout.addWidget(self.graphView)
        self.graphTab.setLayout(self.graphLayout)

class MyTableWidgetItem(QTableWidgetItem):
    """
    Use to overload < operator so that the table will
    sort both numerically and then alphanumerically where appropriate
    """
    def __lt__(self, other):
        try:
            return float(self.text()) < float(other.text())
        except ValueError:
            return self.text() < other.text()
