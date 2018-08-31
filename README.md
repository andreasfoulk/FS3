# Field Statistics Plugin for QGIS 3
A simple data analysis plugin developed by Orden Aitchedji, McKenna Duzac, Andreas Foulk, and Tanner Lee.
This plugin was developed with the guidance of Brian Krzys as part of our CSM 2018 summer session.
It provides a quick and easy way to look at and analyze GIS data. Allowing the user to sort the data by the field of choice,
receive general statistics on this field, look at the unique members of this field, and produce a variety of graphs using
this field and any others within the same dataset.

### Installation
The plugin is available through the official QGIS plugin repository.  The plugin repository's informational page for FS3 can be found here: https://plugins.qgis.org/plugins/FS3/

### Development Installation
To install from source make sure pyrcc5 is installed then on a unix based machince from the root directory of this project run:
```
bash install.sh
```
### Tests
The unit_test directory contains unit tests for statistics.  Run these tests with the following command:
```
python -m unit_test.statTests
```

The test directory contains test generated from https://plugins.qgis.org/plugins/pluginbuilder/
### Style Guide
This code primarily follows the QGIS style guide subsituting PEP8 standards when neccesary for
the Python code. This project enforces these guides through pylint. To check a specific file run the following command from the root direcotry:
```
pylint <file>
```
Or for the whole project:
```
pylint FS3
```
This should use the included config file and say so in the first line of output.
