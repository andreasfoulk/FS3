# -*- coding: utf-8 -*-
"""

	QGIS plugin - Provides basic statistics for numeric and test fields.
				- Includes various tools for optimizing statistical search.
				- For more information see : https://github.com/andreasfoulk/FS3

	Copyright (c) 2018 Orden Aitchedji, Mckenna Duzac, Andreas Foulk, Tanner Lee

	Permission is hereby granted, free of charge, to any person obtaining a copy
	of this software and associated documentation files (the "Software"), to deal
	in the Software without restriction, including without limitation the rights
	to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
	copies of the Software, and to permit persons to whom the Software is
	furnished to do so, subject to the following conditions:

	The above copyright notice and this permission notice shall be included in
	all copies or substantial portions of the Software.

	THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
	IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
	FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
	AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
	LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
	OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
	THE SOFTWARE.

"""

#classFactory is a required function for QGIS Plugins
#Function is called when the plugin gets loaded
#Used to return QGIS an instance of your plugin

def classFactory(iface):
    from .fs3 import FS3Plugin
    return FS3Plugin(iface)
