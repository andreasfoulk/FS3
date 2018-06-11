"""

    roundFunc.py -- Plugin implimentation handling all numeric rounding
                 -- For more information see : https://github.com/andreasfoulk/FS3
                 -- This function is tested with helperTests.py
    
    Copyright (c) 2018 Orden Aitchedji, Mckenna Duzac, Andreas Foulk, Tanner Lee

    This software may be modified and distributed under the terms
    of the MIT license.  See the LICENSE file for details.

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
