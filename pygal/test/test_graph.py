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

import os
import pygal
import uuid
import sys
import pytest
from pygal import i18n
from pygal.graph.frenchmap import DEPARTMENTS, REGIONS
from pygal.util import cut
from pygal._compat import u
from pygal.test import make_data

try:
    import cairosvg
except ImportError:
    cairosvg = None


def test_multi_render(Chart, datas):
    chart = Chart()
    chart = make_data(chart, datas)
    chart.x_labels = (str(a) for a in 'labels')
    chart.y_labels = (str(a) for a in range(6))
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


@pytest.mark.skipif(not cairosvg, reason="CairoSVG not installed")
def test_render_to_png(Chart, datas):
    file_name = '/tmp/test_graph-%s.png' % uuid.uuid4()
    if os.path.exists(file_name):
        os.remove(file_name)

    chart = Chart()
    chart = make_data(chart, datas)
    chart.render_to_png(file_name)
    png = chart._repr_png_()

    with open(file_name, 'rb') as f:
        assert png == f.read()
    os.remove(file_name)


def test_metadata(Chart):
    chart = Chart()
    v = range(7)
    if Chart in (pygal.Box,):
        return  # summary charts cannot display per-value metadata
    elif Chart == pygal.XY:
        v = list(map(lambda x: (x, x + 1), v))
    elif Chart == pygal.Worldmap or Chart == pygal.SupranationalWorldmap:
        v = [(i, k) for k, i in enumerate(i18n.COUNTRIES.keys())]
    elif Chart == pygal.FrenchMap_Regions:
        v = [(i, k) for k, i in enumerate(REGIONS.keys())]
    elif Chart == pygal.FrenchMap_Departments:
        v = [(i, k) for k, i in enumerate(DEPARTMENTS.keys())]

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

    if Chart in (pygal.Pie, pygal.Treemap):
        # Slices with value 0 are not rendered
        assert len(v) - 1 == len(q('.tooltip-trigger').siblings('.value'))
    elif Chart not in (
            pygal.Worldmap, pygal.SupranationalWorldmap,
            pygal.FrenchMap_Regions, pygal.FrenchMap_Departments):
        # Tooltip are not working on maps
        assert len(v) == len(q('.tooltip-trigger').siblings('.value'))


def test_empty_lists(Chart):
    chart = Chart()
    chart.add('A', [1, 2])
    chart.add('B', [])
    chart.x_labels = ('red', 'green', 'blue')
    q = chart.render_pyquery()
    assert len(q(".legend")) == 2


def test_empty_lists_with_nones(Chart):
    chart = Chart()
    chart.add('A', [None, None])
    chart.add('B', [None, 4, 4])
    chart.x_labels = ('red', 'green', 'blue')
    q = chart.render_pyquery()
    assert len(q(".legend")) == 2


def test_only_one_value(Chart):
    chart = Chart()
    chart.add('S', [1])
    chart.x_labels = ('single')
    q = chart.render_pyquery()
    assert len(q(".legend")) == 1


def test_only_one_value_log(Chart):
    chart = Chart(logarithmic=True)
    chart.add('S', [1])
    chart.x_labels = ('single')
    q = chart.render_pyquery()
    assert len(q(".legend")) == 1


def test_only_one_value_intrp(Chart):
    chart = Chart(interpolate='cubic')
    chart.add('S', [1])
    chart.x_labels = ('single')
    q = chart.render_pyquery()
    assert len(q(".legend")) == 1


def test_non_iterable_value(Chart):
    chart = Chart(no_prefix=True)
    chart.add('A', 1)
    chart.add('B', 2)
    chart.x_labels = ('red', 'green', 'blue')
    chart1 = chart.render()
    chart = Chart(no_prefix=True)
    chart.add('A', [1])
    chart.add('B', [2])
    chart.x_labels = ('red', 'green', 'blue')
    chart2 = chart.render()
    assert chart1 == chart2


def test_iterable_types(Chart):
    chart = Chart(no_prefix=True)
    chart.add('A', [1, 2])
    chart.add('B', [])
    chart.x_labels = ('red', 'green', 'blue')
    chart1 = chart.render()

    chart = Chart(no_prefix=True)
    chart.add('A', (1, 2))
    chart.add('B', tuple())
    chart.x_labels = ('red', 'green', 'blue')
    chart2 = chart.render()
    assert chart1 == chart2


def test_values_by_dict(Chart):
    chart1 = Chart(no_prefix=True)
    chart2 = Chart(no_prefix=True)

    if not issubclass(Chart, (
            pygal.Worldmap,
            pygal.FrenchMap_Departments,
            pygal.FrenchMap_Regions)):
        chart1.add('A', {'red': 10, 'green': 12, 'blue': 14})
        chart1.add('B', {'green': 11, 'red': 7})
        chart1.add('C', {'blue': 7})
        chart1.add('D', {})
        chart1.add('E', {'blue': 2, 'red': 13})
        chart1.x_labels = ('red', 'green', 'blue')

        chart2.add('A', [10, 12, 14])
        chart2.add('B', [7, 11])
        chart2.add('C', [None, None, 7])
        chart2.add('D', [])
        chart2.add('E', [13, None, 2])
        chart2.x_labels = ('red', 'green', 'blue')
    else:
        chart1.add('A', {'fr': 10, 'us': 12, 'jp': 14})
        chart1.add('B', {'cn': 99})
        chart1.add('C', {})

        chart2.add('A', [('fr', 10), ('us', 12), ('jp', 14)])
        chart2.add('B', [('cn', 99)])
        chart2.add('C', [None, (None, None)])

    assert chart1.render() == chart2.render()


def test_no_data_with_no_values(Chart):
    chart = Chart()
    q = chart.render_pyquery()
    assert q(".text-overlay text").text() == "No data"


def test_no_data_with_no_values_with_include_x_axis(Chart):
    chart = Chart(include_x_axis=True)
    q = chart.render_pyquery()
    assert q(".text-overlay text").text() == "No data"


def test_no_data_with_empty_serie(Chart):
    chart = Chart()
    chart.add('Serie', [])
    q = chart.render_pyquery()
    assert q(".text-overlay text").text() == "No data"


def test_no_data_with_empty_series(Chart):
    chart = Chart()
    chart.add('Serie1', [])
    chart.add('Serie2', [])
    q = chart.render_pyquery()
    assert q(".text-overlay text").text() == "No data"


def test_no_data_with_none(Chart):
    chart = Chart()
    chart.add('Serie', None)
    q = chart.render_pyquery()
    assert q(".text-overlay text").text() == "No data"


def test_no_data_with_list_of_none(Chart):
    chart = Chart()
    chart.add('Serie', [None])
    q = chart.render_pyquery()
    assert q(".text-overlay text").text() == "No data"


def test_no_data_with_lists_of_nones(Chart):
    chart = Chart()
    chart.add('Serie1', [None, None, None, None])
    chart.add('Serie2', [None, None, None])
    q = chart.render_pyquery()
    assert q(".text-overlay text").text() == "No data"


def test_unicode_labels_decode(Chart):
    chart = Chart()
    chart.add(u('Série1'), [{
        'value': 1,
        'xlink': 'http://1/',
        'label': u('{\}Â°ĳæð©&×&<—×€¿_…\{_…')
    }, {
        'value': 2,
        'xlink': {
            'href': 'http://6.example.com/'
        },
        'label': u('æÂ°€≠|€æÂ°€əæ')
    }, {
        'value': 3,
        'label': 'unicode <3'
    }])
    chart.x_labels = [u('&œ'), u('¿?'), u('††††††††'), 'unicode <3']
    chart.render_pyquery()


def test_unicode_labels_python2(Chart):
    if sys.version_info[0] == 3:
        return
    chart = Chart()
    chart.add(u('Série1'), [{
        'value': 1,
        'xlink': 'http://1/',
        'label': eval("u'{\}Â°ĳæð©&×&<—×€¿_…\{_…'")
    }, {
        'value': 2,
        'xlink': {
            'href': 'http://6.example.com/'
        },
        'label': eval("u'æÂ°€≠|€æÂ°€əæ'")
    }, {
        'value': 3,
        'label': eval("'unicode <3'")
    }])
    chart.x_labels = eval("[u'&œ', u'¿?', u'††††††††', 'unicode <3']")
    chart.render_pyquery()


def test_unicode_labels_python3(Chart):
    if sys.version_info[0] == 2:
        return
    chart = Chart()
    chart.add(u('Série1'), [{
        'value': 1,
        'xlink': 'http://1/',
        'label': eval("'{\}Â°ĳæð©&×&<—×€¿_…\{_…'")
    }, {
        'value': 2,
        'xlink': {
            'href': 'http://6.example.com/'
        },
        'label': eval("'æÂ°€≠|€æÂ°€əæ'")
    }, {
        'value': 3,
        'label': eval("b'unicode <3'")
    }])
    chart.x_labels = eval("['&œ', '¿?', '††††††††', 'unicode <3']")
    chart.render_pyquery()


def test_labels_with_links(Chart):
    chart = Chart()
    # link on chart and label
    chart.add({
        'title': 'Red', 'xlink': {'href': 'http://en.wikipedia.org/wiki/Red'}
    }, [{
        'value': 2,
        'label': 'This is red',
        'xlink': {'href': 'http://en.wikipedia.org/wiki/Red'}}])

    # link on chart only
    chart.add('Green', [{
        'value': 4,
        'label': 'This is green',
        'xlink': {
            'href': 'http://en.wikipedia.org/wiki/Green',
            'target': '_top'}}])

    # link on label only opens in new tab
    chart.add({'title': 'Yellow', 'xlink': {
        'href': 'http://en.wikipedia.org/wiki/Yellow',
        'target': '_blank'}}, 7)

    # link on chart only
    chart.add('Blue', [{
        'value': 5,
        'xlink': {
            'href': 'http://en.wikipedia.org/wiki/Blue',
            'target': '_blank'}}])

    # link on label and chart with diffrent behaviours
    chart.add({
        'title': 'Violet',
        'xlink': 'http://en.wikipedia.org/wiki/Violet_(color)'
    }, [{
        'value': 3,
        'label': 'This is violet',
        'xlink': {
            'href': 'http://en.wikipedia.org/wiki/Violet_(color)',
            'target': '_self'}}])

    q = chart.render_pyquery()
    links = q('a')

    if issubclass(chart.cls,
                  (pygal.graph.worldmap.Worldmap,
                   pygal.graph.frenchmap.FrenchMapDepartments)):
        # No country is found in this case so:
        assert len(links) == 4  # 3 links and 1 tooltip
    else:
        assert len(links) == 8  # 7 links and 1 tooltip


def test_sparkline(Chart, datas):
    chart = Chart()
    chart = make_data(chart, datas)
    assert chart.render_sparkline()


def test_secondary(Chart):
    chart = Chart()
    rng = [83, .12, -34, 59]
    chart.add('First serie', rng)
    chart.add('Secondary serie',
              map(lambda x: x * 2, rng),
              secondary=True)
    assert chart.render_pyquery()


def test_ipython_notebook(Chart, datas):
    chart = Chart()
    chart = make_data(chart, datas)
    assert chart._repr_svg_()


def test_long_title(Chart, datas):
    chart = Chart(
        title="A chart is a graphical representation of data, in which "
        "'the data is represented by symbols, such as bars in a bar chart, "
        "lines in a line chart, or slices in a pie chart'. A chart can "
        "represent tabular numeric data, functions or some kinds of "
        "qualitative structure and provides different info.")
    chart = make_data(chart, datas)
    q = chart.render_pyquery()
    assert len(q('.titles text')) == 5
