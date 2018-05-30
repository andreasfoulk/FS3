"""
Created by: McKenna Duzac
Last Edited: 25 May 2018

These functions are tested with uniqueTests.py

"""

def decimalRound(toRound, numDec):
    """
    decimalRound
    Function used to round numbers to given decimal value with the following rules:
        -should add zeroes if numDec > current number of decimal places
        -should round up/down properly
        -numDec = 0 should return an int

    @param toRound << number to round
    @param numDec  << number of decimal places wanted
    @return correctDec << correctly rounded number
    """

    correctDec = round(toRound, numDec)
    return correctDec
