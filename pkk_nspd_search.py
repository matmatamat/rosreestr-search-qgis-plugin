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
import time

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

            ### Артём, спасибо за помощь в парсинге json !
            session = requests.Session()
           
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36',
                'Accept': '*/*',
                'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
                'Referer': 'https://nspd.gov.ru/map?thematic=PKK&zoom=18.565066407456115&coordinate_x=6223932.21047097&coordinate_y=7962267.622666277&baseLayerId=235&theme_id=1&is_copy_url=true',
                'Origin': 'https://nspd.gov.ru',
                'x-kl-ksospc-ajax-request': 'Ajax_Request',
                'priority': 'u=1, i',
                'sec-ch-ua': '"Not:A-Brand";v="99", "Google Chrome";v="145", "Chromium";v="145"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
            }
           
            params = {
                'query': cnum,
                'thematicSearchId': '1'
            }
           
            # Загружаем главную страницу для получения cookies
            main_response = session.get(
                'https://nspd.gov.ru/map',
                headers=headers,
                timeout=10,
                verify=False
            )
           
            time.sleep(1)
           
            # Отправляем поисковый запрос
            response = session.get(
                'https://nspd.gov.ru/api/geoportal/v2/search/geoportal',
                params=params,
                headers=headers,
                timeout=10,
                verify=False
            )
           
            session.close()
           
            cont = response.content
            resp = html.unescape(cont.decode("utf-8"))
            q = json.loads(resp)
            ###
            
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




