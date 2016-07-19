from unittest import TestCase
from pygal import Gauge


class TestGauge(TestCase):
    def test_chartplots(self):
        gauge_chart = Gauge(human_readable =True)
        gauge_chart.title = 'DeltaBlue V8 benchmark results'
        gauge_chart.range = [0, 10000]
        gauge_chart.add('Chrome', 8212)
        gauge_chart.add('Firefox', 8099)
        gauge_chart.add('Opera', 2933)
        gauge_chart.add('IE', 41)

        assert gauge_chart.render()

    def test_anticclockplots(self):

        gauge_chartcwise = Gauge(human_readable = True,clockwise = True)

        gauge_chartcwise.title = 'DeltaBlue V8 benchmark results'
        gauge_chartcwise.range = [0, 10000]
        gauge_chartcwise.add('Chrome', 8212)
        gauge_chartcwise.add('Firefox', 8099)
        gauge_chartcwise.add('Opera', 2933)
        gauge_chartcwise.add('IE', 41)

        assert gauge_chartcwise.render()
