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

__version__ = '1.7.0'
import sys
from pygal.config import Config
from pygal.ghost import Ghost, REAL_CHARTS

CHARTS = []
CHARTS_BY_NAME = {}

for NAME in REAL_CHARTS.keys():
    _CHART = type(NAME, (Ghost,), {})
    CHARTS.append(_CHART)
    CHARTS_BY_NAME[NAME] = _CHART
    setattr(sys.modules[__name__], NAME, _CHART)


__all__ = list(CHARTS_BY_NAME.keys()) + [
    Config.__name__, 'CHARTS', 'CHARTS_BY_NAME']
