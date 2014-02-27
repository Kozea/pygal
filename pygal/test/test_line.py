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
from __future__ import division
from pygal import Line
from pygal.test.utils import texts
from math import cos, sin


def test_simple_line():
    line = Line()
    rng = range(-30, 31, 5)
    line.add('test1', [cos(x / 10) for x in rng])
    line.add('test2', [sin(x / 10) for x in rng])
    line.add('test3', [cos(x / 10) - sin(x / 10) for x in rng])
    line.x_labels = map(str, rng)
    line.title = "cos sin and cos - sin"
    q = line.render_pyquery()
    assert len(q(".axis.x")) == 1
    assert len(q(".axis.y")) == 1
    assert len(q(".plot .series path")) == 3
    assert len(q(".legend")) == 3
    assert len(q(".x.axis .guides")) == 13
    assert len(q(".y.axis .guides")) == 13
    assert len(q(".dots")) == 3 * 13
    assert q(".axis.x text").map(texts) == [
        '-30', '-25', '-20', '-15', '-10', '-5',
        '0', '5', '10', '15', '20', '25', '30']
    assert q(".axis.y text").map(texts) == [
        '-1.2', '-1.0', '-0.8', '-0.6', '-0.4', '-0.2',
        '0.0', '0.2', '0.4', '0.6', '0.8', '1.0', '1.2']
    assert q(".title").text() == 'cos sin and cos - sin'
    assert q(".legend text").map(texts) == ['test1', 'test2', 'test3']


def test_line():
    line = Line()
    rng = [8, 12, 23, 73, 39, 57]
    line.add('Single serie', rng)
    line.title = "One serie"
    q = line.render_pyquery()
    assert len(q(".axis.x")) == 0
    assert len(q(".axis.y")) == 1
    assert len(q(".plot .series path")) == 1
    assert len(q(".x.axis .guides")) == 0
    assert len(q(".y.axis .guides")) == 7


def test_one_dot():
    line = Line()
    line.add('one dot', [12])
    line.x_labels = ['one']
    q = line.render_pyquery()
    assert len(q(".axis.x")) == 1
    assert len(q(".axis.y")) == 1
    assert len(q(".y.axis .guides")) == 1


def test_no_dot():
    line = Line()
    line.add('no dot', [])
    q = line.render_pyquery()
    assert q(".text-overlay text").text() == 'No data'


def test_no_dot_at_all():
    q = Line().render_pyquery()
    assert q(".text-overlay text").text() == 'No data'


def test_not_equal_x_labels():
    line = Line()
    line.add('test1', range(100))
    line.x_labels = map(str, range(11))
    q = line.render_pyquery()
    assert len(q(".dots")) == 100
    assert len(q(".axis.x")) == 1
    assert q(".axis.x text").map(texts) == ['0', '1', '2', '3', '4', '5', '6',
                                            '7', '8', '9', '10']
