"""
#Created by: McKenna Duzac
#Last Edited: 18 May 2018

All of these tests written with the following assumptions:
    -functions take in a list of values

The following functions need to be created for NumericStats:
    itemCount()     << counts the number of items in the input list
    maxValue()      << find the maximum valued item in input list
    minValue()      << find the minimum valued item in input list
    meanValue()     << find the mean value of all items in input list
    medianValue()   << find the median value in input list
    sumValue()      << find the sum of all items in input list
    stdDevValue()   << find the standard deviation of an input list
    coeffVarValue() << find the coefficieint of variation given an input list

The following functions need to be created for CharacterStats:
    maxLength()     << finds the length of the longest item in the list

TODO:
    import stat files
    Fringe cases not currently checked
    Improper input cases not currently checked
    Most of the CharcterStats functions currently unknown
"""

#These imports are required for unit tests
import unittest
import statistics

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
        expected = len(inputArray)
        actual = itemCount(inputArray)
        self.assertTrue(expected == actual)

    def testMaxFunction(self):
        """
        testMaxFunction
        Used to test max value functionality
        """
        inputArray = [1, 4, 8, 3, 6]
        expected = max(inputArray)
        actual = maxValue(inputArray)
        self.assertTrue(expected == actual)

    def testMinFunction(self):
        """
        testCountFunction
        Used to test min value functionality
        """
        inputArray = [1, 4, 8, 3, 6]
        expected = min(inputArray)
        actual = minValue(inputArray)
        self.assertTrue(expected == actual)

    def testMeanFunction(self):
        """
        testCountFunction
        Used to test mean value functionality
        """
        inputArray = [1, 4, 8, 3, 6]
        expected = sum(inputArray)/float(len(inputArray))
        actual = meanValue(inputArray)
        self.assertTrue(expected == actual)

    def testMedianFunction(self):
        """
        testCountFunction
        Used to test median value functionality
        """
        inputArray = [1, 4, 8, 3, 6]
        expected = statistics.median(inputArray)
        actual = medianValue(inputArray)
        self.assertTrue(expected == actual)

    def testSumFunction(self):
        """
        testCountFunction
        Used to test sum value functionality
        """
        inputArray = [1, 4, 8, 3, 6]
        expected = sum(inputArray)
        actual = sumValue(inputArray)
        self.assertTrue(expected == actual)

    def testStandardDeviation(self):
        """
        testCountFunction
        Used to test standard deviation value
        """
        inputArray = [1, 4, 8, 3, 6]
        expected = 2.7018512172213
        actual = stdDevValue(inputArray)
        self.assertTrue(expected == actual)

    def testCoefficientOfVariation(self):
        """
        testCountFunction
        Used to test coefficient of variation value
        """
        inputArray = [1, 4, 8, 3, 6]
        expected = 0.614057094823
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
