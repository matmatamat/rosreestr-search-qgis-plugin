# -*- coding: utf-8 -*-
# Rosreestr-nspd-search-qgis-plugin
# Licensed under the terms of GNU GPL 2
# Thanks to Martin Dobias for the 'QGIS Minimalist Plugin Skeleton': 
#   https://github.com/wonder-sk/qgis-minimal-plugin

import os
from PyQt5.QtWidgets import QAction
from qgis.PyQt.QtGui import QIcon
from .get_user_parameters import GetParameters

def classFactory(iface):
    return PkkSearch(iface)

class PkkSearch:

    def __init__(self, iface):
        self.iface = iface
       
    def initGui(self):
        self.action = (QAction(QIcon(os.path.dirname(__file__) + "/icon.png"),
            'Поиск по Публичной кадастровой карте',
            self.iface.mainWindow()))
        self.action.triggered.connect(self.run)
        self.iface.addToolBarIcon(self.action)        

    def unload(self):
        self.iface.removeToolBarIcon(self.action)
        del self.action

    def run(self):
        self.buttons = GetParameters()

        self.buttons.show()
        self.result = self.buttons.exec_()
        
        if self.result:
            pass
