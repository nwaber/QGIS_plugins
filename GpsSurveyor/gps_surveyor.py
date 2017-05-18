# -*- coding: utf-8 -*-
"""
/***************************************************************************
 GpsSurveyor
                                 A QGIS plugin
 Collects GPS survey data
                              -------------------
        begin                : 2016-04-04
        git sha              : $Format:%H$
        copyright            : (C) 2016 by Nick Waber
        email                : nwaber@gmail.com
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
from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from PyQt4.QtGui import QAction, QIcon, QFileDialog
# Initialize Qt resources from file resources.py
import resources
# Import the code for the dialog
from gps_surveyor_dialog import GpsSurveyorDialog
import os.path
from PyQt4.QtCore import QVariant
from PyQt4.QtCore import QVariant
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *

class GpsSurveyor:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'GpsSurveyor_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.dlg = GpsSurveyorDialog()

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&GPS Surveyor')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'GpsSurveyor')
        self.toolbar.setObjectName(u'GpsSurveyor')

        #NEW
        #  "save as..." dialog box action
        self.dlg.lineEdit.clear()
        self.dlg.pushButton.clicked.connect(self.select_output_file)

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('GpsSurveyor', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/GpsSurveyor/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'Collect GPS survey data.'),
            callback=self.run,
            parent=self.iface.mainWindow())


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&GPS Surveyor'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar

    def select_output_file(self):
        filename = QFileDialog.getSaveFileName(self.dlg, "Select output file ","", '*.shp')
        self.dlg.lineEdit.setText(filename)


    def run(self):
        """Run method that performs all the real work"""


        """The following code has been adapted, massaged,
            and cannibalized from a variety of places.  It's a mess,
            and could use a bit of culling with the defunct commented lines."""

        newFont = QFont("Arial", 18)
        self.iface.layerCombo = QComboBox()
        #self.dlg.layerCombo.addItems(["Topo", "Artifact", "Datum", "Feature", "Other"])
        self.dlg.layerCombo.setFont(newFont)
        #layerCombo.resize(300,100)
        #layerCombo.show()

        
        # Run the dialog event loop
        #result = self.dlg.exec_()
        # See if OK was pressed
        #if result:
            # Do something useful here - delete the line containing pass and
        # substitute with your code.
        # GPS NMEA data acquisition plugin by Nick Waber
        # Goal: two-click data capture
        # Button 1: Capture data
        # Button 2: Apply data and entered fields to point attributes

        #
        #
        #
        # The GPS Part from http://imasdemase.com/en/programacion-2/get-gps-info-qgis-python-console/
        # First we get the connectionRegistry

        connectionRegistry = QgsGPSConnectionRegistry().instance()
         
        # Now the connections list from that registry instance
         
        connectionList = connectionRegistry.connectionList()
         
        # If we have just one, we get the info from the first of them:
         
        GPSInfo = connectionList[0].currentGPSInformation()
         
        # And now, we extract the info we want 
         
        longitude = GPSInfo.longitude
        latitude = GPSInfo.latitude
        elevation = GPSInfo.elevation
        fix = GPSInfo.quality
        satsUsed = GPSInfo.satellitesUsed


        #
        #
        #
        #

        # The point part - add a point to the map
        #from PyQt4.QtCore import QVariant
        #from PyQt4.QtCore import *
        #from PyQt4.QtGui import *

        #layer = QgsVectorLayer('C:/Users/Nick/Documents/GIS_DataBase/Temps/RTK_01.shp', 'Piksi Rover' , 'ogr')
        layer = QgsVectorLayer('Point?crs=epsg:4326', 'Piksi Rover' ,"memory")

        pr = layer.dataProvider()

        fields = pr.fields()
        pt = QgsFeature(fields)
        point1 = QgsPoint(longitude,latitude)
        pr.addAttributes([QgsField("ID", QVariant.Int)])
        pr.addAttributes([QgsField("Point type", QVariant.String)])
        pr.addAttributes([QgsField("Elevation",QVariant.Double)])
        pr.addAttributes([QgsField("Longitude",QVariant.Double)])
        pr.addAttributes([QgsField("Latitude",QVariant.Double)])
        pr.addAttributes([QgsField("Fix",QVariant.Int)])
        pr.addAttributes([QgsField("Satellites",QVariant.Int)])


        point1 = QgsPoint(longitude,latitude)
        pt.setGeometry(QgsGeometry.fromPoint(point1))
        #pr.addFeatures([pt])
        layer.updateFields()
        layer.updateExtents()
        QgsMapLayerRegistry.instance().addMapLayers([layer])



        
        def collectPoint():
            #QgsGPSConnectionRegistry(self, None)
            
            connectionRegistry = QgsGPSConnectionRegistry().instance()
             
            # Now the connections list from that registry instance
             
            connectionList = connectionRegistry.connectionList()
             
            # If we have just one, we get the info from the first of them:
             
            GPSInfo = connectionList[0].currentGPSInformation()
         
            # And now, we extract the info we want 
             
            longitude = GPSInfo.longitude
            latitude = GPSInfo.latitude
            elevation = GPSInfo.elevation
            fix = GPSInfo.quality
            satsUsed = GPSInfo.satellitesUsed

            #
            #
            #
            #

            # The point part - add a point to the map
            from PyQt4.QtCore import QVariant

            #layer = QgsVectorLayer('Point?crs=epsg:4326', 'Piksi Rover' , "memory")
            #pr = layer.dataProvider()

            layer.startEditing()

            fields = pr.fields()
            pt = QgsFeature(fields)
            point1 = QgsPoint(longitude,latitude)
            pt.setGeometry(QgsGeometry.fromPoint(point1))
            #pr.addFeatures([pt])
            
            text = self.dlg.layerCombo.currentText()

            #f = QgsFeature(fields)
            pt["Point type"] = text
            pt["Elevation"] = elevation
            pt["Latitude"]= latitude
            pt["Longitude"]=longitude
            pt["Fix"] = fix
            pt["Satellites"] = satsUsed
            
            pr.addFeatures([pt])
            #fid1 = 2
            text = layer.fieldNameIndex("Point type")
            gpsLong = layer.fieldNameIndex("Longitude")
            gpsLat = layer.fieldNameIndex("Latitude")
            elev = layer.fieldNameIndex("Elevation")
            gpsFix = layer.fieldNameIndex("Fix")
            gpsSats = layer.fieldNameIndex("Satellites")
            #attr1 = {elev:elevation, gpsLong:longitude ,gpsLat:latitude}
            #layer.dataProvider().changeAttributeValues({fid1:attr1})

            
            

            layer.commitChanges()

            layer.updateExtents()


        

        self.iface.button = QPushButton()
        self.dlg.button.setText("Collect point")
        self.dlg.button.setFont(newFont)
        self.dlg.button.clicked.connect(collectPoint)
        # show the dialog
        self.dlg.show()


        def saveLayer():
            filename = self.dlg.lineEdit.text()
            QgsVectorFileWriter.writeAsVectorFormat(layer,filename,"utf-8",None,"ESRI Shapefile")

        self.iface.button = QPushButton()
        self.dlg.saveButton.setText("SAVE")
        self.dlg.saveButton.setFont(newFont)
        self.dlg.saveButton.clicked.connect(saveLayer)

        #NEW
#  create file??
        result = self.dlg.exec_()
        if result:
            filename = self.dlg.lineEdit.text()
            QgsVectorFileWriter.writeAsVectorFormat(layer,filename,"utf-8",None,"ESRI Shapefile")

            
'''
        newFont = QFont("Arial", 24)

        layerCombo = QComboBox()
        layerCombo.addItems(["Topo", "Artifact", "Datum", "Feature", "Other"])
        layerCombo.setFont(newFont)
        #layerCombo.resize(300,100)
        #layerCombo.show()

        button = QPushButton()
        button.setText("Collect point")
        button.setFont(newFont)
        button.clicked.connect(collectPoint)
        #button.resize(300,200)
        #button.show()

                       

'''

