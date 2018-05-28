"""
Created by: McKenna Duzac
Last Edited: 23 May 2018

All of these tests written with the following assumptions:

TODO:
    Improper input cases not currently checked
"""

#These imports are required for unit tests
import unittest
from roundFunc import decimalRound

class RoundFuncTests(unittest.TestCase):
    """
    RoundFuncTests
    Tests for our rounding function
    """

    def testRound0(self):
        """
        Test adding zeros after integer when not enough
        and there currently aren't any decimals
        """
        inputNum = 1
        numDecimals = 2
        expected = 1.00
        actual = decimalRound(inputNum, numDecimals)
        self.assertEqual(actual, expected)

    def testRound1(self):
        """
        Test adding zeros after integer when not enough
        """
        inputNum = 1.1
        numDecimals = 3
        expected = 1.100
        actual = decimalRound(inputNum, numDecimals)
        self.assertEqual(actual, expected)

    def testRound2(self):
        """
        Test rounding number (up) to given decimal point
        """
        inputNum = 1.3456789
        numDecimals = 2
        expected = 1.35
        actual = decimalRound(inputNum, numDecimals)
        self.assertEqual(actual, expected)

    def testRound3(self):
        """
        Test rounding number (down) to given decimal point
        """
        inputNum = 1.3426789
        numDecimals = 2
        expected = 1.34
        actual = decimalRound(inputNum, numDecimals)
        self.assertEqual(actual, expected)

    def testRound4(self):
        """
        Test rounding (down) number to no decimal values
        """
        inputNum = 1.3456789
        numDecimals = 0
        expected = 1
        actual = decimalRound(inputNum, numDecimals)
        self.assertEqual(actual, expected)

    def testRound5(self):
        """
        Test rounding (up) number to no decimal values
        """
        inputNum = 1.7456789
        numDecimals = 0
        expected = 2
        actual = decimalRound(inputNum, numDecimals)
        self.assertEqual(actual, expected)

def main():
    unittest.main()

if __name__ == '__main__':
    main()
