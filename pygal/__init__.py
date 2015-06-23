# -*- coding: utf-8 -*-
# This file is part of pygal
#
# A python svg graph plotting library
# Copyright © 2012-2014 Kozea
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

__version__ = '1.9.9'

from pygal.graph.bar import Bar
from pygal.graph.box import Box
from pygal.graph.dot import Dot
from pygal.graph.frenchmap import FrenchMapDepartments, FrenchMapRegions
from pygal.graph.hungarianmap import HungarianCountyMap
from pygal.graph.funnel import Funnel
from pygal.graph.gauge import Gauge
from pygal.graph.histogram import Histogram
from pygal.graph.horizontalbar import HorizontalBar
from pygal.graph.horizontalstackedbar import HorizontalStackedBar
from pygal.graph.line import Line
from pygal.graph.pie import Pie
from pygal.graph.pyramid import Pyramid
from pygal.graph.radar import Radar
from pygal.graph.stackedbar import StackedBar
from pygal.graph.stackedline import StackedLine
from pygal.graph.swissmap import SwissMapCantons
from pygal.graph.time import DateLine, DateTimeLine, TimeLine, TimeDeltaLine
from pygal.graph.treemap import Treemap
from pygal.graph.verticalpyramid import VerticalPyramid
from pygal.graph.worldmap import Worldmap, SupranationalWorldmap
from pygal.graph.xy import XY
from pygal.graph.graph import Graph
from pygal.config import Config


CHARTS_BY_NAME = dict(
    [(k, v) for k, v in locals().items()
     if isinstance(v, type) and issubclass(v, Graph) and v != Graph])

CHARTS_NAMES = list(CHARTS_BY_NAME.keys())
CHARTS = list(CHARTS_BY_NAME.values())
