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
import plotly
import plotly.graph_objs as go
import plotly.offline as offline

from math import log10
from plotly import tools
#from shutil import copyfile
from qgis.core import NULL
from PyQt5.QtCore import pyqtSlot
from .graphOptions import GraphOptionsWindow

class Grapher:
    """
    This class contains all the data
    """
    def __init__(self, graphTypeBox=None):
        if platform.system() == 'Windows':
            self.polyfillpath = 'file:///'
            self.plotlypath = 'file:///'
            self.polyfillpath += os.path.join(os.path.dirname(__file__), 'jsscripts/polyfill.min.js')
            self.plotlypath += os.path.join(os.path.dirname(__file__), 'jsscripts/plotly-1.34.0.min.js')
        else:
            self.polyfillpath = os.path.join(os.path.dirname(__file__), 'jsscripts/polyfill.min.js')
            self.plotlypath = os.path.join(os.path.dirname(__file__), 'jsscripts/plotly-1.34.0.min.js')

        self.fields = []
        self.attributes = []
        self.xValues = []
        self.yValues = []
        self.uniqueness = []

        self.graphTypeBox = graphTypeBox
        graphTypes = ['Bar', 'Pie', 'Line', 'Scatter']
        self.graphTypeBox.insertItems(0, graphTypes)

        self.optionsWindow = GraphOptionsWindow()


    def openGraphOptions(self):
        """
        Opens the graph options dialog
        Connected to Open Graph Settings button in fs3Run.py
        """
        self.optionsWindow.exec_()

    def setData(self, fields, attributes, uniqueness):
        """
        Sets self variables
        xValues defaults to 1 through n if no default is selected
        Checks if the data should be sorted or transformed
        Does sort or transform
        """
        self.fields = fields
        self.attributes = attributes
        self.uniqueness = uniqueness

        self.xValues = [i for i in range(len(self.attributes[0]))]
        self.yValues = attributes[0]

        if self.optionsWindow.dataSortingBox.currentText() == 'Acending':
            self.yValues = sorted(self.yValues)

        if self.optionsWindow.dataSortingBox.currentText() == 'Decending':
            self.yValues = sorted(self.yValues, reverse = True)

        if self.optionsWindow.dataTransformBox.currentText() == 'Log':
            try:
                temp = []
                for val in self.yValues:
                    if val <= 0:
                        temp.append(val)
                    else:
                        temp.append(log10(val))
                self.yValues = temp
            except TypeError:
                # TODO Error message
                pass


    def makeGraph(self):
        """
        Creates the currently selected graph type
        returns the path of the created graph
        """

        # refesh data to include any options from the options window
        self.setData(self.fields, self.attributes, self.uniqueness)

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
        allNull = True
        for value in self.yValues:
            if value != NULL:
                allNull = False
                break
        if allNull:
            return

        trace = go.Bar(
            x = self.xValues,
            y = self.yValues,
            name='{} x {}'.format('self.fields[0]', 'self.fields[1]')
        )

        data = [trace]
        layout = go.Layout(
            barmode = 'group'
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

        allNull = True
        for attribute in self.attributes:
            for value in attribute:
                if value != NULL:
                    allNull = False
                    break
        if allNull:
            return

        if len(self.attributes) is 1:
            self.attributes.append([i for i in range(len(self.attributes[0]))])

            trace = go.Scatter(
                x = self.attributes[1],
                y = self.attributes[0],
                name='{}'.format(self.fields[0])
            )
        else:
            trace = go.Scatter(
                x = self.attributes[0],
                y = self.attributes[1],
                name='{} x {}'.format(self.fields[0], self.fields[1])
            )

        data = [trace]

        layout = go.Layout(
            barmode = 'group'
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

        allNull = True
        for attribute in self.attributes:
            for value in attribute:
                if value != NULL:
                    allNull = False
                    break
        if allNull:
            return

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
            barmode = 'group'
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

        return js_str
