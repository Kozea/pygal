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
    FrenchMap_Regions, FrenchMap_Departments)
from pygal.graph.frenchmap import REGIONS, DEPARTMENTS, aggregate_regions


def test_frenchmaps():
    datas = {}
    for dept in DEPARTMENTS.keys():
        datas[dept] = int(''.join([x for x in dept if x.isdigit()])) * 10

    fmap = FrenchMap_Departments()
    fmap.add('departements', datas)
    q = fmap.render_pyquery()
    assert len(
        q('#departements .departement,#dom-com .departement')
    ) == len(DEPARTMENTS)

    fmap = FrenchMap_Regions()
    fmap.add('regions', aggregate_regions(datas))
    q = fmap.render_pyquery()
    assert len(q('#regions .region,#dom-com .region')) == len(REGIONS)

    assert aggregate_regions(datas.items()) == aggregate_regions(datas)
