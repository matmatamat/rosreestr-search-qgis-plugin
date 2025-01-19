# -*- coding: utf -8 -*-
# Rosreestr-nspd-search-qgis-plugin
# Licensed under the terms of GNU GPL 2

from qgis.core import QgsDataSourceUri
from qgis.PyQt import QtWidgets
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QRadioButton,
                         QPushButton, QLineEdit, QMessageBox)
# from PyQt5.QtCore import QSettings
from PyQt5.QtGui import QPalette, QColor
import re
from .pkk_nspd_search import nspd_pkk

class GetParameters(QtWidgets.QDialog):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.mv = ['&thematicSearchId=1']

        self.layout =  QVBoxLayout()
        
        self.label = QtWidgets.QLabel('Укажите тип объекта для поиска')
        self.font = self.label.font()
        self.font.setPointSize(10)
        self.palette = QPalette()
        self.palette.setColor(QPalette.Foreground, QColor("grey"))
        self.label.setPalette( self.palette)
        
        self.rb1 = QRadioButton('ЗУ, ОКС')
        self.rb1.setChecked(True)

        self.rb2 = QRadioButton('ЗОУИТ')
        self.button =  QPushButton("Найти участок")
        
        self.textbox = QLineEdit(self)

        self.rb1.toggled.connect(self.rb1_active)
        self.rb2.toggled.connect(self.rb2_active)
        self.button.clicked.connect(self.push_button)
        
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.rb1)
        self.layout.addWidget(self.rb2)
        self.layout.addWidget(self.textbox)
        self.layout.addWidget(self.button)
        
        # self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('Поиск участка по кадастровому номеру')

        self.setLayout(self.layout)

    def rb1_active(self, on):
        if on:
            self.mv.append('&thematicSearchId=1')
        else:
            self.mv.remove('&thematicSearchId=1')

    def rb2_active(self, on):
        if on:
            self.mv.append('&thematicSearchId=5')          
        else:
            self.mv.remove('&thematicSearchId=5')            

    def push_button(self):
        self.type_obj = self.mv
        self.cnum = self.textbox.text()
        self.cnum = self.cnum.replace(' ', '')
        # self.textbox.clear()

        if self.cnum == '' or self.cnum.isspace():
            QMessageBox.warning(None, "Warning", "Не указан номер объекта")
        elif re.compile(r'(\d{2}\:\d{2}\:\d{1,7}\:\d+)+$').match(self.cnum) and self.type_obj == ['&thematicSearchId=1']:
            nspd_pkk(self.cnum, self.type_obj)
        elif re.compile(r'(\d{2}\:\d{2}\-\d+\.\d+)+$').match(self.cnum) and self.type_obj == ['&thematicSearchId=5']:
            nspd_pkk(self.cnum, self.type_obj)            
        else:
            QMessageBox.warning(None, "Warning", "Кадастровый номер не соответствует выбранному типу\nили содержит ошибку!")
