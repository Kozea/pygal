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
Bar chart

"""

from __future__ import division
from pygal.graph.graph import Graph
from pygal.util import swap, ident, compute_scale, decorate


class Bar(Graph):
    """Bar graph"""

    _series_margin = .06
    _serie_margin = .06

    def __init__(self, *args, **kwargs):
        self._x_ranges = None
        super(Bar, self).__init__(*args, **kwargs)

    def _bar(self, parent, x, y, index, i, zero, shift=True):
        width = (self.view.x(1) - self.view.x(0)) / self._len
        x, y = self.view((x, y))
        series_margin = width * self._series_margin
        x += series_margin
        width -= 2 * series_margin
        if shift:
            width /= self._order
            x += index * width
            serie_margin = width * self._serie_margin
            x += serie_margin
            width -= 2 * serie_margin
        height = self.view.y(zero) - y
        r = self.rounded_bars * 1 if self.rounded_bars else 0
        self.svg.transposable_node(
            parent, 'rect',
            x=x, y=y, rx=r, ry=r, width=width, height=height,
            class_='rect reactive tooltip-trigger')
        transpose = swap if self.horizontal else ident
        return transpose((x + width / 2, y + height / 2))

    def bar(self, serie_node, serie, index):
        """Draw a bar graph for a serie"""
        bars = self.svg.node(serie_node['plot'], class_="bars")
        for i, (x, y) in enumerate(serie.points):
            if None in (x, y) or (self.logarithmic and y <= 0):
                continue
            metadata = serie.metadata.get(i)

            bar = decorate(
                self.svg,
                self.svg.node(bars, class_='bar'),
                metadata)
            val = self._format(serie.values[i])

            x_center, y_center = self._bar(
                bar, x, y, index, i, self.zero)
            self._tooltip_data(
                bar, val, x_center, y_center, classes="centered")
            self._static_value(serie_node, val, x_center, y_center)

    def _compute(self):
        if self._min:
            self._box.ymin = min(self._min, self.zero)
        if self._max:
            self._box.ymax = max(self._max, self.zero)

        x_pos = [
            x / self._len for x in range(self._len + 1)
        ] if self._len > 1 else [0, 1]  # Center if only one value

        self._points(x_pos)

        y_pos = compute_scale(
            self._box.ymin, self._box.ymax, self.logarithmic, self.order_min
        ) if not self.y_labels else map(float, self.y_labels)

        self._x_labels = self.x_labels and zip(self.x_labels, [
            (i + .5) / self._len for i in range(self._len)])
        self._y_labels = zip(map(self._format, y_pos), y_pos)

    def _plot(self):
        for index, serie in enumerate(self.series):
            self.bar(self._serie(index), serie, index)
