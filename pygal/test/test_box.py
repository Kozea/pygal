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
from pygal.graph.box import Box
from pygal import Box as ghostedBox


def test_quartiles():
    a = [-2.0, 3.0, 4.0, 5.0, 8.0]  # odd test data
    q0, q1, q2, q3, q4 = Box._box_points(a)

    assert q1 == 7.0 / 4.0
    assert q2 == 4.0
    assert q3 == 23 / 4.0
    assert q0 == 7.0 / 4.0 - 6.0  # q1 - 1.5 * iqr
    assert q4 == 23 / 4.0 + 6.0  # q3 + 1.5 * iqr

    b = [1.0, 4.0, 6.0, 8.0]  # even test data
    q0, q1, q2, q3, q4 = Box._box_points(b)

    assert q2 == 5.0

    c = [2.0, None, 4.0, 6.0, None]  # odd with None elements
    q0, q1, q2, q3, q4 = Box._box_points(c)

    assert q2 == 4.0

    d = [4]
    q0, q1, q2, q3, q4 = Box._box_points(d)

    assert q0 == 4
    assert q1 == 4
    assert q2 == 4
    assert q3 == 4
    assert q4 == 4

def test_quartiles_min_extremes():
    a = [-2.0, 3.0, 4.0, 5.0, 8.0]  # odd test data
    q0, q1, q2, q3, q4 = Box._box_points(a, mode='extremes')

    assert q1 == 7.0 / 4.0
    assert q2 == 4.0
    assert q3 == 23 / 4.0
    assert q0 == -2.0  # min
    assert q4 == 8.0  # max

    b = [1.0, 4.0, 6.0, 8.0]  # even test data
    q0, q1, q2, q3, q4 = Box._box_points(b, mode='extremes')

    assert q2 == 5.0

    c = [2.0, None, 4.0, 6.0, None]  # odd with None elements
    q0, q1, q2, q3, q4 = Box._box_points(c, mode='extremes')

    assert q2 == 4.0

    d = [4]
    q0, q1, q2, q3, q4 = Box._box_points(d, mode='extremes')

    assert q0 == 4
    assert q1 == 4
    assert q2 == 4
    assert q3 == 4
    assert q4 == 4


def test_simple_box():
    box = ghostedBox()
    box.add('test1', [-1, 2, 3, 3.1, 3.2, 4, 5])
    box.add('test2', [2, 3, 5, 6, 6, 4])
    box.title = 'Box test'
    q = box.render_pyquery()

    assert len(q(".axis.y")) == 1
    assert len(q(".legend")) == 2
    assert len(q(".plot .series rect")) == 2
