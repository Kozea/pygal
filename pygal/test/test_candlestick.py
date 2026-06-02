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
"""Candlestick chart related tests"""

import pytest

import pygal
from pygal import Candlestick


def test_simple_candlestick():
    """Simple candlestick test."""
    chart = Candlestick()
    chart.add('AAPL', [
        (10, 15, 8, 12),
        (12, 18, 10, 11),
        None,
        (11, 14, 9, 14),
    ])
    chart.x_labels = ['Mon', 'Tue', 'Wed', 'Thu']
    q = chart.render_pyquery()

    assert len(q('.axis.y')) == 1
    assert len(q('.legend')) == 1
    assert len(q('.candlesticks .candle')) == 3
    assert len(q('.candlesticks .candle.up')) == 2
    assert len(q('.candlesticks .candle.down')) == 1
    assert len(q('.candlesticks rect.body')) == 3
    assert len(q('.candlesticks path.wick')) == 3


def test_candlestick_is_public_chart():
    """Candlestick is exported by the public API."""
    assert pygal.Candlestick is Candlestick
    assert 'Candlestick' in pygal.CHARTS_BY_NAME


def test_candlestick_axis_uses_all_ohlc_values():
    """Open/high/low/close values all contribute to y-axis bounds."""
    chart = Candlestick()
    chart.add('AAPL', [(10, 100, 1, 11)])
    chart.render()

    assert chart.state is None
    chart.setup()
    try:
        assert chart._min == 1
        assert chart._max == 100
        assert chart._box.ymin <= 1
        assert chart._box.ymax >= 100
    finally:
        chart.teardown()


def test_candlestick_tooltip_formats_ohlc_values():
    """Tooltip text contains each OHLC component."""
    chart = Candlestick()
    chart.add('AAPL', [(10, 15, 8, 12)])
    svg = chart.render(is_unicode=True)

    assert 'Open: 10' in svg
    assert 'High: 15' in svg
    assert 'Low: 8' in svg
    assert 'Close: 12' in svg


def test_candlestick_multiple_series_are_grouped():
    """Multiple OHLC series share each x slot."""
    chart = Candlestick()
    chart.add('AAPL', [(10, 15, 8, 12), (12, 18, 10, 11)])
    chart.add('GOOG', [(20, 25, 18, 24), (24, 28, 22, 23)])
    q = chart.render_pyquery()

    assert len(q('.legend')) == 2
    assert len(q('.candlesticks .candle')) == 4


def test_candlestick_accepts_single_values_as_doji():
    """Single numeric values render as doji candles."""
    chart = Candlestick()
    chart.add('AAPL', [10, 12, None, 11])
    q = chart.render_pyquery()

    assert len(q('.candlesticks .candle')) == 3
    assert len(q('.candlesticks .candle.up')) == 3
    assert len(q('.candlesticks rect.body')) == 3


def test_candlestick_rejects_bad_shape():
    """Candlestick values must be OHLC tuples."""
    chart = Candlestick()
    chart.add('bad', [(1, 2, 3)])

    with pytest.raises(ValueError):
        chart.render()


def test_candlestick_rejects_inconsistent_high_low():
    """High and low must contain open and close values."""
    chart = Candlestick()
    chart.add('bad', [(10, 9, 8, 12)])

    with pytest.raises(ValueError):
        chart.render()
