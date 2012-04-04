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
Horizontal graph

"""
from pygal.graph.graph import Graph
from pygal.graph.bar import Bar
from pygal.graph.stackedbar import StackedBar


class HorizontalGraph(Graph):
    """Horizontal graph"""
    def __init__(self, *args, **kwargs):
        self.first_pass = True
        self.horizontal = True
        super(HorizontalGraph, self).__init__(*args, **kwargs)

    def _compute(self):
        self.first_pass = False
        # Stupid pylint
        # pylint: disable-msg=E0203,W0201
        if self.first_pass and self.x_labels:
            self.x_labels = list(reversed(self.x_labels))
        # pylint: enable-msg=W0201,E0203
        super(HorizontalGraph, self)._compute()
        self._x_labels, self._y_labels = self._y_labels, self._x_labels
        self._box.swap()
        # Y axis is inverted
        if self.first_pass:
            for serie in self.series:
                serie.values = list(reversed(serie.values))


class HorizontalBar(HorizontalGraph, Bar):
    """Horizontal Bar graph"""


class HorizontalStackedBar(HorizontalGraph, StackedBar):
    """Horizontal Stacked Bar graph"""
