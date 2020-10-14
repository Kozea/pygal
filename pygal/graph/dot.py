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
"""
Dot chart displaying values as a grid of dots, the bigger the value
the bigger the dot
"""

from math import log10

from pygal._compat import to_str
from pygal.graph.graph import Graph
from pygal.util import alter, cached_property, decorate, safe_enumerate
from pygal.view import ReverseView, View


class Dot(Graph):
    """Dot graph class"""

    def dot(self, serie, r_max):
        """Draw a dot line"""
        serie_node = self.svg.serie(serie)
        view_values = list(map(self.view, serie.points))
        for i, value in safe_enumerate(serie.values):
            x, y = view_values[i]

            if self.logarithmic:
                log10min = log10(self._min) - 1
                log10max = log10(self._max or 1)

                if value != 0:
                    size = r_max * ((log10(abs(value)) - log10min) /
                                    (log10max - log10min))
                else:
                    size = 0
            else:
                size = r_max * (abs(value) / (self._max or 1))

            metadata = serie.metadata.get(i)
            dots = decorate(
                self.svg, self.svg.node(serie_node['plot'], class_="dots"),
                metadata
            )
            alter(
                self.svg.node(
                    dots,
                    'circle',
                    cx=x,
                    cy=y,
                    r=size,
                    class_='dot reactive tooltip-trigger' +
                    (' negative' if value < 0 else '')
                ), metadata
            )

            val = self._format(serie, i)
            self._tooltip_data(
                dots, val, x, y, 'centered', self._get_x_label(i)
            )
            self._static_value(serie_node, val, x, y, metadata)

    def _compute(self):
        """Compute y min and max and y scale and set labels"""
        x_len = self._len
        y_len = self._order
        self._box.xmax = x_len
        self._box.ymax = y_len

        self._x_pos = [n / 2 for n in range(1, 2 * x_len, 2)]
        self._y_pos = [n / 2 for n in reversed(range(1, 2 * y_len, 2))]

        for j, serie in enumerate(self.series):
            serie.points = [(self._x_pos[i], self._y_pos[j])
                            for i in range(x_len)]

    def _compute_y_labels(self):
        self._y_labels = list(
            zip(
                self.y_labels and map(to_str, self.y_labels) or [
                    serie.title['title']
                    if isinstance(serie.title, dict) else serie.title or ''
                    for serie in self.series
                ], self._y_pos
            )
        )

    def _set_view(self):
        """Assign a view to current graph"""
        view_class = ReverseView if self.inverse_y_axis else View

        self.view = view_class(
            self.width - self.margin_box.x, self.height - self.margin_box.y,
            self._box
        )

    @cached_property
    def _values(self):
        """Getter for series values (flattened)"""
        return [abs(val) for val in super(Dot, self)._values if val != 0]

    @cached_property
    def _max(self):
        """Getter for the maximum series value"""
        return (
            self.range[1] if (self.range and self.range[1] is not None) else
            (max(map(abs, self._values)) if self._values else None)
        )

    def _plot(self):
        """Plot all dots for series"""
        r_max = min(
            self.view.x(1) - self.view.x(0),
            (self.view.y(0) or 0) - self.view.y(1)
        ) / (2 * 1.05)
        for serie in self.series:
            self.dot(serie, r_max)
