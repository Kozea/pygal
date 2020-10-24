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
"""Treemap chart: Visualize data using nested recangles"""

from pygal.adapters import none_to_zero, positive
from pygal.graph.graph import Graph
from pygal.util import alter, cut, decorate


class Treemap(Graph):
    """Treemap graph class"""

    _adapters = [positive, none_to_zero]

    def _rect(self, serie, serie_node, rects, val, x, y, w, h, i):
        rx, ry = self.view((x, y))
        rw, rh = self.view((x + w, y + h))
        rw -= rx
        rh -= ry

        metadata = serie.metadata.get(i)

        val = self._format(serie, i)

        rect = decorate(
            self.svg, self.svg.node(rects, class_="rect"), metadata
        )

        alter(
            self.svg.node(
                rect,
                'rect',
                x=rx,
                y=ry,
                width=rw,
                height=rh,
                class_='rect reactive tooltip-trigger'
            ), metadata
        )

        self._tooltip_data(
            rect, val, rx + rw / 2, ry + rh / 2, 'centered',
            self._get_x_label(i)
        )
        self._static_value(serie_node, val, rx + rw / 2, ry + rh / 2, metadata)

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
                    list(enumerate(datum.values)), total, x, y, w, h, (
                        datum, serie_node,
                        self.svg.node(serie_node['plot'], class_="rects")
                    )
                )
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
            self._binary_tree(half1, half1_sum, x, y, w, y_pivot, parent)
            self._binary_tree(
                half2, half2_sum, x, y + y_pivot, w, h - y_pivot, parent
            )
        else:
            x_pivot = pivot_pct * w
            self._binary_tree(half1, half1_sum, x, y, x_pivot, h, parent)
            self._binary_tree(
                half2, half2_sum, x + x_pivot, y, w - x_pivot, h, parent
            )

    def _compute_x_labels(self):
        pass

    def _compute_y_labels(self):
        pass

    def _plot(self):
        total = sum(map(sum, map(lambda x: x.values, self.series)))
        if total == 0:
            return

        gw = self.width - self.margin_box.x
        gh = self.height - self.margin_box.y

        self.view.box.xmin = self.view.box.ymin = x = y = 0
        self.view.box.xmax = w = (total * gw / gh)**.5
        self.view.box.ymax = h = total / w
        self.view.box.fix()

        self._binary_tree(self.series, total, x, y, w, h)
