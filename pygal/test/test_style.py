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
from pygal.style import Style


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
'''
