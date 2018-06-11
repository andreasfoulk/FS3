"""

    fs3Unique.py -- Plugin implimentation handling all unique values computation
                 -- For more information see : https://github.com/andreasfoulk/FS3
                 -- These functions are tested with uniqueTests.py

    Copyright (c) 2018 Orden Aitchedji, Mckenna Duzac, Andreas Foulk, Tanner Lee

    This software may be modified and distributed under the terms
    of the MIT license.  See the LICENSE file for details.

"""

from qgis.core import NULL
from .roundFunc import decimalRound
from PyQt5.QtCore import QCoreApplication

class FS3Uniqueness(object):
    """
    FS3Uniqueness
    """

    def __init__(self):
        """ Variable definitions """
        self.uniqueValues = 0
        self.uniqueNumOccur = 0
        self.uniquePercent = 0
        self.totalValues = 0
        self.statName = [QCoreApplication.translate("FS3Uniqueness", "Value"),
                         QCoreApplication.translate("FS3Uniqueness", "Occurrences"),
                         QCoreApplication.translate("FS3Uniqueness", "Percentage (%)")]
        self.statCount = 3
        self.numItems = 0

    def initialize(self, inputArray):
        """
        initialize
        """
        if len(inputArray) > 1:
            inputArray = self.multiListHandler(inputArray)
        else:
            inputArray = inputArray[0]

        self.numItems = len(inputArray)
        self.uniqueValues = uniqueValues(inputArray)
        self.uniqueNumOccur = uniqueNumberOccurances(self.uniqueValues, inputArray)
        self.uniquePercent = uniquePercent(self.uniqueNumOccur, self.numItems)
        self.totalValues = len(self.uniqueValues)

    def multiListHandler(self, inputArray):
        """
        multiListHandler
        Handles the instance where inputArray has more than one list
        """
        returnArray = []
        for j in range(len(inputArray[0])):
            returnArray.append('[')
            for i in range(len(inputArray)):
                returnArray[j] += str(inputArray[i][j]) + '] , ['
            returnArray[j] = returnArray[j][:-4]
        return returnArray

    def roundUniqueness(self, precision):
        tempArray = []
        for percent in self.uniquePercent:
            tempArray.append(decimalRound(percent, precision))
        self.uniquePercent = tempArray



def uniqueValues(inputArray):
    """
    uniqueValues
    return all instances of unique values
    """
    valueList = []
    for value in inputArray:
        if value not in valueList:
            if value == NULL and QCoreApplication.translate("FS3Uniqueness", "NULL (Empty)") not in valueList:
                valueList.append(QCoreApplication.translate("FS3Uniqueness", "NULL (Empty)"))
            elif value == NULL and QCoreApplication.translate("FS3Uniqueness", "NULL (Empty)") in valueList:
                continue
            else:
                valueList.append(value)
    return valueList

def uniqueNumberOccurances(inputArray, originalArray):
    """
    uniqueNumberOccurances
    returns total occurences of each unique values
    """
    valueList = []
    for value in inputArray:
        if value == QCoreApplication.translate("FS3Uniqueness", "NULL (Empty)"):
            valueList.append(originalArray.count(None))
        else:
            valueList.append(originalArray.count(value))
    return valueList

def uniquePercent(inputArray, numItems):
    """
    uniquePercent
    returns a percentage of occurences for the unique values
    """
    valueList = []
    for value in inputArray:
        valueList.append((value/numItems)*100)
    return valueList
