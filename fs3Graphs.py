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
        self.hasNull = False

        # When this is something else sorting will need to be done as pairs...
        self.xValues = list(range(len(self.attributes[0])))
        self.yValues = attributes[0]

        # Start by removing the null attributes and their associated fields
        for index in range(0, len(self.yValues)):
            if self.yValues[index] == NULL:
                # Remove this from both lists
                self.hasNull = True
                self.yValues[index] = 'NULL'
        
        if self.optionsWindow.dataSortingBox.currentText() == 'Acending':
            self.yValues = sorted(self.yValues)

        if self.optionsWindow.dataSortingBox.currentText() == 'Decending':
            self.yValues = sorted(self.yValues, reverse = True)

        if self.optionsWindow.dataTransformBox.currentText() == 'Log':
            try:
                self.yValues = [log10(val) if val > 0 else 0 for val in self.yValues]
            except TypeError:
                # TODO Error message?
                pass

            # TODO update axis label to reflect transform?


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
        # insert callback for javascript events
        # raw_plot += js_callback()

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
        # insert callback for javascript events
        # raw_plot += js_callback()

        # use regex to replace the string ReplaceTheDiv with the correct plot id generated by plotly
        match = re.search('Plotly.newPlot\("([^"]+)', raw_plot)
        substr = match.group(1)
        raw_plot = raw_plot.replace('ReplaceTheDiv', substr)

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
        # insert callback for javascript events
        # raw_plot += js_callback()

        # use regex to replace the string ReplaceTheDiv with the correct plot id generated by plotly
        match = re.search('Plotly.newPlot\("([^"]+)', raw_plot)
        substr = match.group(1)
        raw_plot = raw_plot.replace('ReplaceTheDiv', substr)

        plot_path = os.path.join(tempfile.gettempdir(), 'temp_plot_name.html')
        with open(plot_path, "w") as f:
            f.write(raw_plot)

        return plot_path


    def makeScatterGraph(self):

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
        # insert callback for javascript events
        # raw_plot += js_callback()

        # use regex to replace the string ReplaceTheDiv with the correct plot id generated by plotly
        match = re.search('Plotly.newPlot\("([^"]+)', raw_plot)
        substr = match.group(1)
        raw_plot = raw_plot.replace('ReplaceTheDiv', substr)

        plot_path = os.path.join(tempfile.gettempdir(), 'temp_plot_name.html')
        with open(plot_path, "w") as f:
            f.write(raw_plot)

        return plot_path


    def js_callback(self):
        '''
        returns a string that is added to the end of the plot. This string is
        necessary for the interaction between plot and map objects
        WARNING! The string ReplaceTheDiv is a default string that will be
        replaced in a second moment
        '''

        js_str = '''
        <script>
        // additional js function to select and click on the data
        // returns the ids of the selected/clicked feature
        var plotly_div = document.getElementById('ReplaceTheDiv')
        var plotly_data = plotly_div.data
        // selecting function
        plotly_div.on('plotly_selected', function(data){
        var dds = {};
        dds["mode"] = 'selection'
        dds["type"] = data.points[0].data.type
        featureIds = [];
        featureIdsTernary = [];
        data.points.forEach(function(pt){
        featureIds.push(parseInt(pt.id))
        featureIdsTernary.push(parseInt(pt.pointNumber))
        dds["id"] = featureIds
        dds["tid"] = featureIdsTernary
            })
        //console.log(dds)
        window.status = JSON.stringify(dds)
        })
        // clicking function
        plotly_div.on('plotly_click', function(data){
        var featureIds = [];
        var dd = {};
        dd["fidd"] = data.points[0].id
        dd["mode"] = 'clicking'
        // loop and create dictionary depending on plot type
        for(var i=0; i < data.points.length; i++){
        // scatter plot
        if(data.points[i].data.type == 'scatter'){
            dd["uid"] = data.points[i].data.uid
            dd["type"] = data.points[i].data.type
            data.points.forEach(function(pt){
            dd["fid"] = pt.id
            })
        }
        // pie
        else if(data.points[i].data.type == 'pie'){
          dd["type"] = data.points[i].data.type
          dd["label"] = data.points[i].label
          dd["field"] = data.points[i].data.name
          console.log(data.points[i].label)
          console.log(data.points[i])
        }
        // histogram
        else if(data.points[i].data.type == 'histogram'){
            dd["type"] = data.points[i].data.type
            dd["uid"] = data.points[i].data.uid
            dd["field"] = data.points[i].data.name
            // correct axis orientation
            if(data.points[i].data.orientation == 'v'){
                dd["id"] = data.points[i].x
                dd["bin_step"] = data.points[i].data.xbins.size
            }
            else {
                dd["id"] = data.points[i].y
                dd["bin_step"] = data.points[i].data.ybins.size
            }
        }
        // box plot
        else if(data.points[i].data.type == 'box'){
            dd["uid"] = data.points[i].data.uid
            dd["type"] = data.points[i].data.type
            dd["field"] = data.points[i].data.customdata
                // correct axis orientation
                if(data.points[i].data.orientation == 'v'){
                    dd["id"] = data.points[i].x
                }
                else {
                    dd["id"] = data.points[i].y
                }
            }
        // violin plot
        else if(data.points[i].data.type == 'violin'){
            dd["uid"] = data.points[i].data.uid
            dd["type"] = data.points[i].data.type
            dd["field"] = data.points[i].data.customdata
                // correct axis orientation (for violin is viceversa)
                if(data.points[i].data.orientation == 'v'){
                    dd["id"] = data.points[i].x
                }
                else {
                    dd["id"] = data.points[i].y
                }
            }
        // bar plot
        else if(data.points[i].data.type == 'bar'){
            dd["uid"] = data.points[i].data.uid
            dd["type"] = data.points[i].data.type
            dd["field"] = data.points[i].data.customdata
                // correct axis orientation
                if(data.points[i].data.orientation == 'v'){
                    dd["id"] = data.points[i].x
                }
                else {
                    dd["id"] = data.points[i].y
                }
            }
        // ternary
        else if(data.points[i].data.type == 'scatterternary'){
            dd["uid"] = data.points[i].data.uid
            dd["type"] = data.points[i].data.type
            dd["field"] = data.points[i].data.customdata
            dd["fid"] = data.points[i].pointNumber
            }
            }
        window.status = JSON.stringify(dd)
        });
        </script>'''

        return js_str
