# -*- coding: utf-8 -*-
"""

@author: Orden Aitchedji, Mckenna Duzac, Andreas Foulk, Tanner Lee
@Repository: https://github.com/andreasfoulk/FS3

"""
from __future__ import print_function

import os
from qgis.core import QgsProject, NULL
from PyQt5 import uic

from PyQt5.QtCore import Qt, pyqtSlot, QUrl
from PyQt5.QtWidgets import QApplication, QMainWindow, QErrorMessage
from PyQt5.QtWidgets import QVBoxLayout, QTableWidget, QTableWidgetItem
# TODO what do we need from the QWebKit?
#from PyQt5.QtWebKit import QWebView
from PyQt5.QtWebKitWidgets import QWebView

from .layerFieldGetter import LayerFieldGetter
from .fs3Stats import FS3NumericalStatistics, FS3CharacterStatistics
from .fs3Stats import removeEmptyCells
from .fs3Graphs import Grapher
from .fs3Unique import FS3Uniqueness
from .roundFunc import decimalRound

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
        self.emptyCellDict = {}    #{feature_id:cell}

        self.percentile25Update()
        self.currentDecimalPrecision = 0

        self.error = QErrorMessage()

        ### Tabs
        self.dataTableLayout = QVBoxLayout()
        self.tableWidget = QTableWidget()
        ### Data Table Widget Connection
        self.tableWidget.cellChanged.connect(self.attributeCellChanged)
        self.statisticLayout = QVBoxLayout()
        self.statisticTable = QTableWidget()
        self.uniqueLayout = QVBoxLayout()
        self.uniqueTable = QTableWidget()
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
        # Toggle Edit Mode
        self.editModeCheck.stateChanged.connect(self.handleEditModeChecked)
        # Decimal Selector
        self.numberOfDecimalsBox.valueChanged.connect(self.handleDecimalChanged)

        ### Layer Combo Box and Field List Widget
        self.selectLayerComboBox.currentIndexChanged \
                        .connect(self.refreshFields)
        self.selectFieldListWidget.itemSelectionChanged \
                        .connect(self.refreshAttributes)

        ### Handles graph stuffs
        self.grapher = Grapher(self.graphTypeBox)
        self.graphTypeBox.currentIndexChanged.connect(self.refreshGraph)
        self.selectFieldListWidget.itemSelectionChanged \
                        .connect(self.refreshGraph)


    def refresh(self):
        """
        Reload data
        """
        self.refreshLayers()
        self.refreshFields()
        self.refreshAttributes()


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
            self.refreshAttributes()
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
            self.refreshAttributes()

    ### Edit Mode Checkbox
    @pyqtSlot()
    def handleEditModeChecked(self):
        # Edit box was checked
        # Check state
        if self.editModeCheck.isChecked():
            # Check if the layer is already in edit mode
            if self.currentLayer.isEditable():
                # Our work here is already done
                return
            # Else set the layer to editable
            self.currentLayer.startEditing()
        else:
            # Else the checkbox is unchecked
            # Check state of the layer
            if not self.currentLayer.isEditable():
                # Our work here is already done
                return
            # Else set the layer to noneditable
            self.currentLayer.commitChanges()

    ### Editing Started and Stopped Signals
    @pyqtSlot()
    def editingStartedQGIS(self):
        if self.editModeCheck.isChecked():
            # The checkbox is already checked, return
            return
        self.editModeCheck.setChecked(True)

    @pyqtSlot()
    def editingStoppedQGIS(self):
        if not self.editModeCheck.isChecked():
            # The checkbox is already unchecked, return
            return
        self.editModeCheck.setChecked(False)

    ### User has changed a value of a attribute cell
    @pyqtSlot('int', 'int')
    def attributeCellChanged(self, row, column):
        newValue = self.tableWidget.item(row, column)
        if self.currentLayer.isEditable():
            # Make the change then commit the change
            fieldname = self.tableWidget.horizontalHeaderItem(column).text()
            for fid, cell in self.emptyCellDict.items():
                feature = self.currentLayer.getFeature(fid)
                fieldIndex = feature.fieldNameIndex(fieldname)
                if cell == newValue:
                    success = self.currentLayer.changeAttributeValue(fid,
                                                            fieldIndex,
                                                            newValue.text())
                    if success:
                        # Update was successful, commit changes
                        successCommit = self.currentLayer.commitChanges()
                        if not successCommit:
                            commitError = str((len(self.currentLayer.commitErrors())))
                            commitError += '\n' + str((self.currentLayer.commitErrors()[0]))
                            self.error.showMessage(commitError)
                        else:
                            #Else the operation was a success
                            self.currentLayer.startEditing()
                    else:
                        # Update failed, report error
                        updateError = 'Attribute update failed'
                        self.error.showMessage(updateError)


    ### Update on new selection
    @pyqtSlot()
    def handleSelectionChanged(self):
        #If there are selected layers in QGIS
        self.refreshAttributes()

    ### Decimal Selection Box
    @pyqtSlot()
    def handleDecimalChanged(self):
        self.currentDecimalPrecision = self.numberOfDecimalsBox.value()
        self.refreshAttributes()

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

            #Listen for editing mode enabled and disabled
            self.currentLayer.editingStarted.connect(self.editingStartedQGIS)
            self.currentLayer.editingStopped.connect(self.editingStoppedQGIS)



    @pyqtSlot()
    def refreshAttributes(self):
        """
        Refresh the table content with coresponding Layer & field selection
        """
        self.tableWidget.setSortingEnabled(False)
        self.emptyCellDict.clear()
        self.tableWidget.blockSignals(True)
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
                    if attribute == NULL:
                        cell = MyTableWidgetItem("")
                        self.tableWidget.setItem(row, col, cell)
                        self.emptyCellDict[feature.id()] = cell
                    else:
                        cell = MyTableWidgetItem(str(attribute))
                        self.tableWidget.setItem(row, col, cell)
                        self.emptyCellDict[feature.id()] = cell
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
                    if attribute == NULL:
                        cell = MyTableWidgetItem("")
                        self.tableWidget.setItem(row, col, cell)
                        self.emptyCellDict[feature.id()] = cell
                    else:
                        cell = MyTableWidgetItem(str(attribute))
                        self.tableWidget.setItem(row, col, cell)
                        self.emptyCellDict[feature.id()] = cell
                    col += 1

            row += 1
            featureInst = feature


        if 'All' in fields:
            fields = self.fieldGetterInst.getAllFields(self.currentLayer)
            self.tableWidget.setHorizontalHeaderLabels(fields)
        else:
            self.tableWidget.setHorizontalHeaderLabels(fields)

            statistics = []
            data = []
            uniquenesses = []
            for i in range(len(fields)):
                fieldIndex = featureInst.fieldNameIndex(fields[i])
                uniquenesses.append(statValues[i])
                if self.allFields.at(fieldIndex).isNumeric():
                    #Generate numeric statistics
                    statistics.append(self.createNumericalStatistics(statValues[i]))
                    data.append(statValues[i])
                else:
                    #Generate character statistics
                    statistics.append(self.createCharacterStatistics(statValues[i]))
                    data.append(statValues[i])

            self.grapher.setData(fields, data)
            self.fields = fields
            self.attributes = data
            uniqueCalculation = self.createUniqueness(uniquenesses)
            self.refreshUnique(fields, uniqueCalculation)

            self.refreshStatistics(fields, statistics)

        self.dataTableLayout.addWidget(self.tableWidget)
        self.dataTab.setLayout(self.dataTableLayout)
        self.tableWidget.blockSignals(False)
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
            self.error.showMessage('Invalid Value for Percentile Detected!')
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
            self.error.showMessage('Invalid Value for Percentile Detected!')
            percentileArray = []
        emptyCellsRemoved = removeEmptyCells(inputArray)
        characterStatistics = FS3CharacterStatistics()
        characterStatistics.initialize(emptyCellsRemoved, percentileArray)
        characterStatistics.roundCharacterStatistics(self.currentDecimalPrecision)
        return characterStatistics

    def createUniqueness(self, inputArray):
        """
        createUniqueness
        Method that instantiates Uniqueness class and initializes it
        """
        uniqueness = FS3Uniqueness()
        uniqueness.initialize(inputArray)
        uniqueness.roundUniqueness(self.currentDecimalPrecision)
        return uniqueness


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

    def refreshUnique(self, fields, unique):
        #Start by clearing the layout
        self.uniqueTable.setSortingEnabled(False)
        row = 0
        col = 0
        self.uniqueTable.clear()
        self.uniqueTable.setRowCount(unique.totalValues)
        self.uniqueTable.setColumnCount(unique.statCount)
        horizontalHeaders = unique.statName
        #Append the names of the fields to the value field
        horizontalHeaders[0] += ' ('
        for field in fields:
            horizontalHeaders[0] += field + ', '
        horizontalHeaders[0] = horizontalHeaders[0][:-2]
        horizontalHeaders[0] += ')'
        self.uniqueTable.setHorizontalHeaderLabels(horizontalHeaders)
        for value in unique.uniqueValues:
            self.uniqueTable.setItem(row, col,
                                 MyTableWidgetItem(str(value)))
            row += 1
        row = 0
        col += 1
        for occurance in unique.uniqueNumOccur:
            self.uniqueTable.setItem(row, col,
                                 MyTableWidgetItem(str(occurance)))
            row += 1
        row = 0
        col += 1
        for percent in unique.uniquePercent:
            self.uniqueTable.setItem(row, col,
                                 MyTableWidgetItem(str(percent)))
            row += 1
        self.uniqueTable.setSortingEnabled(True)
        self.uniqueLayout.addWidget(self.uniqueTable)
        self.uniqueTab.setLayout(self.uniqueLayout)

    @pyqtSlot()
    def refreshGraph(self):
        plot_path = self.grapher.makeGraph()
        self.graphView.load(QUrl.fromLocalFile(plot_path))
        self.graphLayout.addWidget(self.graphView)
        self.graphFrame.setLayout(self.graphLayout)
        self.graphView.show()


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
