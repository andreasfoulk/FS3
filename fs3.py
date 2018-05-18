# -*- coding: utf-8 -*-
"""
Created on Tue May 15 11:12:02 2018

@author: Tanner Lee
https://github.com/tleecsm
"""

from PyQt5.QtWidgets import QAction
from PyQt5.QtGui import QIcon
from .fs3Run import FS3MainWindow

class FS3Plugin:
    def __init__(self, iface):
        self.iface = iface
        self.mainWindow = FS3MainWindow()

    #initGui is a required method
    #Used by QGIS to make the icon and the menu items for the plugin    
    def initGui(self):
        self.iconPath = ":/plugins/FS3/icon.png"
        self.icon = QIcon(self.iconPath)
        self.action = QAction(self.icon, 
                              "FS3 -- FieldStats3", 
                              self.iface.mainWindow())
        self.action.setObjectName("FS3 Plugin")
        self.action.setWhatsThis("Configuration for FS3")
        self.action.setStatusTip("This is a tip")
        self.action.triggered.connect(self.run)
        
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu("&FS3 Plugin", self.action)
        
    def unload(self):
        self.iface.removePluginMenu("&FS3 Plugin", self.action)
        self.iface.removeToolBarIcon(self.action)
        
    def run(self):
        print("Running!")
        self.mainWindow.show()