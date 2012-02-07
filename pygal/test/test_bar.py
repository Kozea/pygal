from pygal.bar import Bar
from math import cos, sin


def test_simple_bar():
    bar = Bar()
    rng = [-3, -32, -39]
    bar.add('test1', rng)
    bar.add('test2', map(abs, rng))
    bar.x_labels = map(str, rng)
    bar.title = "Bar test"
    bar._in_browser()
