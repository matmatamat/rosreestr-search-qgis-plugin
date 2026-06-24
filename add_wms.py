# -*- coding: utf-8 -*-
# Rosreestr-nspd-search-qgis-plugin
# Licensed under the terms of GNU GPL 2
from urllib.parse import quote

from qgis.PyQt.QtWidgets import QMessageBox
from qgis.core import QgsRasterLayer, QgsProject


def show_invalid_layer_warning(name):
    QMessageBox.warning(
        None,
        'https://nspd.gov.ru/map',
        'Не удалось добавить слой:\n'
        + name
        + '\n\nQGIS отклонил источник данных как некорректный.'
    )


def nspd_wms_uri(head, active_layer, layer_id, extra=''):
    return (
        head
        + quote(active_layer, safe='')
        + '&layers='
        + str(layer_id)
        + '&styles='
        + extra
        + '&IgnoreGetMapUrl=1'
        + '&url=https://nspd.gov.ru/api/aeggis/v3/'
        + str(layer_id)
        + '/wms'
    )


def add_layer(layer):
    if not layer.isValid():
        show_invalid_layer_warning(layer.name())
        return None

    QgsProject.instance().addMapLayer(layer)
    return layer


def add_raster_layer(uri, name, provider='wms'):
    return add_layer(QgsRasterLayer(uri, name, provider))

# Thanks to Slinger (https://geodesist.ru/members/slinger.4082/)
# https://geodesist.ru/threads/rosreestr-otkryl-portal-nspd.94512/page-6#post-1128441
nspd_cadastre = {
    '':[],
    'Единицы кадастрового деления':[
        '', 'Кадастровые округа', 'Кадастровые районы', 'Кадастровые кварталы'
        ],
    'Административные границы': [
        '', 'Государственная граница Российской Федерации', 
        'Субъекты Российской Федерации (полигоны)', 'Субъекты Российской Федерации (линии)', 
        'Муниципальные образования (полигоны)', 'Муниципальные образования (линии)',
        'Населённые пункты (полигоны)', 'Населённые пункты (линии)'
        ],
    'Земельные участки': [
        '', 'Земельные участки из ЕГРН', 'Земельные участки из ЕГРН (подписи)',
        'Земельные участки, образуемые по схеме расположения земельного участка',
        'Земельные участки, выставленные на аукцион', 'Земельные участки, свободные от прав третьих лиц',
        'Земля для стройки ПКК', 'Земля для туризма ПКК', 'Земельные участки, образуемые по проекту межевания территории'
        ],
    'Объекты капитального строительства':[
        '', 'Здания', 'Здания (подписи)', 'Сооружения', 'Объекты незавершенного строительства'
        ],
    'Комплексы объектов':[
        '', 'Единые недвижимые комплексы', 'Предприятие как имущественный комплекс'
        ],
    'Зоны с особыми условиями использования территории': [
        '', 'ЗОУИТ объектов культурного наследия', 'ЗОУИТ объектов энергетики, связи, транспорта',
        'ЗОУИТ природных территорий', 'ЗОУИТ охраняемых объектов и безопасности', 'Иные ЗОУИТ'
        ],
    'Зонирование и планирование территории': [
        '', 'Территориальные зоны', 'Красные линии'
        ],
    'Природные территории': [
        '', 'Особо охраняемые природные территории', 'Охотничьи угодья', 'Лесничества',
        'Береговые линии (границы водных объектов)(полигональный)',
        'Береговые линии (границы водных объектов)(линейный)'
        ],
    'Зоны социального, экономического развития': [
        '', 'Особые экономические зоны', 'Территории опережающего развития', 'Игорные зоны'
        ],
    'Территории объектов культурного наследия народов РФ' : [
        '', 'Территории объектов культурного наследия'
        ],
    'Иные территории':[
        '', 'Территории выполнения комплексных кадастровых работ',
        'Территория проведения мероприятий по ликвидации накопленного вреда окружающей среде, образовавшегося в результате производства химической продукции в г. Усолье-Сибирское Иркутской области',
         'Негативные процессы', 'Объекты туристского интереса'
        ],
    'Тепловые карты': [
        '', 'Кадастровая стоимость объекта', 'Удельный показатель кадастровой стоимости'
        ]
}

def add_nspd_cadastre(cad_maps):
    head = 'contextualWMSLegend=0&crs=EPSG:3857&dpiMode=7&featureCount=10&format=image/png&http-header:referer=https://nspd.gov.ru/map?active_layers%3D'

    # Единицы кадастрового деления
    if cad_maps[0] == 'Кадастровые округа':
        layer_path = QgsRasterLayer(head + '遑&layers=36945&styles&url=https://nspd.gov.ru/api/aeggis/v3/36945/wms', "Кадастровые округа", "wms")
        add_layer(layer_path)
    elif cad_maps[0] == 'Кадастровые районы':
        layer_path = QgsRasterLayer(head + '賦&layers=36070&styles&url=https://nspd.gov.ru/api/aeggis/v3/36070/wms', 'Кадастровые районы', 'wms')
        add_layer(layer_path) 
    elif cad_maps[0] == 'Кадастровые кварталы':
        layer_path = QgsRasterLayer(head + '賧&layers=36071&styles&url=https://nspd.gov.ru/api/aeggis/v3/36071/wms', 'Кадастровые кварталы', 'wms')
        add_layer(layer_path)
    
    # Административные границы
    elif cad_maps[0] == 'Государственная граница Российской Федерации':
        layer_path = QgsRasterLayer(head + '釁&layers=37313&styles&url=https://nspd.gov.ru/api/aeggis/v3/37313/wms', 'Государственная граница Российской Федерации', 'wms')
        add_layer(layer_path)
    elif cad_maps[0] == 'Субъекты Российской Федерации (полигоны)':
        layer_path = QgsRasterLayer(head + '釃&layers=37315&styles&url=https://nspd.gov.ru/api/aeggis/v3/37315/wms', 'Субъекты Российской Федерации (полигоны)', 'wms')
        add_layer(layer_path)
    elif cad_maps[0] == 'Субъекты Российской Федерации (линии)':
        layer_path = QgsRasterLayer(head + '釂&layers=37314&styles&url=https://nspd.gov.ru/api/aeggis/v3/37314/wms', 'Субъекты Российской Федерации (линии)', 'wms')
        add_layer(layer_path)               
    elif cad_maps[0] == 'Муниципальные образования (полигоны)':
        layer_path = QgsRasterLayer(head + '趶&layers=36278&styles&url=https://nspd.gov.ru/api/aeggis/v3/36278/wms', 'Муниципальные образования (полигоны)', 'wms')
        add_layer(layer_path)
    elif cad_maps[0] == 'Муниципальные образования (линии)':
        layer_path = QgsRasterLayer(head + '趷&layers=36279&styles&url=https://nspd.gov.ru/api/aeggis/v3/36279/wms', 'Муниципальные образования (линии)', 'wms')
        add_layer(layer_path)
    elif cad_maps[0] == 'Населённые пункты (полигоны)':
        layer_path = QgsRasterLayer(head + '趹&layers=36281&styles&url=https://nspd.gov.ru/api/aeggis/v3/36281/wms', 'Населённые пункты (полигоны)', 'wms')
        add_layer(layer_path)                
    elif cad_maps[0] == 'Населённые пункты (линии)':
        layer_path = QgsRasterLayer(head + '釄&layers=37316&styles&url=https://nspd.gov.ru/api/aeggis/v3/37316/wms', 'Населённые пункты (линии)', 'wms')
        add_layer(layer_path) 

    # Земельные участки
    elif cad_maps[0] == 'Земельные участки из ЕГРН':
        add_raster_layer(nspd_wms_uri(head, '賐', 36048), 'Земельные участки из ЕГРН')
    elif cad_maps[0] == 'Земельные участки из ЕГРН (подписи)':
        add_raster_layer(nspd_wms_uri(head, '賐', 36327), 'Земельные участки из ЕГРН (подписи)')
    elif cad_maps[0] == 'Земельные участки, образуемые по схеме расположения земельного участка':
        layer_path = QgsRasterLayer(head + '醮&layers=37294&styles&url=https://nspd.gov.ru/api/aeggis/v3/37294/wms', 'Земельные участки, образуемые по схеме расположения земельного участка', 'wms')
        add_layer(layer_path)
    elif cad_maps[0] == 'Земельные участки, выставленные на аукцион':
        layer_path = QgsRasterLayer(head + '醳&layers=37299&styles&url=https://nspd.gov.ru/api/aeggis/v3/37299/wms', 'Земельные участки, выставленные на аукцион', 'wms')
        add_layer(layer_path)
    elif cad_maps[0] == 'Земельные участки, свободные от прав третьих лиц':
        layer_path = QgsRasterLayer(head + '醲&layers=37298&styles&url=https://nspd.gov.ru/api/aeggis/v3/37298/wms', 'Земельные участки, свободные от прав третьих лиц', 'wms')
        add_layer(layer_path)             
    elif cad_maps[0] == 'Земля для стройки ПКК':
        layer_path = QgsRasterLayer(head + '%EF%BF%BF%2C%EF%BF%BF%2C%EF%BF%BF%2C%EF%BF%BF%2C%EF%BF%BF%2C%EF%BF%BF%2C%EF%BF%BF%2C%EF%BF%BF%2C%EF%BF%BF%2C%EF%BF%BF%2C%EF%BF%BF%2C%EF%BF%BF%2C&layers=849407&styles&url=https://nspd.gov.ru/api/aeggis/v3/849407/wms',
            'Земля для стройки ПКК', 'wms')
        add_layer(layer_path)
    elif cad_maps[0] == 'Земля для туризма ПКК':
        layer_path = QgsRasterLayer(head + '%EF%BF%BF%2C%EF%BF%BF%2C%EF%BF%BF%2C%EF%BF%BF%2C%EF%BF%BF%2C%EF%BF%BF%2C%EF%BF%BF%2C%EF%BF%BF%2C%EF%BF%BF%2C%EF%BF%BF%2C%EF%BF%BF%2C%EF%BF%BF%2C&layers=849453&styles&url=https://nspd.gov.ru/api/aeggis/v3/849453/wms',
             'Земля для туризма ПКК', 'wms')
        add_layer(layer_path)
    elif cad_maps[0] == 'Земельные участки, образуемые по проекту межевания территории':
        layer_path = QgsRasterLayer(head + '蹹&layers=36473&styles&url=https://nspd.gov.ru/api/aeggis/v3/36473/wms', 'Земельные участки, образуемые по проекту межевания территории', 'wms')
        add_layer(layer_path) 

    # Объекты капитального строительства
    elif cad_maps[0] == 'Здания':
        layer_path = QgsRasterLayer(head + '賑&layers=36049&styles&url=https://nspd.gov.ru/api/aeggis/v3/36049/wms', 'Здания', 'wms')
        add_layer(layer_path)
    elif cad_maps[0] == 'Здания (подписи)':
        layer_path = QgsRasterLayer(head + '賑&layers=36326&styles&url=https://nspd.gov.ru/api/aeggis/v3/36326/wms', 'Здания (подписи)', 'wms')
        add_layer(layer_path)
    elif cad_maps[0] == 'Сооружения':
        layer_path = QgsRasterLayer(head + '跨&layers=36328&styles&url=https://nspd.gov.ru/api/aeggis/v3/36328/wms', 'Сооружения', 'wms')
        add_layer(layer_path)
    elif cad_maps[0] == 'Объекты незавершенного строительства':
        layer_path = QgsRasterLayer(head + '跩&layers=36329&styles&url=https://nspd.gov.ru/api/aeggis/v3/36329/wms', 'Объекты незавершенного строительства', 'wms')
        add_layer(layer_path)                     

    # Комплексы объектов
    elif cad_maps[0] == 'Единые недвижимые комплексы':
        layer_path = QgsRasterLayer(head + '鈹&layers=37433&styles&url=https://nspd.gov.ru/api/aeggis/v3/37433/wms', 'Единые недвижимые комплексы', 'wms')
        add_layer(layer_path)
    elif cad_maps[0] == 'Предприятие как имущественный комплекс':
        layer_path = QgsRasterLayer(head + '鈺&layers=37434&styles&url=https://nspd.gov.ru/api/aeggis/v3/37434/wms', 'Предприятие как имущественный комплекс', 'wms')
        add_layer(layer_path)

    # Зоны с особыми условиями использования территории
    elif cad_maps[0] == 'ЗОУИТ объектов культурного наследия':
        layer_path = QgsRasterLayer(head + '鋉&layers=37577&styles&url=https://nspd.gov.ru/api/aeggis/v3/37577/wms', 'ЗОУИТ объектов культурного наследия', 'wms')
        add_layer(layer_path)
    elif cad_maps[0] == 'ЗОУИТ объектов энергетики, связи, транспорта':
        layer_path = QgsRasterLayer(head + '鋊&layers=37578&styles&url=https://nspd.gov.ru/api/aeggis/v3/37578/wms', 'ЗОУИТ объектов энергетики, связи, транспорта', 'wms')
        add_layer(layer_path)
    elif cad_maps[0] == 'ЗОУИТ природных территорий':
        layer_path = QgsRasterLayer(head + '鋌&layers=37580&styles&url=https://nspd.gov.ru/api/aeggis/v3/37580/wms', 'ЗОУИТ природных территорий', 'wms')
        add_layer(layer_path)
    elif cad_maps[0] == 'ЗОУИТ охраняемых объектов и безопасности':
        layer_path = QgsRasterLayer(head + '鋋&layers=37579&styles&url=https://nspd.gov.ru/api/aeggis/v3/37579/wms', 'ЗОУИТ охраняемых объектов и безопасности', 'wms')
        add_layer(layer_path)
    elif cad_maps[0] == 'Иные ЗОУИТ':
        layer_path = QgsRasterLayer(head + '鋍&layers=37581&styles&url=https://nspd.gov.ru/api/aeggis/v3/37581/wms', 'Иные ЗОУИТ', 'wms')
        add_layer(layer_path)

    # Зонирование и планирование территории
    elif cad_maps[0] == 'Территориальные зоны':
        layer_path = QgsRasterLayer(head + '跛&layers=36315&styles&url=https://nspd.gov.ru/api/aeggis/v3/36315/wms', 'Территориальные зоны', 'wms')
        add_layer(layer_path)
    elif cad_maps[0] == 'Красные линии':
        layer_path = QgsRasterLayer(head + '醭&layers=37293&styles&tilePixelRatio=0&url=https://nspd.gov.ru/api/aeggis/v3/37293/wms', 'Красные линии', 'wms')
        add_layer(layer_path) 

    # Природные территории
    elif cad_maps[0] == 'Особо охраняемые природные территории':
        layer_path = QgsRasterLayer(head + '距&layers=36317&styles&url=https://nspd.gov.ru/api/aeggis/v3/36317/wms', 'Особо охраняемые природные территории', 'wms')
        add_layer(layer_path)
    elif cad_maps[0] == 'Охотничьи угодья':
        layer_path = QgsRasterLayer(head + '跗&layers=36311&styles&url=https://nspd.gov.ru/api/aeggis/v3/36311/wms', 'Охотничьи угодья', 'wms')
        add_layer(layer_path) 
    elif cad_maps[0] == 'Лесничества':
        layer_path = QgsRasterLayer(head + '跚&layers=36314&styles&url=https://nspd.gov.ru/api/aeggis/v3/36314/wms', 'Лесничества', 'wms')
        add_layer(layer_path)
    elif cad_maps[0] == 'Береговые линии (границы водных объектов)(полигональный)':
        layer_path = QgsRasterLayer(head + '蹵&layers=36469&styles&url=https://nspd.gov.ru/api/aeggis/v3/36469/wms', 'Береговые линии (границы водных объектов)(полигональный)', 'wms')
        add_layer(layer_path)
    elif cad_maps[0] == 'Береговые линии (границы водных объектов)(линейный)':
        layer_path = QgsRasterLayer(head + '蹶&layers=36470&styles&url=https://nspd.gov.ru/api/aeggis/v3/36470/wms', 'Береговые линии (границы водных объектов)(линейный)', 'wms')
        add_layer(layer_path)

    # Зоны социального, экономического развития
    elif cad_maps[0] == 'Особые экономические зоны':
        layer_path = QgsRasterLayer(head + '跏&layers=36303&styles&url=https://nspd.gov.ru/api/aeggis/v3/36303/wms', 'Особые экономические зоны', 'wms')
        add_layer(layer_path)
    elif cad_maps[0] == 'Территории опережающего развития':
        layer_path = QgsRasterLayer(head + '跘&layers=36312&styles&url=https://nspd.gov.ru/api/aeggis/v3/36312/wms', 'Территории опережающего развития', 'wms')
        add_layer(layer_path) 
    elif cad_maps[0] == 'Игорные зоны':
        layer_path = QgsRasterLayer(head + '蹷&layers=36471&styles&url=https://nspd.gov.ru/api/aeggis/v3/36471/wms', 'Игорные зоны', 'wms')
        add_layer(layer_path)        

    # Территории объектов культурного наследия народов РФ
    elif cad_maps[0] == 'Территории объектов культурного наследия':
        rasterLyr = QgsRasterLayer(head + '跜&layers=36316&styles&url=https://nspd.gov.ru/api/aeggis/v3/36316/wms', 'Территории объектов культурного наследия', 'wms')
        add_layer(rasterLyr)

    # Иные территории
    elif cad_maps[0] == 'Территории выполнения комплексных кадастровых работ':
        layer_path = QgsRasterLayer(head + '鈶&layers=37430&styles&url=https://nspd.gov.ru/api/aeggis/v3/37430/wms', 'Территории выполнения комплексных кадастровых работ', 'wms')
        add_layer(layer_path)
    elif cad_maps[0] == 'Территория проведения мероприятий по ликвидации накопленного вреда окружающей среде, образовавшегося в результате производства химической продукции в г. Усолье-Сибирское Иркутской области':
        layer_path = QgsRasterLayer(head + '醯&layers=37295&styles&url=https://nspd.gov.ru/api/aeggis/v3/37295/wms', 'Территория проведения мероприятий по ликвидации накопленного вреда окружающей среде, образовавшегося в результате производства химической продукции в г. Усолье-Сибирское Иркутской области', 'wms')
        add_layer(layer_path)
    elif cad_maps[0] == 'Негативные процессы':
        layer_path = QgsRasterLayer(head + '醰&layers=37296&styles&url=https://nspd.gov.ru/api/aeggis/v3/37296/wms', 'Негативные процессы', 'wms')
        add_layer(layer_path)
    elif cad_maps[0] == 'Объекты туристского интереса':
        layer_path = QgsRasterLayer(head + '%EF%BF%BF%2C%EF%BF%BF%2C%EF%BF%BF%2C%EF%BF%BF%2C%EF%BF%BF%2C%EF%BF%BF%2C%EF%BF%BF%2C%EF%BF%BF%2C%EF%BF%BF%2C%EF%BF%BF%2C%EF%BF%BF%2C%EF%BF%BF%2C&layers=849601&styles&tilePixelRatio=0&url=https://nspd.gov.ru/api/aeggis/v3/849601/wms', 'Объекты туристского интереса', 'wms')
        add_layer(layer_path) 

    # Тепловые карты
    elif cad_maps[0] == 'Кадастровая стоимость объекта':
        layer_path = QgsRasterLayer(head + '酴&layers=37236&styles&url=https://nspd.gov.ru/api/aeggis/v3/37236/wms', 'Кадастровая стоимость объекта', 'wms')
        add_layer(layer_path)
    elif cad_maps[0] == 'Удельный показатель кадастровой стоимости':
        layer_path = QgsRasterLayer(head + '鍾&layers=37758&styles&url=https://nspd.gov.ru/api/aeggis/v3/37758/wms', 'Удельный показатель кадастровой стоимости', 'wms')
        add_layer(layer_path)


nspd_maps = [  
        '', 'Цифровая объектовая схема (справочный слой)', 'Единая электронная картографическая основа (основный слой)',
        'Единая электронная картографическая основа (основный слой) z14', 'Единая электронная картографическая основа (основный слой) z15',
        'Единая электронная картографическая основа (основный слой) z16', 'Единая электронная картографическая основа (основный слой) z17',
        'Единая электронная картографическая основа (основный слой) z18', 'ЦОС',
        'ДЗЗ Российская федерация', 'Единая электронная картографическая основа (ортофото)(основной слой)', 'Ортофотопланы 10000', 'Ортофотопланы 2000'
]

def add_nspd_maps(nspd_maps):
    maphead = 'http-header:referer=https://nspd.gov.ru/map?baseLayerId%3D'

    # Цифровая объектовая схема (справочный слой)
    if nspd_maps[0] == 'Цифровая объектовая схема (справочный слой)':
        layer_path = QgsRasterLayer(maphead + '235&referer=https://nspd.gov.ru/map?baseLayerId%3D235&type=xyz&url=https://nspd.gov.ru/api/aeggis/v2/235/wmts/%7Bz%7D/%7Bx%7D/%7By%7D.png&zmax=18&zmin=0', 'Цифровая объектовая схема (справочный слой)', 'wms')
        add_layer(layer_path)
    
    # Единая электронная картографическая основа (основный слой)
    elif nspd_maps[0] == 'Единая электронная картографическая основа (основный слой)':
        layer_path = QgsRasterLayer(maphead + '36347&referer=https://nspd.gov.ru/map?baseLayerId%3D36347&type=xyz&url=https://nspd.gov.ru/cgk/map/38/tms/%7Bz%7D/%7Bx%7D/%7By%7D.png&zmax=18&zmin=0', 'Единая электронная картографическая основа (основный слой)', 'wms')
        add_layer(layer_path)
    elif nspd_maps[0] == 'Единая электронная картографическая основа (основный слой) z14':
        layer_path = QgsRasterLayer(maphead + '36347&referer=https://nspd.gov.ru/map?baseLayerId%3D36347&type=xyz&url=https://nspd.gov.ru/cgk/map/38/tms/%7Bz%7D/%7Bx%7D/%7By%7D.png&zmax=14&zmin=0', 'Единая электронная картографическая основа (основный слой) z14', 'wms')
        add_layer(layer_path) 
    elif nspd_maps[0] == 'Единая электронная картографическая основа (основный слой) z15':
        layer_path = QgsRasterLayer(maphead + '36347&referer=https://nspd.gov.ru/map?baseLayerId%3D36347&type=xyz&url=https://nspd.gov.ru/cgk/map/38/tms/%7Bz%7D/%7Bx%7D/%7By%7D.png&zmax=15&zmin=0', 'Единая электронная картографическая основа (основный слой) z15', 'wms')
        add_layer(layer_path) 
    elif nspd_maps[0] == 'Единая электронная картографическая основа (основный слой) z16':
        layer_path = QgsRasterLayer(maphead + '36347&referer=https://nspd.gov.ru/map?baseLayerId%3D36347&type=xyz&url=https://nspd.gov.ru/cgk/map/38/tms/%7Bz%7D/%7Bx%7D/%7By%7D.png&zmax=16&zmin=0', 'Единая электронная картографическая основа (основный слой) z16', 'wms')
        add_layer(layer_path)               
    elif nspd_maps[0] == 'Единая электронная картографическая основа (основный слой) z17':
        layer_path = QgsRasterLayer(maphead + '36347&referer=https://nspd.gov.ru/map?baseLayerId%3D36347&type=xyz&url=https://nspd.gov.ru/cgk/map/38/tms/%7Bz%7D/%7Bx%7D/%7By%7D.png&zmax=17&zmin=0', 'Единая электронная картографическая основа (основный слой) z17', 'wms')
        add_layer(layer_path)
    elif nspd_maps[0] == 'Единая электронная картографическая основа (основный слой) z18':
        layer_path = QgsRasterLayer(maphead + '36347&referer=https://nspd.gov.ru/map?baseLayerId%3D36347&type=xyz&url=https://nspd.gov.ru/cgk/map/38/tms/%7Bz%7D/%7Bx%7D/%7By%7D.png&zmax=18&zmin=0', 'Единая электронная картографическая основа (основный слой) z18', 'wms')
        add_layer(layer_path)

    # ЦОС
    elif nspd_maps[0] == 'ЦОС':
        layer_path = QgsRasterLayer(maphead + '849241&referer=https://nspd.gov.ru/map?%26baseLayerId%3D849241&type=xyz&url=https://nspd.gov.ru/api/aeggis/v2/849241/wmts/%7Bz%7D/%7Bx%7D/%7By%7D.png&zmax=18&zmin=0', 'ЦОС', 'wms')
        add_layer(layer_path) 

    # ДЗЗ. Российская федерация
    elif nspd_maps[0] == 'ДЗЗ Российская федерация':
        layer_path = QgsRasterLayer(maphead + '36067&type=xyz&url=https://nspd.gov.ru/ntsomz/RUS_GKMSS100_012021080120210831_11700/TOARO/acr/PSRGB/%7Bz%7D/%7Bx%7D/%7By%7D&zmax=11&zmin=0', 'ДЗЗ Российская федерация', 'wms')
        add_layer(layer_path) 

    # Единая электронная картографическая основа (ортофото)(основной слой)
    elif nspd_maps[0] == 'Единая электронная картографическая основа (ортофото)(основной слой)':
        layer_path = QgsRasterLayer(maphead + '36346&referer=https://nspd.gov.ru/map?%26baseLayerId%3D36346&type=xyz&url=https://nspd.gov.ru/cgk/map/39/tms/%7Bz%7D/%7Bx%7D/%7By%7D.png&zmax=18&zmin=0', 'Единая электронная картографическая основа (ортофото)(основной слой)', 'wms')
        add_layer(layer_path) 

    # Ортофотопланы 10000
    elif nspd_maps[0] == 'Ортофотопланы 10000':
        layer_path = QgsRasterLayer(maphead + '36345&referer=https://nspd.gov.ru/map?%26baseLayerId%3D36345&type=xyz&url=https://nspd.gov.ru/api/aeggis/v2/36345/wmts/%7Bz%7D/%7Bx%7D/%7By%7D.png&zmax=18&zmin=0', 'Ортофотопланы 10000', 'wms')
        add_layer(layer_path)      

    # Ортофотопланы 2000
    elif nspd_maps[0] == 'Ортофотопланы 2000':
        layer_path = QgsRasterLayer(maphead + '36344&type=xyz&url=https://nspd.gov.ru/api/aeggis/v2/36344/wmts/%7Bz%7D/%7Bx%7D/%7By%7D.png&zmax=18&zmin=0', 'Ортофотопланы 2000', 'wms')
        add_layer(layer_path)


other_maps = [    
    '', 'Yandex', 'Yandex Satellite', 'OpenStreetMap'
]

def add_other_maps(other_maps):
    # Яндекс Карты
    if other_maps[0] == 'Yandex':
        layer_path = QgsRasterLayer('http-header:referer=&type=xyz&url=https://core-renderer-tiles.maps.yandex.net/tiles?l%3Dmap%26v%3D21.07.05-0-b210701140430%26x%3D%7Bx%7D%26y%3D%7By%7D%26z%3D%7Bz%7D%26scale%3D1%26lang%3Dru_RU%26amp&zmax=19&zmin=0', 'Yandex', 'wms')
        crs = layer_path.crs()
        crs.createFromId(3395)
        layer_path.setCrs(crs)
        add_layer(layer_path)

    # Yandex Satellite
    elif other_maps[0] == 'Yandex Satellite':
        layer_path = QgsRasterLayer('type=xyz&zmin=0&zmax=18&url=https://sat04.maps.yandex.net/tiles?l%3Dsat%26x%3D{x}%26y%3D{y}%26z%3D{z}', 'Yandex Satellite', 'wms')
        crs = layer_path.crs()
        crs.createFromId(3395)
        layer_path.setCrs(crs)
        add_layer(layer_path)

    # OpenStreetMap
    elif other_maps[0] == 'OpenStreetMap':
        layer_path = QgsRasterLayer('type=xyz&url=http://c.tile.openstreetmap.org/{z}/{x}/{y}.png', 'OSM', 'wms')
        add_layer(layer_path)
