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
    Line, Dot, Pie, Radar, Config, Bar, Funnel, Worldmap,
    SupranationalWorldmap, Histogram, Gauge, Box,
    FrenchMap_Regions, FrenchMap_Departments)
from pygal._compat import u
from pygal.test.utils import texts
from pygal.test import pytest_generate_tests, make_data
from uuid import uuid4


def test_config_behaviours():
    line1 = Line()
    line1.show_legend = False
    line1.fill = True
    line1.pretty_print = True
    line1.no_prefix = True
    line1.x_labels = ['a', 'b', 'c']
    line1.add('_', [1, 2, 3])
    l1 = line1.render()

    q = line1.render_pyquery()
    assert len(q(".axis.x")) == 1
    assert len(q(".axis.y")) == 1
    assert len(q(".plot .series path")) == 1
    assert len(q(".legend")) == 0
    assert len(q(".x.axis .guides")) == 3
    assert len(q(".y.axis .guides")) == 21
    assert len(q(".dots")) == 3
    assert q(".axis.x text").map(texts) == ['a', 'b', 'c']

    line2 = Line(
        show_legend=False,
        fill=True,
        pretty_print=True,
        no_prefix=True,
        x_labels=['a', 'b', 'c'])
    line2.add('_', [1, 2, 3])
    l2 = line2.render()
    assert l1 == l2

    class LineConfig(Config):
        show_legend = False
        fill = True
        pretty_print = True
        no_prefix = True
        x_labels = ['a', 'b', 'c']

    line3 = Line(LineConfig)
    line3.add('_', [1, 2, 3])
    l3 = line3.render()
    assert l1 == l3

    line4 = Line(LineConfig())
    line4.add('_', [1, 2, 3])
    l4 = line4.render()
    assert l1 == l4

    line_config = Config()
    line_config.show_legend = False
    line_config.fill = True
    line_config.pretty_print = True
    line_config.no_prefix = True
    line_config.x_labels = ['a', 'b', 'c']

    line5 = Line(line_config)
    line5.add('_', [1, 2, 3])
    l5 = line5.render()
    assert l1 == l5


def test_config_alterations_class():
    class LineConfig(Config):
        no_prefix = True
        show_legend = False
        fill = True
        pretty_print = True
        x_labels = ['a', 'b', 'c']

    line1 = Line(LineConfig)
    line1.add('_', [1, 2, 3])
    l1 = line1.render()

    LineConfig.stroke = False
    line2 = Line(LineConfig)
    line2.add('_', [1, 2, 3])
    l2 = line2.render()
    assert l1 != l2

    l1bis = line1.render()
    assert l1 == l1bis


def test_config_alterations_instance():
    class LineConfig(Config):
        no_prefix = True
        show_legend = False
        fill = True
        pretty_print = True
        x_labels = ['a', 'b', 'c']

    config = LineConfig()
    line1 = Line(config)
    line1.add('_', [1, 2, 3])
    l1 = line1.render()

    config.stroke = False
    line2 = Line(config)
    line2.add('_', [1, 2, 3])
    l2 = line2.render()
    assert l1 != l2

    l1bis = line1.render()
    assert l1 == l1bis


def test_config_alterations_kwargs():
    class LineConfig(Config):
        no_prefix = True
        show_legend = False
        fill = True
        pretty_print = True
        x_labels = ['a', 'b', 'c']

    config = LineConfig()

    line1 = Line(config)
    line1.add('_', [1, 2, 3])
    l1 = line1.render()

    line1.stroke = False
    l1bis = line1.render()
    assert l1 != l1bis

    line2 = Line(config)
    line2.add('_', [1, 2, 3])
    l2 = line2.render()
    assert l1 == l2
    assert l1bis != l2

    line3 = Line(config, title='Title')
    line3.add('_', [1, 2, 3])
    l3 = line3.render()
    assert l3 != l2

    l2bis = line2.render()
    assert l2 == l2bis


def test_logarithmic():
    line = Line(logarithmic=True)
    line.add('_', [1, 10 ** 10, 1])
    q = line.render_pyquery()
    assert len(q(".axis.x")) == 0
    assert len(q(".axis.y")) == 1
    assert len(q(".plot .series path")) == 1
    assert len(q(".legend")) == 1
    assert len(q(".x.axis .guides")) == 0
    assert len(q(".y.axis .guides")) == 51
    assert len(q(".dots")) == 3


def test_interpolation(Chart):
    chart = Chart(interpolate='cubic')
    chart.add('1', [1, 3, 12, 3, 4])
    chart.add('2', [7, -4, 10, None, 8, 3, 1])
    q = chart.render_pyquery()
    assert len(q(".legend")) == 2


def test_no_data_interpolation(Chart):
    chart = Chart(interpolate='cubic')
    q = chart.render_pyquery()
    assert q(".text-overlay text").text() == "No data"


def test_no_data_with_empty_serie_interpolation(Chart):
    chart = Chart(interpolate='cubic')
    chart.add('Serie', [])
    q = chart.render_pyquery()
    assert q(".text-overlay text").text() == "No data"


def test_logarithmic_bad_interpolation():
    line = Line(logarithmic=True, interpolate='cubic')
    line.add('_', [.001, .00000001, 1])
    q = line.render_pyquery()
    assert len(q(".y.axis .guides")) == 41


def test_logarithmic_big_scale():
    line = Line(logarithmic=True)
    line.add('_', [10 ** -10, 10 ** 10, 1])
    q = line.render_pyquery()
    assert len(q(".y.axis .guides")) == 41


def test_value_formatter():
    line = Line(value_formatter=lambda x: str(x) + u('‰'))
    line.add('_', [10 ** 4, 10 ** 5, 23 * 10 ** 4])
    q = line.render_pyquery()
    assert len(q(".y.axis .guides")) == 11
    assert q(".axis.y text").map(texts) == list(map(
        lambda x: str(x) + u('‰'), map(float, range(20000, 240000, 20000))))


def test_logarithmic_small_scale():
    line = Line(logarithmic=True)
    line.add('_', [1 + 10 ** 10, 3 + 10 ** 10, 2 + 10 ** 10])
    q = line.render_pyquery()
    assert len(q(".y.axis .guides")) == 21


def test_human_readable():
    line = Line()
    line.add('_', [10 ** 4, 10 ** 5, 23 * 10 ** 4])
    q = line.render_pyquery()
    assert q(".axis.y text").map(texts) == list(map(
        str, map(float, range(20000, 240000, 20000))))
    line.human_readable = True
    q = line.render_pyquery()
    assert q(".axis.y text").map(texts) == list(map(
        lambda x: '%dk' % x, range(20, 240, 20)))


def test_show_legend():
    line = Line()
    line.add('_', [1, 2, 3])
    q = line.render_pyquery()
    assert len(q(".legend")) == 1
    line.show_legend = False
    q = line.render_pyquery()
    assert len(q(".legend")) == 0


def test_show_dots():
    line = Line()
    line.add('_', [1, 2, 3])
    q = line.render_pyquery()
    assert len(q(".dots")) == 3
    line.show_dots = False
    q = line.render_pyquery()
    assert len(q(".dots")) == 0


def test_no_data():
    line = Line()
    q = line.render_pyquery()
    assert q(".text-overlay text").text() == "No data"
    line.no_data_text = u("þæ®þæ€€&ĳ¿’€")
    q = line.render_pyquery()
    assert q(".text-overlay text").text() == u("þæ®þæ€€&ĳ¿’€")


def test_include_x_axis(Chart):
    chart = Chart()
    if Chart in (Pie, Radar, Funnel, Dot, Gauge, Worldmap,
                 SupranationalWorldmap, Histogram, Box,
                 FrenchMap_Regions, FrenchMap_Departments):
        return
    if not chart.cls._dual:
        data = 100, 200, 150
    else:
        data = (1, 100), (3, 200), (2, 150)
    chart.add('_', data)
    q = chart.render_pyquery()
    # Ghost thing
    yaxis = ".axis.%s .guides text" % (
        'y' if not chart._last__inst.horizontal else 'x')
    if not issubclass(chart.cls, Bar().cls):
        assert '0.0' not in q(yaxis).map(texts)
    else:
        assert '0.0' in q(yaxis).map(texts)
    chart.include_x_axis = True
    q = chart.render_pyquery()
    assert '0.0' in q(yaxis).map(texts)


def test_css(Chart):
    css = "{{ id }}text { fill: #bedead; }\n"
    css_file = '/tmp/pygal_custom_style-%s.css' % uuid4()
    with open(css_file, 'w') as f:
        f.write(css)

    config = Config()
    config.css.append(css_file)

    chart = Chart(config)
    chart.add('/', [10, 1, 5])
    svg = chart.render().decode('utf-8')
    assert '#bedead' in svg


def test_inline_css(Chart):
    css = "{{ id }}text { fill: #bedead; }\n"

    config = Config()
    config.css.append('inline:' + css)
    chart = Chart(config)
    chart.add('/', [10, 1, 5])
    svg = chart.render().decode('utf-8')
    assert '#bedead' in svg


def test_meta_config():
    from pygal.config import CONFIG_ITEMS
    assert all(c.name != 'Unbound' for c in CONFIG_ITEMS)
