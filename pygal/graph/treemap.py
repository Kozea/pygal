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
from pygal.util import decorate, cut
from pygal.graph.graph import Graph
from pygal.adapters import positive, none_to_zero


class Treemap(Graph):
    """Treemap graph"""

    _adapters = [positive, none_to_zero]

    def _rect(self, serie, serie_node, rects, val, x, y, w, h, i):
        rx, ry = self.view((x, y))
        rw, rh = self.view((x + w, y + h))
        rw -= rx
        rh -= ry

        metadata = serie.metadata.get(i)
        value = self._format(val)

        rect = decorate(
            self.svg,
            self.svg.node(rects, class_="rect"),
            metadata)

        self.svg.node(rect, 'rect',
                      x=rx,
                      y=ry,
                      width=rw,
                      height=rh,
                      class_='rect reactive tooltip-trigger')

        self._tooltip_data(rect, value,
                           rx + rw / 2,
                           ry + rh / 2,
                           classes='centered')
        self._static_value(serie_node, value,
                           rx + rw / 2,
                           ry + rh / 2)

    def _binary_tree(self, data, total, x, y, w, h, parent=None):
        if total == 0:
            return
        if len(data) == 1:
            if parent:
                i, datum = data[0]
                serie, serie_node, rects = parent
                self._rect(serie, serie_node, rects, datum, x, y, w, h, i)
            else:
                datum = data[0]
                serie_node = self.svg.serie(datum)
                self._binary_tree(
                    list(enumerate(datum.values)),
                    total, x, y, w, h,
                    (datum, serie_node,
                     self.svg.node(serie_node['plot'], class_="rects")))
            return

        midpoint = total / 2
        pivot_index = 1
        running_sum = 0
        for i, elt in enumerate(data):
            if running_sum >= midpoint:
                pivot_index = i
                break

            running_sum += elt[1] if parent else sum(elt.values)

        half1 = data[:pivot_index]
        half2 = data[pivot_index:]

        if parent:
            half1_sum = sum(cut(half1, 1))
            half2_sum = sum(cut(half2, 1))
        else:
            half1_sum = sum(map(sum, map(lambda x: x.values, half1)))
            half2_sum = sum(map(sum, map(lambda x: x.values, half2)))
        pivot_pct = half1_sum / total

        if h > w:
            y_pivot = pivot_pct * h
            self._binary_tree(
                half1, half1_sum, x, y, w, y_pivot, parent)
            self._binary_tree(
                half2, half2_sum, x, y + y_pivot, w, h - y_pivot, parent)
        else:
            x_pivot = pivot_pct * w
            self._binary_tree(
                half1, half1_sum, x, y, x_pivot, h, parent)
            self._binary_tree(
                half2, half2_sum, x + x_pivot, y, w - x_pivot, h, parent)

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

        self._binary_tree(self.series, total, x, y, w, h)
