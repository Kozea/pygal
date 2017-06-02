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
Histogram chart: like a bar chart but with data plotted along a x axis
as bars of varying width.
"""

from __future__ import division

from pygal.graph.bar import Bar
from pygal.graph.dual import Dual
from pygal.util import alter, cached_property, decorate


class Histogram(Dual, Bar):

    """Histogram chart class"""
    _series_margin = 0

    @cached_property
    def _values(self):
        """Getter for secondary series values (flattened)"""
        return self.yvals

    @cached_property
    def _secondary_values(self):
        """Getter for secondary series values (flattened)"""
        return [val[0]
                for serie in self.secondary_series
                for val in serie.values
                if val[0] is not None]

    @cached_property
    def xvals(self):
        """All x values"""
        return [val
                for serie in self.all_series
                for dval in serie.values
                for val in dval[1:3]
                if val is not None]

    @cached_property
    def yvals(self):
        """All y values"""
        return [val[0]
                for serie in self.series
                for val in serie.values
                if val[0] is not None]

    def _bar(self, serie, parent, x0, x1, y, i, zero, secondary=False):
        """Internal bar drawing function"""
        x, y = self.view((x0, y))
        x1, _ = self.view((x1, y))
        width = x1 - x
        height = self.view.y(zero) - y
        series_margin = width * self._series_margin
        x += series_margin
        width -= 2 * series_margin

        r = serie.rounded_bars * 1 if serie.rounded_bars else 0
        alter(self.svg.transposable_node(
            parent, 'rect',
            x=x, y=y, rx=r, ry=r, width=width, height=height,
            class_='rect reactive tooltip-trigger'), serie.metadata.get(i))
        return x, y, width, height

    def bar(self, serie, rescale=False):
        """Draw a bar graph for a serie"""
        serie_node = self.svg.serie(serie)
        bars = self.svg.node(serie_node['plot'], class_="histbars")
        points = serie.points

        for i, (y, x0, x1) in enumerate(points):
            if None in (x0, x1, y) or (self.logarithmic and y <= 0):
                continue
            metadata = serie.metadata.get(i)

            bar = decorate(
                self.svg,
                self.svg.node(bars, class_='histbar'),
                metadata)
            val = self._format(serie, i)

            bounds = self._bar(
                serie, bar, x0, x1, y, i, self.zero, secondary=rescale)
            self._tooltip_and_print_values(
                serie_node, serie, bar, i, val, metadata, *bounds)

    def _compute(self):
        """Compute x/y min and max and x/y scale and set labels"""
        if self.xvals:
            xmin = min(self.xvals)
            xmax = max(self.xvals)
            xrng = (xmax - xmin)
        else:
            xrng = None

        if self.yvals:
            ymin = min(min(self.yvals), self.zero)
            ymax = max(max(self.yvals), self.zero)
            yrng = (ymax - ymin)
        else:
            yrng = None

        for serie in self.all_series:
            serie.points = serie.values

        if xrng:
            self._box.xmin, self._box.xmax = xmin, xmax
        if yrng:
            self._box.ymin, self._box.ymax = ymin, ymax

        if self.range and self.range[0] is not None:
            self._box.ymin = self.range[0]

        if self.range and self.range[1] is not None:
            self._box.ymax = self.range[1]
