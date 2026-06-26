# -*- coding: utf-8 -*-
# Rosreestr-nspd-search-qgis-plugin
# Licensed under the terms of GNU GPL 2
# Thanks to Martin Dobias for the 'QGIS Minimalist Plugin Skeleton': 
#   https://github.com/wonder-sk/qgis-minimal-plugin

import os
from qgis.PyQt.QtGui import QIcon
from .compat import Compat
from .get_user_parameters import GetParameters
from .nspd_requests import install_nspd_request_hook, remove_nspd_request_hook
from qgis.core import Qgis
from qgis.PyQt.QtWidgets import QMessageBox

MIN_QGIS_VERSION_INT = 34000
MIN_QGIS_VERSION_STR = '3.40'

class IncompatiblePlugin:
    
    def __init__(self, iface):
        self.iface = iface
        self._shown = False

    def initGui(self):
        if not self._shown:
            self._shown = True
            QMessageBox.critical(
                self.iface.mainWindow(),
                'Несовместимая версия QGIS',
                'Плагин rosreestr-search-qgis-plugin v 2.5 несовместим с данной версией QGIS.\n\n'
                f'Текущая версия: {Qgis.QGIS_VERSION}\n'
                f'Требуется версия: {MIN_QGIS_VERSION_STR} или выше.\n\n'
                'Плагин не будет загружен.'
            )
            
    def unload(self):
        pass

def classFactory(iface):
    
    if Qgis.QGIS_VERSION_INT < MIN_QGIS_VERSION_INT:
        return IncompatiblePlugin(iface)
    return PkkSearch(iface)

class PkkSearch:

    def __init__(self, iface):
        self.iface = iface
        self.nspd_request_processor_id = None
       
    def initGui(self):
        self.nspd_request_processor_id = install_nspd_request_hook()
        self.action = (Compat.QAction(QIcon(os.path.dirname(__file__) + '/icon.png'),
            'Поиск по Публичной кадастровой карте НСПД',
            self.iface.mainWindow()))
        self.action.triggered.connect(self.run)
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu("&Поиск по ПКК НСПД", self.action)
        self.first_start = True

    def unload(self):
        remove_nspd_request_hook(self.nspd_request_processor_id)
        self.nspd_request_processor_id = None
        self.iface.removePluginMenu('&Поиск по ПКК НСПД', self.action)
        self.iface.removeToolBarIcon(self.action)
        del self.action

    def run(self):
        if self.first_start == True:
            self.first_start = False
            self.buttons = GetParameters()

        self.buttons.show()
        self.result = Compat.exec_dialog(self.buttons)
        
        if self.result:
            pass
