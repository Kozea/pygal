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

__version__ = '0.12.1'
import sys
from pygal.config import Config
from pygal.ghost import Ghost
from pygal.graph import CHARTS_NAMES

CHARTS = []
CHARTS_BY_NAME = {}

for NAME in CHARTS_NAMES:
    _CHART = type(NAME, (Ghost,), {})
    CHARTS.append(_CHART)
    CHARTS_BY_NAME[NAME] = _CHART
    setattr(sys.modules[__name__], NAME, _CHART)


__all__ = CHARTS_NAMES + [Config.__name__, 'CHARTS', 'CHARTS_BY_NAME']
