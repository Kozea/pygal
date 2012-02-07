from pygal.line import Line
from pygal.config import Config
from math import cos, sin


def test_simple_line():
    line = Line(Config(scale=.5))
    rng = range(-30, 31, 5)
    line.add('test1', [cos(x / 10.) for x in rng])
    line.add('test2', [sin(x / 10.) for x in rng])
    line.add('test3', [cos(x / 10.) - sin(x / 10.) for x in rng])
    line.x_labels = map(str, rng)
    line.title = "cos sin and cos - sin"
    line._in_browser()


def test_line():
    line = Line()
    rng = [8, 12, 23, 73, 39, 57]
    line.add('-_-', rng)
    line.x_labels = map(str, rng)
    line.title = "cos sin and cos - sin"
    line._in_browser()


def test_one_dot():
    line = Line()
    line.add('one dot', [12])
    line.x_labels = ['one']
    line.render()


def test_no_dot():
    line = Line()
    line.add('no dot', [])
    line.render()


def test_no_dot_at_all():
    line = Line()
    line.render()
