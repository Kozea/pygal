# -*- coding: utf-8 -*-
# This file is part of pygal
#
# A python svg graph plotting library
# Copyright © 2012 Kozea
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
"""
Pygal -  A python svg graph plotting library

"""

__version__ = '0.10.0'

from pygal.config import Config
from pygal.graph.bar import Bar
from pygal.graph.dot import Dot
from pygal.graph.funnel import Funnel
from pygal.graph.gauge import Gauge
from pygal.graph.horizontal import HorizontalBar
from pygal.graph.horizontal import HorizontalStackedBar
from pygal.graph.line import Line
from pygal.graph.pie import Pie
from pygal.graph.pyramid import Pyramid
from pygal.graph.radar import Radar
from pygal.graph.stackedbar import StackedBar
from pygal.graph.stackedline import StackedLine
from pygal.graph.xy import XY


#: List of all chart types
CHARTS = [
    Bar,
    Dot,
    Funnel,
    Gauge,
    HorizontalBar,
    HorizontalStackedBar,
    Line,
    Pie,
    Pyramid,
    Radar,
    StackedBar,
    StackedLine,
    XY
]
