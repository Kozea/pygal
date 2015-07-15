# -*- coding: utf-8 -*-
# This file is part of pygal
#
# A python svg graph plotting library
# Copyright © 2012-2015 Kozea
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

"""Style related tests"""

from pygal import Line
from pygal.style import (
    LightStyle,
    LightenStyle, DarkenStyle, SaturateStyle, DesaturateStyle, RotateStyle
)

STYLES = LightenStyle, DarkenStyle, SaturateStyle, DesaturateStyle, RotateStyle


def test_parametric_styles():
    """Test that no parametric produce the same result"""
    chart = None
    for style in STYLES:
        line = Line(style=style('#f4e83a'))
        line.add('_', [1, 2, 3])
        line.x_labels = 'abc'
        new_chart = line.render()
        assert chart != new_chart
        chart = new_chart


def test_parametric_styles_with_parameters():
    """Test a parametric style with parameters"""
    line = Line(style=RotateStyle(
        '#de3804', step=12, max_=180, base_style=LightStyle))
    line.add('_', [1, 2, 3])
    line.x_labels = 'abc'
    assert line.render()
