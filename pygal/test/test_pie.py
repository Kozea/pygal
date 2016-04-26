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

"""Donut chart related tests"""

from pygal import Pie


def test_donut():
    """Test a donut pie chart"""
    chart = Pie(inner_radius=.3, pretty_print=True)
    chart.title = 'Browser usage in February 2012 (in %)'
    chart.add('IE', 19.5)
    chart.add('Firefox', 36.6)
    chart.add('Chrome', 36.3)
    chart.add('Safari', 4.5)
    chart.add('Opera', 2.3)
    assert chart.render()


def test_multiseries_donut():
    """Test a donut pie chart with multiserie"""
    # this just demos that the multiseries pie does not respect
    # the inner_radius
    chart = Pie(inner_radius=.3, pretty_print=True)
    chart.title = 'Browser usage by version in February 2012 (in %)'
    chart.add('IE', [5.7, 10.2, 2.6, 1])
    chart.add('Firefox', [.6, 16.8, 7.4, 2.2, 1.2, 1, 1, 1.1, 4.3, 1])
    chart.add('Chrome', [.3, .9, 17.1, 15.3, .6, .5, 1.6])
    chart.add('Safari', [4.4, .1])
    chart.add('Opera', [.1, 1.6, .1, .5])
    assert chart.render()


def test_half_pie():
    """Test a half pie chart"""
    pie = Pie()
    pie.add('IE', 19.5)
    pie.add('Firefox', 36.6)
    pie.add('Chrome', 36.3)
    pie.add('Safari', 4.5)
    pie.add('Opera', 2.3)

    half = Pie(half_pie=True)
    half.add('IE', 19.5)
    half.add('Firefox', 36.6)
    half.add('Chrome', 36.3)
    half.add('Safari', 4.5)
    half.add('Opera', 2.3)
    assert pie.render() != half.render()
