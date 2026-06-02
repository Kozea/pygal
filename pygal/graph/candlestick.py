# -*- coding: utf-8 -*-
# This file is part of pygal
#
# A python svg graph plotting library
# Copyright 漏 2012-2025 Kozea
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
Candlestick chart: Plot OHLC data points as high/low wicks and open/close
bodies.
"""

from functools import reduce

from pygal._compat import is_list_like
from pygal.adapters import decimal_to_float
from pygal.config import SerieConfig
from pygal.graph.dual import Dual
from pygal.graph.graph import Graph
from pygal.serie import Serie
from pygal.util import alter, cached_property, compose, decorate, ident


class Candlestick(Dual, Graph):
    """Candlestick graph class"""

    _body_width = .6
    _x_adapters = []

    def prepare_values(self, raw, offset=0):
        """Prepare 5-item OHLC values."""
        self._x_adapt = reduce(
            compose, self._x_adapters
        ) if not self.strict and self._x_adapters else ident

        raw = [(
            list(raw_values) if not isinstance(raw_values, dict) else
            raw_values, serie_config_kwargs
        ) for raw_values, serie_config_kwargs in raw]
        series = []

        for raw_values, serie_config_kwargs in raw:
            metadata = {}
            values = []
            for index, raw_value in enumerate(raw_values):
                if isinstance(raw_value, dict):
                    raw_value = dict(raw_value)
                    value = raw_value.pop('value', None)
                    metadata[index] = raw_value
                else:
                    value = raw_value

                if value is None:
                    value = (None, None, None, None, None)
                elif not is_list_like(value):
                    value = (index, value, value, value, value)
                elif len(value) == 4:
                    value = (index, ) + tuple(value)
                elif len(value) != 5:
                    raise ValueError(
                        'Candlestick values must be '
                        '(x, open, high, low, close) or '
                        '(open, high, low, close) tuples'
                    )
                value = (
                    self._x_adapt(value[0]),
                    decimal_to_float(value[1]),
                    decimal_to_float(value[2]),
                    decimal_to_float(value[3]),
                    decimal_to_float(value[4])
                )
                values.append(value)

            serie_config = SerieConfig()
            serie_config(
                **dict((k, v) for k, v in self.state.__dict__.items()
                       if k in dir(serie_config))
            )
            serie_config(**serie_config_kwargs)
            series.append(
                Serie(offset + len(series), values, serie_config, metadata)
            )
        return series

    @cached_property
    def xvals(self):
        """All x values"""
        return [
            val[0] for serie in self.all_series for val in serie.values
            if val[0] is not None
        ]

    @cached_property
    def yvals(self):
        """All OHLC y values"""
        return [
            ohlc for serie in self.series for val in serie.values
            for ohlc in val[1:] if ohlc is not None
        ]

    @cached_property
    def _values(self):
        """Getter for primary values"""
        return self.yvals

    @cached_property
    def _secondary_values(self):
        """Getter for secondary values."""
        return [
            ohlc for serie in self.secondary_series for val in serie.values
            for ohlc in val[1:] if ohlc is not None
        ]

    def _value_format(self, value):
        """Format an OHLC value for tooltips."""
        x, open_, high, low, close = value
        return '%s: open=%s high=%s low=%s close=%s' % (
            self._x_format(x), self._y_format(open_), self._y_format(high),
            self._y_format(low), self._y_format(close)
        )

    def _compute(self):
        """Compute x/y min and max and x/y scale."""
        if self.xvals:
            xmin = min(self.xvals)
            xmax = max(self.xvals)
            if self.xrange:
                xmin = self._x_adapt(self.xrange[0])
                xmax = self._x_adapt(self.xrange[1])
            if xmin == xmax:
                xmin -= 1
                xmax += 1
            self._box.xmin, self._box.xmax = xmin, xmax

        if self.yvals:
            ymin = self.range[0] if (
                self.range and self.range[0] is not None
            ) else min(self.yvals)
            ymax = self.range[1] if (
                self.range and self.range[1] is not None
            ) else max(self.yvals)
            if self.include_x_axis:
                ymin = min(ymin, 0)
                ymax = max(ymax, 0)
            self._box.ymin, self._box.ymax = ymin, ymax

        for serie in self.all_series:
            serie.points = serie.values

    def _plot(self):
        """Draw candlesticks for all primary series."""
        for serie in self.all_series:
            self.candlesticks(serie)

    def candlesticks(self, serie):
        """Draw one candlestick serie."""
        serie_node = self.svg.serie(serie)
        group = self.svg.node(serie_node['plot'], class_='candlesticks')
        width = self._candlestick_width()

        for i, value in enumerate(serie.points):
            x, open_, high, low, close = value
            if None in value:
                continue

            metadata = serie.metadata.get(i)
            candle = decorate(
                self.svg, self.svg.node(group, class_='candlestick'), metadata
            )
            x_pos = self.view.x(x)
            open_y = self.view.y(open_)
            high_y = self.view.y(high)
            low_y = self.view.y(low)
            close_y = self.view.y(close)
            top = min(open_y, close_y)
            body_height = abs(close_y - open_y)
            class_ = 'rect reactive tooltip-trigger %s' % (
                'rising' if close >= open_ else 'falling'
            )

            self.svg.node(
                candle,
                'line',
                x1=x_pos,
                x2=x_pos,
                y1=high_y,
                y2=low_y,
                class_='wick'
            )
            alter(
                self.svg.node(
                    candle,
                    'rect',
                    x=x_pos - width / 2,
                    y=top,
                    width=width,
                    height=max(body_height, 1),
                    class_=class_
                ), metadata
            )

            val = self._format(serie, i)
            self._tooltip_data(candle, val, x_pos, (high_y + low_y) / 2)
            self._static_value(
                serie_node, val, x_pos + width / 2,
                top - self.style.value_font_size / 2, metadata
            )

    def _candlestick_width(self):
        """Return the body width in view coordinates."""
        if self._box.xmax == self._box.xmin:
            return 1
        values_count = max(len(serie.values) for serie in self.series) or 1
        return (
            self.view.width / max(values_count, 1) * self._body_width
        )
