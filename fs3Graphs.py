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
import plotly.offline as offline


from plotly import tools
#from shutil import copyfile
from qgis.core import NULL
from PyQt5.QtCore import pyqtSlot
from .graphOptions import GraphOptionsWindow
from .layerFieldGetter import LayerFieldGetter
from PyQt5.QtCore import QCoreApplication

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
            self.optionsWindow.xAxisDefaultBox.insertItem(0, QCoreApplication.translate("Grapher", "None"))
            self.optionsWindow.xAxisDefaultBox.insertItems(1, fields)

    def setData(self, layer, attributes=[[]], uniqueness=[], limitToSelected=False, fields=['']):
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
        self.fields = fields

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
                    if not value:
                        value = QCoreApplication.translate("Grapher", "NULL")
                    self.xValues.append(value)

        self.allYValues = attributes

        # Replace NULL with 'NULL'
        for i in range(len(self.allYValues)):
            for j in range(len(self.allYValues[i])):
                if not self.allYValues[i][j]:
                    self.allYValues[i][j] = QCoreApplication.translate("Grapher", "NULL")

        # Apply sort and transform
        if self.optionsWindow.dataSortingBox.currentText() == QCoreApplication.translate("Grapher", "Ascending"):
            zipped = zip(self.xValues, *self.allYValues)
            zipped = sorted(zipped, key = itemgetter(1))
            self.xValues, *self.allYValues = zip(*list(zipped))

        if self.optionsWindow.dataSortingBox.currentText() == QCoreApplication.translate("Grapher", "Descending"):
            zipped = zip(self.xValues, *self.allYValues)
            zipped = sorted(zipped, key = itemgetter(1), reverse = True)
            self.xValues, *self.allYValues = zip(*list(zipped))

        if self.optionsWindow.dataTransformBox.currentText() == QCoreApplication.translate("Grapher", "Log"):
            temp = []
            for yValues in self.allYValues:
                try:
                    temp.append([log10(val) if val > 0 else 0 for val in yValues])
                except TypeError:
                    # Don't do anything for characture data
                    pass
            self.allYValues = temp


    def makeGraph(self):
        """
        Creates the currently selected graph type
        returns the path of the created graph
        """

        # refesh data to include any options from the options window
        self.setData(self.layer, self.attributes, self.uniqueness, self.limitToSelected, self.fields)

        if self.graphTypeBox.currentText() == QCoreApplication.translate("Grapher", "Bar"):
            plot_path = self.makeBarGraph()
        elif self.graphTypeBox.currentText() == QCoreApplication.translate("Grapher", "Pie"):
            plot_path = self.makePieGraph()
        elif self.graphTypeBox.currentText() == QCoreApplication.translate("Grapher", "Line"):
            plot_path = self.makeLineGraph()
        elif self.graphTypeBox.currentText() == QCoreApplication.translate("Grapher", "Scatter"):
            plot_path = self.makeScatterGraph()
        else:
            plot_path = ''

        return plot_path

    def makeBarGraph(self):

        data = []
        i = 0
        for yValues in self.allYValues:
            trace = go.Bar(
                    x = self.xValues,
                    y = yValues,
                    name = self.fields[i]
            )
            data.append(trace)
            i += 1

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
        raw_plot += plotly.offline.plot(fig, output_type='div',
        filename='bar-graph', include_plotlyjs=False, show_link=False, image='png')

        # Generate a temporary html file that can be viewed on a web browser
        # Allows use of plotly's full features QGIS does not support.
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
        raw_plot += plotly.offline.plot(fig, output_type='div',
        filename='pie-graph', include_plotlyjs=False, show_link=False, image='png')

        # Generate a temporary html file that can be viewed on a web browser
        # Allows use of plotly's full features QGIS does not support.
        plot_path = os.path.join(tempfile.gettempdir(), 'temp_plot_name.html')
        with open(plot_path, "w") as f:
            f.write(raw_plot)
            
        return plot_path


    def makeLineGraph(self):

        data = []
        i = 0
        for yValues in self.allYValues:
            trace = go.Scatter(
                    x = self.xValues,
                    y = yValues,
                    name = self.fields[i]
            )
            data.append(trace)
            i += 1

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

        raw_plot += plotly.offline.plot(fig, output_type='div',
                include_plotlyjs=False, filename='/tmp/line-graph', show_link=False, image='png')

        # Generate a temporary html file that can be viewed on a web browser
        # Allows use of plotly's full features QGIS does not support.
        plot_path = os.path.join(tempfile.gettempdir(), 'temp_plot_name.html')
        with open(plot_path, "w") as f:
            f.write(raw_plot)

        return plot_path


    def makeScatterGraph(self):
        #img_name = 'my-plot'
        #dload = os.path.expanduser('~/Downloads')
        #save_dir = '/tmp'

        data = []
        i = 0
        for yValues in self.allYValues:
            trace = go.Scatter(
                    x = self.xValues,
                    y = yValues,
                    name = self.fields[i],
                    mode = 'markers'
            )
            data.append(trace)
            i += 1

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
        raw_plot += plotly.offline.plot(fig, output_type='div',
        include_plotlyjs=False, show_link=False, filename='/tmp/scatter-graph', image='png')

        # Generate a temporary html file that can be viewed on a web browser
        # Allows use of plotly's full features QGIS does not support.
        plot_path = os.path.join(tempfile.gettempdir(), 'temp_plot_name.html')
        with open(plot_path, "w") as f:
            f.write(raw_plot)

        #copyfile('{}/{}.png'.format(save_dir, img_name),
        #       '{}/{}.png'.format(dload, img_name))
        return plot_path

