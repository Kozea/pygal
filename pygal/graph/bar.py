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
Bar chart that presents grouped data with rectangular bars with lengths
proportional to the values that they represent.
"""

from pygal.graph.graph import Graph
from pygal.util import alter, decorate, ident, swap


class Bar(Graph):
    """Bar graph class"""

    _series_margin = .06
    _serie_margin = .06

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
        alter(
            self.svg.transposable_node(
                parent,
                'rect',
                x=x,
                y=y,
                rx=r,
                ry=r,
                width=width,
                height=height,
                class_='rect reactive tooltip-trigger'
            ), serie.metadata.get(i)
        )
        return x, y, width, height

    def _tooltip_and_print_values(
            self, serie_node, serie, parent, i, val, metadata, x, y, width,
            height
    ):
        transpose = swap if self.horizontal else ident
        x_center, y_center = transpose((x + width / 2, y + height / 2))
        x_top, y_top = transpose((x + width, y + height))
        x_bottom, y_bottom = transpose((x, y))
        if self._dual:
            v = serie.values[i][0]
        else:
            v = serie.values[i]
        sign = -1 if v < self.zero else 1
        self._tooltip_data(
            parent, val, x_center, y_center, "centered", self._get_x_label(i)
        )

        if self.print_values_position == 'top':
            if self.horizontal:
                x = x_bottom + sign * self.style.value_font_size / 2
                y = y_center
            else:
                x = x_center
                y = y_bottom - sign * self.style.value_font_size / 2
        elif self.print_values_position == 'bottom':
            if self.horizontal:
                x = x_top + sign * self.style.value_font_size / 2
                y = y_center
            else:
                x = x_center
                y = y_top - sign * self.style.value_font_size / 2
        else:
            x = x_center
            y = y_center
        self._static_value(serie_node, val, x, y, metadata, "middle")

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
            val = self._format(serie, i)

            bar = decorate(
                self.svg, self.svg.node(bars, class_='bar'), metadata
            )

            x_, y_, width, height = self._bar(
                serie, bar, x, y, i, self.zero, secondary=rescale
            )

            self._confidence_interval(
                serie_node['overlay'], x_ + width / 2, y_, serie.values[i],
                metadata
            )

            self._tooltip_and_print_values(
                serie_node, serie, bar, i, val, metadata, x_, y_, width, height
            )

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

    def _plot(self):
        """Draw bars for series and secondary series"""
        for serie in self.series:
            self.bar(serie)
        for serie in self.secondary_series:
            self.bar(serie, True)
