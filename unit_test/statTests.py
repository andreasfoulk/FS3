"""
#Created by: McKenna Duzac
#Last Edited: 18 May 2018

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
import statistics
from fs3Stats import itemCount, maxValue, minValue
from fs3Stats import meanValue, medianValue, sumValue
from fs3Stats import stdDevValue, coeffVarValue, maxLength

class NumericStatTests(unittest.TestCase):
    """
    NumericStatTests
    Contains several test cases for our statistics calculations
    """

    def testCountFunction(self):
        """
        testCountFunction
        Used to test item count functionality
        """
        inputArray = ['a', 'b', 'c', 'd']
        expected = 4
        actual = itemCount(inputArray)
        self.assertTrue(expected == actual)

    def testMaxFunction(self):
        """
        testMaxFunction
        Used to test max value functionality
        """
        inputArray = [1, 4, 8, 3, 6]
        expected = 8
        actual = maxValue(inputArray)
        self.assertTrue(expected == actual)

    def testMinFunction(self):
        """
        testCountFunction
        Used to test min value functionality
        """
        inputArray = [1, 4, 8, 3, 6]
        expected = 1
        actual = minValue(inputArray)
        self.assertTrue(expected == actual)

    def testMeanFunction(self):
        """
        testCountFunction
        Used to test mean value functionality
        """
        inputArray = [1, 4, 8, 3, 6]
        expected = 4.4
        actual = meanValue(inputArray)
        self.assertTrue(expected == actual)

    def testMedianFunction(self):
        """
        testCountFunction
        Used to test median value functionality
        """
        inputArray = [1, 4, 8, 3, 6]
        expected = 4
        actual = medianValue(inputArray)
        self.assertTrue(expected == actual)

    def testSumFunction(self):
        """
        testCountFunction
        Used to test sum value functionality
        """
        inputArray = [1, 4, 8, 3, 6]
        expected = 22
        actual = sumValue(inputArray)
        self.assertTrue(expected == actual)

    def testStandardDeviation(self):
        """
        testCountFunction
        Used to test standard deviation value
        """
        inputArray = [1, 4, 8, 3, 6]
        expected = 2.701851217221259
        actual = stdDevValue(inputArray)
        self.assertTrue(expected == actual)

    def testCoefficientOfVariation(self):
        """
        testCountFunction
        Used to test coefficient of variation value
        """
        inputArray = [1, 4, 8, 3, 6]
        expected = 7.3
        actual = coeffVarValue(inputArray)
        self.assertTrue(expected == actual)


class CharacterStatTests(unittest.TestCase):
    """
    CharacterStatTests
    Contains several test cases for our statistics calculations
    """


    def testMaxFieldLength(self):
        """
        testCountFunction
        Used to test max field length value
        """
        inputArray = ['a', 'cat', 'went', 'home', 'yesterday']
        expected = 9
        actual = maxLength(inputArray)
        self.assertTrue(expected == actual)


def main():
    unittest.main()

if __name__ == '__main__':
    main()
