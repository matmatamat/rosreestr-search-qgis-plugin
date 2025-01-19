# -*- coding: utf -8 -*-
# Rosreestr-nspd-search-qgis-plugin
# Licensed under the terms of GNU GPL 2

import os
import re
import requests
import ssl
import urllib.request
import html
import json
from PyQt5.QtWidgets import (
    QMessageBox
)   
from qgis.PyQt.QtGui import QIcon
from qgis.utils import iface
from qgis.core import (
    QgsVectorLayer,
    QgsProject
)

def add_gjsn(pth, gjsn):
    with open(pth, 'w') as gjsn_file:
        pass
        gjsn_file.write(gjsn)
        
    lr = QgsVectorLayer(pth, 'pkk_poly', 'ogr')

    if not lr.isValid():
        print("Объект {} не может быть загружен".format(lr.name()))
    QgsProject.instance().addMapLayers([lr])

    canvas = iface.mapCanvas()
        
    lr.selectAll()
    canvas.zoomToSelected()
    lr.removeSelection()
    canvas.refresh()


def nspd_pkk(cnum, type_obj):

    loop= True
    cou = 0
    while loop and cou < 60:
        try:                       
            # удаляет старые слои из легенды
            for layer in QgsProject.instance().mapLayers().values():
                if layer.name()=='pkk_poly':
                    QgsProject.instance().removeMapLayers([layer.id()])

            ###
            pth = os.path.abspath(__file__) + 'pkk_poly' + '.geojson'

            prjc_crs = re.findall(r'\b\d+\b', str(QgsProject.instance().crs()))

            url = 'https://nspd.gov.ru/api/geoportal/v2/search/geoportal?query=' + cnum + type_obj[0]
            r = requests.get(url, verify=False)
            cont = r.content
            resp = html.unescape(cont.decode("utf-8"))
            q = json.loads(resp)

            if list(q.keys())[0] == 'data':
                obj_counter = len((q['data'])['features'])
                if obj_counter == 1:  
                    geom = str((((q['data'])['features'][0])['geometry']))
                    geom = geom.replace(", 'crs': {'type': 'name', 'properties': {'name': 'EPSG:3857'}}", "")
                    properties = str((((q['data'])['features'][0])['properties']))
                    gjsn = "{'type': 'FeatureCollection', 'crs': {'type': 'name', 'properties': { 'name': 'urn:ogc:def:crs:EPSG::3857' }},'features': [{'type': 'Feature', 'geometry': " + geom + ", 'properties': " + properties + '}]}'
                    gjsn = gjsn.replace("\"", "")
                    gjsn = gjsn.replace("'", "\"")
                    gjsn = gjsn.replace('None', '"None"')
                    gjsn = gjsn.replace('True', '"True"')

                    if str((((q['data'])['features'][0])['geometry'])['type']) == 'Point':
                        QMessageBox.information(iface.mainWindow(), 'Info', 'Без координат границ')
                        add_gjsn(pth, gjsn)
                    else:
                        add_gjsn(pth, gjsn)
 
                else:
                    QMessageBox.information(iface.mainWindow(), 'https://nspd.gov.ru', 'Без координат границ или ошибка категории (возвращено: ' + str(obj_counter) + ' features)')
            else: 
                QMessageBox.information(iface.mainWindow(), 'https://nspd.gov.ru', 
                json.dumps(q) + 
                '\n\nВозможные причины ошибки:\n1. Запрошенный участок не является ЗУ, ОКС или ЗОУИТ\n2. Ошибка ввода кадастрового номера\nНапример, указано неверное количество незначащих "0" в номере кадастрового квартала')
            ###
            
            loop = False
        except requests.exceptions.SSLError:
            cou += 1
            loop = True
        except requests.exceptions.ConnectionError:
            cou += 1
            loop = True
        if cou == 60:
            QMessageBox.information(iface.mainWindow(),
            str(cou),
                'Превышено количество запросов')        
