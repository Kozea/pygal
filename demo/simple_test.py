#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of pygal
#
# A python svg graph plotting library
# Copyright © 2012 Kozea
#
# This library is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# This library is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with pygal. If not, see <http://www.gnu.org/licenses/>.
from pygal import (
    Line, Bar, XY, Pie, Radar, StackedBar, Config,
    StackedLine, HorizontalBar, HorizontalStackedBar)
from pygal.style import NeonStyle
from math import cos, sin

bar = Bar()
rng = [-6, -19, 0, -1, 2]
bar.add('test1', rng)
bar.add('test2', map(abs, rng))
bar.add('inc', [None, 1, None, 2])
bar.x_labels = map(str, rng)
bar.title = "Bar test"
bar.fill = True
bar.render_to_file('out-bar.svg')

hbar = HorizontalBar()
rng = [18, 9, 7, 3, 1, None, -5]
hbar.add('test1', rng)
rng2 = [16, 14, 10, 9, 7, 3, -1]
hbar.add('test2', rng2)
rng3 = [123, None, None, 4, None, 6]
hbar.add('test3', rng3)
hbar.x_labels = map(
    lambda x: '%s / %s' % x, zip(map(str, rng), map(str, rng2)))
hbar.title = "Horizontal Bar test"
hbar.render_to_file('out-horizontalbar.svg')

rng = [3, -32, 39, 12]
rng2 = [24, -8, 18, 12]
rng3 = [6, 1, -10, 0]
config = Config()
config.x_label_rotation = 35
config.x_labels = map(lambda x: '%s  / %s / %s' % x,
                        zip(map(str, rng),
                            map(str, rng2),
                            map(str, rng3)))
config.title = "Stacked Bar test"
config.style = NeonStyle

stackedbar = StackedBar(config)
stackedbar.add('@@@@@@@', rng)
stackedbar.add('++++++', rng2)
stackedbar.add('--->', rng3)
stackedbar.add('None', [None, 42, 42])
stackedbar.render_to_file('out-stackedbar.svg')

config.title = "Horizontal Stacked Bar test"
hstackedbar = HorizontalStackedBar(config)
hstackedbar.add('@@@@@@@', rng)
hstackedbar.add('++++++', rng2)
hstackedbar.add('--->', rng3)
hstackedbar.render_to_file('out-horizontalstackedbar.svg')

line = Line(Config(y_scale=.0005, style=NeonStyle,
                   zero=1,
                   human_readable=True, logarithmic=True))
# rng = range(-30, 31, 1)

# line.add('test1', [1000 ** cos(x / 10.) for x in rng])
# line.add('test2', [1000 ** sin(x / 10.) for x in rng])
# line.add('test3', [1000 ** (cos(x / 10.) - sin(x / 10.)) for x in rng])
rng = range(1, 2000, 25)
# line.add('x', rng)
# line.add('x', rng)
# line.add('10^10^x', map(lambda x: ((x / 333.) ** (x / 333.)), rng))
# line.add('None', [None, None, None, 12, 31, 11, None, None, 12, 14])
line.add('2', [None, None, 2, 4, 8, None, 14, 10, None])
line.add('1', [1, 5, 3, 4, 6, 12, 13, 7, 2])
line.x_labels = map(str, rng)
line.title = "Line test"
line.interpolate = "cubic"
line.interpolation_precision = 200
line.render_to_file('out-line.svg')

stackedline = StackedLine(Config(y_scale=.0005, fill=True))
stackedline.add('test1', [1, 3, 2, None, 2, 13, 2, 5, 8])
stackedline.add('test2', [4, 1, 1,  3, 12,  3])
stackedline.add('test3', [9, 3, 2, 10,  8,  2])
stackedline.x_labels = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
stackedline.title = "Stackedline test"
stackedline.interpolate = "cubic"
stackedline.render_to_file('out-stackedline.svg')

xy = XY(Config(x_scale=1, fill=True, style=NeonStyle, interpolate='cubic'))
xy.add('test1', [(1981, 1), (1999, -4), (2001, 2), (2003, 10), (2012, 8)])
xy.add('test2', [(1988, -1), (1986, 12), (2007, 7), (2010, 4)])
xy.add('test2', [(None, None), (None, 12), (2007, None), (2002.3, 12)])
# xy.add('test2', [(1980, 0), (1985, 2), (1995, -2), (2005, 4), (2020, -4)])
                 # (2005, 6), (2010, -6), (2015, 3), (2020, -3), (2025, 0)])
xy.title = "XY test"
xy.render_to_file('out-xy.svg')

pie = Pie(Config(style=NeonStyle))
pie.add('test', [11, 8, 21])
pie.add('test2', [29, None, 9])
pie.add('test3', [24, 10, 32])
pie.add('test4', [20, 18, 9])
pie.add('test5', [17, 5, 10])
pie.add('test6', [None, None, 10])
pie.title = "Pie test"
pie.render_to_file('out-pie.svg')

config = Config()
config.fill = True
config.style = NeonStyle
config.x_labels = (
    'black', 'red', 'blue', 'yellow', 'orange', 'green', 'white')
config.interpolate = 'nearest'
radar = Radar(config)
radar.add('test', [1, 4, 1, 5, None, 2, 5])
radar.add('test2', [10, 2, 0, 5, 1, 9, 4])

radar.title = "Radar test"
radar.render_to_file('out-radar.svg')
