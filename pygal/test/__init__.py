# -*- coding: utf-8 -*-
# This file is part of pygal
#
# A python svg graph plotting library
# Copyright © 2012 Kozea
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

import pygal
from pygal.util import cut


def get_data(i):
    return [
        [(-1, 1), (2, 0), (0, 4)],
        [(0, 1), (None, 2), (3, 2)],
        [(-3, 3), (1, 3), (1, 1)],
        [(1, 1), (1, 1), (1, 1)],
        [(3, 2), (2, 1), (1, 1)]][i]


def pytest_generate_tests(metafunc):
    if "Chart" in metafunc.funcargnames:
        metafunc.parametrize("Chart", pygal.CHARTS)
    if "datas" in metafunc.funcargnames:
        metafunc.parametrize(
            "datas",
            [
                [("Serie %d" % i, get_data(i)) for i in range(s)]
                for s in (5, 1, 0)
            ])


def make_data(chart, datas):
    for data in datas:
        chart.add(data[0],
                  data[1] if chart.__class__ == pygal.XY else cut(data[1]))
    return chart
