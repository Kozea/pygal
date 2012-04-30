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

"""
Config module with all options
"""

from pygal.style import DefaultStyle


class FontSizes(object):
    """Container for font sizes"""


class Config(object):
    """Class holding config values"""

    #: Graph width
    width = 800
    #: Graph height
    height = 600
    #: Display values in human readable format (ie: 12.4M)
    human_readable = False
    #: Display values in logarithmic scale
    logarithmic = False
    #: List of css file, can be an absolute file path or an external link
    css = ('style.css', 'graph.css')  # Relative path to pygal css
    #: List of js file, can be a filepath or an external link
    js = (
        'https://raw.github.com/Kozea/pygal.js/master/svg.jquery.js',
        'https://raw.github.com/Kozea/pygal.js/master/pygal-tooltips.js'
    )
    #: Style holding values injected in css
    style = DefaultStyle
    #: Various font sizes
    label_font_size = 10
    value_font_size = 8
    tooltip_font_size = 20
    title_font_size = 16
    legend_font_size = 14
    #: Specify labels rotation angles in degrees
    x_label_rotation = 0
    y_label_rotation = 0
    #: Set to false to remove legend
    show_legend = True
    #: Set to true to position legend at bottom
    legend_at_bottom = False
    #: Set to false to remove dots
    show_dots = True
    #: Size of legend boxes
    legend_box_size = 12
    #: X labels, must have same len than data.
    #: Leave it to None to disable x labels display.
    x_labels = None
    #: You can specify explicit y labels (must be list(int))
    y_labels = None
    #: Graph title
    #: Leave it to None to disable title.
    title = None
    #: Set this to the desired radius in px
    rounded_bars = False
    #: Always include x axis
    include_x_axis = False
    #: Fill areas under lines
    fill = False
    #: Line dots (set it to false to get a scatter plot)
    stroke = True
    #: Interpolation, this requires scipy module
    #: May be any of 'linear', 'nearest', 'zero', 'slinear', 'quadratic,
    #: 'cubic', 'krogh', 'barycentric', 'univariate',
    #: or an integer specifying the order
    #: of the spline interpolator
    interpolate = None
    #: Number of interpolated points between two values
    interpolation_precision = 250
    #: Explicitly specify min and max of values (ie: (0, 100))
    range = None
    #: Set the ordinate zero value (for filling)
    zero = 0
    #: Text to display when no data is given
    no_data_text = "No data"
    #: Print values when graph is in non interactive mode
    print_values = True
    #: Print zeroes when graph is in non interactive mode
    print_zeroes = False
    #: Animate tooltip steps (0 disable animation)
    animation_steps = 0
    #: Don't write xml declaration and return unicode instead of string
    #: (usefull for writing output in html)
    disable_xml_declaration = False
    #: Write width and height attributes
    explicit_size = False
    #: Legend string length truncation threshold (None = auto)
    truncate_legend = None
    #: Label string length truncation threshold (None = auto)
    truncate_label = None
    #: Pretty print the svg
    pretty_print = False

    def __init__(self, **kwargs):
        """Can be instanciated with config kwargs"""
        self.css = list(self.css)
        self.js = list(self.js)
        self.__dict__.update(kwargs)

    def __call__(self, **kwargs):
        """Can be updated with kwargs"""
        self.__dict__.update(kwargs)

    def font_sizes(self, with_unit=True):
        """Getter for all font size configs"""
        fs = FontSizes()
        for name in dir(self):
            if name.endswith('_font_size'):
                setattr(
                    fs,
                    name.replace('_font_size', ''),
                    ('%dpx' % getattr(self, name)
                 ) if with_unit else getattr(self, name))
        return fs

    def to_dict(self):
        config = {}
        for attr in dir(self):
            if not attr.startswith('__'):
                value = getattr(self, attr)
                if hasattr(value, 'to_dict'):
                    config[attr] = value.to_dict()
                elif not hasattr(value, '__call__'):
                    config[attr] = value
        return config
