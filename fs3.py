# -*- coding: utf-8 -*-
# pylint: disable=wildcard-import, method-hidden
"""

	QGIS plugin - Provides basic statistics for numeric and test fields.
				- Includes various tools for optimizing statistical search.
				- For more information see : https://github.com/andreasfoulk/FS3

	Copyright (c) 2018 Orden Aitchedji, Mckenna Duzac, Andreas Foulk, Tanner Lee

	Permission is hereby granted, free of charge, to any person obtaining a copy
	of this software and associated documentation files (the "Software"), to deal
	in the Software without restriction, including without limitation the rights
	to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
	copies of the Software, and to permit persons to whom the Software is
	furnished to do so, subject to the following conditions:

	The above copyright notice and this permission notice shall be included in
	all copies or substantial portions of the Software.

	THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
	IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
	FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
	AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
	LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
	OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
	THE SOFTWARE.

"""

from PyQt5.QtCore import QTranslator, QSettings, QCoreApplication, qVersion
from PyQt5.QtWidgets import QAction
from PyQt5.QtGui import QIcon
from .fs3Run import FS3MainWindow

from .resources import QtCore
from .layerFieldGetter import LayerFieldGetter
import os.path
#os.system("python resources.py")
class FS3Plugin(object):
    """
    FS3Plugin handles the linking to QGIS.
    - The icon is declared here
    - The plugin is loaded to the toolbar here
    - The main interface is called here
    """
    def __init__(self, iface):
        self.iface = iface

        self.pluginDir = os.path.dirname(__file__)
        locale = QSettings().value('locale/userLocale')[0:2]
        localePath = os.path.join(self.pluginDir, 'i18n', 'fs3_{}.qm'.format(locale))

        if os.path.exists(localePath):
            self.translator = QTranslator()
            self.translator.load(localePath)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the Main plugin window after translations
        self.mainWindow = FS3MainWindow()
        self.iconPath = ":/plugins/FS3/FS3Icon.png"
        self.icon = QIcon(self.iconPath)
        self.action = QAction(self.icon,
                              "FS3 -- FieldStats3",
                              self.iface.mainWindow())


    def translation(self, stringToTranslate):
        """
        Gets the Strings to translate using the Qt translation API
        """
        return QCoreApplication.translate('FS3Plugin', stringToTranslate)


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

        #self.iface.removePluginMenu("&FS3 Plugin", self.action)

        self.iface.removePluginMenu(self.translation(u'&FS3 Plugin'), self.action)
        self.iface.removeToolBarIcon(self.action)

    def run(self):
        """
        Acts as the entry point to the main program
        Runs when a window is opened
        Creates and runs an instance of the window
        """
        layersCount = len(LayerFieldGetter.getVectorLayers())
        if layersCount == 0:
            self.iface.messageBar().pushMessage(self.translation("Project has NO vector layer loaded"))
            return
        self.mainWindow.show()
