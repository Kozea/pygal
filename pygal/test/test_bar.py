from pygal.bar import Bar
from math import cos, sin


def test_simple_bar():
    bar = Bar()
    rng = [12, 3, 30, -5, 40, 10, 9, 2]
    bar.add('test1', rng)
    bar.x_labels = map(str, rng)
    bar.title = "Bar test"
    bar._in_browser()
