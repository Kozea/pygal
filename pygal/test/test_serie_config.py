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
"""Test per serie configuration"""

from pygal import Line

s1 = [1, 3, 12, 3, 4]
s2 = [7, -4, 10, None, 8, 3, 1]


def test_no_serie_config():
    """Test per serie no configuration"""
    chart = Line()
    chart.add('1', s1)
    chart.add('2', s2)
    q = chart.render_pyquery()
    assert len(q('.serie-0 .line')) == 1
    assert len(q('.serie-1 .line')) == 1
    assert len(q('.serie-0 .dot')) == 5
    assert len(q('.serie-1 .dot')) == 6


def test_global_config():
    """Test global configuration"""
    chart = Line(stroke=False)
    chart.add('1', s1)
    chart.add('2', s2)
    q = chart.render_pyquery()
    assert len(q('.serie-0 .line')) == 0
    assert len(q('.serie-1 .line')) == 0
    assert len(q('.serie-0 .dot')) == 5
    assert len(q('.serie-1 .dot')) == 6


def test_serie_config():
    """Test per serie configuration"""
    chart = Line()
    chart.add('1', s1, stroke=False)
    chart.add('2', s2)
    q = chart.render_pyquery()
    assert len(q('.serie-0 .line')) == 0
    assert len(q('.serie-1 .line')) == 1
    assert len(q('.serie-0 .dot')) == 5
    assert len(q('.serie-1 .dot')) == 6


def test_serie_precedence_over_global_config():
    """Test that per serie configuration overide global configuration"""
    chart = Line(stroke=False)
    chart.add('1', s1, stroke=True)
    chart.add('2', s2)
    q = chart.render_pyquery()
    assert len(q('.serie-0 .line')) == 1
    assert len(q('.serie-1 .line')) == 0
    assert len(q('.serie-0 .dot')) == 5
    assert len(q('.serie-1 .dot')) == 6
