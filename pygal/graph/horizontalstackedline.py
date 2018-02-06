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
"""Horizontal Stacked Line graph"""

from pygal.graph.horizontal import HorizontalGraph
from pygal.graph.stackedline import StackedLine


class HorizontalStackedLine(HorizontalGraph, StackedLine):
    """Horizontal Stacked Line graph"""

    def _plot(self):
        """Draw the lines in reverse order"""
        for serie in self.series[::-1]:
            self.line(serie)
        for serie in self.secondary_series[::-1]:
            self.line(serie, True)
