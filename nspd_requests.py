# -*- coding: utf-8 -*-
# Rosreestr-nspd-search-qgis-plugin
# Licensed under the terms of GNU GPL 2

import os

from qgis.PyQt.QtNetwork import QSslCertificate
from qgis.core import QgsNetworkAccessManager
from .compat import Compat
from .get_random_user_agent import get_random_user_agent

NSPD_HOST = 'nspd.gov.ru'
CERTS_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'certs')
NSPD_CA_BUNDLE = os.path.join(CERTS_DIR, 'nspd-ca-bundle.pem')

_nspd_ca_certs = None


def is_nspd_host(host):
    host = (host or '').lower()
    return host == NSPD_HOST or host.endswith('.' + NSPD_HOST)


def load_nspd_ca_certs():
    global _nspd_ca_certs

    if _nspd_ca_certs is None:
        _nspd_ca_certs = QSslCertificate.fromPath(NSPD_CA_BUNDLE, Compat.pem_encoding_format())

    return _nspd_ca_certs


def install_nspd_request_hook():
    if not os.path.exists(NSPD_CA_BUNDLE):
        return None

    nspd_ca_certs = load_nspd_ca_certs()
    if not nspd_ca_certs:
        return None

    # nspd по HTTP/1.1 блокирует юзер-агент QGIS (403), по HTTP/2 Qt со сжатием заголовков
    # получает пустой ответ - слой WMS выходит "невалидным".
    # Подменяем юзер-агент на браузерный, принудительно используем HTTP/1.1.
    http2_allowed_attribute = Compat.http2_allowed_attribute()
    nspd_user_agent = get_random_user_agent().encode('latin-1', 'ignore')

    def nspd_request_preprocessor(request):
        url = request.url()

        if url.scheme().lower() != 'https' or not is_nspd_host(url.host()):
            return ''

        ssl_config = request.sslConfiguration()
        ssl_config.setCaCertificates(ssl_config.caCertificates() + nspd_ca_certs)
        request.setSslConfiguration(ssl_config)
        request.setAttribute(http2_allowed_attribute, False)
        request.setRawHeader(b'User-Agent', nspd_user_agent)
        return ''

    return QgsNetworkAccessManager.setRequestPreprocessor(nspd_request_preprocessor)


def remove_nspd_request_hook(processor_id):
    if not processor_id:
        return

    try:
        QgsNetworkAccessManager.removeRequestPreprocessor(processor_id)
    except KeyError:
        pass
