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
from pygal import Line, Bar
from pygal._compat import u


def test_basic_sparktext():
    chart = Line()
    chart.add('_', [1, 5, 22, 13, 53])
    chart.render_sparktext() == u('▁▁▃▂▇')


def test_another_sparktext():
    chart = Line()
    chart.add('_', [0, 30, 55, 80, 33, 150])
    chart.render_sparktext() == u('▁▂▃▅▂▇')
    chart.render_sparktext() == chart.render_sparktext()
    chart2 = Bar()
    chart2.add('_', [0, 30, 55, 80, 33, 150])
    chart2.render_sparktext() == chart.render_sparktext()


def test_negative_and_float_and_no_data_sparktext():
    chart = Line()
    chart.add('_', [0.1, 0.2, 0.9, -0.5])
    chart.render_sparktext() == u('▄▅█▁')

    chart2 = Line()
    chart2.add('_', [])
    chart2.render_sparktext() == u('')

    chart3 = Line()
    chart3.render_sparktext() == u('')
