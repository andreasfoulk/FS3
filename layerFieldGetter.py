"""

    layerFieldGetter.py -- Plugin implimentation linking to QGIS
                        -- For more information see : https://github.com/andreasfoulk/FS3

    Copyright (c) 2018 Orden Aitchedji, McKenna Duzac, Andreas Foulk, Tanner Lee

    This software may be modified and distributed under the terms
    of the MIT license.  See the LICENSE file for details.

"""

from qgis.core import QgsProject, QgsMapLayer

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
        getVectorLayers
        Retrieve the layers currently loaded in to QGIS
        @return A sorted list of all layers currently loaded in to QGIS
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
        getSingleLayer
        Returns a single vector layer
        @param layerName Layer to retrieve
        @return layer
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
        getAllFields
        Returns the name of the fields in a given layer
        @param layer Layer to retrieve fields list for
        @return fieldLists List of all fields for the given layer
        """
        fields = layer.fields()
        fieldLists = []
        for field in fields:
            fieldLists.append(field.name())
        return fieldLists
