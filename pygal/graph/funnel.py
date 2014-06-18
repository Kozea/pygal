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
Funnel chart

"""

from __future__ import division
from pygal.util import decorate, cut, compute_scale
from pygal.adapters import positive, none_to_zero
from pygal.graph.graph import Graph


class Funnel(Graph):
    """Funnel graph"""

    _adapters = [positive, none_to_zero]

    def _format(self, value):
        return super(Funnel, self)._format(abs(value))

    def funnel(self, serie):
        """Draw a dot line"""
        serie_node = self.svg.serie(serie)
        fmt = lambda x: '%f %f' % x
        for i, poly in enumerate(serie.points):
            metadata = serie.metadata.get(i)
            value = self._format(serie.values[i])

            funnels = decorate(
                self.svg,
                self.svg.node(serie_node['plot'], class_="funnels"),
                metadata)

            self.svg.node(
                funnels, 'polygon',
                points=' '.join(map(fmt, map(self.view, poly))),
                class_='funnel reactive tooltip-trigger')

            x, y = self.view((
                self._x_labels[serie.index][1],  # Poly center from label
                sum([point[1] for point in poly]) / len(poly)))
            self._tooltip_data(funnels, value, x, y, classes='centered')
            self._static_value(serie_node, value, x, y)

    def _compute(self):
        x_pos = [
            (x + 1) / self._order for x in range(self._order)
        ] if self._order != 1 else [.5]  # Center if only one value

        previous = [[self.zero, self.zero] for i in range(self._len)]
        for i, serie in enumerate(self.series):
            y_height = - sum(serie.safe_values) / 2
            all_x_pos = [0] + x_pos
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

        y_pos = compute_scale(
            self._box.ymin, self._box.ymax, self.logarithmic, self.order_min
        ) if not self.y_labels else list(map(float, self.y_labels))

        self._x_labels = list(
            zip(cut(self.series, 'title'),
                map(lambda x: x - 1 / (2 * self._order), x_pos)))
        self._y_labels = list(zip(map(self._format, y_pos), y_pos))

    def _plot(self):
        for serie in self.series:
            self.funnel(serie)
