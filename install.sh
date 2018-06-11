#!/bin/bash

pyrcc5 resources.qrc -o resources.py

if [[ "$OSTYPE" == "linux-gnu" ]]; then

    mkdir -p ~/.local/share/QGIS/QGIS3/profiles/default/python/plugins/FS3/jsscripts

    cp *py ~/.local/share/QGIS/QGIS3/profiles/default/python/plugins/FS3/.
    cp *ui ~/.local/share/QGIS/QGIS3/profiles/default/python/plugins/FS3/.
    cp *png ~/.local/share/QGIS/QGIS3/profiles/default/python/plugins/FS3/.
    cp jsscripts/*js ~/.local/share/QGIS/QGIS3/profiles/default/python/plugins/FS3/jsscripts/.

    cp metadata.txt ~/.local/share/QGIS/QGIS3/profiles/default/python/plugins/FS3/.
    cp resources.qrc ~/.local/share/QGIS/QGIS3/profiles/default/python/plugins/FS3/.
    cp -r i18n ~/.local/share/QGIS/QGIS3/profiles/default/python/plugins/FS3/.

elif [[ "$OSTYPE" == "darwin"* ]]; then

    mkdir -p ~/Library/Application\ Support/QGIS/QGIS3/profiles/default/python/plugins/FS3/jsscripts

    cp *py ~/Library/Application\ Support/QGIS/QGIS3/profiles/default/python/plugins/FS3/.
    cp *ui ~/Library/Application\ Support/QGIS/QGIS3/profiles/default/python/plugins/FS3/.
    cp *png ~/Library/Application\ Support/QGIS/QGIS3/profiles/default/python/plugins/FS3/.
    cp jsscripts/*js ~/Library/Application\ Support/QGIS/QGIS3/profiles/default/python/plugins/FS3/jsscripts/.

    cp metadata.txt ~/Library/Application\ Support/QGIS/QGIS3/profiles/default/python/plugins/FS3/.
    cp resources.qrc ~/Library/Application\ Support/QGIS/QGIS3/profiles/default/python/plugins/FS3/. 
    cp -r i18n ~/Library/Application\ Support/QGIS/QGIS3/profiles/default/python/plugins/FS3/.

else
    echo "Your OS is not supported with this installer"
fi
