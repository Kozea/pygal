# -*- coding: utf-8 -*-
# This file is part of pygal
#
# A python svg graph plotting library
# Copyright © 2012-2015 Kozea
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
Main pygal package.

This package holds all available charts in pygal, the Config class
and the maps extensions namespace module.

"""

__version__ = '2.0.7'

import pkg_resources
import sys
import traceback
import warnings

from pygal.graph.bar import Bar
from pygal.graph.box import Box
from pygal.graph.dot import Dot
from pygal.graph.funnel import Funnel
from pygal.graph.gauge import Gauge
from pygal.graph.histogram import Histogram
from pygal.graph.horizontalbar import HorizontalBar
from pygal.graph.horizontalstackedbar import HorizontalStackedBar
from pygal.graph.line import Line
from pygal.graph.pie import Pie
from pygal.graph.pyramid import Pyramid, VerticalPyramid
from pygal.graph.radar import Radar
from pygal.graph.stackedbar import StackedBar
from pygal.graph.stackedline import StackedLine
from pygal.graph.time import DateLine, DateTimeLine, TimeLine, TimeDeltaLine
from pygal.graph.treemap import Treemap
from pygal.graph.xy import XY
from pygal.graph.graph import Graph
from pygal.config import Config
from pygal import maps


CHARTS_BY_NAME = dict(
    [(k, v) for k, v in locals().items()
     if isinstance(v, type) and issubclass(v, Graph) and v != Graph])


from pygal.graph.map import BaseMap
for entry in pkg_resources.iter_entry_points('pygal.maps'):
    try:
        module = entry.load()
    except Exception:
        warnings.warn('Unable to load %s pygal plugin \n\n%s' % (
            entry, traceback.format_exc()), Warning)
        continue
    setattr(maps, entry.name, module)
    for k, v in module.__dict__.items():
        if isinstance(v, type) and issubclass(v, BaseMap) and v != BaseMap:
            CHARTS_BY_NAME[entry.name.capitalize() + k + 'Map'] = v

CHARTS_NAMES = list(CHARTS_BY_NAME.keys())
CHARTS = list(CHARTS_BY_NAME.values())


class PluginImportFixer(object):

    """
    Allow external map plugins to be imported from pygal.maps package.

    It is a ``sys.meta_path`` loader.
    """

    def find_module(self, fullname, path=None):
        """
        Tell if the module to load can be loaded by
        the load_module function, ie: if it is a ``pygal.maps.*``
        module.
        """
        if fullname.startswith('pygal.maps.') and hasattr(
                maps, fullname.split('.')[2]):
            return self
        return None

    def load_module(self, name):
        """
        Load the ``pygal.maps.name`` module from the previously
        loaded plugin
        """
        if name not in sys.modules:
            sys.modules[name] = getattr(maps, name.split('.')[2])
        return sys.modules[name]

sys.meta_path += [PluginImportFixer()]
