# -*- coding: utf-8 -*-
"""
Created on Fri May 18 14:26:25 2018

@author: Tanner Lee
https://github.com/tleecsm
"""

import statistics
import numpy
from .roundFunc import decimalRound
from qgis.core import NULL

# pylint: disable=too-few-public-methods
class FS3NumericalStatistics(object):
    """
    FS3NumericStatistics
    Class that contains all of the statistics calculated for numeric fields
    Contains an initialize function to run all calculations
    Overloads print function for debugging purposes
    """

    def __init__(self):
        """ Variable definitions """
        self.itemCount = 0
        self.maxValue = 0
        self.minValue = 0
        self.meanValue = 0
        self.medianValue = 0
        self.sumValue = 0
        self.stdDevValue = 0
        self.coeffVarValue = 0
        self.statCount = 8
        self.statName = ""

    def initialize(self, inputArray, percentileArray):
        """
        initialize
        Runs all numerical analysis
        Stores the output in class self.variables
        """
        # Check to ensure we are not passing an empty list
        if len(inputArray) < 1:
            return
        self.itemCount = itemCount(inputArray)
        self.maxValue = maxValue(inputArray)
        self.minValue = minValue(inputArray)
        self.meanValue = meanValue(inputArray)
        self.medianValue = medianValue(inputArray)
        self.sumValue = sumValue(inputArray)
        self.stdDevValue = stdDevValue(inputArray)
        self.coeffVarValue = coeffVarValue(inputArray)
        self.percentiles = percentileValues(inputArray, percentileArray)
        self.statCount = 8 + len(self.percentiles)

        self.statName = ["Item Count",
                         "Max Value",
                         "Min Value",
                         "Mean Value",
                         "Median Value",
                         "Sum Value",
                         "Standard Deviation",
                         "Coefficient of Variation"]
        for percentileNumber in percentileArray:
            self.statName.append('Percentile: ' + str(percentileNumber) + '%')

    def roundNumericStatistics(self, precision):
        self.itemCount = decimalRound(self.itemCount, precision)
        self.maxValue = decimalRound(self.maxValue, precision)
        self.minValue = decimalRound(self.minValue, precision)
        self.meanValue = decimalRound(self.meanValue, precision)
        self.medianValue = decimalRound(self.medianValue, precision)
        self.sumValue = decimalRound(self.sumValue, precision)
        self.stdDevValue = decimalRound(self.stdDevValue, precision)
        self.coeffVarValue = decimalRound(self.coeffVarValue, precision)
        tempPercentiles = []
        for percentile in self.percentiles:
            tempPercentiles.append(decimalRound(percentile, precision))
        self.percentiles = tempPercentiles

    def __repr__(self):
        printString = 'Item Count :: ' + str(self.itemCount)
        printString += '\nMax Value :: ' + str(self.maxValue)
        printString += '\nMin Value :: ' + str(self.minValue)
        printString += '\nMean Value :: ' + str(self.meanValue)
        printString += '\nMedian Value :: ' + str(self.medianValue)
        printString += '\nSum Value :: ' + str(self.sumValue)
        printString += '\nStandard Deviation :: ' + str(self.stdDevValue)
        printString += '\nCoefficient of Variation :: '
        printString += str(self.coeffVarValue)
        return printString

class FS3CharacterStatistics(object):
    """
    FS3CharacterStatistics
    Class that contains all of the statistics calculated for numeric fields
    Contains an initialize function to run all calculations
    Overloads print function for debugging purposes
    """

    def __init__(self):
        """ Variable definitions """
        self.itemCount = 0
        self.maxLength = 0
        self.minLength = 0
        self.meanLength = 0
        self.medianLength = 0
        self.sumLength = 0
        self.stdDevLength = 0
        self.coeffVarLength = 0
        self.statCount = 8
        self.statName = ""

    def initialize(self, inputArray, percentileArray):
        """
        initialize
        Runs all numerical analysis
        Stores the output in class self.variables
        """
        # Check to ensure we are not passing an empty list
        if len(inputArray) < 1:
            return
        # Start by converting the inputArray to a length array of the strings
        tempArray = []
        for string in inputArray:
            tempArray.append(len(string))
        inputArray = tempArray
        self.itemCount = itemCount(inputArray)
        self.maxLength = maxValue(inputArray)
        self.minLength = minValue(inputArray)
        self.meanLength = meanValue(inputArray)
        self.medianLength = medianValue(inputArray)
        self.sumLength = sumValue(inputArray)
        self.stdDevLength = stdDevValue(inputArray)
        self.coeffVarLength = coeffVarValue(inputArray)
        self.percentiles = percentileValues(inputArray, percentileArray)
        self.statCount = 8 + len(self.percentiles)

        self.statName = ["Item Count",
                         "Max Length",
                         "Min Length",
                         "Mean Length",
                         "Median Length",
                         "Sum Length",
                         "Standard Deviation (Length)",
                         "Coefficient of Variation (Length)"]
        for percentileNumber in percentileArray:
            self.statName.append('Percentile: ' + str(percentileNumber) +
                                 '% (Length)')

    def roundCharacterStatistics(self, precision):
        self.itemCount = decimalRound(self.itemCount, precision)
        self.maxLength = decimalRound(self.maxLength, precision)
        self.minLength = decimalRound(self.minLength, precision)
        self.meanLength = decimalRound(self.meanLength, precision)
        self.medianLength = decimalRound(self.medianLength, precision)
        self.sumLength = decimalRound(self.sumLength, precision)
        self.stdDevLength = decimalRound(self.stdDevLength, precision)
        self.coeffVarLength = decimalRound(self.coeffVarLength, precision)
        tempPercentiles = []
        for percentile in self.percentiles:
            tempPercentiles.append(decimalRound(percentile, precision))
        self.percentiles = tempPercentiles

    def __repr__(self):
        printString = 'Item Count :: ' + str(self.itemCount)
        printString += '\nMax Length :: ' + str(self.maxLength)
        printString += '\nMin Length :: ' + str(self.minLength)
        printString += '\nMean Length :: ' + str(self.meanLength)
        printString += '\nMedian Length :: ' + str(self.medianLength)
        printString += '\nSum Length :: ' + str(self.sumLength)
        printString += '\nStandard Deviation (Length) :: '
        printString += str(self.stdDevLength)
        printString += '\nCoefficient of Variation (Length) :: '
        printString += str(self.coeffVarLength)
        return printString

def removeEmptyCells(inputArray):
    """
    removeEmptyCells
    Function used to remove empty cells from a list
    This allows our calculations to remain accurate with incomplete data
    @param inputArray Array passed for calculation
    @return outputArray Array with the empty cells removed
    """
    outputArray = []
    for string in inputArray:
        if not string == NULL:
            outputArray.append(string)
    return outputArray

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
    # Standard Deviation Requires a size of 2+
    if len(inputArray) < 2:
        return 0
    stdDevValueReturn = statistics.stdev(inputArray)
    return stdDevValueReturn

def coeffVarValue(inputArray):
    """
    coeffVarValue
    Function used to calculate the coefficient of variation of an array
    @param inputArray Array passed for calculation
    @return coeffVarReturn The integer value returned by the calculation
    """
    # Variance Requires a size of 2+
    if len(inputArray) < 2:
        return 0
    coeffVarReturn = statistics.variance(inputArray)
    return coeffVarReturn

def percentileValues(inputArray, percentileArray):
    """
    percentileValues
    Function used to calculate the percentiles of a given array
    @param inputArray Array passed for calculation
    @param percentileArray Array containing user selected percentiles
    @return percDict Dictionary of percentiles to values
    """
    percentiles = []
    for p in percentileArray:
        val = numpy.percentile(inputArray, p)
        percentiles.append(val)
    return percentiles
