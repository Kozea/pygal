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

"""Stacked chart related tests"""

from pygal import StackedLine


def test_stacked_line():
    """Test stacked line"""
    stacked = StackedLine()
    stacked.add('one_two', [1, 2])
    stacked.add('ten_twelve', [10, 12])
    q = stacked.render_pyquery()
    assert set([v.text for v in q("desc.value")]) == set(
        ('1', '2', '11 (+10)', '14 (+12)'))


def test_stacked_line_reverse():
    """Test stack from top stacked line"""
    stacked = StackedLine(stack_from_top=True)
    stacked.add('one_two', [1, 2])
    stacked.add('ten_twelve', [10, 12])
    q = stacked.render_pyquery()
    assert set([v.text for v in q("desc.value")]) == set(
        ('11 (+1)', '14 (+2)', '10', '12'))


def test_stacked_line_log():
    """Test logarithmic stacked line"""
    stacked = StackedLine(logarithmic=True)
    stacked.add('one_two', [1, 2])
    stacked.add('ten_twelve', [10, 12])
    q = stacked.render_pyquery()
    assert set([v.text for v in q("desc.value")]) == set(
        ('1', '2', '11 (+10)', '14 (+12)'))


def test_stacked_line_interpolate():
    """Test interpolated stacked line"""
    stacked = StackedLine(interpolate='cubic')
    stacked.add('one_two', [1, 2])
    stacked.add('ten_twelve', [10, 12])
    q = stacked.render_pyquery()
    assert set([v.text for v in q("desc.value")]) == set(
        ('1', '2', '11 (+10)', '14 (+12)'))
