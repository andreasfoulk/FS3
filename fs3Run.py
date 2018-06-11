# -*- coding: utf-8 -*-
"""

    fs3Run.py -- Plugin implimentation handling UI features
              -- For more information see : https://github.com/andreasfoulk/FS3

    Copyright (c) 2018 Orden Aitchedji, Mckenna Duzac, Andreas Foulk, Tanner Lee

    This software may be modified and distributed under the terms
    of the MIT license.  See the LICENSE file for details.

"""
from __future__ import print_function

import os

from qgis.core import QgsProject, NULL

from PyQt5 import uic
from PyQt5.QtCore import Qt, pyqtSlot, QUrl, pyqtSignal, QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QErrorMessage
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem
from PyQt5.QtWebKitWidgets import QWebView
from PyQt5.QtGui import QColor

from .layerFieldGetter import LayerFieldGetter
from .fs3Stats import FS3NumericalStatistics, FS3CharacterStatistics
from .fs3Stats import removeEmptyCells
from .fs3Graphs import Grapher
from .fs3Unique import FS3Uniqueness
from .roundFunc import decimalRound
from .graphOptions import GraphOptionsWindow

QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'fs3.ui'))

class FS3MainWindow(QMainWindow, FORM_CLASS):
    """
    FS3MainWindow
    Handles the creation and display of the window.
    Makes use of the fs3.ui QT ui file.
    """
    resized = pyqtSignal()
    def __init__(self, parent=None):
        super(FS3MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.mainWindowSplitter.setStretchFactor(1, 10)
        self.setWindowTitle('FS3 -- FieldStats3')

        self.fieldGetterInst = LayerFieldGetter()
        self.currentProject = QgsProject.instance()
        self.currentLayer = None
        self.allFields = None
        self.emptyCellDict = {}    #{feature_id:cell}

        self.percentile25Update()
        self.currentDecimalPrecision = 0

        self.error = QErrorMessage()

        ### Tabs
        self.tabFields.currentChanged.connect(self.graphTabLoaded)
        self.dataTableLayout = QVBoxLayout()
        self.tableWidget = QTableWidget()
        ### Data Table Widget Connection
        self.tableWidget.cellChanged.connect(self.attributeCellChanged)
        self.horizontalHeader = self.tableWidget.horizontalHeader()
        self.horizontalHeader.sectionClicked.connect(self.handleDataSortSignal)
        self.statisticLayout = QVBoxLayout()
        self.statisticTable = QTableWidget()
        self.uniqueLayout = QVBoxLayout()
        self.uniqueTable = QTableWidget()
        self.uniqueTable.verticalHeader().hide()
        self.graphLayout = QHBoxLayout()
        self.graphView = QWebView()
        self.uniqueHHeader = self.uniqueTable.horizontalHeader()
        self.uniqueHHeader.sectionClicked.connect(self.handleUniqueSortSignal)
        
        ### Window resized
        self.resizeTimer = QTimer()
        self.resizeTimer.setSingleShot(True)
        self.resizeTimer.timeout.connect(self.windowTimeout)
        self.resized.connect(self.windowResized)

        ###Background Color Brush
        self.backgroundBrush = QColor.fromRgb(230, 230, 250)
        self.defaultBrush = QColor.fromRgbF(0, 0, 0, 0)

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
        self.graphTypeBox.currentIndexChanged.connect(self.refreshAttributes)

        self.openGraphSettings.clicked.connect(self.openGraphOptions)

    @pyqtSlot()
    def openGraphOptions(self):
        dialog = GraphOptionsWindow()
        dialog.exec_()

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
        """ Tokenize percentile display """
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
        self.refreshAttributes()

    ### Edit Mode Checkbox
    @pyqtSlot()
    def handleEditModeChecked(self):
        """ Edit Mode trigger within plugin UI """
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
        """ Handles events when in Edit Mode """
        if self.editModeCheck.isChecked():
            # The checkbox is already checked, return
            return
        self.editModeCheck.setChecked(True)

    @pyqtSlot()
    def editingStoppedQGIS(self):
        """ Handles events when out of Edit Mode """
        if not self.editModeCheck.isChecked():
            # The checkbox is already unchecked, return
            return
        self.editModeCheck.setChecked(False)

    ### User has changed a value of a attribute cell
    @pyqtSlot('int', 'int')
    def attributeCellChanged(self, row, column):
        """ Handles updates case any change were made in Edit Mode """
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


    ### User has clicked on a header in the table
    @pyqtSlot()
    def handleDataSortSignal(self):
        """ Handles propper sorting of statistic data """
        #Recolor the table
        for i in range(0, self.tableWidget.columnCount()):
            for j in range(0, self.tableWidget.rowCount()):
                cell = self.tableWidget.item(j, i)
                if (j%2) == 0:
                    #This is an even row, color it
                    cell.setBackground(self.backgroundBrush)
                else:
                    #This is an odd row, default its color
                    cell.setBackground(self.defaultBrush)

    @pyqtSlot()
    def handleUniqueSortSignal(self):
        """ Handles propper sorting of unique data """
        #Recolor the table
        for i in range(0, self.uniqueTable.columnCount()):
            for j in range(0, self.uniqueTable.rowCount()):
                cell = self.uniqueTable.item(j, i)
                if (j%2) == 0:
                    #This is an even row, color it
                    cell.setBackground(self.backgroundBrush)
                else:
                    #This is an odd row, default its color
                    cell.setBackground(self.defaultBrush)

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
                        attribute = decimalRound(attribute, self.currentDecimalPrecision)
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

            self.fields = fields
            self.attributes = data
            uniqueCalculation = self.createUniqueness(uniquenesses)
            self.grapher.setData(fields, data, uniqueCalculation)
            
            self.refreshUnique(fields, uniqueCalculation)

            self.refreshStatistics(fields, statistics)
            
            self.refreshGraph()

        self.dataTableLayout.addWidget(self.tableWidget)
        self.dataTab.setLayout(self.dataTableLayout)
        self.tableWidget.blockSignals(False)
        self.tableWidget.setSortingEnabled(True)
        self.handleDataSortSignal()


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
        originalSize = len(inputArray)
        emptyCellsRemoved = removeEmptyCells(inputArray)
        numericalStatistics = FS3NumericalStatistics()
        numericalStatistics.initialize(emptyCellsRemoved, percentileArray, originalSize)
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
        originalSize = len(inputArray)
        emptyCellsRemoved = removeEmptyCells(inputArray)
        characterStatistics = FS3CharacterStatistics()
        characterStatistics.initialize(emptyCellsRemoved, percentileArray, originalSize)
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
                emptyData = stat.totalItemCount - stat.itemCount
                row = 0
                self.statisticTable.setItem(row, col,
                                            QTableWidgetItem(str(stat.totalItemCount)))
                row += 1
                self.statisticTable.setItem(row, col,
                                            QTableWidgetItem(str(stat.itemCount)))
                row += 1
                self.statisticTable.setItem(row, col,
                                            QTableWidgetItem(str(emptyData)))
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
                                            QTableWidgetItem(str(stat.modeValue)))
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

                emptyData = stat.totalItemCount - stat.itemCount
                self.statisticTable.setItem(row, col,
                                            QTableWidgetItem(str(stat.totalItemCount)))
                row += 1
                self.statisticTable.setItem(row, col,
                                            QTableWidgetItem(str(stat.itemCount)))
                row += 1
                self.statisticTable.setItem(row, col,
                                            QTableWidgetItem(str(emptyData)))
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
                                            QTableWidgetItem(str(stat.modeLength)))
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

        self.handleStatisticsColor()

    def handleStatisticsColor(self):
        """ Method implements zebra colors with table rows """
        for i in range(0, self.statisticTable.columnCount()):
            for j in range(0, self.statisticTable.rowCount()):
                cell = self.statisticTable.item(j, i)
                if cell is None:
                    cell = MyTableWidgetItem("")
                    self.statisticTable.setItem(j, i, cell)
                if (j%2) == 0:
                    #This is an even row, color it
                    cell.setBackground(self.backgroundBrush)
                else:
                    #This is an odd row, default its color
                    cell.setBackground(self.defaultBrush)

    def refreshUnique(self, fields, unique):
        """
        refreshUnique
        Method that updates the unique table
        """
        #Start by clearing the layout
        self.uniqueTable.setSortingEnabled(False)
        row = 0
        col = 0
        self.uniqueTable.clear()
        self.uniqueTable.setRowCount(unique.totalValues)
        self.uniqueTable.setColumnCount(unique.statCount)
        horizontalHeaders = unique.statName
        #Append the names of the fields to the value field
        horizontalHeaders[0] += ' (['
        for field in fields:
            horizontalHeaders[0] += field + '] , ['
        horizontalHeaders[0] = horizontalHeaders[0][:-5]
        horizontalHeaders[0] += '])'
        self.uniqueTable.setHorizontalHeaderLabels(horizontalHeaders)
        for value in unique.uniqueValues:
            cell = MyTableWidgetItem(str(value))
            self.uniqueTable.setItem(row, col, cell)
            row += 1
        row = 0
        col += 1
        for occurance in unique.uniqueNumOccur:
            cell = MyTableWidgetItem(str(occurance))
            self.uniqueTable.setItem(row, col, cell)
            row += 1
        row = 0
        col += 1
        for percent in unique.uniquePercent:
            cell = MyTableWidgetItem(str(percent))
            self.uniqueTable.setItem(row, col, cell)
            row += 1
        self.uniqueTable.setSortingEnabled(True)
        self.handleUniqueSortSignal()
        self.uniqueLayout.addWidget(self.uniqueTable)
        self.uniqueTab.setLayout(self.uniqueLayout)

    @pyqtSlot()
    def refreshGraph(self):
        plot_path = self.grapher.makeGraph()
        self.graphView.load(QUrl.fromLocalFile(plot_path))
        self.graphLayout.addWidget(self.graphView)
        self.graphFrame.setLayout(self.graphLayout)
        self.graphView.show()
        
    def resizeEvent(self, event):
        self.resized.emit()
        return super(FS3MainWindow, self).resizeEvent(event)
    
    @pyqtSlot()
    def windowResized(self):
        self.resizeTimer.start(250)
        
    def windowTimeout(self):
        currentTab = self.tabFields.currentWidget()
        if currentTab == self.graphTab:
            #Refresh the attributes to create a new graph
            self.refreshAttributes()
        
    @pyqtSlot()
    def graphTabLoaded(self):
        currentTab = self.tabFields.currentWidget()
        if currentTab == self.graphTab:
            #Refresh the attributes to create a new graph
            self.refreshAttributes()

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
