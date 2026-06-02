# -*- coding: utf-8 -*-
# This file is part of pygal
"""Candlestick chart related tests"""

import pygal
from pygal.test.utils import texts


def test_simple_candlestick():
    """Simple candlestick test"""
    chart = pygal.Candlestick()
    chart.add('Price', [
        (1, 10, 15, 8, 12),
        (2, 12, 18, 11, 9),
        (3, 9, 13, 7, 13),
    ])
    q = chart.render_pyquery()
    assert len(q(".axis.x")) == 1
    assert len(q(".axis.y")) == 1
    assert len(q(".plot .series .candlestick")) == 3
    assert len(q(".plot .series .wick")) == 3
    assert len(q(".plot .series rect.tooltip-trigger")) == 3
    assert len(q(".plot .series rect.rising")) == 2
    assert len(q(".plot .series rect.falling")) == 1


def test_candlestick_formatting_and_metadata():
    """Candlestick values support metadata and default formatting"""
    chart = pygal.Candlestick(print_labels=True)
    chart.add('Price', [
        {
            'value': (1, 10, 15, 8, 12),
            'label': 'Session A',
        }
    ])
    q = chart.render_pyquery()
    assert 'Session A' in q('desc').map(texts)
    assert 'open=10' in q('desc.value').text()
    assert 'high=15' in q('desc.value').text()
    assert 'low=8' in q('desc.value').text()
    assert 'close=12' in q('desc.value').text()


def test_candlestick_public_api():
    """Candlestick is available through pygal's public chart registry"""
    assert pygal.Candlestick in pygal.CHARTS
    assert pygal.CHARTS_BY_NAME['Candlestick'] is pygal.Candlestick
