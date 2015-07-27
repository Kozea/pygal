# -*- coding: utf-8 -*-
# This file is part of pygal
#
# A python svg graph plotting library
# Copyright © 2012-2015 Kozea
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
Bar chart that presents grouped data with rectangular bars with lengths
proportional to the values that they represent.
"""

from __future__ import division

from pygal.graph.graph import Graph
from pygal.util import alter, decorate, ident, swap


class Bar(Graph):

    """Bar graph class"""

    _series_margin = .06
    _serie_margin = .06

    def __init__(self, *args, **kwargs):
        """Bar chart creation"""
        self._x_ranges = None
        super(Bar, self).__init__(*args, **kwargs)

    def _bar(self, serie, parent, x, y, i, zero, secondary=False):
        """Internal bar drawing function"""
        width = (self.view.x(1) - self.view.x(0)) / self._len
        x, y = self.view((x, y))
        series_margin = width * self._series_margin
        x += series_margin
        width -= 2 * series_margin
        width /= self._order
        if self.horizontal:
            serie_index = self._order - serie.index - 1
        else:
            serie_index = serie.index
        x += serie_index * width

        serie_margin = width * self._serie_margin
        x += serie_margin
        width -= 2 * serie_margin
        height = self.view.y(zero) - y
        r = serie.rounded_bars * 1 if serie.rounded_bars else 0
        alter(self.svg.transposable_node(
            parent, 'rect',
            x=x, y=y, rx=r, ry=r, width=width, height=height,
            class_='rect reactive tooltip-trigger'), serie.metadata.get(i))
        transpose = swap if self.horizontal else ident
        return transpose((x + width / 2, y + height / 2))

    def bar(self, serie, rescale=False):
        """Draw a bar graph for a serie"""
        serie_node = self.svg.serie(serie)
        bars = self.svg.node(serie_node['plot'], class_="bars")
        if rescale and self.secondary_series:
            points = self._rescale(serie.points)
        else:
            points = serie.points

        for i, (x, y) in enumerate(points):
            if None in (x, y) or (self.logarithmic and y <= 0):
                continue
            metadata = serie.metadata.get(i)

            bar = decorate(
                self.svg,
                self.svg.node(bars, class_='bar'),
                metadata)
            val = self._format(serie.values[i])

            x_center, y_center = self._bar(
                serie, bar, x, y, i, self.zero, secondary=rescale)
            self._tooltip_data(
                bar, val, x_center, y_center, "centered",
                self._get_x_label(i))
            self._static_value(serie_node, val, x_center, y_center, metadata)

    def _compute(self):
        """Compute y min and max and y scale and set labels"""
        if self._min:
            self._box.ymin = min(self._min, self.zero)
        if self._max:
            self._box.ymax = max(self._max, self.zero)

        self._x_pos = [
            x / self._len for x in range(self._len + 1)
        ] if self._len > 1 else [0, 1]  # Center if only one value

        self._points(self._x_pos)

        self._x_pos = [(i + .5) / self._len for i in range(self._len)]

    def _compute_secondary(self):
        """Compute parameters for secondary series rendering"""
        if self.secondary_series:
            y_pos = list(zip(*self._y_labels))[1]
            ymin = self._secondary_min
            ymax = self._secondary_max

            min_0_ratio = (self.zero - self._box.ymin) / self._box.height or 1
            max_0_ratio = (self._box.ymax - self.zero) / self._box.height or 1

            if ymax > self._box.ymax:
                ymin = -(ymax - self.zero) * (1 / max_0_ratio - 1)
            else:
                ymax = (self.zero - ymin) * (1 / min_0_ratio - 1)

            left_range = abs(self._box.ymax - self._box.ymin)
            right_range = abs(ymax - ymin) or 1
            self._scale = left_range / right_range
            self._scale_diff = self._box.ymin
            self._scale_min_2nd = ymin
            self._y_2nd_labels = [
                (self._format(self._box.xmin + y * right_range / left_range),
                 y)
                for y in y_pos]

    def _plot(self):
        """Draw bars for series and secondary series"""
        for serie in self.series:
            self.bar(serie)
        for serie in self.secondary_series:
            self.bar(serie, True)
