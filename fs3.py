# -*- coding: utf-8 -*-
# pylint: disable=wildcard-import, method-hidden
"""

@author: Orden Aitchedji, Mckenna Duzac, Andreas Foulk, Tanner Lee
@Repository: https://github.com/andreasfoulk/FS3

"""

from PyQt5.QtWidgets import QAction
from PyQt5.QtGui import QIcon
from .fs3Run import FS3MainWindow

from .resources import * # pylint: disable=unused-import

class FS3Plugin(object):
    """
    FS3Plugin handles the linking to QGIS.
    The icon is declared here
    The plugin is loaded to the toolbar here
    And the main interface is called here
    """
    def __init__(self, iface):
        self.iface = iface
        self.mainWindow = FS3MainWindow()
        self.iconPath = ":/plugins/FS3/FS3Icon.png"
        self.icon = QIcon(self.iconPath)
        self.action = QAction(self.icon,
                              "FS3 -- FieldStats3",
                              self.iface.mainWindow())


    def initGui(self):
        """
        initGui is a required method
        Used by QGIS to make the icon and the menu items for the plugin
        """
        self.action.setObjectName("FS3 Plugin")
        self.action.setWhatsThis("Configuration for FS3")
        self.action.setStatusTip("This is a tip")
        self.action.triggered.connect(self.run)
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu("&FS3 Plugin", self.action)


    def unload(self):
        """
        unload is a required method
        Used by QGIS to remove the plugin from the menu and toolbar
        """
        self.iface.removePluginMenu("&FS3 Plugin", self.action)
        self.iface.removeToolBarIcon(self.action)

    def run(self):
        """
        Acts as the entry point to the main program
        Runs when a window is opened
        Creates and runs an instance of the window
        """
        self.mainWindow.show()
