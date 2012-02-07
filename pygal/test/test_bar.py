from pygal.bar import Bar
from math import cos, sin


def test_simple_bar():
    bar = Bar(800, 600)
    rng = [12, 3, 30, 4, 40, 10, 9, 2]
    bar.add('test1', rng)
    bar.x_labels = map(str, rng)
    bar.title = "Bar test"
    bar.render()


def test_null_bar():
    bar = Bar(800, 600, scale=.25)
    rng = [1, 1]
    bar.add('test1', rng)
    bar.x_labels = map(str, rng)
    bar.title = "Bar test"
    bar._in_browser()
