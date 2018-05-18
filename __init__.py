# -*- coding: utf-8 -*-
"""
Created on Thu May 17 15:54:37 2018

@author: Tanner Lee
https://github.com/tleecsm
"""

#classFactory is a required function for QGIS Plugins
#Function is called when the plugin gets loaded
#Used to return QGIS an instance of your plugin 

def classFactory(iface):
    from .fs3 import FS3Plugin
    return FS3Plugin(iface)