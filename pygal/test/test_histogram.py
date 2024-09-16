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

"""Histogram chart related tests"""


from pygal import Histogram


def test_histogram():
    """Simple histogram test"""
    hist = Histogram()
    hist.add('1', [
        (2, 0, 1),
        (4, 1, 3),
        (3, 3.5, 5),
        (1.5, 5, 10)
    ])
    hist.add('2', [(2, 2, 8)], secondary=True)
    q = hist.render_pyquery()
    assert len(q('.rect')) == 5
