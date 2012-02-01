from pygal.line import Line


def test_simple_line():
    line = Line(800, 600)
    line.add('test', [10, 20, 5, 17])
    line._in_browser()
