# -*- coding: utf-8 -*-
"""
/***************************************************************************
 LithicEdgeWear
                                 A QGIS plugin
 This plugin quantifies lithic edge wear
                             -------------------
        begin                : 2017-10-30
        copyright            : (C) 2017 by Nick Waber
        email                : nwaber@gmail.com
        git sha              : $Format:%H$
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


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load LithicEdgeWear class from file LithicEdgeWear.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .lithic_edge_wear import LithicEdgeWear
    return LithicEdgeWear(iface)
