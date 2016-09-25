# This file is test file for NoneMaxSolved
# I have modified the line.py and passed other test
# This test is for us to test whether the none value
# in the Log graph will be max or not (issue #309)

from __future__ import division
from pygal import Line
from pygal.test.utils import texts
from math import cos, sin

chart = Line(title='test', x_label_rotation=90, human_readable=True, logarithmic=True)
chart.add('test 1', [None, None, None, None, -38, 48, None, 4422, 34443, 345586, 40003452, 1235533, 2235533])
chart.add('test 2', [ 1, 7, 19, 30, 40, 20, 38, 283, 2937, 29374, 20399, 293874, 3947])
q = chart.render_pyquery()
assert len(q(".dots")) == 20
