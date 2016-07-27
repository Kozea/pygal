from pygal import Gauge

def test_render():
    """Tests that a gauge plots"""
    chart = Gauge()
    chart.range = [0,40]
    chart.add('Connor', 21)
    chart.add('Mike', 30)
    chart.add('Jules', 10)
    assert chart.render()
