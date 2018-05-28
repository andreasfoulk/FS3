# -*- coding: utf-8 -*-
"""
Created on Fri May 18 14:26:25 2018

@author: Tanner Lee
https://github.com/tleecsm
"""

import statistics

class FS3NumericalStatistics(object):
    """
    FS3NumericStatistics
    Class that contains all of the statistics calculated for numeric fields
    Contains an initialize function to run all calculations
    Overloads print function for debugging purposes
    """

    def __init__(self):
        """ Variable definitions """
        self.itemCount = None
        self.maxValue = None
        self.minValue = None
        self.meanValue = None
        self.medianValue = None
        self.sumValue = None
        self.stdDevValue = None
        self.coeffVarValue = None
        self.statCount = 0
        self.statName = ""

    def initialize(self, inputArray):
        """
        initialize
        Runs all numerical analysis
        Stores the output in class self.variables
        """
        self.itemCount = itemCount(inputArray)
        self.maxValue = maxValue(inputArray)
        self.minValue = minValue(inputArray)
        self.meanValue = meanValue(inputArray)
        self.medianValue = medianValue(inputArray)
        self.sumValue = sumValue(inputArray)
        self.stdDevValue = stdDevValue(inputArray)
        self.coeffVarValue = coeffVarValue(inputArray)
        self.statCount = 8
        self.statName = ["Item Count", "Max Value", "Min Value", "Mean Value", "Median Value", "Sum Value", "Standard Deviation", "Coefficient of Variation"]
        
def itemCount(inputArray):
    """
    itemCount
    Function used to calculate the number of items in an array
    @param inputArray Array passed for calculation
    @return itemCountReturn The integer value returned by the calculation
    """

    itemCountReturn = len(inputArray)
    return itemCountReturn

def maxValue(inputArray):
    """
    maxValue
    Function used to calculate the maximum value of an array
    @param inputArray Array passed for calculation
    @return maxValueReturn The integer value returned by the calculation
    """
    maxValueReturn = max(inputArray)
    return maxValueReturn

def minValue(inputArray):
    """
    minValue
    Function used to calculate the minimum value of an array
    @param inputArray Array passed for calculation
    @return minValueReturn The integer value returned by the calculation
    """
    minValueReturn = min(inputArray)
    return minValueReturn

def meanValue(inputArray):
    """
    meanValue
    Function used to calculate the mean value of an array
    @param inputArray Array passed for calculation
    @return meanValueReturn The integer value returned by the calculation
    """
    meanValueReturn = sum(inputArray)/float(len(inputArray))
    return meanValueReturn

def medianValue(inputArray):
    """
    medianValue
    Function used to calculate the median value of an array
    @param inputArray Array passed for calculation
    @return medianValueReturn The integer value returned by the calculation
    """
    medianValueReturn = statistics.median(inputArray)
    return medianValueReturn

def sumValue(inputArray):
    """
    sumValue
    Function used to calculate the sum value of an array
    @param inputArray Array passed for calculation
    @return sumValueReturn The integer value returned by the calculation
    """
    sumValueReturn = sum(inputArray)
    return sumValueReturn

def stdDevValue(inputArray):
    """
    stdDevValue
    Function used to calculate the Standard Deviation of an array
    @param inputArray Array passed for calculation
    @return stdDevValueReturn The integer value returned by the calculation
    """
    stdDevValueReturn = statistics.stdev(inputArray)
    return stdDevValueReturn

def coeffVarValue(inputArray):
    """
    coeffVarValue
    Function used to calculate the coefficient of variation of an array
    @param inputArray Array passed for calculation
    @return coeffVarReturn The integer value returned by the calculation
    """
    coeffVarReturn = statistics.variance(inputArray)
    return coeffVarReturn

def maxLength(inputArray):
    """
    maxLength
    Function used to calculate the maximum element length in an array
    @param inputArray Array passed for calculation
    @return maxLengthReturn The integer value returned by the calculation
    """
    maxLengthReturn = 0
    for i in inputArray:
        if len(i) > maxLengthReturn:
            maxLengthReturn = len(i)
    return maxLengthReturn
