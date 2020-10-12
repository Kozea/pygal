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
"""Box chart related tests"""

from pyquery import PyQuery as pq

from pygal import Pie


def test_pie_table():
    """Test rendering a table for a pie"""
    chart = Pie(inner_radius=.3, pretty_print=True)
    chart.title = 'Browser usage in February 2012 (in %)'
    chart.add('IE', 19.5)
    chart.add('Firefox', 36.6)
    chart.add('Chrome', 36.3)
    chart.add('Safari', 4.5)
    chart.add('Opera', 2.3)
    q = pq(chart.render_table())
    assert len(q('table')) == 1
