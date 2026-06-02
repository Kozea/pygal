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
"""Candlestick chart: display open-high-low-close market data."""

from pygal.graph.graph import Graph
from pygal.util import alter, cached_property, decorate


class Candlestick(Graph):
    """
    Candlestick chart.

    Values must be ``(open, high, low, close)`` tuples. Single numeric values
    render as doji candles for compatibility with generic graph helpers.
    ``None`` values are allowed and render as gaps.
    """

    _series_margin = .06
    _serie_margin = .08

    @staticmethod
    def _is_ohlc(value):
        """Return whether a value looks like an OHLC tuple."""
        return isinstance(value, (list, tuple)) and len(value) == 4

    def _prices(self, value):
        """Yield adapted price values for axis scaling."""
        if value is None:
            return
        if self._is_ohlc(value):
            values = value
        elif isinstance(value, (list, tuple)):
            return
        else:
            values = (value, )

        for price in values:
            if price is not None:
                price = self._adapt(price)
                if price is not None:
                    yield price

    def _normalize_ohlc(self, value):
        """Validate and adapt a raw OHLC value."""
        if value is None:
            return None
        if not self._is_ohlc(value):
            if isinstance(value, (list, tuple)):
                raise ValueError(
                    'Candlestick values must be '
                    '(open, high, low, close) tuples'
                )
            value = self._adapt(value)
            if value is None:
                return None
            return (value, value, value, value)

        open_, high, low, close = value
        if None in value:
            return None
        open_, high, low, close = tuple(
            map(self._adapt, (open_, high, low, close))
        )
        if None in (open_, high, low, close):
            return None
        if high < max(open_, close) or low > min(open_, close):
            raise ValueError(
                'Candlestick high/low values must contain open and close'
            )
        return open_, high, low, close

    @cached_property
    def _values(self):
        """Flatten OHLC tuples into numeric values for y-axis scaling."""
        return [
            price
            for serie in self.series
            for value in serie.values
            for price in self._prices(value)
        ]

    @cached_property
    def _secondary_values(self):
        """Flatten secondary OHLC tuples into numeric values."""
        return [
            price
            for serie in self.secondary_series
            for value in serie.values
            for price in self._prices(value)
        ]

    def _value_format(self, value):
        """Format OHLC values for tooltip display."""
        if value is None:
            return ''
        if not self._is_ohlc(value):
            return self._y_format(value)
        open_, high, low, close = value
        return 'Open: %s\nHigh: %s\nLow: %s\nClose: %s' % (
            self._y_format(open_),
            self._y_format(high),
            self._y_format(low),
            self._y_format(close),
        )

    def _compute(self):
        """Compute axes and normalize series values."""
        self.interpolate = None

        if self._values:
            if self.include_x_axis:
                self._box.ymin = min(self._min, self.zero)
                self._box.ymax = max(self._max, self.zero)
            else:
                self._box.ymin = self._min
                self._box.ymax = self._max

        self._x_pos = [
            x / self._len for x in range(self._len + 1)
        ] if self._len > 1 else [0, 1]
        self._points(self._x_pos)
        self._x_pos = [(i + .5) / self._len for i in range(self._len)] \
            if self._len else []

        for serie in self.all_series:
            serie.points = [
                (self._x_pos[i], self._normalize_ohlc(value))
                for i, value in enumerate(serie.values)
            ]

    def _plot(self):
        """Draw candlesticks for each series."""
        for serie in self.series:
            self.candlesticks(serie)
        for serie in self.secondary_series:
            self.candlesticks(serie)

    def candlesticks(self, serie):
        """Draw an OHLC candlestick series."""
        serie_node = self.svg.serie(serie)
        candles = self.svg.node(serie_node['plot'], class_='candlesticks')

        for index, (x_pos, value) in enumerate(serie.points):
            if value is None:
                continue

            metadata = serie.metadata.get(index)
            open_, high, low, close = value
            direction = 'up' if close >= open_ else 'down'
            candle = decorate(
                self.svg,
                self.svg.node(candles, class_='candle %s' % direction),
                metadata
            )

            x, y = self._draw_candle(
                candle, x_pos, open_, high, low, close, serie.index, metadata
            )
            self._tooltip_data(
                candle, self._format(serie, index), x, y,
                xlabel=self._get_x_label(index)
            )
            self._static_value(
                serie_node, self._format(serie, index), x, y,
                metadata, 'middle'
            )

    def _draw_candle(
            self, node, x_pos, open_, high, low, close, serie_index, metadata
    ):
        """Draw a single candle and return its visual center."""
        slot_width = self.view.width / (self._len or 1)
        slot_left = self.view.x(x_pos) - slot_width / 2
        series_margin = slot_width * self._series_margin
        series_width = slot_width - 2 * series_margin
        candle_slot_width = series_width / (self._order or 1)
        candle_left = (
            slot_left + series_margin + serie_index * candle_slot_width
        )
        serie_margin = candle_slot_width * self._serie_margin
        candle_left += serie_margin
        candle_width = max(candle_slot_width - 2 * serie_margin, 1)
        center_x = candle_left + candle_width / 2

        high_y = self.view.y(high)
        low_y = self.view.y(low)
        open_y = self.view.y(open_)
        close_y = self.view.y(close)
        body_y = min(open_y, close_y)
        body_height = max(abs(close_y - open_y), 1)

        alter(
            self.svg.line(
                node,
                coords=[(center_x, high_y), (center_x, low_y)],
                class_='wick reactive',
                attrib={'stroke-width': 1.5}
            ), metadata
        )

        body_class = 'body reactive tooltip-trigger'
        if close >= open_:
            body_class += ' subtle-fill'
        alter(
            self.svg.node(
                node,
                tag='rect',
                x=candle_left,
                y=body_y,
                width=candle_width,
                height=body_height,
                class_=body_class,
                attrib={'stroke-width': 1.5}
            ), metadata
        )

        return center_x, (high_y + low_y) / 2
