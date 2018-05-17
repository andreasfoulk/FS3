#!/bin/bash

pyrcc5 resources.qrc -o resources.py

if [[ "$OSTYPE" == "linux-gnu" ]]; then

    mkdir ~/.local/share/QGIS/QGIS3/profiles/default/python/plugins
    mkdir ~/.local/share/QGIS/QGIS3/profiles/default/python/plugins/FS3

    cp *py ~/.local/share/QGIS/QGIS3/profiles/default/python/plugins/FS3/.
    cp *ui ~/.local/share/QGIS/QGIS3/profiles/default/python/plugins/FS3/.
    cp *png ~/.local/share/QGIS/QGIS3/profiles/default/python/plugins/FS3/.

    cp metadata.txt ~/.local/share/QGIS/QGIS3/profiles/default/python/plugins/FS3/.
    cp resources.qrc ~/.local/share/QGIS/QGIS3/profiles/default/python/plugins/FS3/.


elif [[ "$OSTYPE" == "darwin"* ]]; then

    mkdir ~/Library/Application\ Support/QGIS/QGIS3/profiles/default/python/plugins
    mkdir ~/Library/Application\ Support/QGIS/QGIS3/profiles/default/python/plugins/FS3

    cp *py ~/Library/Application\ Support/QGIS/QGIS3/profiles/default/python/plugins/FS3/.
    cp *ui ~/Library/Application\ Support/QGIS/QGIS3/profiles/default/python/plugins/FS3/.
    cp *png ~/Library/Application\ Support/QGIS/QGIS3/profiles/default/python/plugins/FS3/.

    cp metadata.txt ~/Library/Application\ Support/QGIS/QGIS3/profiles/default/python/plugins/FS3/.
    cp resources.qrc ~/Library/Application\ Support/QGIS/QGIS3/profiles/default/python/plugins/FS3/.

else
    echo "Your OS is not supported with this installer"
fi
