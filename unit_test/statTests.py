"""
Created by: McKenna Duzac
Last Edited: 23 May 2018

All of these tests written with the following assumptions:
    -functions take in a list of values
    -using standard deviation, not population stdev
        -just statistics.pstdev vs statistics.stdev

The following functions need to be created for NumericStats:

TODO:
    import stat files
    Fringe cases not currently checked
    Improper input cases not currently checked
    Most of the CharcterStats functions currently unknown
"""

#These imports are required for unit tests
import unittest

from fs3Stats import FS3CharacterStatistics, FS3NumericalStatistics

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


class CharacterStatTests(unittest.TestCase):
    """
    CharacterStatTests
    Contains several test cases for our statistics calculations
    """

    @classmethod
    def setUpClass(self):
        self.goodValues = FS3CharacterStatistics()
        self.goodValues.initialize(['a', 'cat', 'went', 'home', 'yesterday'], [25, 50, 75])

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


def main():
    unittest.main()

if __name__ == '__main__':
    main()
