# -*- coding: utf-8 -*-
# Rosreestr-nspd-search-qgis-plugin
# Licensed under the terms of GNU GPL 2

from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtGui import QPalette
from qgis.PyQt.QtNetwork import QSsl

try:
    from qgis.PyQt.QtGui import QAction as QgisAction
except ImportError:
    from qgis.PyQt.QtWidgets import QAction as QgisAction


class Compat:
    QAction = QgisAction

    @staticmethod
    def exec_dialog(dialog):
        if hasattr(dialog, 'exec'):
            return dialog.exec()

        return dialog.exec_()

    @staticmethod
    def palette_foreground_role():
        color_role = getattr(QPalette, 'ColorRole', QPalette)
        return getattr(color_role, 'Foreground', color_role.WindowText)

    @staticmethod
    def pem_encoding_format():
        if hasattr(QSsl, 'EncodingFormat'):
            return QSsl.EncodingFormat.Pem

        return QSsl.Pem

    @staticmethod
    def right_to_left_layout_direction():
        layout_direction = getattr(Qt, 'LayoutDirection', Qt)
        return layout_direction.RightToLeft
