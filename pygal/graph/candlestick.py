# -*- coding: utf-8 -*-
# This file is part of pygal
#
# A python svg graph plotting library
# Copyright © 2012-2025 Kozea
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
Candlestick chart: display open-high-low-close data as financial candles.
"""

from pygal.graph.dual import Dual
from pygal.graph.graph import Graph
from pygal.util import alter, cached_property, decorate


class Candlestick(Dual, Graph):
    """Candlestick graph class"""

    _candle_margin = .2

    @cached_property
    def xvals(self):
        """All x values"""
        return [
            val[0] for serie in self.all_series for val in serie.values
            if val[0] is not None
        ]

    @cached_property
    def yvals(self):
        """All open, high, low and close values"""
        return [
            y for serie in self.series for val in serie.values
            for y in val[1:] if y is not None
        ]

    @cached_property
    def _values(self):
        """Getter for series values (flattened)"""
        return self.yvals

    @cached_property
    def _secondary_values(self):
        """Getter for secondary series values (flattened)"""
        return [
            y for serie in self.secondary_series for val in serie.values
            for y in val[1:] if y is not None
        ]

    def _value_format(self, value):
        """Format value for tooltip display."""
        x, open_, high, low, close = value
        return (
            '%s\nOpen: %s\nHigh: %s\nLow: %s\nClose: %s' % (
                self._x_format(x), self._y_format(open_),
                self._y_format(high), self._y_format(low),
                self._y_format(close)
            )
        )

    def _compute(self):
        """Compute x/y min and max and candle points."""
        if self.xvals:
            if self.xrange:
                x_adapter = getattr(self, '_x_adapt', None) or (lambda x: x)
                xmin = x_adapter(self.xrange[0])
                xmax = x_adapter(self.xrange[1])
            else:
                xmin = min(self.xvals)
                xmax = max(self.xvals)
                xstep = self._x_step()
                xmin -= xstep / 2
                xmax += xstep / 2
            self._box.xmin, self._box.xmax = xmin, xmax

        if self.yvals:
            ymin = min(self.yvals)
            ymax = max(self.yvals)
            if self.include_x_axis:
                ymin = min(ymin, 0)
                ymax = max(ymax, 0)
            self._box.ymin, self._box.ymax = ymin, ymax

        if self.range and self.range[0] is not None:
            self._box.ymin = self.range[0]
        if self.range and self.range[1] is not None:
            self._box.ymax = self.range[1]

        for serie in self.all_series:
            serie.points = serie.values

    def _plot(self):
        """Draw candles for series and secondary series."""
        for serie in self.series:
            self.candles(serie)
        for serie in self.secondary_series:
            self.candles(serie, True)

    def candles(self, serie, rescale=False):
        """Draw a candlestick series."""
        serie_node = self.svg.serie(serie)
        group = self.svg.node(serie_node['plot'], class_='candlesticks')
        points = self._rescale_ohlc(serie.points) if rescale else serie.points

        for i, value in enumerate(points):
            x, open_, high, low, close = value
            if None in value or (self.logarithmic and min(value[1:]) <= 0):
                continue

            metadata = serie.metadata.get(i)
            candle = decorate(
                self.svg, self.svg.node(
                    group,
                    class_='candlestick %s' % (
                        'rising' if close >= open_ else 'falling'
                    )
                ), metadata
            )
            self._draw_candle(candle, x, open_, high, low, close, metadata)

            x_px = self.view.x(x)
            y_px = self.view.y((open_ + close) / 2)
            val = self._format(serie, i)
            self._tooltip_data(candle, val, x_px, y_px, "centered")
            self._static_value(serie_node, val, x_px, y_px, metadata, "middle")

    def _draw_candle(self, parent, x, open_, high, low, close, metadata):
        """Draw the wick and candle body for one OHLC point."""
        x_px = self.view.x(x)
        high_y = self.view.y(high)
        low_y = self.view.y(low)
        open_y = self.view.y(open_)
        close_y = self.view.y(close)

        width = self._candle_width()
        left = x_px - width / 2
        body_y = min(open_y, close_y)
        body_height = max(abs(close_y - open_y), 1)

        alter(
            self.svg.line(
                parent,
                coords=[(x_px, high_y), (x_px, low_y)],
                class_='wick reactive',
                attrib={'stroke-width': 2}
            ), metadata
        )
        alter(
            self.svg.node(
                parent,
                tag='rect',
                x=left,
                y=body_y,
                width=width,
                height=body_height,
                class_='body reactive tooltip-trigger'
            ), metadata
        )

    def _candle_width(self):
        """Compute candle body width in pixels."""
        x_values = sorted(set(self.xvals))
        if len(x_values) > 1:
            pixel_gaps = [
                abs(self.view.x(right) - self.view.x(left))
                for left, right in zip(x_values, x_values[1:])
            ]
            return max(1, min(pixel_gaps) * (1 - self._candle_margin))
        return max(1, self.view.width / 5)

    def _x_step(self):
        """Return the smallest x gap, or 1 for a single candle."""
        x_values = sorted(set(self.xvals))
        if len(x_values) > 1:
            return min(
                right - left for left, right in zip(x_values, x_values[1:])
            )
        return 1

    def _rescale_ohlc(self, points):
        """Scale secondary-axis OHLC points onto the primary y axis."""
        return [
            (x, ) + tuple(
                self._scale_diff + (y - self._scale_min_2nd) * self._scale
                if y is not None else None for y in value[1:]
            )
            for value in points
            for x in (value[0], )
        ]
