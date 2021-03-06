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
 This script initializes the plugin, making it known to QGIS.
"""

__author__ = '3liz'
__date__ = '2019-05-24'
__copyright__ = '(C) 2019 by 3liz'


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load The3lizTools class from file The3lizTools.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .the_3liz_tools import The3lizToolsPlugin
    return The3lizToolsPlugin()
