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

import pygal
from pygal import Candlestick
from pygal.test.utils import texts


def test_candlestick_is_exported():
    """Candlestick is available from the public pygal namespace."""
    assert pygal.Candlestick is Candlestick


def test_simple_candlestick():
    """Simple candlestick chart test"""
    chart = Candlestick(truncate_label=1000)
    chart.add('OHLC', [
        (1, 10, 15, 8, 14),
        (2, 14, 16, 11, 12),
        (3, 12, 18, 10, 12),
    ])
    q = chart.render_pyquery()

    assert len(q(".axis.x")) == 1
    assert len(q(".axis.y")) == 1
    assert len(q(".candlestick")) == 3
    assert len(q(".candlestick .wick")) == 3
    assert len(q(".candlestick .body")) == 3
    assert len(q(".candlestick.rising")) == 2
    assert len(q(".candlestick.falling")) == 1
    x_labels = q(".axis.x text").map(texts)
    assert '1' in x_labels
    assert '2' in x_labels
    assert '3' in x_labels


def test_candlestick_accepts_ohlc_without_x_value():
    """Four-value OHLC tuples use the value index as x."""
    chart = Candlestick(truncate_label=1000)
    chart.add('OHLC', [
        (10, 15, 8, 14),
        (14, 16, 11, 12),
    ])
    q = chart.render_pyquery()

    assert len(q(".candlestick")) == 2
    x_labels = q(".axis.x text").map(texts)
    assert '0' in x_labels
    assert '1' in x_labels
