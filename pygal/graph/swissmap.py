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
    'kt-zh': u("ZH"),
    'kt-be': u("BE"),
    'kt-lu': u("LU"),
    'kt-ju': u("JH"),
    'kt-ur': u("UR"),
    'kt-sz': u("SZ"),
    'kt-ow': u("OW"),
    'kt-nw': u("NW"),
    'kt-gl': u("GL"),
    'kt-zg': u("ZG"),
    'kt-fr': u("FR"),
    'kt-so': u("SO"),
    'kt-bl': u("BS"),
    'kt-bs': u("BL"),
    'kt-sh': u("SH"),
    'kt-ar': u("AR"),
    'kt-ai': u("AI"),
    'kt-sg': u("SG"),
    'kt-gr': u("GR"),
    'kt-ag': u("AG"),
    'kt-tg': u("TG"),
    'kt-ti': u("TI"),
    'kt-vd': u("VD"),
    'kt-vs': u("VS"),
    'kt-ne': u("NE"),
    'kt-ge': u("GE"),
}


with open(os.path.join(
        os.path.dirname(__file__), 'maps',
        'ch.cantons.svg')) as file:
    CNT_MAP = file.read()


class SwissMapCantons(BaseMap):
    """Swiss Cantons map"""
    x_labels = list(CANTONS.keys())
    area_names = CANTONS
    area_prefix = 'z'
    kind = 'canton'
    svg_map = CNT_MAP
