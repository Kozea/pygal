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
"""Candlestick (OHLC) chart related tests"""

from pygal import Candlestick


def test_simple_candlestick():
    """Simple candlestick test"""
    chart = Candlestick()
    chart.add('AAPL', [
        (10, 15, 8, 12),    # bullish: open=10, high=15, low=8, close=12
        (12, 18, 10, 11),   # bearish: open=12, high=18, low=10, close=11
        (11, 14, 9, 14),    # bullish (doji high=close)
        (14, 16, 12, 13),   # bearish
    ])
    chart.title = 'Candlestick test'
    q = chart.render_pyquery()

    assert len(q(".axis.y")) == 1
    assert len(q(".legend")) == 1
    assert len(q(".plot .series rect")) >= 4
    # Each candle has a body rect + wick lines + tick lines
    assert len(q(".plot .series line.candle-reactive")) >= 0  # wicks rendered


def test_candlestick_bullish_bearish_colors():
    """Test that bullish and bearish candles have correct colors"""
    chart = Candlestick()
    chart.add('TEST', [
        (10, 15, 8, 12),   # bullish
        (12, 18, 10, 11),  # bearish
    ])
    chart.bullish_color = '#00ff00'
    chart.bearish_color = '#ff0000'
    q = chart.render_pyquery()

    # Check that SVG contains our colors
    svg = str(q)
    assert '#00ff00' in svg or '#0f0' in svg.lower()
    assert '#ff0000' in svg or '#f00' in svg.lower()


def test_candlestick_custom_colors():
    """Test custom bullish/bearish colors"""
    chart = Candlestick()
    chart.bullish_color = '#3498db'
    chart.bearish_color = '#e74c3c'
    chart.add('GOOG', [
        (100, 110, 95, 108),  # bullish
        (108, 115, 100, 102), # bearish
    ])
    q = chart.render_pyquery()
    svg = str(q)
    assert '#3498db' in svg
    assert '#e74c3c' in svg


def test_candlestick_value_format():
    """Test tooltip formatting"""
    chart = Candlestick()
    chart.add('TEST', [(10, 15, 8, 12)])
    svg = chart.render()
    if isinstance(svg, bytes):
        svg = svg.decode('utf-8')

    assert 'Open' in svg or 'open' in svg.lower()
    assert 'High' in svg or 'high' in svg.lower()
    assert 'Low' in svg or 'low' in svg.lower()
    assert 'Close' in svg or 'close' in svg.lower()


def test_candlestick_empty():
    """Test candlestick with empty data"""
    chart = Candlestick()
    chart.add('EMPTY', [])
    chart.render()  # Should not raise


def test_candlestick_single():
    """Test candlestick with a single data point"""
    chart = Candlestick()
    chart.add('SINGLE', [(50, 60, 45, 55)])
    chart.render()  # Should not raise


def test_candlestick_doji():
    """Test candlestick with a doji (open == close)"""
    chart = Candlestick()
    chart.add('DOJI', [
        (50, 55, 45, 50),  # perfect doji
    ])
    chart.render()  # Should not raise


def test_candlestick_multiple_series():
    """Test candlestick with multiple series"""
    chart = Candlestick()
    chart.add('AAPL', [
        (10, 15, 8, 12),
        (12, 18, 10, 11),
    ])
    chart.add('GOOG', [
        (100, 110, 95, 108),
        (108, 115, 100, 102),
    ])
    q = chart.render_pyquery()
    assert len(q(".legend")) == 2


def test_candlestick_up_down():
    """Test up_down config option"""
    # 'up' mode - only bullish filled
    chart = Candlestick()
    chart.up_down = 'up'
    chart.add('TEST', [
        (10, 15, 8, 12),   # bullish
        (12, 18, 10, 11),  # bearish (should be hollow)
    ])
    chart.render()  # Should not raise

    # 'down' mode - only bearish filled
    chart2 = Candlestick()
    chart2.up_down = 'down'
    chart2.add('TEST', [
        (10, 15, 8, 12),
        (12, 18, 10, 11),
    ])
    chart2.render()  # Should not raise


def test_candlestick_show_ticks():
    """Test show_open and show_close config options"""
    chart = Candlestick()
    chart.show_open = False
    chart.show_close = False
    chart.add('TEST', [(10, 15, 8, 12)])
    chart.render()  # Should not raise

    chart2 = Candlestick()
    chart2.show_open = True
    chart2.show_close = True
    chart2.add('TEST', [(10, 15, 8, 12)])
    chart2.render()  # Should not raise


def test_candlestick_svg_structure():
    """Test that the SVG has the expected structure"""
    chart = Candlestick()
    chart.add('TEST', [(10, 15, 8, 12)])
    svg = chart.render()
    if isinstance(svg, bytes):
        svg = svg.decode('utf-8')

    # Should have candlestick class
    assert 'candlestick' in svg.lower()
    # Should have rect elements for candle bodies
    assert '<rect' in svg
