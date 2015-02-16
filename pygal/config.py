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

"""
Config module with all options
"""
from copy import deepcopy
from pygal.style import Style, DefaultStyle
from pygal.interpolate import INTERPOLATIONS


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
        if category not in self._categories:
            self._categories.append(category)

        CONFIG_ITEMS.append(self)

    @property
    def is_boolean(self):
        return self.type == bool

    @property
    def is_numeric(self):
        return self.type in (int, float)

    @property
    def is_string(self):
        return self.type == str

    @property
    def is_dict(self):
        return self.type == dict

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
        elif self.type == dict:
            rv = {}
            for pair in value.split(','):
                key, val = pair.split(':')
                key = key.strip()
                val = val.strip()
                try:
                    rv[key] = self.subtype(val)
                except:
                    rv[key] = val
            return rv
        return self.type(value)


class MetaConfig(type):
    def __new__(mcs, classname, bases, classdict):
        for k, v in classdict.items():
            if isinstance(v, Key):
                v.name = k
        return type.__new__(mcs, classname, bases, classdict)


class BaseConfig(MetaConfig('ConfigBase', (object,), {})):

    def __init__(self, **kwargs):
        """Can be instanciated with config kwargs"""
        for k in dir(self):
            v = getattr(self, k)
            if (k not in self.__dict__ and not
                    k.startswith('_') and not
                    hasattr(v, '__call__')):
                if isinstance(v, Key):
                    if v.is_list and v.value is not None:
                        v = list(v.value)
                    else:
                        v = v.value
                setattr(self, k, v)
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


class CommonConfig(BaseConfig):
    stroke = Key(
        True, bool, "Look",
        "Line dots (set it to false to get a scatter plot)")

    show_dots = Key(True, bool, "Look", "Set to false to remove dots")

    show_only_major_dots = Key(
        False, bool, "Look",
        "Set to true to show only major dots according to their majored label")

    dots_size = Key(2.5, float, "Look", "Radius of the dots")

    fill = Key(
        False, bool, "Look", "Fill areas under lines")

    rounded_bars = Key(
        None, int, "Look",
        "Set this to the desired radius in px (for Bar-like charts)")

    inner_radius = Key(
        0, float, "Look", "Piechart inner radius (donut), must be <.9")


class Config(CommonConfig):
    """Class holding config values"""

    style = Key(
        DefaultStyle, Style, "Style", "Style holding values injected in css")

    css = Key(
        ('style.css', 'graph.css'), list, "Style",
        "List of css file",
        "It can be an absolute file path or an external link",
        str)

    # Look #
    title = Key(
        None, str, "Look",
        "Graph title.", "Leave it to None to disable title.")

    x_title = Key(
        None, str, "Look",
        "Graph X-Axis title.", "Leave it to None to disable X-Axis title.")

    y_title = Key(
        None, str, "Look",
        "Graph Y-Axis title.", "Leave it to None to disable Y-Axis title.")

    width = Key(
        800, int, "Look", "Graph width")

    height = Key(
        600, int, "Look", "Graph height")

    show_x_guides = Key(False, bool, "Look",
                        "Set to true to always show x guide lines")

    show_y_guides = Key(True, bool, "Look",
                        "Set to false to hide y guide lines")

    show_legend = Key(
        True, bool, "Look", "Set to false to remove legend")

    legend_at_bottom = Key(
        False, bool, "Look", "Set to true to position legend at bottom")

    legend_at_bottom_columns = Key(
        None, int, "Look", "Set to true to position legend at bottom")

    legend_box_size = Key(
        12, int, "Look", "Size of legend boxes")

    rounded_bars = Key(
        None, int, "Look", "Set this to the desired radius in px")

    stack_from_top = Key(
        False, bool, "Look", "Stack from top to zero, this makes the stacked "
        "data match the legend order")

    spacing = Key(
        10, int, "Look",
        "Space between titles/legend/axes")

    margin = Key(
        20, int, "Look",
        "Margin around chart")

    margin_top = Key(
        None, int, "Look",
        "Margin around top of chart")

    margin_right = Key(
        None, int, "Look",
        "Margin around right of chart")

    margin_bottom = Key(
        None, int, "Look",
        "Margin around bottom of chart")

    margin_left = Key(
        None, int, "Look",
        "Margin around left of chart")

    tooltip_border_radius = Key(0, int, "Look", "Tooltip border radius")

    inner_radius = Key(
        0, float, "Look", "Piechart inner radius (donut), must be <.9")

    half_pie = Key(
        False, bool, "Look", "Create a half-pie chart")

    x_labels = Key(
        None, list, "Label",
        "X labels, must have same len than data.",
        "Leave it to None to disable x labels display.",
        str)

    x_labels_major = Key(
        None, list, "Label",
        "X labels that will be marked major.",
        subtype=str)

    x_labels_major_every = Key(
        None, int, "Label",
        "Mark every n-th x label as major.")

    x_labels_major_count = Key(
        None, int, "Label",
        "Mark n evenly distributed labels as major.")

    show_x_labels = Key(
        True, bool, "Label", "Set to false to hide x-labels")

    show_minor_x_labels = Key(
        True, bool, "Label", "Set to false to hide x-labels not marked major")

    y_labels = Key(
        None, list, "Label",
        "You can specify explicit y labels",
        "Must be a list of numbers", float)

    y_labels_major = Key(
        None, list, "Label",
        "Y labels that will be marked major. Default: auto",
        subtype=str)

    y_labels_major_every = Key(
        None, int, "Label",
        "Mark every n-th y label as major.")

    y_labels_major_count = Key(
        None, int, "Label",
        "Mark n evenly distributed y labels as major.")

    show_minor_y_labels = Key(
        True, bool, "Label", "Set to false to hide y-labels not marked major")

    show_y_labels = Key(
        True, bool, "Label", "Set to false to hide y-labels")

    x_label_rotation = Key(
        0, int, "Label", "Specify x labels rotation angles", "in degrees")

    y_label_rotation = Key(
        0, int, "Label", "Specify y labels rotation angles", "in degrees")

    x_label_format = Key(
        "%Y-%m-%d %H:%M:%S.%f", str, "Label",
        "Date format for strftime to display the DateY X labels")

    missing_value_fill_truncation = Key(
        "x", str, "Look",
        "Filled series with missing x and/or y values at the end of a series "
        "are closed at the first value with a missing "
        "'x' (default), 'y' or 'either'")

    # Value #
    human_readable = Key(
        False, bool, "Value", "Display values in human readable format",
        "(ie: 12.4M)")

    x_value_formatter = Key(
        None, type(lambda: 1), "Value",
        "A function to convert abscissa numeric value to strings "
        "(used in XY and Date charts)")

    value_formatter = Key(
        None, type(lambda: 1), "Value",
        "A function to convert numeric value to strings")

    logarithmic = Key(
        False, bool, "Value", "Display values in logarithmic scale")

    interpolate = Key(
        None, str, "Value", "Interpolation",
        "May be %s" % ' or '.join(INTERPOLATIONS))

    interpolation_precision = Key(
        250, int, "Value", "Number of interpolated points between two values")

    interpolation_parameters = Key(
        {}, dict, "Value", "Various parameters for parametric interpolations",
        "ie: For hermite interpolation, you can set the cardinal tension with"
        "{'type': 'cardinal', 'c': .5}", int)

    mode = Key(
        None, str, "Value", "Sets the mode to be used. "
        "(Currently only supported on box plot)",
        "May be %s" % ' or '.join(["1.5IQR", "extremes"]))

    order_min = Key(
        None, int, "Value", "Minimum order of scale, defaults to None")

    range = Key(
        None, list, "Value", "Explicitly specify min and max of values",
        "(ie: (0, 100))", int)

    xrange = Key(
        None, list, "Value", "Explicitly specify min and max of x values "
        "(used in XY and Date charts)",
        "(ie: (0, 100))", int)

    include_x_axis = Key(
        False, bool, "Value", "Always include x axis")

    zero = Key(
        0, int, "Value",
        "Set the ordinate zero value",
        "Useful for filling to another base than abscissa")

    # Text #
    no_data_text = Key(
        "No data", str, "Text", "Text to display when no data is given")

    label_font_size = Key(10, int, "Text", "Label font size")

    major_label_font_size = Key(10, int, "Text", "Major label font size")

    value_font_size = Key(8, int, "Text", "Value font size")

    tooltip_font_size = Key(16, int, "Text", "Tooltip font size")

    title_font_size = Key(16, int, "Text", "Title font size")

    legend_font_size = Key(14, int, "Text", "Legend font size")

    no_data_font_size = Key(64, int, "Text", "No data text font size")

    print_values = Key(
        False, bool,
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

    # Misc #
    js = Key(
        ('http://kozea.github.io/pygal.js/javascripts/svg.jquery.js',
         'http://kozea.github.io/pygal.js/javascripts/pygal-tooltips.js'),
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

    no_prefix = Key(
        False, bool, "Misc",
        "Don't prefix css")


class SerieConfig(CommonConfig):
    """Class holding serie config values"""

    secondary = Key(
        False, bool, "Misc",
        "Set it to put the serie in a second axis")
