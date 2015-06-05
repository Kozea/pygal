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
Hungarian maps

"""

from __future__ import division
from collections import defaultdict
from pygal.graph.map import BaseMap
from pygal._compat import u
from numbers import Number

import os


# XXX: use http://hu.wikipedia.org/wiki/NUTS:HU hierarchical codes?
# Counties ~ NUTS-3:
COUNTIES = {
    'nograd':   u('Nógrád'),
    'heves':    u('Heves'),
    'jnsz':     u('Jász-Nagykun-Szolnok'),
    'budapest': u('Budapest'),
    'pest':     u('Pest'),
    'fejer':    u('Fejér'),
    'veszprem': u('Veszprém'),
    'tolna':    u('Tolna'),
    'ke':       u('Komárom-Esztergom'),
    'gyms':     u('Győr-Moson-Sopron'),
    'vas':      u('Vas'),
    'zala':     u('Zala'),
    'somogy':   u('Somogy'),
    'baranya':  u('Baranya'),
    'bk':       u('Bács-Kiskun'),
    'csongrad': u('Csongrád'),
    'bekes':    u('Békés'),
    'hb':       u('Hajdú-Bihar'),
    'szszb':    u('Szabolcs-Szatmár-Bereg'),
    'baz':      u('Borsod-Abaúj-Zemplén'),
}


# TODO: NUTS-1 (country parts) and NUTS-2 (statistical regions)


with open(os.path.join(
        os.path.dirname(__file__), 'maps',
        'HU_counties_blank.svg')) as file:
    COUNTY_MAP = file.read()


class HungarianCountyMap(BaseMap):
    """Hungarian county map"""
    x_labels = list(COUNTIES.keys())
    area_names = COUNTIES
    area_prefix = ''
    # area_prefix = 'HU'
    kind = 'megye'
    svg_map = COUNTY_MAP
