# This file is test file for NoneMaxSolved
# I have modified the line.py and passed other test
# This test is for us to test whether the none value
# in the Log graph will be max or not (issue #309)

from __future__ import division

from pygal import Line

chart = Line(title='test', logarithmic=True)
chart.add('test 1', [None, -38, 48, 4422, 35586, 1003452, 225533])
chart.add('test 2', [1, 40, 20, 38, 2937, 20399, 3947])
q = chart.render_pyquery()
assert len(q(".dots")) == 12
