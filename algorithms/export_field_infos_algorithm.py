# -*- coding: utf-8 -*-

"""
/***************************************************************************
 The3lizTools
                                 A QGIS plugin
 A 3liz processing tools
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2019-05-24
        copyright            : (C) 2019 by 3liz
        email                : info@3liz.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

__author__ = '3liz'
__date__ = '2019-05-24'
__copyright__ = '(C) 2019 by 3liz'

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = '$Format:%H$'

from PyQt5.QtCore import (QCoreApplication, QVariant)
from qgis.core import (QgsProcessing,
                       QgsProcessingContext,
                       QgsProcessingAlgorithm,
                       QgsProcessingParameterFileDestination,
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterFeatureSink,
                       QgsProcessingOutputVectorLayer,
                       QgsProcessingException)
from qgis.core import (QgsVectorFileWriter,
                       QgsFeatureSink,
                       QgsVectorLayer,
                       QgsFeature,
                       QgsFields,
                       QgsField)

from .utils import providerFields


class ExportFieldAlgorithm(QgsProcessingAlgorithm):
    """
    This is an example algorithm that takes a vector layer and
    creates a new identical one.

    It is meant to be used as an example of how to create your own
    algorithms and explain methods and variables used to do it. An
    algorithm like this will be available in all elements, and there
    is not need for additional work.

    All Processing algorithms should extend the QgsProcessingAlgorithm
    class.
    """

    # Constants used to refer to parameters and outputs. They will be
    # used when calling the algorithm from another algorithm, or when
    # calling from the QGIS console.

    INPUT = 'INPUT'
    OUTPUT = 'OUTPUT'
    OUTPUT_LAYER = 'OUTPUT_LAYER'

    def initAlgorithm(self, config):
        """
        Here we define the inputs and output of the algorithm, along
        with some other properties.
        """

        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.INPUT,
                self.tr('Input layer'),
                [QgsProcessing.TypeVector]
            )
        )

        self.addParameter(
            QgsProcessingParameterFileDestination(
                self.OUTPUT,
                self.tr('CSV file'),
                fileFilter='csv'
            )
        )

        self.addOutput(
            QgsProcessingOutputVectorLayer(
                self.OUTPUT_LAYER,
                self.tr('CSV layer'),
                QgsProcessing.TypeVector
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """

        source = self.parameterAsSource(parameters, self.INPUT, context)
        path = self.parameterAsFile(parameters, self.OUTPUT, context)

        field_def = {'idx': QVariant.Int,
                     'name': QVariant.String,
                     'type': QVariant.Int,
                     'typeName': QVariant.String,
                     'length': QVariant.Int,
                     'precision': QVariant.Int,
                     'comment': QVariant.String,
                     'alias': QVariant.String}

        # create virtual layer
        vl = QgsVectorLayer("None", "fields", "memory")
        pr = vl.dataProvider()

        # define fields
        fields = QgsFields()
        for n, t in field_def.items():
            fields.append(QgsField(name=n, type=t))

         # add fields
        pr.addAttributes(fields)
        vl.updateFields() # tell the vector layer to fetch changes from the provider

        # add feature based on field description
        field_index = 0
        for f in providerFields(source.fields()):
            field_index += 1
            feat = QgsFeature()
            feat.setAttributes([field_index, f.name(), f.type(), f.typeName(),
                                f.length(), f.precision(), f.comment(), f.alias()])
            pr.addFeatures([feat])

        # set create file layer options
        options = QgsVectorFileWriter.SaveVectorOptions()
        options.driverName = QgsVectorFileWriter.driverForExtension('csv')
        options.fileEncoding = 'UTF-8'
        options.actionOnExistingFile = QgsVectorFileWriter.CreateOrOverwriteFile
        options.layerOptions = ['CREATE_CSVT=YES']

        # write file
        write_result, error_message = QgsVectorFileWriter.writeAsVectorFormat(
            vl,
            path,
            options)

        # result
        if write_result != QgsVectorFileWriter.NoError:
            raise QgsProcessingException(
                self.tr('* ERROR: {0}').format(error_message))

        del fields
        del pr
        del vl

        # create layer
        dest_layer = QgsVectorLayer(path, self.OUTPUT_LAYER, 'ogr')
        if not dest_layer.isValid():
            raise QgsProcessingException(
                self.tr('* ERROR: Can\'t load layer {1} in {0}').format(path, self.OUTPUT_LAYER))

        # Add layer to context
        context.temporaryLayerStore().addMapLayer(dest_layer)
        context.addLayerToLoadOnCompletion(
            dest_layer.id(),
            QgsProcessingContext.LayerDetails(
                self.OUTPUT_LAYER,
                context.project(),
                self.OUTPUT_LAYER
            )
        )

        return {self.OUTPUT: path, self.OUTPUT_LAYER: dest_layer.id()}

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'export_field_infos'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr('Export field infos')

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr('Descriptions')

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'descriptions'

    def tr(self, string):
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return self.__class__()