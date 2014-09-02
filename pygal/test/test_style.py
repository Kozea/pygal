# -*- coding: utf-8 -*-
# This file is part of pygal
#
# A python svg graph plotting library
# Copyright © 2012-2014 Kozea
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
from pygal.style import Style
from pygal import Line
from pygal.style import (
    LightStyle,
    LightenStyle, DarkenStyle, SaturateStyle, DesaturateStyle, RotateStyle
)

STYLES = LightenStyle, DarkenStyle, SaturateStyle, DesaturateStyle, RotateStyle


def test_parametric_styles():
    chart = None
    for style in STYLES:
        line = Line(style=style('#f4e83a'))
        line.add('_', [1, 2, 3])
        line.x_labels = 'abc'
        new_chart = line.render()
        assert chart != new_chart
        chart = new_chart


def test_parametric_styles_with_parameters():
    line = Line(style=RotateStyle(
        '#de3804', step=12, max_=180, base_style=LightStyle))
    line.add('_', [1, 2, 3])
    line.x_labels = 'abc'
    assert line.render()

def test_stroke_style():
    s = Style(stroke_style = 'round')
    assert s.stroke_style == 'round'
    s = Style(stroke_style = 'bevel')
    assert s.stroke_style == 'bevel'
    s = Style(stroke_style = 'miter')
    assert s.stroke_style == 'miter'
    s = Style(stroke_style = 'rounded')
    assert s.stroke_style == 'round'
    s = Style(stroke_style = 'invalid derp')
    assert s.stroke_style == 'round'

def test_stroke_dasharray():
    s = Style(stroke_dasharray = (0,0))
    assert s.stroke_dasharray == '0,0'
    s = Style(stroke_dasharray = (.5,.5))
    assert s.stroke_dasharray == '0,0'
    s = Style(stroke_dasharray = (.9,.9))
    assert s.stroke_dasharray == '0,0'
    s = Style(stroke_dasharray = (1.9,1.9))
    assert s.stroke_dasharray == '1,1'

def test_stroke_dasharray_input_types():
    s = Style(stroke_dasharray = (0,0))
    assert s.stroke_dasharray == '0,0'
    s = Style(stroke_dasharray = '0,0')
    assert s.stroke_dasharray == '0,0'
    s = Style(stroke_dasharray = '0x0')
    assert s.stroke_dasharray == '0,0'
    s = Style(stroke_dasharray = '0  0')
    assert s.stroke_dasharray == '0,0'