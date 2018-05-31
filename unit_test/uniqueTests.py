"""
Created by: McKenna Duzac
Last Edited: 25 May 2018

All of these tests written with the following assumptions:

TODO:
    Improper input cases not currently checked
"""

#These imports are required for unit tests
import unittest
from fs3Unique import FS3Uniqueness

class UniqueValueTests(unittest.TestCase):
    """
    UniqueValueTests
    Tests for our unique tab
    """

    @classmethod
    def setUpClass(self):
        #A simple set of data with no empties
        self.goodValues = FS3Uniqueness()
        self.goodValues.initialize([1,2,1,2,1,2,3])

    def testUniqueGoodValues(self):
        expected = [1,2,3]
        actual = self.goodValues.uniqueValues
        self.assertEqual(actual, expected)

    def testUniqueGoodValuesCounts(self):
        expected = [3,3,1]
        actual = self.goodValues.uniqueNumOccur
        self.assertEqual(actual, expected)

    def testUniqueGoodValuesPercent(self):
        expected = [42.857142857142854, 42.857142857142854, 14.285714285714285]
        actual = self.goodValues.uniquePercent
        self.assertEqual(actual, expected)


def main():
    unittest.main()

if __name__ == '__main__':
    main()
