# -*- coding: utf-8 -*-
"""
/***************************************************************************
 LithicEdgeWear
                                 A QGIS plugin
 This plugin quantifies lithic edge wear
                              -------------------
        begin                : 2017-10-30
        git sha              : $Format:%H$
        copyright            : (C) 2017 by Nick Waber
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
from PyQt4.QtGui import QAction, QIcon
# Initialize Qt resources from file resources.py
import resources
# Import the code for the dialog
from lithic_edge_wear_dialog import LithicEdgeWearDialog
import os.path


class LithicEdgeWear:
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
            'LithicEdgeWear_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)


        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Lithic Edge Wear')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'LithicEdgeWear')
        self.toolbar.setObjectName(u'LithicEdgeWear')

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
        return QCoreApplication.translate('LithicEdgeWear', message)


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

        # Create the dialog (after translation) and keep reference
        self.dlg = LithicEdgeWearDialog()

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

        icon_path = ':/plugins/LithicEdgeWear/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'Lithic Edge Wear'),
            callback=self.run,
            parent=self.iface.mainWindow())


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&Lithic Edge Wear'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar


    def run(self):
        """Run method that performs all the real work"""
        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        import processing
        #need this so processing algs can be used
     
        #fresh MB surface
        self.dlg.comboBox.clear()
        #worn MB surface
        self.dlg.comboBox_2.clear()
        #fresh MB perimeter
        self.dlg.comboBox_3.clear()
        #worn MB perimeter
        self.dlg.comboBox_4.clear()
        #spin box for threshold
        
        layers = self.iface.legendInterface().layers()
        layer_list = []
        for layer in layers:
            layer_list.append(layer.name())
        self.dlg.comboBox.addItems(layer_list)
        self.dlg.comboBox_2.addItems(layer_list)
        self.dlg.comboBox_3.addItems(layer_list)
        self.dlg.comboBox_4.addItems(layer_list)
        
        self.dlg.doubleSpinBox.clear() #start with no value in spin box
        
        
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:

            # Identify selected layer by its index
            selectedLayer1Index = self.dlg.comboBox.currentIndex()
            # use the layer currently in the comboBox
            selectedLayer1 = layers[selectedLayer1Index].name()
            selectedLayer2Index = self.dlg.comboBox_2.currentIndex()
            selectedLayer2 = layers[selectedLayer2Index].name()
            selectedLayer3Index = self.dlg.comboBox_3.currentIndex()
            selectedLayer3 = layers[selectedLayer3Index].name()
            selectedLayer4Index = self.dlg.comboBox_4.currentIndex()
            selectedLayer4 = layers[selectedLayer4Index].name()
            freshSurface = selectedLayer1
            wornSurface = selectedLayer2
            freshPerim = selectedLayer3
            wornPerim = selectedLayer4

            #coords in case needed for GRASS7 module extents (uncomment)
            #ext = layers[selectedLayer1Index].extent()
            #xmin = ext.xMinimum()
            #xmax = ext.xMaximum()
            #ymin = ext.yMinimum()
            #ymax = ext.yMaximum()
            #coords = "%f,%f,%f,%f" %(xmin, xmax, ymin, ymax) # this is a string that stores the coordinate
            
            #subtract the worn surface from the unworn surface
            processing.runalg("saga:rastercalculator",freshSurface,wornSurface,"a-b",0,False,7,"differenceRaster1") #basic worn surface
            processing.runalg('saga:convertlinestopolygons', freshPerim,"freshPoly") #create unworn polygon
            processing.runalg('saga:convertlinestopolygons', wornPerim,"wornPoly") #create worn polygon
            processing.runalg("saga:difference","freshPoly.shp","wornPoly.shp",True,"lostPoly") #create lost material polygon
            processing.runalg('saga:clipgridwithpolygon', "differenceRaster1","wornPoly.shp",0,"differenceRaster2") #clean up difference raster edges with worn surface polygon
            processing.runalg('saga:clipgridwithpolygon', freshSurface,"lostPoly.shp",0,"lostMaterial") #clip fresh surface with total wear polygon
            processing.runalg("gdalogr:merge","differenceRaster2;lostMaterial",False,False,-9999,5,'mergedWear') #merge wear surface with clipped lostMaterial surface
            processing.runalg("saga:rastercalculator",freshSurface,"mergedWear","b/a",0,False,7,"differenceIndex1") #raw wear index
            processing.runalg("saga:rastercalculator","differenceIndex1",None,"ifelse( a>1,1,a)",0,False,7,"differenceIndex2") #wear index max = 1
            processing.runalg("saga:rastercalculator","differenceIndex2",None,"ifelse( a<0,0,a)",0,False,7,"differenceIndex3") #wear index min = 0
            processing.runalg("saga:rastercalculator","mergedWear",None,"ifelse( a>0,a,0)",0,False,7,"wearVolume") #create wear volume raster
            self.iface.addRasterLayer("differenceIndex3", "Wear index") #load Wear Index layer
            self.iface.addRasterLayer("wearVolume", "Wear volume") #load Wear Volume layer

            #Create binary wear mapper based on lineEdit threshold
            #thresh = float( self.dlg.doubleSpinBox.value())
            #processing.runalg("saga:rastercalculator","differenceIndex3",None,"ifelse( a>0.15,1,0)",0,False,7,"wearBinary") #wear index min = 0
            #processing.runalg("gdalogr:polygonize","wearBinary","DN","wearBinaryPoly")
            #processing.runalg("qgis:selectbyattribute","wearBinaryPoly","DN",0,"1")
            #processing.runandload("qgis:saveselectedfeatures","wearBinaryPoly","wornArea")
            #print(thresh) #for debugging lineEdit.value()     
            

