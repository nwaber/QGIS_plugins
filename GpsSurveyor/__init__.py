# -*- coding: utf-8 -*-
"""
/***************************************************************************
 GpsSurveyor
                                 A QGIS plugin
 This plugin collects RTK GPS survey data
                             -------------------
        begin                : 2016-07-23
        copyright            : (C) 2016 by Nick Waber
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
    """Load GpsSurveyor class from file GpsSurveyor.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .gps_surveyor import GpsSurveyor
    return GpsSurveyor(iface)
