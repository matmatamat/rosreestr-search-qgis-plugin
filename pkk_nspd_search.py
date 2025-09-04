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
import processing

def add_layer(type_obj, cnum, lr):
    QgsProject.instance().addMapLayers([lr])

    if type_obj == '&thematicSearchId=2':
        expression = f'"descr" = \'{cnum}\''
        layer = iface.activeLayer()
        layer.setSubsetString(expression)

    canvas = iface.mapCanvas()
        
    lr.selectAll()
    canvas.zoomToSelected()
    lr.removeSelection()
    canvas.refresh()

def add_gjsn(pth, q, cnum, type_obj, ml):
    with open(pth, 'w') as gjsn_file:
        json.dump(q, gjsn_file)

    with open (pth, 'r') as f:
      old_data = f.read()

    new_data = old_data.replace(', "crs": {"type": "name", "properties": {"name": "EPSG:3857"}}', '')
    new_data = old_data.replace('"type": "FeatureCollection",', '"type": "FeatureCollection", "crs": {"type": "name", "properties": { "name": "urn:ogc:def:crs:EPSG::3857" }},')

    with open (pth, 'w') as f:
      f.write(new_data)
    
    lr = QgsVectorLayer(pth, 'pkk_poly', 'ogr')

    if ml == 'f':    
        add_layer(type_obj, cnum, lr)
    elif ml == 't':
        lr.selectAll()
        lr = processing.run("native:saveselectedfeatures", {'INPUT': lr, 'OUTPUT': 'memory:'})['OUTPUT']
        lr.setName(cnum)
        add_layer(type_obj, cnum, lr)
    else:
        pass

def nspd_pkk(cnum, type_obj, ml):

    loop= True
    cou = 0
    while loop and cou < 60:
        try:                       
            for layer in QgsProject.instance().mapLayers().values():
                if layer.name()=='pkk_poly':
                    QgsProject.instance().removeMapLayers([layer.id()])

            ###
            pth = os.path.abspath(__file__) + 'pkk_poly' + '.geojson'

            url = 'https://nspd.gov.ru/api/geoportal/v2/search/geoportal?query=' + cnum + type_obj

            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0",
                "Accept": "application/json, text/plain, */*",
                "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
                "Accept-Encoding": "gzip, deflate, br",
                "Connection": "keep-alive",
                "Referer": "https://nspd.gov.ru/",
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-origin",
                "Pragma": "no-cache",
                "Cache-Control": "no-cache",
                "TE": "trailers"
            }

            r = requests.get(url, headers=headers, timeout=15, verify=False)
            cont = r.content
            resp = html.unescape(cont.decode("utf-8"))
            q = json.loads(resp)
            
            if list(q.keys())[0] == 'data':
                
                obj_counter = len((q['data'])['features'])
                if obj_counter != 1 and type_obj != '&thematicSearchId=2':  
                    QMessageBox.information(iface.mainWindow(), 'https://nspd.gov.ru', 'Без координат границ или ошибка категории (возвращено: ' + str(obj_counter) + ' features)')
                        
                if str((((q['data'])['features'][0])['geometry'])['type']) == 'Point':
                    QMessageBox.information(iface.mainWindow(), 'Info', 'Без координат границ')
                    add_gjsn(pth, q, cnum, type_obj, ml)
                else:
                    add_gjsn(pth, q, cnum, type_obj, ml)
            
            else: 
                QMessageBox.information(iface.mainWindow(), 'https://nspd.gov.ru', 
                json.dumps(q) + 
                '\n\nВозможные причины ошибки:\n1. Неверно выбран тип объекта\n2. Ошибка ввода кадастрового номера\nНапример, указано неверное количество незначащих "0" в номере кадастрового квартала')
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

