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
import re
from math import log10

import plotly
import plotly.graph_objs as go
from plotly import tools

from qgis.core import NULL

from PyQt5.QtCore import pyqtSlot

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
        graphTypes = ['Bar', 'Pie', 'Line', 'Scatter']
        self.graphTypeBox.insertItems(0, graphTypes)

        self.optionsWindow = GraphOptionsWindow()


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

        if self.layer is not None:
            getter = LayerFieldGetter()
            fields = getter.getAllFields(self.layer)
            self.optionsWindow.xAxisDefaultBox.insertItem(0, 'None')
            self.optionsWindow.xAxisDefaultBox.insertItems(1, fields)

    def setData(self, layer, attributes=[[]], uniqueness=[], limitToSelected=False):
        """
        Sets self variables
        xValues defaults to 1 through n if no default is selected
        Checks if the data should be sorted or transformed
        Does sort or transform
        """
        self.layer = layer
        self.attributes = attributes
        self.uniqueness = uniqueness
        self.limitToSelected = limitToSelected

        # Set x-axis to selected field
        if self.optionsWindow.xAxisDefaultBox.currentText() == 'None':
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
                    self.xValues.append(feature.attributes()[fieldIndex])

        self.allYValues = attributes
        self.yValues = attributes[0]

        self.hasNull = False

        # Remove the null attributes and their associated fields
        for index in range(0, len(self.yValues)):
            if self.yValues[index] == NULL:
                # Remove this from both lists
                self.hasNull = True
                self.yValues[index] = 'NULL'

        # Apply sort and transform
        if self.optionsWindow.dataSortingBox.currentText() == 'Ascending':
            #zipped = zip(self.xValues, *self.allYValues)
            self.yValues = sorted(self.yValues)

        if self.optionsWindow.dataSortingBox.currentText() == 'Descending':
            self.yValues = sorted(self.yValues, reverse = True)

        if self.optionsWindow.dataTransformBox.currentText() == 'Log':
            try:
                self.yValues = [log10(val) if val > 0 else 0 for val in self.yValues]
            except TypeError:
                # Don't do anything for characture data
                pass


    def makeGraph(self):
        """
        Creates the currently selected graph type
        returns the path of the created graph
        """

        # refesh data to include any options from the options window
        self.setData(self.layer, self.attributes, self.uniqueness, self.limitToSelected)

        if self.graphTypeBox.currentText() == 'Bar':
            plot_path = self.makeBarGraph()
        elif self.graphTypeBox.currentText() == 'Pie':
            plot_path = self.makePieGraph()
        elif self.graphTypeBox.currentText() == 'Line':
            plot_path = self.makeLineGraph()
        elif self.graphTypeBox.currentText() == 'Scatter':
            plot_path = self.makeScatterGraph()
        else:
            plot_path = ''

        return plot_path

    def makeBarGraph(self):

        data = []
        for yValues in self.allYValues:
            data.append(
                trace = go.Bar(
                    x = self.xValues,
                    y = yValues
                )
            )

        layout = go.Layout(
                title = self.optionsWindow.graphTitleEdit.text(),
                barmode = 'group',
                xaxis = dict(
                        title = self.optionsWindow.xAxisTitleEdit.text()
                        ),
                yaxis = dict(
                        title = self.optionsWindow.yAxisTitleEdit.text()
                        )
        )

        fig = go.Figure(data = data, layout = layout)

        # first lines of additional html with the link to the local javascript
        raw_plot = '<head><meta charset="utf-8" /><script src="{}"></script><script src="{}"></script></head>'.format(self.polyfillpath, self.plotlypath)
        # call the plot method without all the javascript code
        raw_plot += plotly.offline.plot(fig, output_type='div', include_plotlyjs=False, show_link=False)

        # use regex to replace the string ReplaceTheDiv with the correct plot id generated by plotly
        match = re.search('Plotly.newPlot\("([^"]+)', raw_plot)
        substr = match.group(1)
        raw_plot = raw_plot.replace('ReplaceTheDiv', substr)

        plot_path = os.path.join(tempfile.gettempdir(), 'temp_plot_name.html')
        with open(plot_path, "w") as f:
            f.write(raw_plot)

        return plot_path


    def makePieGraph(self):

        trace = go.Pie(
            labels = self.uniqueness.uniqueValues,
            values = self.uniqueness.uniqueNumOccur
        )

        data = [trace]
        layout = go.Layout(
                title = self.optionsWindow.graphTitleEdit.text(),
                barmode = 'group'
        )

        fig = go.Figure(data = data, layout = layout)

        # first lines of additional html with the link to the local javascript
        raw_plot = '<head><meta charset="utf-8" /><script src="{}"></script><script src="{}"></script></head>'.format(self.polyfillpath, self.plotlypath)
        # call the plot method without all the javascript code
        raw_plot += plotly.offline.plot(fig, output_type='div', include_plotlyjs=False, show_link=False)

        # use regex to replace the string ReplaceTheDiv with the correct plot id generated by plotly
        match = re.search('Plotly.newPlot\("([^"]+)', raw_plot)
        substr = match.group(1)
        raw_plot = raw_plot.replace('ReplaceTheDiv', substr)

        plot_path = os.path.join(tempfile.gettempdir(), 'temp_plot_name.html')
        with open(plot_path, "w") as f:
            f.write(raw_plot)

        return plot_path


    def makeLineGraph(self):

        if len(self.attributes) is 1:
            self.attributes.append([i for i in range(len(self.attributes[0]))])

            trace = go.Scatter(
                x = self.attributes[1],
                y = self.attributes[0],
                name='{}'.format('self.fields[0]')
            )
        else:
            trace = go.Scatter(
                x = self.attributes[0],
                y = self.attributes[1],
                name='{} x {}'.format('self.fields[0]', 'self.fields[1]')
            )

        data = [trace]

        layout = go.Layout(
                title = self.optionsWindow.graphTitleEdit.text(),
                barmode = 'group',
                xaxis = dict(
                        title = self.optionsWindow.xAxisTitleEdit.text()
                        ),
                yaxis = dict(
                        title = self.optionsWindow.yAxisTitleEdit.text()
                        )
        )

        fig = go.Figure(data = data, layout = layout)

        # first lines of additional html with the link to the local javascript
        raw_plot = '<head><meta charset="utf-8" /><script src="{}"></script><script src="{}"></script></head>'.format(self.polyfillpath, self.plotlypath)
        # call the plot method without all the javascript code
        raw_plot += plotly.offline.plot(fig, output_type='div', include_plotlyjs=False, show_link=False)

        # use regex to replace the string ReplaceTheDiv with the correct plot id generated by plotly
        match = re.search('Plotly.newPlot\("([^"]+)', raw_plot)
        substr = match.group(1)
        raw_plot = raw_plot.replace('ReplaceTheDiv', substr)

        plot_path = os.path.join(tempfile.gettempdir(), 'temp_plot_name.html')
        with open(plot_path, "w") as f:
            f.write(raw_plot)

        return plot_path


    def makeScatterGraph(self):

        # Create a trace
        if len(self.attributes) is 1:
            self.attributes.append([i for i in range(len(self.attributes[0]))])

            trace = go.Scatter(
                x = self.attributes[1],
                y = self.attributes[0],
                mode = 'markers'
            )
        else:
            trace = go.Scatter(
                x = self.attributes[0],
                y = self.attributes[1],
                mode = 'markers'
            )

        data = [trace]
        layout = go.Layout(
                title = self.optionsWindow.graphTitleEdit.text(),
                barmode = 'group',
                xaxis = dict(
                        title = self.optionsWindow.xAxisTitleEdit.text()
                        ),
                yaxis = dict(
                        title = self.optionsWindow.yAxisTitleEdit.text()
                        )
        )

        fig = go.Figure(data = data, layout = layout)

        # first lines of additional html with the link to the local javascript
        raw_plot = '<head><meta charset="utf-8" /><script src="{}"></script><script src="{}"></script></head>'.format(self.polyfillpath, self.plotlypath)
        # call the plot method without all the javascript code
        raw_plot += plotly.offline.plot(fig, output_type='div', include_plotlyjs=False, show_link=False)

        # use regex to replace the string ReplaceTheDiv with the correct plot id generated by plotly
        match = re.search('Plotly.newPlot\("([^"]+)', raw_plot)
        substr = match.group(1)
        raw_plot = raw_plot.replace('ReplaceTheDiv', substr)

        plot_path = os.path.join(tempfile.gettempdir(), 'temp_plot_name.html')
        with open(plot_path, "w") as f:
            f.write(raw_plot)

        return plot_path
