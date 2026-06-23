# -*- coding: utf-8 -*-
# Rosreestr-nspd-search-qgis-plugin
# Licensed under the terms of GNU GPL 2

import os

from qgis.PyQt.QtNetwork import QSslCertificate
from qgis.core import QgsNetworkAccessManager
from .compat import Compat

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


def install_nspd_ca_hook():
    if not os.path.exists(NSPD_CA_BUNDLE):
        return None

    nspd_ca_certs = load_nspd_ca_certs()
    if not nspd_ca_certs:
        return None

    def nspd_ca_preprocessor(request):
        url = request.url()

        if url.scheme().lower() != 'https' or not is_nspd_host(url.host()):
            return ''

        ssl_config = request.sslConfiguration()
        ssl_config.setCaCertificates(ssl_config.caCertificates() + nspd_ca_certs)
        request.setSslConfiguration(ssl_config)
        return ''

    return QgsNetworkAccessManager.setRequestPreprocessor(nspd_ca_preprocessor)


def remove_nspd_ca_hook(processor_id):
    if not processor_id:
        return

    try:
        QgsNetworkAccessManager.removeRequestPreprocessor(processor_id)
    except KeyError:
        pass
