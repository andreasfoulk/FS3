# -*- coding: utf-8 -*-
"""
Created on Tue May 15 11:12:02 2018

@author: Tanner Lee
"""

import os
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication,QMainWindow
QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)      

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'fs3.ui'))

class FS3MainWindow(QMainWindow, FORM_CLASS):
    def __init__(self, parent=None):
        super(FS3MainWindow,self).__init__(parent)
        self.setupUi(self)
        self.mainWindowSplitter.setStretchFactor(1,10)
        self.counter = 0
        self.setWindowTitle('FS3 -- FieldStats3')    