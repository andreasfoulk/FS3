"""

    statTests.py -- Handles testing for prpper case by case rounding.
                 -- For more information see : https://github.com/andreasfoulk/FS3
    
    Copyright (c) 2018 Orden Aitchedji, Mckenna Duzac, Andreas Foulk, Tanner Lee

    This software may be modified and distributed under the terms
    of the MIT license.  See the LICENSE file for details.
    

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
        self.goodValues.initialize([1, 2, 1, 2, 1, 2, 3])

        #A set of data with empty values
        self.emptyValues = FS3Uniqueness()
        self.emptyValues.initialize([1, 2, 1, None, 2, None, 1, 2])

        #A set of data with length 1
        self.oneValues = FS3Uniqueness()
        self.oneValues.initialize([1])

        #A set of character data
        self.charValues = FS3Uniqueness()
        self.charValues.initialize(['cat', 'dog', None, 'cat', 'bird'])

    #--------------------------------------Good Value Tests--------------------------------------
    def testUniqueGoodValues(self):
        expected = [1, 2, 3]
        actual = self.goodValues.uniqueValues
        self.assertEqual(actual, expected)

    def testUniqueGoodValuesCounts(self):
        expected = [3, 3, 1]
        actual = self.goodValues.uniqueNumOccur
        self.assertEqual(actual, expected)

    def testUniqueGoodValuesPercent(self):
        expected = [42.857142857142854, 42.857142857142854, 14.285714285714285]
        actual = self.goodValues.uniquePercent
        self.assertEqual(actual, expected)

    #--------------------------------------Empty Value Tests--------------------------------------
    def testUniqueEmptyValues(self):
        expected = [1, 2, '[Empty]']
        actual = self.emptyValues.uniqueValues
        self.assertEqual(actual, expected)

    def testUniqueEmptyValuesCounts(self):
        expected = [3, 3, 2]
        actual = self.emptyValues.uniqueNumOccur
        self.assertEqual(actual, expected)

    def testUniqueEmptyValuesPercent(self):
        expected = [37.5, 37.5, 25.0]
        actual = self.emptyValues.uniquePercent
        self.assertEqual(actual, expected)

    #--------------------------------------One Value Tests--------------------------------------
    def testUniqueOneValues(self):
        expected = [1]
        actual = self.oneValues.uniqueValues
        self.assertEqual(actual, expected)

    def testUniqueOneValuesCounts(self):
        expected = [1]
        actual = self.oneValues.uniqueNumOccur
        self.assertEqual(actual, expected)

    def testUniqueOneValuesPercent(self):
        expected = [100]
        actual = self.oneValues.uniquePercent
        self.assertEqual(actual, expected)

    #--------------------------------------Char Value Tests--------------------------------------
    def testUniqueCharValues(self):
        expected = ['cat', 'dog', '[Empty]', 'bird']
        actual = self.charValues.uniqueValues
        self.assertEqual(actual, expected)

    def testUniqueCharValuesCounts(self):
        expected = [2, 1, 1, 1]
        actual = self.charValues.uniqueNumOccur
        self.assertEqual(actual, expected)

    def testUniqueCharValuesPercent(self):
        expected = [40.0, 20.0, 20.0, 20.0]
        actual = self.charValues.uniquePercent
        self.assertEqual(actual, expected)


def main():
    unittest.main()

if __name__ == '__main__':
    main()
