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
"""Generate tests for different chart types with different data"""

import io
import os
import sys
import uuid

import pytest

import pygal
from pygal._compat import u
from pygal.graph.map import BaseMap
from pygal.test import make_data
from pygal.util import cut

try:
    import cairosvg
except ImportError:
    cairosvg = None


def test_multi_render(Chart, datas):
    """Check that a chart always render the same"""
    chart = Chart()
    chart = make_data(chart, datas)
    svg = chart.render()
    for i in range(2):
        assert svg == chart.render()


def test_render_to_file(Chart, datas):
    """Test in file rendering"""
    file_name = '/tmp/test_graph-%s.svg' % uuid.uuid4()
    if os.path.exists(file_name):
        os.remove(file_name)

    chart = Chart()
    chart = make_data(chart, datas)
    chart.render_to_file(file_name)
    with io.open(file_name, encoding="utf-8") as f:
        assert 'pygal' in f.read()
    os.remove(file_name)


@pytest.mark.skipif(not cairosvg, reason="CairoSVG not installed")
def test_render_to_png(Chart, datas):
    """Test in file png rendering"""
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
    """Test metadata values"""
    chart = Chart()
    v = range(7)
    if Chart in (pygal.Box, ):
        return  # summary charts cannot display per-value metadata
    elif Chart == pygal.XY:
        v = list(map(lambda x: (x, x + 1), v))
    elif issubclass(Chart, BaseMap):
        v = [(k, i) for i, k in enumerate(Chart.x_labels)
             if k not in ['oecd', 'nafta', 'eur']]

    chart.add(
        'Serie with metadata', [
            v[0], {
                'value': v[1]
            }, {
                'value': v[2],
                'label': 'Three'
            }, {
                'value': v[3],
                'xlink': 'http://4.example.com/'
            }, {
                'value': v[4],
                'xlink': 'http://5.example.com/',
                'label': 'Five'
            }, {
                'value': v[5],
                'xlink': {
                    'href': 'http://6.example.com/'
                },
                'label': 'Six'
            }, {
                'value': v[6],
                'xlink': {
                    'href': 'http://7.example.com/',
                    'target': '_blank'
                },
                'label': 'Seven'
            }
        ]
    )
    q = chart.render_pyquery()
    for md in ('Three', 'Five', 'Seven'):
        assert md in cut(q('desc'), 'text')

    for md in ('http://7.example.com/', 'http://4.example.com/'):
        assert md in [e.attrib.get('xlink:href') for e in q('a')]

    if Chart in (pygal.Pie, pygal.Treemap, pygal.SolidGauge):
        # Slices with value 0 are not rendered
        assert len(v) - 1 == len(q('.tooltip-trigger').siblings('.value'))
    elif not issubclass(Chart, BaseMap):

        # Tooltip are not working on maps
        assert len(v) == len(q('.tooltip-trigger').siblings('.value'))


def test_empty_lists(Chart):
    """Test chart rendering with an empty serie"""
    chart = Chart()
    chart.add('A', [1, 2])
    chart.add('B', [])
    if not chart._dual:
        chart.x_labels = ('red', 'green', 'blue')
    q = chart.render_pyquery()
    assert len(q(".legend")) == 2


def test_empty_lists_with_nones(Chart):
    """Test chart rendering with a None filled serie"""
    chart = Chart()
    chart.add('A', [None, None])
    chart.add('B', [None, 4, 4])
    q = chart.render_pyquery()
    assert len(q(".legend")) == 2


def test_only_one_value(Chart):
    """Test chart rendering with only one value"""
    chart = Chart()
    chart.add('S', [1])
    q = chart.render_pyquery()
    assert len(q(".legend")) == 1


def test_only_one_value_log(Chart):
    """Test logarithmic chart rendering with only one value"""
    chart = Chart(logarithmic=True)
    chart.add('S', [1])
    if not chart._dual:
        chart.x_labels = ('single')
    q = chart.render_pyquery()
    assert len(q(".legend")) == 1


def test_only_one_value_intrp(Chart):
    """Test interpolated chart rendering with only one value"""
    chart = Chart(interpolate='cubic')
    chart.add('S', [1])
    q = chart.render_pyquery()
    assert len(q(".legend")) == 1


def test_non_iterable_value(Chart):
    """Test serie as non iterable"""
    chart = Chart(no_prefix=True)
    chart.add('A', 1)
    chart.add('B', 2)
    if not chart._dual:
        chart.x_labels = ('red', 'green', 'blue')
    chart1 = chart.render()
    chart = Chart(no_prefix=True)
    chart.add('A', [1])
    chart.add('B', [2])
    if not chart._dual:
        chart.x_labels = ('red', 'green', 'blue')
    chart2 = chart.render()
    assert chart1 == chart2


def test_iterable_types(Chart):
    """Test serie as various iterable"""
    chart = Chart(no_prefix=True)
    chart.add('A', [1, 2])
    chart.add('B', [])
    if not chart._dual:
        chart.x_labels = ('red', 'green', 'blue')
    chart1 = chart.render()

    chart = Chart(no_prefix=True)
    chart.add('A', (1, 2))
    chart.add('B', tuple())
    if not chart._dual:
        chart.x_labels = ('red', 'green', 'blue')
    chart2 = chart.render()
    assert chart1 == chart2


def test_values_by_dict(Chart):
    """Test serie as dict"""
    chart1 = Chart(no_prefix=True)
    chart2 = Chart(no_prefix=True)

    if not issubclass(Chart, BaseMap) and not Chart._dual:
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
    elif not Chart._dual:
        chart1.add('A', {'fr': 10, 'us': 12, 'jp': 14})
        chart1.add('B', {'cn': 99})
        chart1.add('C', {})

        chart2.add('A', [('fr', 10), ('us', 12), ('jp', 14)])
        chart2.add('B', [('cn', 99)])
        chart2.add('C', [None, (None, None)])

    assert chart1.render() == chart2.render()


def test_no_data_with_no_values(Chart):
    """Test no data"""
    chart = Chart()
    q = chart.render_pyquery()
    assert q(".text-overlay text").text() == "No data"


def test_no_data_with_no_values_with_include_x_axis(Chart):
    """Test no data and include_x_axis"""
    chart = Chart(include_x_axis=True)
    q = chart.render_pyquery()
    assert q(".text-overlay text").text() == "No data"


def test_no_data_with_empty_serie(Chart):
    """Test no data for empty serie"""
    chart = Chart()
    chart.add('Serie', [])
    q = chart.render_pyquery()
    assert q(".text-overlay text").text() == "No data"


def test_no_data_with_empty_series(Chart):
    """Test no data for 2 empty series"""
    chart = Chart()
    chart.add('Serie1', [])
    chart.add('Serie2', [])
    q = chart.render_pyquery()
    assert q(".text-overlay text").text() == "No data"


def test_no_data_with_none(Chart):
    """Test no data for a None containing serie"""
    chart = Chart()
    chart.add('Serie', None)
    q = chart.render_pyquery()
    assert q(".text-overlay text").text() == "No data"


def test_no_data_with_list_of_none(Chart):
    """Test no data for a None containing serie"""
    chart = Chart()
    chart.add('Serie', [None])
    q = chart.render_pyquery()
    assert q(".text-overlay text").text() == "No data"


def test_no_data_with_lists_of_nones(Chart):
    """Test no data for several None containing series"""
    chart = Chart()
    chart.add('Serie1', [None, None, None, None])
    chart.add('Serie2', [None, None, None])
    q = chart.render_pyquery()
    assert q(".text-overlay text").text() == "No data"


def test_unicode_labels_decode(Chart):
    """Test unicode labels"""
    chart = Chart()
    chart.add(
        u('Série1'), [{
            'value': 1,
            'xlink': 'http://1/',
            'label': u('Â°ĳæð©&×&<—×€¿_…')
        }, {
            'value': 2,
            'xlink': {
                'href': 'http://6.example.com/'
            },
            'label': u('æÂ°€≠|€æÂ°€əæ')
        }, {
            'value': 3,
            'label': 'unicode <3'
        }]
    )
    if not chart._dual:
        chart.x_labels = [u('&œ'), u('¿?'), u('††††††††'), 'unicode <3']
    chart.render_pyquery()


def test_unicode_labels_python2(Chart):
    """Test unicode labels in python 2"""
    if sys.version_info[0] == 3:
        return
    chart = Chart()
    chart.add(
        u('Série1'), [{
            'value': 1,
            'xlink': 'http://1/',
            'label': eval("u'Â°ĳæð©&×&<—×€¿_…'")
        }, {
            'value': 2,
            'xlink': {
                'href': 'http://6.example.com/'
            },
            'label': eval("u'æÂ°€≠|€æÂ°€əæ'")
        }, {
            'value': 3,
            'label': eval("'unicode <3'")
        }]
    )
    if not chart._dual:
        chart.x_labels = eval("[u'&œ', u'¿?', u'††††††††', 'unicode <3']")
    chart.render_pyquery()


def test_unicode_labels_python3(Chart):
    """Test unicode labels in python 3"""
    if sys.version_info[0] == 2:
        return
    chart = Chart()
    chart.add(
        u('Série1'), [{
            'value': 1,
            'xlink': 'http://1/',
            'label': eval("'Â°ĳæð©&×&<—×€¿_…'")
        }, {
            'value': 2,
            'xlink': {
                'href': 'http://6.example.com/'
            },
            'label': eval("'æÂ°€≠|€æÂ°€əæ'")
        }, {
            'value': 3,
            'label': eval("b'unicode <3'")
        }]
    )
    if not chart._dual:
        chart.x_labels = eval("['&œ', '¿?', '††††††††', 'unicode <3']")
    chart.render_pyquery()


def test_labels_with_links(Chart):
    """Test values with links"""
    chart = Chart()
    # link on chart and label
    chart.add({
        'title': 'Red',
        'xlink': {
            'href': 'http://en.wikipedia.org/wiki/Red'
        }
    }, [{
        'value': 2,
        'label': 'This is red',
        'xlink': {
            'href': 'http://en.wikipedia.org/wiki/Red'
        }
    }])

    # link on chart only
    chart.add(
        'Green', [{
            'value': 4,
            'label': 'This is green',
            'xlink': {
                'href': 'http://en.wikipedia.org/wiki/Green',
                'target': '_top'
            }
        }]
    )

    # link on label only opens in new tab
    chart.add({
        'title': 'Yellow',
        'xlink': {
            'href': 'http://en.wikipedia.org/wiki/Yellow',
            'target': '_blank'
        }
    }, 7)

    # link on chart only
    chart.add(
        'Blue', [{
            'value': 5,
            'xlink': {
                'href': 'http://en.wikipedia.org/wiki/Blue',
                'target': '_blank'
            }
        }]
    )

    # link on label and chart with diffrent behaviours
    chart.add({
        'title': 'Violet',
        'xlink': 'http://en.wikipedia.org/wiki/Violet_(color)'
    }, [{
        'value': 3,
        'label': 'This is violet',
        'xlink': {
            'href': 'http://en.wikipedia.org/wiki/Violet_(color)',
            'target': '_self'
        }
    }])

    q = chart.render_pyquery()
    links = q('a')

    assert len(links) == 7 or isinstance(chart, BaseMap) and len(links) == 3


def test_sparkline(Chart, datas):
    """Test sparkline"""
    chart = Chart()
    chart = make_data(chart, datas)
    assert chart.render_sparkline()


def test_secondary(Chart):
    """Test secondary chart"""
    chart = Chart()
    rng = [83, .12, -34, 59]
    chart.add('First serie', rng)
    chart.add('Secondary serie', map(lambda x: x * 2, rng), secondary=True)
    assert chart.render_pyquery()


def test_ipython_notebook(Chart, datas):
    """Test ipython notebook"""
    chart = Chart()
    chart = make_data(chart, datas)
    assert chart._repr_svg_()


def test_long_title(Chart, datas):
    """Test chart rendering with a long title"""
    chart = Chart(
        title="A chart is a graphical representation of data, in which "
        "'the data is represented by symbols, such as bars in a bar chart, "
        "lines in a line chart, or slices in a pie chart'. A chart can "
        "represent tabular numeric data, functions or some kinds of "
        "qualitative structure and provides different info."
    )
    chart = make_data(chart, datas)
    q = chart.render_pyquery()
    assert len(q('.titles text')) == 5
