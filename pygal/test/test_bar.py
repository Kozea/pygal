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
