# -*- coding: utf-8 -*-
# This file is part of pygal
#
# A python svg graph plotting library
# Copyright © 2012-2013 Kozea
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
from pygal.style import Style, darken, lighten


def test_colors():
    style = Style(colors=['red', '#231A3b', '#ff0', 'rgb(12, 231, 3)'])
    assert style.colors == '''\
.color-0 {
  stroke: red;
  fill: red;
}

.color-1 {
  stroke: #231A3b;
  fill: #231A3b;
}

.color-2 {
  stroke: #ff0;
  fill: #ff0;
}

.color-3 {
  stroke: rgb(12, 231, 3);
  fill: rgb(12, 231, 3);
}

.color-4 {
  stroke: red;
  fill: red;
}

.color-5 {
  stroke: #231A3b;
  fill: #231A3b;
}

.color-6 {
  stroke: #ff0;
  fill: #ff0;
}

.color-7 {
  stroke: rgb(12, 231, 3);
  fill: rgb(12, 231, 3);
}

.color-8 {
  stroke: red;
  fill: red;
}

.color-9 {
  stroke: #231A3b;
  fill: #231A3b;
}

.color-10 {
  stroke: #ff0;
  fill: #ff0;
}

.color-11 {
  stroke: rgb(12, 231, 3);
  fill: rgb(12, 231, 3);
}

.color-12 {
  stroke: red;
  fill: red;
}

.color-13 {
  stroke: #231A3b;
  fill: #231A3b;
}

.color-14 {
  stroke: #ff0;
  fill: #ff0;
}

.color-15 {
  stroke: rgb(12, 231, 3);
  fill: rgb(12, 231, 3);
}
'''


def test_darken():
    assert darken('#800', 20) == '#220000'
    assert darken('#ffffff', 10) == '#e6e6e6'
    assert darken('#f3148a', 25) == '#810747'
    assert darken('#121212', 1) == '#0f0f0f'
    assert darken('#999999', 100) == '#000000'
    assert darken('#1479ac', 8) == '#105f87'


def test_lighten():
    assert lighten('#800', 20) == '#ee0000'
    assert lighten('#ffffff', 10) == '#ffffff'
    assert lighten('#f3148a', 25) == '#f98dc6'
    assert lighten('#121212', 1) == '#151515'
    assert lighten('#999999', 100) == '#ffffff'
    assert lighten('#1479ac', 8) == '#1893d1'
