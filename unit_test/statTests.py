"""

    statTests.py -- Handles testing for prpper case by case rounding.
                 -- Functions take in a list of values
                 -- Uses a sample standard deviation
                 -- For more information see : https://github.com/andreasfoulk/FS3
    
    Copyright (c) 2018 Orden Aitchedji, Mckenna Duzac, Andreas Foulk, Tanner Lee

    This software may be modified and distributed under the terms
    of the MIT license.  See the LICENSE file for details.
    

TODO:
    import stat files
    Fringe cases not currently checked
    Improper input cases not currently checked
    Most of the CharcterStats functions currently unknown

"""

#These imports are required for unit tests
import unittest

from fs3Stats import FS3CharacterStatistics, FS3NumericalStatistics
from fs3Stats import removeEmptyCells

class NumericStatTests(unittest.TestCase):
    """
    NumericStatTests
    Contains several test cases for our statistics calculations
    """

    @classmethod
    def setUpClass(self):
        #A simple set of data with no empties
        self.goodValues = FS3NumericalStatistics()
        self.goodValues.initialize([1, 4, 8, 3, 6], [25, 50, 75])

        #A set of data with empties (None)
        inputArray = [9, 20, 36, None, 4, None, 18, 12]
        newArray = removeEmptyCells(inputArray)
        self.emptyValues = FS3NumericalStatistics()
        self.emptyValues.initialize(newArray, [10, 20, 30, 40, 50, 60, 70, 80, 90])

        #A set of varied data (negatives, large numbers, zero)
        self.variedValues = FS3NumericalStatistics()
        self.variedValues.initialize([0, -25, 1000, 76, 93, 12, -416], [18, 42, 66, 73])

    #--------------------------------------Good Value Tests--------------------------------------
    def testCountGoodValues(self):
        """
        testCountFunction
        Used to test item count functionality
        """
        expected = 5
        actual = self.goodValues.itemCount
        self.assertEqual(actual, expected)

    def testMaxGoodValues(self):
        """
        testMaxFunction
        Used to test max value functionality
        """
        expected = 8
        actual = self.goodValues.maxValue
        self.assertEqual(actual, expected)

    def testMinGoodValues(self):
        """
        testCountFunction
        Used to test min value functionality
        """
        expected = 1
        actual = self.goodValues.minValue
        self.assertEqual(actual, expected)

    def testMeanGoodValues(self):
        """
        testCountFunction
        Used to test mean value functionality
        """
        expected = 4.4
        actual = self.goodValues.meanValue
        self.assertEqual(actual, expected)

    def testMedianGoodValues(self):
        """
        testCountFunction
        Used to test median value functionality
        """
        expected = 4
        actual = self.goodValues.medianValue
        self.assertEqual(actual, expected)

    def testSumGoodValues(self):
        """
        testCountFunction
        Used to test sum value functionality
        """
        expected = 22
        actual = self.goodValues.sumValue
        self.assertEqual(actual, expected)

    def testStandardDeviationGoodValues(self):
        """
        testCountFunction
        Used to test standard deviation value
        """
        expected = 2.701851217221259
        actual = self.goodValues.stdDevValue
        self.assertEqual(actual, expected)

    def testCoefficientOfVariationGoodValues(self):
        """
        testCountFunction
        Used to test coefficient of variation value
        """
        expected = 7.3
        actual = self.goodValues.coeffVarValue
        self.assertEqual(actual, expected)

    def testPercentilesGoodValues(self):
        """
        testCountFunction
        Used to test coefficient of variation value
        """
        expected = [3.0, 4.0, 6.0]
        actual = self.goodValues.percentiles
        self.assertEqual(actual, expected)

    #--------------------------------------Empty Value Tests--------------------------------------
    def testCountEmptyValues(self):
        """
        testCountFunction
        Used to test item count functionality
        """
        expected = 6
        actual = self.emptyValues.itemCount
        self.assertEqual(actual, expected)

    def testMaxEmptyValues(self):
        """
        testMaxFunction
        Used to test max value functionality
        """
        expected = 36
        actual = self.emptyValues.maxValue
        self.assertEqual(actual, expected)

    def testMinEmptyValues(self):
        """
        testCountFunction
        Used to test min value functionality
        """
        expected = 4
        actual = self.emptyValues.minValue
        self.assertEqual(actual, expected)

    def testMeanEmptyValues(self):
        """
        testCountFunction
        Used to test mean value functionality
        """
        expected = 16.5
        actual = self.emptyValues.meanValue
        self.assertEqual(actual, expected)

    def testMedianEmptyValues(self):
        """
        testCountFunction
        Used to test median value functionality
        """
        expected = 15
        actual = self.emptyValues.medianValue
        self.assertEqual(actual, expected)

    def testSumEmptyValues(self):
        """
        testCountFunction
        Used to test sum value functionality
        """
        expected = 99
        actual = self.emptyValues.sumValue
        self.assertEqual(actual, expected)

    def testStandardDeviationEmptyValues(self):
        """
        testCountFunction
        Used to test standard deviation value
        """
        expected = 11.20267825120404
        actual = self.emptyValues.stdDevValue
        self.assertEqual(actual, expected)

    def testCoefficientOfVariationEmptyValues(self):
        """
        testCountFunction
        Used to test coefficient of variation value
        """
        expected = 125.5
        actual = self.emptyValues.coeffVarValue
        self.assertEqual(actual, expected)

    def testPercentilesEmptyValues(self):
        """
        testCountFunction
        Used to test coefficient of variation value
        """
        expected = [6.5, 9.0, 10.5, 12.0, 15.0, 18.0, 19.0, 20.0, 28.0]
        actual = self.emptyValues.percentiles
        self.assertEqual(actual, expected)

    #--------------------------------------Varied Value Tests--------------------------------------
    def testCountVariedValues(self):
        """
        testCountFunction
        Used to test item count functionality
        """
        expected = 7
        actual = self.variedValues.itemCount
        self.assertEqual(actual, expected)

    def testMaxVariedValues(self):
        """
        testMaxFunction
        Used to test max value functionality
        """
        expected = 1000
        actual = self.variedValues.maxValue
        self.assertEqual(actual, expected)

    def testMinVariedValues(self):
        """
        testCountFunction
        Used to test min value functionality
        """
        expected = -416
        actual = self.variedValues.minValue
        self.assertEqual(actual, expected)

    def testMeanVariedValues(self):
        """
        testCountFunction
        Used to test mean value functionality
        """
        expected = 105.71428571428571
        actual = self.variedValues.meanValue
        self.assertEqual(actual, expected)

    def testMedianVariedValues(self):
        """
        testCountFunction
        Used to test median value functionality
        """
        expected = 12
        actual = self.variedValues.medianValue
        self.assertEqual(actual, expected)

    def testSumVariedValues(self):
        """
        testCountFunction
        Used to test sum value functionality
        """
        expected = 740
        actual = self.variedValues.sumValue
        self.assertEqual(actual, expected)

    def testStandardDeviationVariedValues(self):
        """
        testCountFunction
        Used to test standard deviation value
        """
        expected = 430.1204150334781
        actual = self.variedValues.stdDevValue
        self.assertEqual(actual, expected)

    def testCoefficientOfVariationVariedValues(self):
        """
        testCountFunction
        Used to test coefficient of variation value
        """
        expected = 185003.57142857142
        actual = self.variedValues.coeffVarValue
        self.assertEqual(actual, expected)

    def testPercentilesVariedValues(self):
        """
        testCountFunction
        Used to test coefficient of variation value
        """
        expected = [-23.0, 6.24, 73.44, 82.46]
        actual = self.variedValues.percentiles
        self.assertEqual(actual, expected)


class CharacterStatTests(unittest.TestCase):
    """
    CharacterStatTests
    Contains several test cases for our statistics calculations
    """

    @classmethod
    def setUpClass(self):
        #A simple set of data with no empties
        self.goodValues = FS3CharacterStatistics()
        self.goodValues.initialize(['a', 'cat', 'went', 'home', 'yesterday'], [25, 50, 75])

        #A set of data with empties (None)
        inputArray = ['cat', 'dog', 'apple', None, 'banana', None, 'fruit', 'animals', None]
        newArray = removeEmptyCells(inputArray)
        self.emptyValues = FS3CharacterStatistics()
        self.emptyValues.initialize(newArray, [10, 40, 50, 60, 90])

#--------------------------------------Good Value Tests--------------------------------------
    def testCountGoodValues(self):
        """
        testCountFunction
        Used to test item count functionality
        """
        expected = 5
        actual = self.goodValues.itemCount
        self.assertEqual(actual, expected)

    def testMaxGoodValues(self):
        """
        testMaxFunction
        Used to test max value functionality
        """
        expected = 9
        actual = self.goodValues.maxLength
        self.assertEqual(actual, expected)

    def testMinGoodValues(self):
        """
        testCountFunction
        Used to test min value functionality
        """
        expected = 1
        actual = self.goodValues.minLength
        self.assertEqual(actual, expected)

    def testMeanGoodValues(self):
        """
        testCountFunction
        Used to test mean value functionality
        """
        expected = 4.2
        actual = self.goodValues.meanLength
        self.assertEqual(actual, expected)

    def testMedianGoodValues(self):
        """
        testCountFunction
        Used to test median value functionality
        """
        expected = 4
        actual = self.goodValues.medianLength
        self.assertEqual(actual, expected)

    def testSumGoodValues(self):
        """
        testCountFunction
        Used to test sum value functionality
        """
        expected = 21
        actual = self.goodValues.sumLength
        self.assertEqual(actual, expected)

    def testStandardDeviationGoodValues(self):
        """
        testCountFunction
        Used to test standard deviation value
        """
        expected = 2.9495762407505253
        actual = self.goodValues.stdDevLength
        self.assertEqual(actual, expected)

    def testCoefficientOfVariationGoodValues(self):
        """
        testCountFunction
        Used to test coefficient of variation value
        """
        expected = 8.700000000000001
        actual = self.goodValues.coeffVarLength
        self.assertEqual(actual, expected)

    def testPercentilesGoodValues(self):
        """
        testCountFunction
        Used to test coefficient of variation value
        """
        expected = [3.0, 4.0, 4.0]
        actual = self.goodValues.percentiles
        self.assertEqual(actual, expected)

    #--------------------------------------Empty Value Tests--------------------------------------
    def testCountEmptyValues(self):
        """
        testCountFunction
        Used to test item count functionality
        """
        expected = 6
        actual = self.emptyValues.itemCount
        self.assertEqual(actual, expected)

    def testMaxEmptyValues(self):
        """
        testMaxFunction
        Used to test max value functionality
        """
        expected = 7
        actual = self.emptyValues.maxLength
        self.assertEqual(actual, expected)

    def testMinEmptyValues(self):
        """
        testCountFunction
        Used to test min value functionality
        """
        expected = 3
        actual = self.emptyValues.minLength
        self.assertEqual(actual, expected)

    def testMeanEmptyValues(self):
        """
        testCountFunction
        Used to test mean value functionality
        """
        expected = 4.833333333333333
        actual = self.emptyValues.meanLength
        self.assertEqual(actual, expected)

    def testMedianEmptyValues(self):
        """
        testCountFunction
        Used to test median value functionality
        """
        expected = 5
        actual = self.emptyValues.medianLength
        self.assertEqual(actual, expected)

    def testSumEmptyValues(self):
        """
        testCountFunction
        Used to test sum value functionality
        """
        expected = 29
        actual = self.emptyValues.sumLength
        self.assertEqual(actual, expected)

    def testStandardDeviationEmptyValues(self):
        """
        testCountFunction
        Used to test standard deviation value
        """
        expected = 1.602081978759722
        actual = self.emptyValues.stdDevLength
        self.assertEqual(actual, expected)

    def testCoefficientOfVariationEmptyValues(self):
        """
        testCountFunction
        Used to test coefficient of variation value
        """
        expected = 2.5666666666666664
        actual = self.emptyValues.coeffVarLength
        self.assertEqual(actual, expected)

    def testPercentilesEmptyValues(self):
        """
        testCountFunction
        Used to test coefficient of variation value
        """
        expected = [3.0, 5.0, 5.0, 5.0, 6.5]
        actual = self.emptyValues.percentiles
        self.assertEqual(actual, expected)


def sMain():
    unittest.main()

if __name__ == '__main__':
    sMain()
