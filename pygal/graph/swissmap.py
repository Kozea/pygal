# -*- coding: utf-8 -*-
# This file is part of pygal
#
# A python svg graph plotting library
# Copyright © 2012-2014 Kozea
#
# This library is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# This library is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with pygal. If not, see <http://www.gnu.org/licenses/>.
"""
Worldmap chart

"""

from __future__ import division
from pygal.graph.map import BaseMap
from pygal._compat import u
import os


CANTONS = {
    'kt-zh': u("Zürich"),
    'kt-be': u("Bern"),
    'kt-lu': u("Luzern"),
    'kt-ju': u("Jura"),
    'kt-ur': u("Uri"),
    'kt-sz': u("Schwyz"),
    'kt-ow': u("Obwalden"),
    'kt-nw': u("Nidwalden"),
    'kt-gl': u("Glarus"),
    'kt-zg': u("Zug"),
    'kt-fr': u("Freiburg"),
    'kt-so': u("Solothurn"),
    'kt-bl': u("Basel-Stadt"),
    'kt-bs': u("Basle-Land"),
    'kt-sh': u("Schaffhausen"),
    'kt-ar': u("Appenzell Ausseroden"),
    'kt-ai': u("Appenzell Innerroden"),
    'kt-sg': u("St. Gallen"),
    'kt-gr': u("Graubünden"),
    'kt-ag': u("Aargau"),
    'kt-tg': u("Thurgau"),
    'kt-ti': u("Tessin"),
    'kt-vd': u("Waadt"),
    'kt-vs': u("Wallis"),
    'kt-ne': u("Neuenburg"),
    'kt-ge': u("Genf"),
}

from .maps.ch_cantons_svg import data as CNT_MAP

class SwissMapCantons(BaseMap):
    """Swiss Cantons map"""
    x_labels = list(CANTONS.keys())
    area_names = CANTONS
    area_prefix = 'z'
    kind = 'canton'
    svg_map = CNT_MAP
