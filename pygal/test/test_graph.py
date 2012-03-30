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
import os
from pygal import Line
import pygal


def test_multi_render():
    for Chart in pygal.CHARTS:
        chart = Chart()
        rng = range(20)
        if Chart == pygal.XY:
            rng = zip(rng, rng)
        chart.add('Serie', rng)
        chart.add('Serie 2', list(reversed(rng)))
        svg = chart.render()
        for i in range(2):
            assert svg == chart.render()


def test_render_to_file():
    file_name = '/tmp/test_graph.svg'
    if os.path.exists(file_name):
        os.remove(file_name)

    line = Line()
    line.add('Serie 1', [1])
    line.render_to_file(file_name)
    with open(file_name) as f:
        assert 'pygal' in f.read()
    os.remove(file_name)


def test_render_to_png():
    try:
        import cairosvg
    except ImportError:
        return

    file_name = '/tmp/test_graph.png'
    if os.path.exists(file_name):
        os.remove(file_name)

    line = Line()
    line.add('Serie 1', [1])
    line.render_to_png(file_name)
    with open(file_name) as f:
        assert f.read()
    os.remove(file_name)
