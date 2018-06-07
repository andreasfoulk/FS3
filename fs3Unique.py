"""

@author: Orden Aitchedji, Mckenna Duzac, Andreas Foulk, Tanner Lee
@Repository: https://github.com/andreasfoulk/FS3

These functions are tested with uniqueTests.py

"""

from qgis.core import NULL
from .roundFunc import decimalRound

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
        self.statName = ['Value',
                         'Occurrences',
                         'Percentage (%)']
        self.statCount = 3

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
    valueList = []
    for x in inputArray:
        if x not in valueList:
            if x == NULL and 'NULL (Empty)' not in valueList:
                valueList.append('NULL (Empty)')
            elif x == NULL and 'NULL (Empty)' in valueList:
                continue
            else:
                valueList.append(x)
    return valueList

def uniqueNumberOccurances(inputArray, originalArray):
    valueList = []
    for x in inputArray:
        if x == 'NULL (Empty)':
            valueList.append(originalArray.count(None))
        else:
            valueList.append(originalArray.count(x))
    return valueList

def uniquePercent(inputArray, numItems):
    valueList = []
    for x in inputArray:
        valueList.append((x/numItems)*100)
    return valueList
