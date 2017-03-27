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
"""Funnel chart: Represent values as a funnel"""

from __future__ import division

from pygal.adapters import none_to_zero, positive
from pygal.graph.graph import Graph
from pygal.util import alter, cut, decorate


class Funnel(Graph):

    """Funnel graph class"""

    _adapters = [positive, none_to_zero]

    def _value_format(self, value):
        """Format value for dual value display."""
        return super(Funnel, self)._value_format(value and abs(value))

    def funnel(self, serie):
        """Draw a funnel slice"""
        serie_node = self.svg.serie(serie)
        fmt = lambda x: '%f %f' % x
        for i, poly in enumerate(serie.points):
            metadata = serie.metadata.get(i)
            val = self._format(serie, i)

            funnels = decorate(
                self.svg,
                self.svg.node(serie_node['plot'], class_="funnels"),
                metadata)

            alter(self.svg.node(
                funnels, 'polygon',
                points=' '.join(map(fmt, map(self.view, poly))),
                class_='funnel reactive tooltip-trigger'), metadata)

            # Poly center from label
            x, y = self.view((
                self._center(self._x_pos[serie.index]),
                sum([point[1] for point in poly]) / len(poly)))
            self._tooltip_data(
                funnels, val, x, y, 'centered',
                self._get_x_label(serie.index))
            self._static_value(serie_node, val, x, y, metadata)

    def _center(self, x):
        return x - 1 / (2 * self._order)

    def _compute(self):
        """Compute y min and max and y scale and set labels"""
        self._x_pos = [
            (x + 1) / self._order for x in range(self._order)
        ] if self._order != 1 else [.5]  # Center if only one value

        previous = [[self.zero, self.zero] for i in range(self._len)]
        for i, serie in enumerate(self.series):
            y_height = - sum(serie.safe_values) / 2
            all_x_pos = [0] + self._x_pos
            serie.points = []
            for j, value in enumerate(serie.values):
                poly = []
                poly.append((all_x_pos[i], previous[j][0]))
                poly.append((all_x_pos[i], previous[j][1]))
                previous[j][0] = y_height
                y_height = previous[j][1] = y_height + value
                poly.append((all_x_pos[i + 1], previous[j][1]))
                poly.append((all_x_pos[i + 1], previous[j][0]))
                serie.points.append(poly)

        val_max = max(list(map(sum, cut(self.series, 'values'))) + [self.zero])
        self._box.ymin = -val_max
        self._box.ymax = val_max

        if self.range and self.range[0] is not None:
            self._box.ymin = self.range[0]

        if self.range and self.range[1] is not None:
            self._box.ymax = self.range[1]

    def _compute_x_labels(self):
        self._x_labels = list(
            zip(self.x_labels and
                map(self._x_format, self.x_labels) or [
                    serie.title['title']
                    if isinstance(serie.title, dict)
                    else serie.title or '' for serie in self.series],
                map(self._center, self._x_pos)))

    def _plot(self):
        """Plot the funnel"""
        for serie in self.series:
            self.funnel(serie)
