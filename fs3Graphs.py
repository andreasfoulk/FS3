# -*- coding: utf-8 -*-
"""
Created on Tue May 31 11:24:02 2018

@author: Andreas Foulk

@descriptions: This file creates plotly graphs
and writes them to a file so that the QWebView
can load them into the gui.
"""

import tempfile
import os
import platform
from math import log10
from operator import itemgetter

import plotly
import plotly.graph_objs as go

from PyQt5.QtCore import QCoreApplication

from qgis.core import NULL

from .graphOptions import GraphOptionsWindow
from .layerFieldGetter import LayerFieldGetter

class Grapher:
    """
    The Grapher class graphs for some reason
    """
    def __init__(self, graphTypeBox):
        if platform.system() == 'Windows':
            self.polyfillpath = 'file:///'
            self.plotlypath = 'file:///'
            self.polyfillpath += os.path.join(os.path.dirname(__file__), 'jsscripts/polyfill.min.js')
            self.plotlypath += os.path.join(os.path.dirname(__file__), 'jsscripts/plotly-1.34.0.min.js')
        else:
            self.polyfillpath = os.path.join(os.path.dirname(__file__), 'jsscripts/polyfill.min.js')
            self.plotlypath = os.path.join(os.path.dirname(__file__), 'jsscripts/plotly-1.34.0.min.js')

        self.graphTypeBox = graphTypeBox
        graphTypes = [QCoreApplication.translate("Grapher", "Bar"),
                      QCoreApplication.translate("Grapher", "Pie"),
                      QCoreApplication.translate("Grapher", "Line"),
                      QCoreApplication.translate("Grapher", "Scatter")]
        self.graphTypeBox.insertItems(0, graphTypes)

        self.optionsWindow = GraphOptionsWindow()

        # Assign with setData
        self.layer = None
        self.xValues = []
        self.allYValues = [[]]
        self.attributes = [[]]
        self.uniqueness = []
        self.fields = ['']
        self.limitToSelected = False


    def openGraphOptions(self):
        """
        Opens the graph options dialog
        Connected to Open Graph Settings button in fs3Run.py
        """
        self.setLayerFields()
        self.optionsWindow.exec_()

    def setLayerFields(self):
        """
        Fill the default x-axis combobox with the current layer's fields
        """
        self.optionsWindow.xAxisDefaultBox.clear()

        if self.layer:
            getter = LayerFieldGetter()
            fields = getter.getAllFields(self.layer)
            self.optionsWindow.xAxisDefaultBox.insertItem(0, QCoreApplication.translate("Grapher", "None"))
            self.optionsWindow.xAxisDefaultBox.insertItems(1, fields)

    def setData(self, layer, attributes=None, uniqueness=None, limitToSelected=False, fields=None):
        """
        Sets self variables
        xValues defaults to 1 through n if no default is selected
        Checks if the data should be sorted or transformed
        Does sort or transform
        """
        self.layer = layer
        self.limitToSelected = limitToSelected
        self.attributes = attributes
        if uniqueness:
            self.uniqueness = uniqueness
        if fields:
            self.fields = fields

        if not self.attributes:
            return

        # Set x-axis to selected field
        if self.optionsWindow.xAxisDefaultBox.currentText() == QCoreApplication.translate("Grapher", "None"):
            self.xValues = list(range(len(self.attributes[0])))
        else:
            if self.layer:
                if self.limitToSelected:
                    if not self.layer.getSelectedFeatures().isClosed():
                        # If there are features selected, get them
                        features = self.layer.getSelectedFeatures()
                    else:
                        # Else get all features
                        features = self.layer.getFeatures()
                else:
                    features = self.layer.getFeatures()

                self.xValues = []
                for feature in features:
                    fieldIndex = feature.fieldNameIndex(self.optionsWindow.xAxisDefaultBox.currentText())
                    value = feature.attributes()[fieldIndex]
                    if value == NULL:
                        value = QCoreApplication.translate("Grapher", "NULL")
                    self.xValues.append(value)

        self.allYValues = self.attributes

        # Apply sort and transform
        if self.optionsWindow.dataSortingBox.currentText() == QCoreApplication.translate("Grapher", "Ascending"):
            zipped = zip(self.xValues, *self.allYValues)
            zipped = sorted(zipped, key=itemgetter(1))
            self.xValues, *self.allYValues = zip(*list(zipped))
            self.xValues = list(self.xValues)
            self.allYValues = [list(yValues) for yValues in self.allYValues]

        if self.optionsWindow.dataSortingBox.currentText() == QCoreApplication.translate("Grapher", "Descending"):
            zipped = zip(self.xValues, *self.allYValues)
            zipped = sorted(zipped, key=itemgetter(1), reverse=True)
            self.xValues, *self.allYValues = zip(*list(zipped))
            self.xValues = list(self.xValues)
            self.allYValues = [list(yValues) for yValues in self.allYValues]

        if self.optionsWindow.dataTransformBox.currentText() == QCoreApplication.translate("Grapher", "Log"):
            temp = []
            for yValues in self.allYValues:
                try:
                    temp.append([log10(val) if val > 0 else 0 for val in yValues])
                except TypeError:
                    # Don't do anything for characture data
                    temp.append(yValues)
            self.allYValues = temp

        ## Prepare data for plotly
        # Replace NULL with 'NULL'
        for i in range(len(self.allYValues)):
            for j in range(len(self.allYValues[i])):
                if self.allYValues[i][j] == NULL:
                    self.allYValues[i][j] = QCoreApplication.translate("Grapher", "NULL")

        # Plotly doesn't like unordered number for x, will auto reorder them
        if self.optionsWindow.xAxisDefaultBox.currentText() == QCoreApplication.translate("Grapher", "None"):
            self.xValues = list(range(len(self.allYValues[0])))


    def makeGraph(self):
        """
        Creates the currently selected graph type
        returns the path of the created graph
        """

        # Ensure there is data to graph
        if not self.attributes:
            return ''

        # refesh data to include any options from the options window
        self.setData(self.layer, self.attributes, self.uniqueness, self.limitToSelected, self.fields)

        if self.graphTypeBox.currentText() == QCoreApplication.translate("Grapher", "Bar"):
            plotPath = self.makeBarGraph()
        elif self.graphTypeBox.currentText() == QCoreApplication.translate("Grapher", "Pie"):
            plotPath = self.makePieGraph()
        elif self.graphTypeBox.currentText() == QCoreApplication.translate("Grapher", "Line"):
            plotPath = self.makeLineGraph()
        elif self.graphTypeBox.currentText() == QCoreApplication.translate("Grapher", "Scatter"):
            plotPath = self.makeScatterGraph()
        else:
            plotPath = ''

        return plotPath

    def makeBarGraph(self):
        """
        Constructs a plotly js bar graph and saves to a tempfile
        returns the path to this tempfile
        """

        data = []
        i = 0
        for yValues in self.allYValues:
            trace = go.Bar(
                x=self.xValues,
                y=yValues,
                name=self.fields[i]
            )
            data.append(trace)
            i += 1

        layout = go.Layout(
            title=self.optionsWindow.graphTitleEdit.text(),
            barmode='group',
            xaxis=dict(
                title=self.optionsWindow.xAxisTitleEdit.text()
                ),
            yaxis=dict(
                title=self.optionsWindow.yAxisTitleEdit.text()
                )
        )

        fig = go.Figure(data=data, layout=layout)

        # first lines of additional html with the link to the local javascript
        rawPlot = '<head><meta charset="utf-8" /><script src="{}"></script><script src="{}"></script></head>'.format(self.polyfillpath, self.plotlypath)

        # call the plot method without all the javascript code
        rawPlot += plotly.offline.plot(fig, output_type='div',
                                       filename='bar-graph', include_plotlyjs=False, show_link=False, image='png')

        # Generate a temporary html file that can be viewed on a web browser
        # Allows use of plotly's full features QGIS does not support.
        plotPath = os.path.join(tempfile.gettempdir(), 'temp_plot_name.html')
        with open(plotPath, "w") as file:
            file.write(rawPlot)

        return plotPath


    def makePieGraph(self):
        """
        Constructs a plotly js pie graph and saves to a tempfile
        returns the path to this tempfile
        """

        trace = go.Pie(
            labels=self.uniqueness.uniqueValues,
            values=self.uniqueness.uniqueNumOccur
        )

        data = [trace]
        layout = go.Layout(
            title=self.optionsWindow.graphTitleEdit.text(),
            barmode='group'
        )

        fig = go.Figure(data=data, layout=layout)

        # first lines of additional html with the link to the local javascript
        rawPlot = '<head><meta charset="utf-8" /><script src="{}"></script><script src="{}"></script></head>'.format(self.polyfillpath, self.plotlypath)

        # call the plot method without all the javascript code
        rawPlot += plotly.offline.plot(fig, output_type='div',
                                       filename='pie-graph', include_plotlyjs=False, show_link=False, image='png')

        # Generate a temporary html file that can be viewed on a web browser
        # Allows use of plotly's full features QGIS does not support.
        plotPath = os.path.join(tempfile.gettempdir(), 'temp_plot_name.html')
        with open(plotPath, "w") as file:
            file.write(rawPlot)

        return plotPath


    def makeLineGraph(self):
        """
        Constructs a plotly js line graph and saves to a tempfile
        returns the path to this tempfile
        """

        data = []
        i = 0
        for yValues in self.allYValues:
            trace = go.Scatter(
                x=self.xValues,
                y=yValues,
                name=self.fields[i]
            )
            data.append(trace)
            i += 1

        layout = go.Layout(
            title=self.optionsWindow.graphTitleEdit.text(),
            barmode='group',
            xaxis=dict(
                title=self.optionsWindow.xAxisTitleEdit.text()
                ),
            yaxis=dict(
                title=self.optionsWindow.yAxisTitleEdit.text()
                )
        )

        fig = go.Figure(data=data, layout=layout)

        # first lines of additional html with the link to the local javascript
        rawPlot = '<head><meta charset="utf-8" /><script src="{}"></script><script src="{}"></script></head>'.format(self.polyfillpath, self.plotlypath)

        # call the plot method without all the javascript code

        rawPlot += plotly.offline.plot(fig, output_type='div',
                                       include_plotlyjs=False, filename='/tmp/line-graph', show_link=False, image='png')

        # Generate a temporary html file that can be viewed on a web browser
        # Allows use of plotly's full features QGIS does not support.
        plotPath = os.path.join(tempfile.gettempdir(), 'temp_plot_name.html')
        with open(plotPath, "w") as file:
            file.write(rawPlot)

        return plotPath


    def makeScatterGraph(self):
        """
        Constructs a plotly js scatter chart and saves to a tempfile
        returns the path to this tempfile
        """

        data = []
        i = 0
        for yValues in self.allYValues:
            trace = go.Scatter(
                x=self.xValues,
                y=yValues,
                name=self.fields[i],
                mode='markers'
            )
            data.append(trace)
            i += 1

        layout = go.Layout(
            title=self.optionsWindow.graphTitleEdit.text(),
            barmode='group',
            xaxis=dict(
                title=self.optionsWindow.xAxisTitleEdit.text()
                ),
            yaxis=dict(
                title=self.optionsWindow.yAxisTitleEdit.text()
                )
        )

        fig = go.Figure(data=data, layout=layout)

        # first lines of additional html with the link to the local javascript
        rawPlot = '<head><meta charset="utf-8" /><script src="{}"></script><script src="{}"></script></head>'.format(self.polyfillpath, self.plotlypath)

        # call the plot method without all the javascript code
        rawPlot += plotly.offline.plot(fig, output_type='div',
                                       include_plotlyjs=False, show_link=False, filename='/tmp/scatter-graph', image='png')

        # Generate a temporary html file that can be viewed on a web browser
        # Allows use of plotly's full features QGIS does not support.
        plotPath = os.path.join(tempfile.gettempdir(), 'temp_plot_name.html')
        with open(plotPath, "w") as file:
            file.write(rawPlot)

        return plotPath
