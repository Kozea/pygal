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
from pygal.style import DefaultStyle


class FontSizes(object):
    """Container for font sizes"""


class Config(object):
    """Class holding config values"""
    _horizontal = False

    # Graph width and height
    width, height = 800, 600
    # Scale order range
    x_scale = 1
    y_scale = 1
    # If set to a filename, this will replace the default css
    base_css = None
    # or default js
    base_js = None
    # Style holding values injected in css
    style = DefaultStyle
    # Various font sizes
    label_font_size = 10
    values_font_size = 18
    title_font_size = 16
    legend_font_size = 14
    # Specify labels rotation angles in degrees
    x_label_rotation = 0
    y_label_rotation = 0
    # Set to false to remove legend
    show_legend = True
    # Set to false to remove dots
    show_dots = True
    # Size of legend boxes
    legend_box_size = 12
    # X labels, must have same len than data.
    # Leave it to None to disable x labels display.
    x_labels = None
    # You can specify explicit y labels (must be list(int))
    y_labels = None
    # Graph title
    # Leave it to None to disable title.
    title = None
    # Set this to the desired radius in px
    rounded_bars = False
    # Always include x axis
    include_x_axis = False
    # Fill areas under lines
    fill = False
    # Line dots (set it to false to get a scatter plot)
    stroke = True
    # Interpolation, this requires scipy module
    # May be any of ‘linear’, ’nearest’, ‘zero’, ‘slinear’, ‘quadratic, ‘cubic’
    # 'krogh', 'barycentric', 'univariate', or an integer specifying the order
    # of the spline interpolator
    interpolate = None
    # Number of interpolated points between two values
    interpolation_precision = 250
    zero = 0

    def __init__(self, **kwargs):
        """Can be instanciated with config kwargs"""
        self.__dict__.update(kwargs)

    def __call__(self, **kwargs):
        """Can be updated with kwargs"""
        self.__dict__.update(kwargs)

    @property
    def font_sizes(self):
        fs = FontSizes()
        for name in dir(self):
            if name.endswith('_font_size'):
                setattr(fs,
                        name.replace('_font_size', ''),
                        '%dpx' % getattr(self, name))
        return fs
