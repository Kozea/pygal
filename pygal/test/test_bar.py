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

"""Bar chart related tests"""
from pygal import Bar


def test_simple_bar():
    """Simple bar test"""
    bar = Bar()
    rng = [-3, -32, -39]
    bar.add('test1', rng)
    bar.add('test2', map(abs, rng))
    bar.x_labels = map(str, rng)
    bar.title = "Bar test"
    q = bar.render_pyquery()
    assert len(q(".axis.x")) == 1
    assert len(q(".axis.y")) == 1
    assert len(q(".legend")) == 2
    assert len(q(".plot .series rect")) == 2 * 3


def test_difference():
    """Tests the difference between labeled graphs and unlabeled graphs"""
    bar = Bar(bar_values=False)
    rng = [-3, -32, -39]
    bar.add('test1', rng)
    bar.add('test2', map(abs, rng))
    bar.x_labels = map(str, rng)
    bar_labelled = Bar(bar_values=True)
    rng = [-3, -32, -39]
    bar_labelled.add('test1', rng)
    bar_labelled.add('test2', map(abs, rng))
    bar.labelled = map(str, rng)

    assert bar != bar_labelled


def test_bar_percent_difference():
    """Tests the difference between percent labeled graphs and unlabeled graphs"""
    bar = Bar()
    rng = [-3, -32, -39]
    bar.add('test1', rng)
    bar.add('test2', map(abs, rng))
    bar.x_labels = map(str, rng)

    barpercent = Bar(percent_values=True)
    rng = [-3, -32, -39]
    barpercent.add('test1', rng)
    barpercent.add('test2', map(abs, rng))
    barpercent.x_labels = map(str, rng)

    assert (bar != barpercent)


def test_chart_renders():
    """Tests that print values and percent values renders"""
    line_chart = Bar(print_values=True, percent_values=True, print_values_position='top')
    line_chart.title = 'Browser usage evolution (in %)'
    line_chart.x_labels = map(str, range(2002, 2013))
    line_chart.add('Firefox', [None, None, 0, 16.6, 25, 31, 36.4, 45.5, 46.3, 42.8, 37.1])
    line_chart.add('Chrome', [None, None, None, None, None, None, 0, 3.9, 10.8, 23.8, 35.3])
    line_chart.add('IE', [85.8, 84.6, 84.7, 74.5, 66, 58.6, 54.7, 44.8, 36.2, 26.6, 20.1])
    line_chart.add('Others', [14.2, 15.4, 15.3, 8.9, 9, 10.4, 8.9, 5.8, 6.7, 6.8, 7.5])
    assert line_chart.render()
