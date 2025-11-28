from pygal import Gauge


def test_gauge_reverse_direction():
    """Test that reverse_direction config is respected"""
    gauge = Gauge(reverse_direction=True)
    assert gauge.config.reverse_direction is True

    gauge.add('A', 10)
    gauge.range = (0, 10)
    gauge.setup()

    # When reversed, the polar box should be (0, 1, max, min)
    # min=0, max=10
    # reversed: (0, 1, 10, 0)
    assert gauge._box._tmin == 10
    assert gauge._box._tmax == 0
    assert gauge._box._rmin == 0
    assert gauge._box._rmax == 1

def test_gauge_normal_direction():
    """Test that normal direction works as expected"""
    gauge = Gauge()
    assert gauge.config.reverse_direction is False

    gauge.add('A', 10)
    gauge.range = (0, 10)
    gauge.setup()

    # min=0, max=10
    # normal: (0, 1, 0, 10)
    assert gauge._box._tmin == 0
    assert gauge._box._tmax == 10
    assert gauge._box._rmin == 0
    assert gauge._box._rmax == 1
