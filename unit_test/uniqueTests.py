"""
Created by: McKenna Duzac
Last Edited: 25 May 2018

All of these tests written with the following assumptions:

TODO:
    Improper input cases not currently checked
"""

#These imports are required for unit tests
import unittest
from roundFunc import decimalRound

class UniqueValueTests(unittest.TestCase):
    """
    UniqueValueTests
    Tests for our unique tab
    """

    def testUnique_0(self):
        """
        Perfect Data
        """
        inputNum = 1
        numDecimals = 2
        expected = 1.00
        actual = decimalRound(inputNum, numDecimals)
        self.assertEqual(actual, expected)


def main():
    unittest.main()

if __name__ == '__main__':
    main()
