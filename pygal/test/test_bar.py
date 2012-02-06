from pygal.bar import Bar
from math import cos, sin


def test_simple_bar():
    bar = Bar(800, 600, precision=2, format='f')
    rng = [12, 3, 30, 4, 40, 10, 9, 2]
    bar.add('test1', rng)
    bar.x_labels = map(str, rng)
    bar.title = "Bar test"
    bar._in_browser()
