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
import pygal
import uuid
from pygal.util import cut
from pygal.test import pytest_generate_tests, make_data


def test_multi_render(Chart, datas):
    chart = Chart()
    chart = make_data(chart, datas)
    svg = chart.render()
    for i in range(2):
        assert svg == chart.render()


def test_render_to_file(Chart, datas):
    file_name = '/tmp/test_graph-%s.svg' % uuid.uuid4()
    if os.path.exists(file_name):
        os.remove(file_name)

    chart = Chart()
    chart = make_data(chart, datas)
    chart.render_to_file(file_name)
    with open(file_name) as f:
        assert 'pygal' in f.read()
    os.remove(file_name)


def test_render_to_png(Chart, datas):
    try:
        import cairosvg
    except ImportError:
        return

    file_name = '/tmp/test_graph-%s.png' % uuid.uuid4()
    if os.path.exists(file_name):
        os.remove(file_name)

    chart = Chart()
    chart = make_data(chart, datas)
    chart.render_to_png(file_name)
    with open(file_name, 'rb') as f:
        assert f.read()
    os.remove(file_name)


def test_metadata(Chart):
    chart = Chart()
    v = range(7)
    if Chart == pygal.XY:
        v = map(lambda x: (x, x + 1), v)

    chart.add('Serie with metadata', [
        v[0],
        {'value': v[1]},
        {'value': v[2], 'label': 'Three'},
        {'value': v[3], 'xlink': 'http://4.example.com/'},
        {'value': v[4], 'xlink': 'http://5.example.com/', 'label': 'Five'},
        {'value': v[5], 'xlink': {
            'href': 'http://6.example.com/'}, 'label': 'Six'},
        {'value': v[6], 'xlink': {
            'href': 'http://7.example.com/',
            'target': '_blank'}, 'label': 'Seven'}
    ])
    q = chart.render_pyquery()
    for md in (
            'Three', 'http://4.example.com/',
            'Five', 'http://7.example.com/', 'Seven'):
        assert md in cut(q('desc'), 'text')


def test_empty_lists(Chart):
    chart = Chart()
    chart.add('A', [1, 2])
    chart.add('B', [])
    chart.x_labels = ('red', 'green', 'blue')
    q = chart.render_pyquery()
    assert len(q(".legend")) == 2

    chart = Chart()
    chart.add('A', [None, None])
    chart.add('B', [None, 4, 4])
    chart.x_labels = ('red', 'green', 'blue')
    q = chart.render_pyquery()
    assert len(q(".legend")) == 2


def test_non_iterable_value(Chart):
    chart = Chart()
    chart.add('A', 1)
    chart.add('B', 2)
    chart.x_labels = ('red', 'green', 'blue')
    chart1 = chart.render()
    chart = Chart()
    chart.add('A', [1])
    chart.add('B', [2])
    chart.x_labels = ('red', 'green', 'blue')
    chart2 = chart.render()
    assert chart1 == chart2


def test_iterable_types(Chart):
    chart = Chart()
    chart.add('A', [1, 2])
    chart.add('B', [])
    chart.x_labels = ('red', 'green', 'blue')
    chart1 = chart.render()

    chart = Chart()
    chart.add('A', (1, 2))
    chart.add('B', tuple())
    chart.x_labels = ('red', 'green', 'blue')
    chart2 = chart.render()
    assert chart1 == chart2


def test_values_by_dict(Chart):
    chart = Chart()
    chart.add('A', {'red': 10, 'green': 12, 'blue': 14})
    chart.add('B', {'green': 11, 'red': 7})
    chart.add('C', {'blue': 7})
    chart.add('D', {})
    chart.add('E', {'blue': 2, 'red': 13})
    chart.x_labels = ('red', 'green', 'blue')
    chart1 = chart.render()

    chart = Chart()
    chart.add('A', [10, 12, 14])
    chart.add('B', [7, 11])
    chart.add('C', [None, None, 7])
    chart.add('D', [])
    chart.add('E', [13, None, 2])
    chart.x_labels = ('red', 'green', 'blue')
    chart2 = chart.render()
    assert chart1 == chart2
