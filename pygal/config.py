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
from copy import deepcopy
from pygal.style import Style, DefaultStyle


class FontSizes(object):
    """Container for font sizes"""

CONFIG_ITEMS = []


class Key(object):

    def __init__(self, default_value, type_, doc, subdoc="", subtype=None):
        self.value = default_value
        self.type = type_
        self.doc = doc
        self.subdoc = subdoc
        self.subtype = subtype
        self.name = "Unbound"
        CONFIG_ITEMS.append(self)

    @property
    def is_boolean(self):
        return self.type == bool

    @property
    def is_numeric(self):
        return self.type == int

    @property
    def is_string(self):
        return self.type == str

    @property
    def is_list(self):
        return self.type == list

    def coerce(self, value):
        if self.type == Style:
            return value
        elif self.type == list:
            return self.type(
                map(
                    self.subtype, map(
                        lambda x: x.strip(), value.split(','))))
        return self.type(value)


class MetaConfig(type):
    def __new__(mcs, classname, bases, classdict):
        for k, v in classdict.items():
            if isinstance(v, Key):
                v.name = k
        return type.__new__(mcs, classname, bases, classdict)


class Config(object):
    """Class holding config values"""

    __metaclass__ = MetaConfig

    width = Key(800, int, "Graph width")

    height = Key(600, int, "Graph height")

    human_readable = Key(
        False, bool, "Display values in human readable format",
        "(ie: 12.4M)")

    logarithmic = Key(False, bool, "Display values in logarithmic scale")

    order_min = Key(None, int, "Minimum order of scale, defaults to None")

    css = Key(
        ('style.css', 'graph.css'), list,
        "List of css file",
        "It can be an absolute file path or an external link",
        str)

    js = Key(
        ('https://raw.github.com/Kozea/pygal.js/master/svg.jquery.js',
         'https://raw.github.com/Kozea/pygal.js/master/pygal-tooltips.js'),
        list, "List of js file",
        "It can be a filepath or an external link",
        str)

    style = Key(DefaultStyle, Style, "Style holding values injected in css")

    label_font_size = Key(10, int, "Label font size")

    value_font_size = Key(8, int, "Value font size")

    tooltip_font_size = Key(20, int, "Tooltip font size")

    title_font_size = Key(16, int, "Title font size")

    legend_font_size = Key(14, int, "Legend font size")

    x_label_rotation = Key(
        0, int, "Specify x labels rotation angles", "in degrees")

    y_label_rotation = Key(
        0, int, "Specify y labels rotation angles", "in degrees")

    show_legend = Key(True, bool, "Set to false to remove legend")

    legend_at_bottom = Key(
        False, bool, "Set to true to position legend at bottom")

    show_dots = Key(True, bool, "Set to false to remove dots")

    legend_box_size = Key(12, int, "Size of legend boxes")

    x_labels = Key(
        None, list,
        "X labels, must have same len than data.",
        "Leave it to None to disable x labels display.",
        str)

    y_labels = Key(
        None, list,
        "You can specify explicit y labels",
        "(must be list(int))", int)

    title = Key(
        None, str, "Graph title.", "Leave it to None to disable title.")

    rounded_bars = Key(False, bool, "Set this to the desired radius in px")

    include_x_axis = Key(False, bool, "Always include x axis")

    fill = Key(False, bool, "Fill areas under lines")

    stroke = Key(
        True, bool, "Line dots (set it to false to get a scatter plot)")

    interpolate = Key(
        None, str, "Interpolation, this requires scipy module",
        "May be any of 'linear', 'nearest', 'zero', 'slinear', 'quadratic,"
        "'cubic', 'krogh', 'barycentric', 'univariate',"
        "or an integer specifying the order"
        "of the spline interpolator")

    interpolation_precision = Key(
        250, int, "Number of interpolated points between two values")

    range = Key(
        None, list, "Explicitly specify min and max of values",
        "(ie: (0, 100))", int)

    zero = Key(
        0, int, "Set the ordinate zero value", "(for filling)")

    no_data_text = Key(
        "No data", str, "Text to display when no data is given")

    print_values = Key(
        True, bool, "Print values when graph is in non interactive mode")

    print_zeroes = Key(
        False, bool, "Print zeroes when graph is in non interactive mode")

    disable_xml_declaration = Key(
        False, bool,
        "Don't write xml declaration and return str instead of string",
        "usefull for writing output directly in html")

    explicit_size = Key(False, bool, "Write width and height attributes")

    truncate_legend = Key(
        None, int, "Legend string length truncation threshold (None = auto)")

    truncate_label = Key(
        None, int, "Label string length truncation threshold (None = auto)")

    pretty_print = Key(False, bool, "Pretty print the svg")

    strict = Key(
        False, bool, "If True don't try to adapt / filter wrong values")

    def __init__(self, **kwargs):
        """Can be instanciated with config kwargs"""
        for k in dir(self):
            v = getattr(self, k)
            if (k not in self.__dict__ and not
                    k.startswith('_') and not
                    hasattr(v, '__call__')):
                if isinstance(v, Key):
                    v = v.value
                setattr(self, k, v)

        self.css = list(self.css)
        self.js = list(self.js)
        self._update(kwargs)

    def __call__(self, **kwargs):
        """Can be updated with kwargs"""
        self._update(kwargs)

    def _update(self, kwargs):
        self.__dict__.update(
            dict([(k, v) for (k, v) in kwargs.items()
                  if not k.startswith('_') and k in dir(self)]))

    def font_sizes(self, with_unit=True):
        """Getter for all font size configs"""
        fs = FontSizes()
        for name in dir(self):
            if name.endswith('_font_size'):
                setattr(
                    fs,
                    name.replace('_font_size', ''),
                    ('%dpx' % getattr(self, name))
                    if with_unit else getattr(self, name))
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

    def copy(self):
        return deepcopy(self)
