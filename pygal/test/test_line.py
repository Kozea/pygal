from pygal.line import Line
from math import cos, sin


def test_simple_line():
    line = Line(800, 600)
    line.add('test1', [cos(x / 10.) for x in range(-30, 30, 5)])
    line.add('test2', [sin(x / 10.) for x in range(-30, 30, 5)])
    line.add('test3', [cos(x / 10.) - sin(x / 10.) for x in range(-30, 30, 5)])
    line.set_labels(map(str, range(-30, 30, 5)))
    line.title = "cos sin and cos - sin"
    line._in_browser()
