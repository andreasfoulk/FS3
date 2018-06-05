# -*- coding: utf-8 -*-
"""

@author: Orden Aitchedji, Mckenna Duzac, Andreas Foulk, Tanner Lee
@Repository: https://github.com/andreasfoulk/FS3

"""

#classFactory is a required function for QGIS Plugins
#Function is called when the plugin gets loaded
#Used to return QGIS an instance of your plugin

def classFactory(iface):
    from .fs3 import FS3Plugin
    return FS3Plugin(iface)
