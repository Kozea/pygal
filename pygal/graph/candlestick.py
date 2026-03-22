# -*- coding: utf-8 -*-
# This file is part of pygal
#
# A python svg graph plotting library
# Copyright © 2012-2025 Kozea
#
# This library is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with pygal. If not, see <http://www.gnu.org/licenses/>.

"""
Candlestick (OHLC) chart: displays open, high, low, close price data
as candlestick bars with wicks.

Each data point is a 4-element tuple: (open, high, low, close)
"""

from pygal.graph.graph import Graph
from pygal.util import alter, decorate


class Candlestick(Graph):
    """
    Candlestick (OHLC) chart.

    Each data point should be a 4-tuple: (open, high, low, close).

    When close >= open, the candle is bullish (green by default).
    When close < open, the candle is bearish (red by default).

    Config options:
        - bullish_color: color for bullish candles (default: '#00cc00')
        - bearish_color: color for bearish candles (default: '#cc0000')
        - close_color: color for the close price indicator line
        - show_close: whether to show a small line at the close price
        - show_open: whether to show a small line at the open price
        - up_down: 'up'/'down' to only show candles of that type as filled,
                   'both' (default) to fill all candles
        - box_mode: ignored (kept for compat)
    """

    _series_margin = .06

    def _value_format(self, value, serie):
        """Format value for tooltip display."""
        if not isinstance(value, (list, tuple)) or len(value) != 4:
            return self._y_format(value)

        open_val, high_val, low_val, close_val = value
        return (
            'Open : %s\nHigh : %s\nLow  : %s\nClose: %s' %
            tuple(map(self._y_format, value))
        )

    def _compute(self):
        """Compute x positions and y range."""
        for serie in self.series:
            # Each value should be (open, high, low, close)
            points = []
            for v in serie.values:
                if isinstance(v, (list, tuple)) and len(v) == 4:
                    points.append(tuple(v))
                else:
                    points.append((0, 0, 0, 0))
            serie.points = points

        self._x_pos = [(i + .5) / self._order for i in range(self._order)]

    @property
    def _values(self):
        """Flatten OHLC tuples into individual numeric values for range calc."""
        values = []
        for serie in self.series:
            for val in serie.values:
                if val is not None:
                    if isinstance(val, (list, tuple)):
                        values.extend(val)
                    else:
                        values.append(val)
        return values

    def _plot(self):
        """Plot the candlestick series."""
        for serie in self.series:
            self._candlestickf(serie)

    def _candlestickf(self, serie):
        """Draw candlestick bars for a series."""
        serie_node = self.svg.serie(serie)
        candles = self.svg.node(serie_node['plot'], class_="candlesticks")

        metadata = serie.metadata.get(0)

        for i, point in enumerate(serie.points):
            if not point or len(point) != 4:
                continue

            open_val, high_val, low_val, close_val = point
            is_bullish = close_val >= open_val

            metadata = serie.metadata.get(i)
            candle_node = decorate(
                self.svg, self.svg.node(candles, class_='candle'), metadata
            )

            x_center, y_center = self._draw_candle(
                candle_node, open_val, high_val, low_val, close_val,
                i, serie.index, is_bullish, metadata
            )

            val = self._format(serie, i)
            self._tooltip_data(
                candle_node, val, x_center, y_center, "centered",
                self._get_x_label(i)
            )

    def _draw_candle(self, parent_node, open_val, high_val, low_val,
                     close_val, candle_index, serie_index, is_bullish,
                     metadata):
        """Draw a single candlestick and return its center."""
        width = (self.view.x(1) - self.view.x(0)) / self._order
        series_margin = width * self._series_margin
        left_edge = self.view.x(0) + width * candle_index + series_margin
        body_width = width - 2 * series_margin
        mid_x = left_edge + body_width / 2

        bullish_color = getattr(self.config, 'bullish_color', '#00cc00')
        bearish_color = getattr(self.config, 'bearish_color', '#cc0000')

        color = bullish_color if is_bullish else bearish_color
        fill_color = color
        # For hollow candles: bullish = hollow (stroke only), bearish = filled
        up_down = getattr(self.config, 'up_down', 'both')

        if up_down == 'up' and not is_bullish:
            fill_color = 'none'
        elif up_down == 'down' and is_bullish:
            fill_color = 'none'

        # High-Low wick (shadow line)
        alter(
            self.svg.line(
                parent_node,
                coords=[(mid_x, self.view.y(high_val)),
                        (mid_x, self.view.y(low_val))],
                class_='reactive tooltip-trigger',
                attrib={
                    'stroke': color,
                    'stroke-width': 1.5
                }
            ), metadata
        )

        # Candle body (rect from open to close)
        y_top = self.view.y(max(open_val, close_val))
        y_bottom = self.view.y(min(open_val, close_val))
        body_height = y_bottom - y_top

        # Ensure minimum visible height for doji candles
        if body_height < 1:
            body_height = 1

        alter(
            self.svg.node(
                parent_node,
                tag='rect',
                x=left_edge,
                y=y_top,
                height=body_height,
                width=body_width,
                fill=fill_color,
                stroke=color,
                class_='reactive tooltip-trigger'
            ), metadata
        )

        # Open price tick mark
        show_open = getattr(self.config, 'show_open', True)
        if show_open:
            alter(
                self.svg.line(
                    parent_node,
                    coords=[(left_edge, self.view.y(open_val)),
                            (mid_x, self.view.y(open_val))],
                    class_='reactive tooltip-trigger',
                    attrib={
                        'stroke': color,
                        'stroke-width': 1.5
                    }
                ), metadata
            )

        # Close price tick mark
        show_close = getattr(self.config, 'show_close', True)
        if show_close:
            alter(
                self.svg.line(
                    parent_node,
                    coords=[(mid_x, self.view.y(close_val)),
                            (left_edge + body_width, self.view.y(close_val))],
                    class_='reactive tooltip-trigger',
                    attrib={
                        'stroke': color,
                        'stroke-width': 1.5
                    }
                ), metadata
            )

        return (
            mid_x,
            self.view.y((high_val + low_val) / 2)
        )
