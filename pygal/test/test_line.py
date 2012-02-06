from pygal.line import Line
from pygal.style import LightStyle
from math import cos, sin


def test_simple_line():
    line = Line(800, 600, style=LightStyle, precision=2, format='f')
    rng = range(-30, 30, 5)
    line.add('test1', [cos(x / 10.) for x in rng])
    line.add('test2', [sin(x / 10.) for x in rng])
    line.add('test3', [cos(x / 10.) - sin(x / 10.) for x in rng])
    line.x_labels = map(str, rng)
    line.title = "cos sin and cos - sin"
    line._in_browser()
