"""
Created on Tue May 15 2018

@author: Tanner Lee, Orden Aitchedji, McKenna Duzac, Andreas Foulk

"""
from PyQt5.QtCore import QVariant
from qgis.core import QgsProject, QgsMapLayer

#https://qgis.org/api/classQgsProject.html

class LayerFieldGetter(object):
    """
    TODO This classes docstring
    """
    def __init__(self):
        """
        Must have for self construtor?
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

    @staticmethod
    def getNextField(layer, fieldName):
        """
        Get the next field to work with
        """
        fields = LayerFieldGetter.getAllFields(layer)
        current = 0
        for field in fields:
            if field == fieldName:
                if current < len(fields) - 1:
                    return fields[current + 1]
                return field[0]
            current += 1
        return None

    @staticmethod
    def getPreviousField(layer, fieldName):
        """
        Get the next field to work with
        """
        fields = LayerFieldGetter.getAllFields(layer)
        current = 0
        for field in fields:
            if field == fieldName:
                if current > 0:
                    return fields[current - 1]
                return field[len(fields) - 1]
            current += 1
        return None

    @staticmethod
    def getFieldType(layer, fieldName):
        """
        Returns the selected field type
        """
        fields = layer.pendingFields()
        for field in fields:
            if field.name() == fieldName:
                return field.typeName()
        return None

    @staticmethod
    def getFieldLength(layer, fieldName):
        """
        Returns the selected field length
        """
        fields = layer.pendingFields()
        for field in fields:
            if field.name() == fieldName:
                return field.length()
        return None

    @staticmethod
    def getFieldPrecision(layer, fieldName):
        """
        Return the precision for the field selected
        """
        fields = layer.pendingFields()
        for field in fields:
            if field.name() == fieldName:
                return field.precision()
        return None
