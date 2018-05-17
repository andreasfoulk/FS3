# -*- coding: utf-8 -*-

"""

    QGIS basic statistics for numeric and text fields plugin.

    For more information see: https://github.com/andreasfoulk/FS3

    Copyright (C) 2018 Andreas Foulk

    Permission is hereby granted, free of charge, to any person
    obtaining a copy of this software and associated documentation
    files (the "Software"), to deal in the Software without
    restriction, including without limitation the rights to use,
    copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the
    Software is furnished to do so, subject to the following
    conditions:

    The above copyright notice and this permission notice shall be
    included in all copies or substantial portions of the Software.
    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
    EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
    OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
    NON-INFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
    HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
    WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
    FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
    OTHER DEALINGS IN THE SOFTWARE.

"""

def name():
    return "FS3"


def description():
    return "Basic statistics for numeric and text fields."


def category():
    return "Vector"


def version():
    return "0.1"


def qgisMinimumVersion():
    return "3.0"


def author():
    return "Orden, McKenna, Andreas, and Tanner"


def email():
    return "afoulk@mines.edu"


def icon():
    return "icons/fieldstats.png"
