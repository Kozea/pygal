from pygal import Gauge
import pytest

def test_render():
    """Tests that a gauge plots"""
    chart = Gauge()
    chart.range = [0,40]
    chart.add('Connor', 21)
    chart.add('Mike', 30)
    chart.add('Jules', 10)
    assert chart.render()


def test_ccrender():
    """Tests that a clockwise gauge plots"""
    clock_chart = Gauge(clockwise=True)
    clock_chart.range = [0, 40]
    clock_chart.add('Connor', 21)
    clock_chart.add('Mike', 30)
    clock_chart.add('Jules', 10)
    assert clock_chart.render()

def test_difference():
    """Tests the difference between a clockwise and counter clockwise graph"""
    chart = Gauge()
    chart.range = [0, 10000]
    chart.add('Chrome', 8212)
    chart.add('Firefox', 8099)
    chart.add('Opera', 2933)
    chart.add('IE', 41)

    clock_chart = Gauge(clockwise=True)
    clock_chart.range = [0, 10000]
    clock_chart.add('Chrome', 8212)
    clock_chart.add('Firefox', 8099)
    clock_chart.add('Opera', 2933)
    clock_chart.add('IE', 41)
    assert clock_chart.render() != chart.render()


