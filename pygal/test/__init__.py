# -*- coding: utf-8 -*-
# This file is part of pygal
#
# A python svg graph plotting library
# Copyright © 2012-2016 Kozea
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
"""Pygal test package"""

from decimal import Decimal

import pygal
from pygal.graph.map import BaseMap
from pygal.util import cut


def get_data(i):
    """Return sample test data for an index"""
    return [[(-1, 1), (2, 0), (0, 4)], [(0, 1), (None, 2), (3, 2)],
            [(-3, 3), (1, 3), (1, 1)], [(1, 1), (Decimal('1.'), 1),
                                        (1, 1)], [(3, 2), (2, 1), (1., 1)]][i]


def adapt(chart, data):
    """Adapt data to chart type"""
    if isinstance(chart, pygal.XY):
        return data

    data = cut(data)
    if isinstance(chart, BaseMap):
        return list(
            map(lambda x: chart.__class__.x_labels[
                int(x) % len(chart.__class__.x_labels)]
                if x is not None else None, data))
    return data


def make_data(chart, datas):
    """Add sample data to the test chart"""
    for i, data in enumerate(datas):
        chart.add(data[0], adapt(chart, data[1]), secondary=bool(i % 2))
    return chart
