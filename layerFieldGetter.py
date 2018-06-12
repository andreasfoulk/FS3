"""

    layerFieldGetter.py -- Plugin implimentation linking to QGIS
                        -- For more information see : https://github.com/andreasfoulk/FS3

    Copyright (c) 2018 Orden Aitchedji, Mckenna Duzac, Andreas Foulk, Tanner Lee

    This software may be modified and distributed under the terms
    of the MIT license.  See the LICENSE file for details.

"""
#from PyQt5.QtCore import QVariant
from qgis.core import QgsProject, QgsMapLayer

#https://qgis.org/api/classQgsProject.html

class LayerFieldGetter(object):
    """
    Handles Layer and Field retrieval
    """
    def __init__(self):
        """
        Must have for self construtor
        """

    @staticmethod
    def getVectorLayers():
        """
        The current map layer is loaded into qgis
        """
        project = QgsProject.instance()
        layerMap = project.mapLayers()
        layerList = []
        for name, layer in layerMap.items():
            if layer.type() == QgsMapLayer.VectorLayer:
                layerList.append((layer.name()))
        return sorted(layerList)

    @staticmethod
    def getSingleLayer(layerName):
        """
        Returns a single vector layer
        """
        project = QgsProject.instance()
        layerMap = project.mapLayers()
        for name, layer in layerMap.items():
            if layer.type() == QgsMapLayer.VectorLayer and \
            layer.name() == layerName:
                if layer.isValid():
                    return layer
                return None
        return None

    @staticmethod
    def getAllFields(layer):
        """
        Returns the name of the fields
        """
        fields = layer.fields()
        fieldLists = []
        for field in fields:
            fieldLists.append(field.name())
        return fieldLists
