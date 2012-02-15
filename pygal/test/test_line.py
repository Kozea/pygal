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
from pygal import Line
from pygal.config import Config
from math import cos, sin


def test_simple_line():
    line = Line(Config(scale=.0005))
    rng = range(-30, 31, 5)
    line.add('test1', [cos(x / 10.) for x in rng])
    line.add('test2', [sin(x / 10.) for x in rng])
    line.add('test3', [cos(x / 10.) - sin(x / 10.) for x in rng])
    line.x_labels = map(str, rng)
    line.title = "cos sin and cos - sin"
    line._in_browser()


def test_line():
    line = Line()
    rng = [8, 12, 23, 73, 39, 57]
    line.add('-_-', rng)
    line.x_labels = map(str, rng)
    line.title = "cos sin and cos - sin"
    line._in_browser()


def test_one_dot():
    line = Line()
    line.add('one dot', [12])
    line.x_labels = ['one']
    line.render()


def test_no_dot():
    line = Line()
    line.add('no dot', [])
    line.render()


def test_no_dot_at_all():
    line = Line()
    line.render()
