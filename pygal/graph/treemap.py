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
Treemap chart

"""

from __future__ import division
from pygal.util import decorate
from pygal.graph.graph import Graph
from pygal.adapters import positive, none_to_zero


class Treemap(Graph):
    """Treemap graph"""

    _adapters = [positive, none_to_zero]

    def _rect(self, serie, x, y, w, h):
        rx, ry = self.view((x, y))
        rw, rh = self.view((x + w, y + h))
        rw -= rx
        rh -= ry

        serie_node = self._serie(serie._index)
        rects = self.svg.node(serie_node['plot'], class_="rects")
        # metadata = serie.metadata.get(i)
        # value = self._format(serie.values[i])

        # rect = decorate(
        #     self.svg,
        #     self.svg.node(rects, class_="rect"),
        #     metadata)

        self.svg.node(rects, 'rect',
                      x=rx,
                      y=ry,
                      width=rw,
                      height=rh,
                      class_='rect reactive tooltip-trigger')

        # self._tooltip_data(rect, value,
        #                    self.view.x(acc + w / 2),
        #                    self.view.y(.5),
        #                    classes='centered')
        # self._static_value(serie_node, value,
        #                    self.view.x(acc + w / 2),
        #                    self.view.y(.5))

    def _binary_tree(self, series, total, x, y, w, h):
        if len(series) == 1:
            self._rect(series[0], x, y, w, h)
            return

        midpoint = total / 2
        pivot_index = 1
        running_sum = 0
        for serie in series:
            if running_sum >= midpoint:
                pivot_index = serie._index
                break

            running_sum += sum(serie.values)

        half1 = series[:pivot_index]
        half2 = series[pivot_index:]

        half1_sum = sum(map(sum, map(lambda x: x.values, half1)))
        half2_sum = sum(map(sum, map(lambda x: x.values, half2)))
        pivot_pct = half1_sum / total
        if h > w:
            y_pivot = pivot_pct * h
            self._binary_tree(
                half1, half1_sum, x, y, w, y_pivot)
            self._binary_tree(
                half2, half2_sum, x, y + y_pivot, w, h - y_pivot)
        else:
            x_pivot = pivot_pct * w
            self._binary_tree(
                half1, half1_sum, x, y, x_pivot, h)
            self._binary_tree(
                half2, half2_sum, x + x_pivot, y, w - x_pivot, h)

    def _plot(self):
        total = sum(map(sum, map(lambda x: x.values, self.series)))
        if total == 0:
            return

        gw = self.width - self.margin.x
        gh = self.height - self.margin.y

        self.view.box.xmin = self.view.box.ymin = x = y = 0
        self.view.box.xmax = w = (total * gw / gh) ** .5
        self.view.box.ymax = h = total / w
        self.view.box.fix()

        for index, serie in enumerate(self.series):
            serie._index = index

        self._binary_tree(self.series, total, x, y, w, h)
