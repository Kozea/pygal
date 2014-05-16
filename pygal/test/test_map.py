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

from pygal import (
    Worldmap, SupranationalWorldmap)
from pygal.i18n import COUNTRIES, SUPRANATIONAL, set_countries
import operator
try:
    from functools import reduce
except ImportError:
    pass

_COUNTRIES = dict(COUNTRIES)


def test_worldmap():
    set_countries(_COUNTRIES, True)
    datas = {}
    for i, ctry in enumerate(COUNTRIES):
        datas[ctry] = i

    wmap = Worldmap()
    wmap.add('countries', datas)
    q = wmap.render_pyquery()
    assert len(
        q('.country.color-0')
    ) == len(COUNTRIES)
    assert 'France' in q('#fr').text()


def test_worldmap_i18n():
    set_countries(_COUNTRIES, True)
    datas = {}
    for i, ctry in enumerate(COUNTRIES):
        datas[ctry] = i

    set_countries({'fr': 'Francia'})
    wmap = Worldmap()
    wmap.add('countries', datas)
    q = wmap.render_pyquery()
    assert len(
        q('.country.color-0')
    ) == len(COUNTRIES)
    assert 'Francia' in q('#fr').text()


def test_worldmap_i18n_clear():
    set_countries(_COUNTRIES, True)
    wmap = Worldmap()
    wmap.add('countries', dict(fr=12))
    set_countries({'fr': 'Frankreich'}, clear=True)
    q = wmap.render_pyquery()
    assert len(
        q('.country.color-0')
    ) == 1
    assert 'Frankreich' in q('#fr').text()


def test_supranationalworldmap():
    set_countries(_COUNTRIES, True)
    datas = {}
    for i, supra in enumerate(SUPRANATIONAL):
        datas[supra] = i + 1

    wmap = SupranationalWorldmap()
    wmap.add('supra', datas)
    q = wmap.render_pyquery()
    assert len(
        q('.country.color-0')
    ) == len(
        reduce(operator.or_, map(set, SUPRANATIONAL.values())))
