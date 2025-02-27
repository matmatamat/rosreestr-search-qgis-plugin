# -*- coding: utf -8 -*-
# Rosreestr-nspd-search-qgis-plugin
# Licensed under the terms of GNU GPL 2

from qgis.core import QgsDataSourceUri
from qgis.PyQt import QtWidgets
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QRadioButton, QCheckBox,
                         QPushButton, QLineEdit, QMessageBox, QComboBox)
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt
import re
from .pkk_nspd_search import nspd_pkk

from .add_wms import nspd_cadastre, add_nspd_cadastre, nspd_maps, add_nspd_maps, other_maps, add_other_maps

from qgis.utils import iface
dlg = QtWidgets.QDialog(iface.mainWindow())

class GetParameters(QtWidgets.QDialog):
    def __init__(self, parent=dlg):
        QWidget.__init__(self, parent)

        self.mv = ['&thematicSearchId=1']

        self.meml = ['f']

        self.cad_maps = []

        self.nspd_maps = []

        self.other_maps = []

        self.layout =  QVBoxLayout()
        
        self.label_1 = QtWidgets.QLabel('Укажите тип объекта для поиска')
        self.font = self.label_1.font()
        
        self.label_2 = QtWidgets.QLabel('Введите кадастровый номер')
        self.font = self.label_2.font()

        self.label_3 = QtWidgets.QLabel('\n' + 'Публичная кадастровая карта. Добавить слой')
        self.font = self.label_3.font()

        self.label_4 = QtWidgets.QLabel('\n' + 'НСПД, картооснова. Добавить слой')
        self.font = self.label_3.font() 

        self.label_5 = QtWidgets.QLabel('\n' + 'Cторонние картоосновы. Добавить слой')
        self.font = self.label_5.font()       
        
        self.font.setPointSize(10)
        self.palette = QPalette()
        self.palette.setColor(QPalette.Foreground, QColor("grey"))

        self.label_1.setPalette( self.palette)
        self.label_2.setPalette( self.palette)
        self.label_3.setPalette( self.palette)
        self.label_4.setPalette( self.palette)
        self.label_5.setPalette( self.palette)        

        self.rb1 = QRadioButton('Объекты недвижимости (ЗУ, ОКС)')
        self.rb1.setChecked(True)

        self.rb2 = QRadioButton('Кадастровое деление')

        self.rb3 = QRadioButton('Административно-территориальное деление')

        self.rb4 = QRadioButton('Зоны и территории (ЗОУИТ)')

        self.rb5 = QRadioButton('Территориальные зоны')

        self.cb1 = QCheckBox('Добавить, как временный слой')
        self.cb1.setLayoutDirection(Qt.RightToLeft) 
        
        self.button =  QPushButton("Найти участок")
        
        self.textbox = QLineEdit(self)

        self.category_combobox  = QComboBox(self)
        self.item_combobox = QComboBox(self)

        self.nspd_maps_combobox  = QComboBox(self)

        self.other_maps_combobox  = QComboBox(self)

        self.rb1.toggled.connect(self.rb1_active)
        self.rb2.toggled.connect(self.rb2_active)
        self.rb3.toggled.connect(self.rb3_active)
        self.rb4.toggled.connect(self.rb4_active)
        self.rb5.toggled.connect(self.rb5_active)
        self.cb1.toggled.connect(self.cb1_active)
        self.button.clicked.connect(self.push_button)

        self.category_combobox.currentTextChanged.connect(self.set_category)
        self.category_combobox.addItems(nspd_cadastre.keys())
        self.item_combobox.currentTextChanged.connect(self.set_item)

        self.nspd_maps_combobox.currentTextChanged.connect(self.set_nspd_maps)
        self.nspd_maps_combobox.addItems(nspd_maps)

        self.other_maps_combobox.currentTextChanged.connect(self.set_other_maps)
        self.other_maps_combobox.addItems(other_maps)         

        self.layout.addWidget(self.label_1)
        self.layout.addWidget(self.rb1)
        self.layout.addWidget(self.rb2)
        self.layout.addWidget(self.rb3)
        self.layout.addWidget(self.rb4)
        self.layout.addWidget(self.rb5)
        self.layout.addWidget(self.cb1)
        self.layout.addWidget(self.label_2)
        self.layout.addWidget(self.textbox)
        self.layout.addWidget(self.button)
        self.layout.addWidget(self.label_3)
        self.layout.addWidget(self.category_combobox)
        self.layout.addWidget(self.item_combobox)
        self.layout.addWidget(self.label_4)
        self.layout.addWidget(self.nspd_maps_combobox)
        self.layout.addWidget(self.label_5)
        self.layout.addWidget(self.other_maps_combobox)        
        
        # self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('https://nspd.gov.ru/map')
        # self.setWindowFlags(Qt.WindowStaysOnTopHint)

        self.setLayout(self.layout)

    def rb1_active(self, on):
        if on:
            self.mv.append('&thematicSearchId=1')
        else:
            self.mv.clear()

    def rb2_active(self, on):
        if on:
            self.mv.append('&thematicSearchId=2')
        else:
            self.mv.clear()

    def rb3_active(self, on):
        if on:
            self.mv.append('&thematicSearchId=4')
        else:
            self.mv.clear()          

    def rb4_active(self, on):
        if on:
            self.mv.append('&thematicSearchId=5')         
        else:
            self.mv.clear()

    def rb5_active(self, on):
        if on:
            self.mv.append('&thematicSearchId=7')       
        else:
            self.mv.clear()

    def cb1_active(self, on):
        if on:
            self.meml.remove('f')
            self.meml.append('t')
        else:
            self.meml.remove('t')
            self.meml.append('f')     
         
    def set_category(self, text):
        self.item_combobox.clear()
        self.item_combobox.addItems(nspd_cadastre.get(text, []))

    def set_item(self, text):
        if text:
            self.cad_maps.clear()
            self.cad_maps.append(text)
            add_nspd_cadastre(self.cad_maps)

    def set_nspd_maps(self, text):
        if text:
            self.nspd_maps.clear()
            self.nspd_maps.append(text)
            add_nspd_maps(self.nspd_maps)

    def set_other_maps(self, text):
        if text:
            self.other_maps.clear()
            self.other_maps.append(text)
            add_other_maps(self.other_maps)                                  

    def push_button(self):
        self.mv = sorted(self.mv)
        self.type_obj = self.mv[0]
        self.ml = self.meml[0]
        self.cnum = self.textbox.text()
        self.cnum = self.cnum.replace(' ', '')
        # self.textbox.clear()

        if self.cnum == '' or self.cnum.isspace():
            QMessageBox.warning(None, "Warning", "Не указан номер объекта")
        # Объекты недвижимости
        elif re.compile(r'(\d{2}\:\d{2}\:\d{1,7}\:\d+)+$').match(self.cnum) and self.type_obj == '&thematicSearchId=1':
            nspd_pkk(self.cnum, self.type_obj, self.ml)
        # Кадастровое деление
        elif re.compile(r'(\d{2})+$').match(self.cnum) and self.type_obj == '&thematicSearchId=2': 
            nspd_pkk(self.cnum, self.type_obj, self.ml)
        elif re.compile(r'(\d{2}\:\d{2})+$').match(self.cnum) and self.type_obj == '&thematicSearchId=2': 
            nspd_pkk(self.cnum, self.type_obj, self.ml)
        elif re.compile(r'(\d{2}\:\d{2}\:\d{1,7})+$').match(self.cnum) and self.type_obj == '&thematicSearchId=2': 
            nspd_pkk(self.cnum, self.type_obj, self.ml)
        # Административно-территориальное деление
        elif re.compile(r'(\d{2}\:\d{2}\-\d+\.\d+)+$').match(self.cnum) and self.type_obj == '&thematicSearchId=4':
            nspd_pkk(self.cnum, self.type_obj, self.ml)
        # Зоны и территории
        elif re.compile(r'(\d{2}\:\d{2}\-\d+\.\d+)+$').match(self.cnum) and self.type_obj == '&thematicSearchId=5':
            nspd_pkk(self.cnum, self.type_obj, self.ml)
        # Территориальные зоны
        elif re.compile(r'(\d{2}\:\d{2}\-\d+\.\d+)+$').match(self.cnum) and self.type_obj == '&thematicSearchId=7':
            nspd_pkk(self.cnum, self.type_obj, self.ml)       

        else:
            QMessageBox.warning(None, "Warning", "Кадастровый номер не соответствует выбранному типу\nили содержит ошибку!")
