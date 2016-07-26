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
from unittest import TestCase

from wheel.signatures import assertTrue

from pygal import Bar
from pygal.graph.graph import Graph
from pygal import Config


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


def test_Bar_Value_is_False():
    """Test to check the bar_value is initialised as false"""
    assert Bar(bar_values=False)


def test_difference():
    bar = Bar(bar_values=False)
    rng = [-3, -32, -39]
    bar.add('test1', rng)
    bar.add('test2', map(abs, rng))
    bar.x_labels = map(str, rng)
    bar_labelled = Bar(bar_values=True)
    rng = [-3, -32, -39]
    bar_labelled.add('test1', rng)
    bar + bar_labelled.add('test2', map(abs, rng))
    bar.labelled = map(str, rng)

    assert bar == bar_labelled


# def test_bar_values(CommonConfig):

#   assert self.Bar(print_values==True)

def test_calc_percent():
    bar = Bar()
    rng = [-3, -32, -39]
    bar.add('test1', rng)
    bar.add('test2', map(abs, rng))
    bar.x_labels = map(str, rng)



    assert bar.calc_percent(rng) is float

def test_bar_percent_difference():
    bar = Bar()
    rng = [-3, -32, -39]
    bar.add('test1', rng)
    bar.add('test2', map(abs, rng))
    bar.x_labels = map(str, rng)

    barpercent = Bar(percent_values=True)
    rng = [-3, -32, -39]
    barpercent.add('test1', rng)
    barpercent.add('test2', map(abs, rng))
    barpercent.x_labels = map(str, rng)

    assert (bar != barpercent)






