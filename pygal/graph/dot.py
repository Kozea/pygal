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
Dot chart

"""

from __future__ import division
from pygal.util import decorate, cut, safe_enumerate
from pygal.adapters import positive
from pygal.graph.graph import Graph


class Dot(Graph):
    """Dot graph"""

    _adapters = [positive]

    def dot(self, serie, r_max):
        """Draw a dot line"""
        serie_node = self.svg.serie(serie)
        view_values = list(map(self.view, serie.points))
        for i, value in safe_enumerate(serie.values):
            x, y = view_values[i]
            size = r_max * value
            value = self._format(value)
            metadata = serie.metadata.get(i)
            dots = decorate(
                self.svg,
                self.svg.node(serie_node['plot'], class_="dots"),
                metadata)
            self.svg.node(dots, 'circle', cx=x, cy=y, r=size,
                          class_='dot reactive tooltip-trigger')

            self._tooltip_data(dots, value, x, y, classes='centered')
            self._static_value(serie_node, value, x, y)

    def _compute(self):
        x_len = self._len
        y_len = self._order
        self._box.xmax = x_len
        self._box.ymax = y_len

        x_pos = [n / 2 for n in range(1, 2 * x_len, 2)]
        y_pos = [n / 2 for n in reversed(range(1, 2 * y_len, 2))]

        for j, serie in enumerate(self.series):
            serie.points = [
                (x_pos[i], y_pos[j])
                for i in range(x_len)]

        self._x_labels = self.x_labels and list(zip(self.x_labels, x_pos))
        self._y_labels = list(zip(
            self.y_labels or cut(self.series, 'title'), y_pos))

    def _plot(self):
        r_max = min(
            self.view.x(1) - self.view.x(0),
            (self.view.y(0) or 0) - self.view.y(1)) / (2 * (self._max or 1) * 1.05)
        for serie in self.series:
            self.dot(serie, r_max)
