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

    _categories = []

    def __init__(
            self, default_value, type_, category, doc,
            subdoc="", subtype=None):

        self.value = default_value
        self.type = type_
        self.doc = doc
        self.category = category
        self.subdoc = subdoc
        self.subtype = subtype
        self.name = "Unbound"
        if not category in self._categories:
            self._categories.append(category)

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

    style = Key(
        DefaultStyle, Style, "Style", "Style holding values injected in css")

    css = Key(
        ('style.css', 'graph.css'), list, "Style",
        "List of css file",
        "It can be an absolute file path or an external link",
        str)

    ############ Look ############
    title = Key(
        None, str, "Look",
        "Graph title.", "Leave it to None to disable title.")

    width = Key(
        800, int, "Look", "Graph width")

    height = Key(
        600, int, "Look", "Graph height")

    show_dots = Key(True, bool, "Look", "Set to false to remove dots")

    stroke = Key(
        True, bool, "Look",
        "Line dots (set it to false to get a scatter plot)")

    fill = Key(
        False, bool, "Look", "Fill areas under lines")

    show_legend = Key(
        True, bool, "Look", "Set to false to remove legend")

    legend_at_bottom = Key(
        False, bool, "Look", "Set to true to position legend at bottom")

    legend_box_size = Key(
        12, int, "Look", "Size of legend boxes")

    rounded_bars = Key(
        None, int, "Look", "Set this to the desired radius in px")

    ############ Label ############
    x_labels = Key(
        None, list, "Label",
        "X labels, must have same len than data.",
        "Leave it to None to disable x labels display.",
        str)

    y_labels = Key(
        None, list, "Label",
        "You can specify explicit y labels",
        "Must be a list of numbers", float)

    x_label_rotation = Key(
        0, int, "Label", "Specify x labels rotation angles", "in degrees")

    y_label_rotation = Key(
        0, int, "Label", "Specify y labels rotation angles", "in degrees")

    ############ Value ############
    human_readable = Key(
        False, bool, "Value", "Display values in human readable format",
        "(ie: 12.4M)")

    logarithmic = Key(
        False, bool, "Value", "Display values in logarithmic scale")

    interpolate = Key(
        None, str, "Value", "Interpolation, this requires scipy module",
        "May be any of 'linear', 'nearest', 'zero', 'slinear', 'quadratic,"
        "'cubic', 'krogh', 'barycentric', 'univariate',"
        "or an integer specifying the order"
        "of the spline interpolator")

    interpolation_precision = Key(
        250, int, "Value", "Number of interpolated points between two values")

    order_min = Key(
        None, int, "Value", "Minimum order of scale, defaults to None")

    range = Key(
        None, list, "Value", "Explicitly specify min and max of values",
        "(ie: (0, 100))", int)

    include_x_axis = Key(
        False, bool, "Value", "Always include x axis")

    zero = Key(
        0, int, "Value",
        "Set the ordinate zero value",
        "Useful for filling to another base than abscissa")

    ############ Text ############
    no_data_text = Key(
        "No data", str, "Text", "Text to display when no data is given")

    label_font_size = Key(10, int, "Text", "Label font size")

    value_font_size = Key(8, int, "Text", "Value font size")

    tooltip_font_size = Key(20, int, "Text", "Tooltip font size")

    title_font_size = Key(16, int, "Text", "Title font size")

    legend_font_size = Key(14, int, "Text", "Legend font size")

    no_data_font_size = Key(64, int, "Text", "No data text font size")

    print_values = Key(
        True, bool,
        "Text", "Print values when graph is in non interactive mode")

    print_zeroes = Key(
        False, bool,
        "Text", "Print zeroes when graph is in non interactive mode")

    truncate_legend = Key(
        None, int, "Text",
        "Legend string length truncation threshold", "None = auto")

    truncate_label = Key(
        None, int, "Text",
        "Label string length truncation threshold", "None = auto")

    ############ Misc ############
    js = Key(
        ('https://raw.github.com/Kozea/pygal.js/master/svg.jquery.js',
         'https://raw.github.com/Kozea/pygal.js/master/pygal-tooltips.js'),
        list, "Misc", "List of js file",
        "It can be a filepath or an external link",
        str)

    disable_xml_declaration = Key(
        False, bool, "Misc",
        "Don't write xml declaration and return str instead of string",
        "usefull for writing output directly in html")

    explicit_size = Key(
        False, bool, "Misc", "Write width and height attributes")

    pretty_print = Key(
        False, bool, "Misc", "Pretty print the svg")

    strict = Key(
        False, bool, "Misc",
        "If True don't try to adapt / filter wrong values")

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
