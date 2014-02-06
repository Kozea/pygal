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
Horizontal bar graph

"""
from pygal.graph.horizontal import HorizontalGraph
from pygal.graph.bar import Bar


class HorizontalBar(HorizontalGraph, Bar):
    """Horizontal Bar graph"""

    def _plot(self):
        for index, serie in enumerate(self.series[::-1]):
            num = len(self.series) - index - 1
            self.bar(self._serie(num), serie, index)
        for index, serie in enumerate(self.secondary_series[::-1]):
            num = len(self.secondary_series) + len(self.series) - index - 1
            self.bar(self._serie(num), serie, index + len(self.series), True)
