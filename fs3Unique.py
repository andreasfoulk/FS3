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
        self.uniqueValues = None
        self.uniqueNumOccur = None
        self.uniquePercent = None

    def initialize(self, inputArray):
        """
        initialize
        """
        self.numItems = len(inputArray)
        self.uniqueValues = uniqueValues(inputArray)
        self.uniqueNumOccur = uniqueNumberOccurances(self.uniqueValues, inputArray)
        self.uniquePercent = uniquePercent(self.uniqueNumOccur, self.numItems)


def uniqueValues(inputArray):
    valueList = []
    for x in inputArray:
        if x not in valueList:
            valueList.append(x)
    return valueList

def uniqueNumberOccurances(inputArray, originalArray):
    valueList = []
    for x in inputArray:
        valueList.append(originalArray.count(x))
    return valueList

def uniquePercent(inputArray, numItems):
    valueList = []
    for x in inputArray:
        valueList.append((x/numItems)*100)
    return valueList
