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
"""Test sparktext rendering"""

from pygal import Bar, Line
from pygal._compat import u


def test_basic_sparktext():
    """Test basic sparktext"""
    chart = Line()
    chart.add('_', [1, 5, 22, 13, 53])
    assert chart.render_sparktext() == u('▁▁▃▂█')


def test_all_sparktext():
    """Test all character sparktext"""
    chart = Line()
    chart.add('_', range(8))
    assert chart.render_sparktext() == u('▁▂▃▄▅▆▇█')


def test_shifted_sparktext():
    """Test relative_to option in sparktext"""
    chart = Line()
    chart.add('_', list(map(lambda x: x + 10000, range(8))))
    assert chart.render_sparktext() == u('▁▂▃▄▅▆▇█')
    assert chart.render_sparktext(relative_to=0) == u('▇▇▇▇▇▇▇█')


def test_another_sparktext():
    """Test that same data produces same sparktext"""
    chart = Line()
    chart.add('_', [0, 30, 55, 80, 33, 150])
    assert chart.render_sparktext() == u('▁▂▃▄▂█')
    assert chart.render_sparktext() == chart.render_sparktext()
    chart2 = Bar()
    chart2.add('_', [0, 30, 55, 80, 33, 150])
    assert chart2.render_sparktext() == chart.render_sparktext()


def test_negative_and_float__sparktext():
    """Test negative values"""
    """Test negative values"""
    chart = Line()
    chart.add('_', [0.1, 0.2, 0.9, -0.5])
    assert chart.render_sparktext() == u('▁▂█▁')


def test_no_data_sparktext():
    """Test no data sparktext"""
    chart2 = Line()
    chart2.add('_', [])
    assert chart2.render_sparktext() == u('')

    chart3 = Line()
    assert chart3.render_sparktext() == u('')


def test_same_max_and_relative_values_sparktext():
    """Test flat sparktexts"""
    chart = Line()
    chart.add('_', [0, 0, 0, 0, 0])
    assert chart.render_sparktext() == u('▁▁▁▁▁')

    chart2 = Line()
    chart2.add('_', [1, 1, 1, 1, 1])
    assert chart2.render_sparktext(relative_to=1) == u('▁▁▁▁▁')
