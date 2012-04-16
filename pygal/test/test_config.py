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
from pygal import Line, Dot, Pie, Radar
from pygal.test.utils import texts
from pygal.test import pytest_generate_tests, make_data


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


def test_logarithmic_bad_interpolation():
    try:
        import scipy
    except ImportError:
        return
    line = Line(logarithmic=True, interpolate='cubic')
    line.add('_', [.001, .00000001, 1])
    q = line.render_pyquery()
    assert len(q(".y.axis .guides")) == 40


def test_logarithmic_big_scale():
    line = Line(logarithmic=True)
    line.add('_', [10 ** -10, 10 ** 10, 1])
    q = line.render_pyquery()
    assert len(q(".y.axis .guides")) == 41


def test_logarithmic_small_scale():
    line = Line(logarithmic=True)
    line.add('_', [1 + 10 ** 10, 3 + 10 ** 10, 2 + 10 ** 10])
    q = line.render_pyquery()
    assert len(q(".y.axis .guides")) == 21


def test_human_readable():
    line = Line()
    line.add('_', [10 ** 4, 10 ** 5, 23 * 10 ** 4])
    # q = line.render_pyquery()
    # assert q(".axis.y text").map(texts) == map(
        # str, range(20000, 240000, 20000))
    line.human_readable = True
    q = line.render_pyquery()
    assert q(".axis.y text").map(texts) == map(
        lambda x: '%dk' % x, range(20, 240, 20))


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
    assert q("text").text() == "No data"
    line.no_data_text = u"þæ®þæ€€&ĳ¿’€"
    q = line.render_pyquery()
    assert q("text").text() == u"þæ®þæ€€&ĳ¿’€"
