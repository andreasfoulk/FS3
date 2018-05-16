# -*- coding: utf-8 -*-
"""
Created on Tue May 15 11:12:02 2018

@author: Tanner Lee
"""

import sys
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.uic import loadUi

class SimpleCounter(QDialog):
    """ Our test class to ensure proper Qt functionality """
    def __init__(self):
        super(SimpleCounter, self).__init__()
        loadUi('test_ui.ui', self)
        self.counter = 0
        self.setWindowTitle('Counter Interface')
        self.pushButton.clicked.connect(self.increaseCounter)
        self.dial.setWrapping(False)
        self.dial.setNotchesVisible(True)
        self.dial.valueChanged.connect(self.increaseCounterDial)

    #pyqtSlot decorate declares the following pythod method into a QT slot
    #Allows a C++ signature to be provided
    #Slightly reduces memory used and is slightly faster
    @pyqtSlot()
    def increaseCounter(self):
        """ Is this a docstring? """
        self.counter += 1
        self.lcdNumber.display(self.counter)

    @pyqtSlot()
    def increaseCounterDial(self):
        """ Yes this a docstring, method does the thing it is named for... """
        self.counter = self.dial.value()
        self.lcdNumber.display(self.counter)

app = QApplication(sys.argv)
widget = SimpleCounter()
widget.show()
sys.exit(app.exec_())
