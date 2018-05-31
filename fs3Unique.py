"""
Created by: McKenna Duzac
Last Edited: 31 May 2018

These functions are tested with uniqueTests.py

"""

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
                         'Occurances',
                         'Percentage']
        self.statCount = 3

    def initialize(self, inputArray):
        """
        initialize
        """
        self.numItems = len(inputArray)
        self.uniqueValues = uniqueValues(inputArray)
        self.uniqueNumOccur = uniqueNumberOccurances(self.uniqueValues, inputArray)
        self.uniquePercent = uniquePercent(self.uniqueNumOccur, self.numItems)
        self.totalValues = len(self.uniqueValues)


def uniqueValues(inputArray):
    valueList = []
    for x in inputArray:
        if x not in valueList:
            if x is None and '[Empty]' not in valueList:
                valueList.append('[Empty]')
            elif x is None and '[Empty]' in valueList:
                continue
            else:
                valueList.append(x)
    return valueList

def uniqueNumberOccurances(inputArray, originalArray):
    valueList = []
    for x in inputArray:
        if x == '[Empty]':
            valueList.append(originalArray.count(None))
        else:
            valueList.append(originalArray.count(x))
    return valueList

def uniquePercent(inputArray, numItems):
    valueList = []
    for x in inputArray:
        valueList.append((x/numItems)*100)
    return valueList
