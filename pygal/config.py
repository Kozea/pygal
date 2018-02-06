# -*- coding: utf-8 -*-
# This file is part of pygal
#
# A python svg graph plotting library
# Copyright © 2012-2016 Kozea
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
"""Config module holding all options and their default values."""

from copy import deepcopy

from pygal import formatters
from pygal.interpolate import INTERPOLATIONS
from pygal.style import DefaultStyle, Style

CONFIG_ITEMS = []
callable = type(lambda: 1)


class Key(object):
    """
    Represents a config parameter.

    A config parameter has a name, a default value, a type,
    a category, a documentation, an optional longer documentatation
    and an optional subtype for list style option.

    Most of these informations are used in cabaret to auto generate
    forms representing these options.
    """

    _categories = []

    def __init__(
            self, default_value, type_, category, doc, subdoc="", subtype=None
    ):
        """Create a configuration key"""
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

    def __repr__(self):
        """
        Make a documentation repr.
        This is a hack to generate doc from inner doc
        """
        return """
        Type: %s%s     
        Default: %r     
        %s%s
        """ % (
            self.type.__name__, (' of %s' % self.subtype.__name__)
            if self.subtype else '', self.value, self.doc,
            (' %s' % self.subdoc) if self.subdoc else ''
        )

    @property
    def is_boolean(self):
        """Return `True` if this parameter is a boolean"""
        return self.type == bool

    @property
    def is_numeric(self):
        """Return `True` if this parameter is numeric (int or float)"""
        return self.type in (int, float)

    @property
    def is_string(self):
        """Return `True` if this parameter is a string"""
        return self.type == str

    @property
    def is_dict(self):
        """Return `True` if this parameter is a mapping"""
        return self.type == dict

    @property
    def is_list(self):
        """Return `True` if this parameter is a list"""
        return self.type == list

    def coerce(self, value):
        """Cast a string into this key type"""
        if self.type == Style:
            return value
        elif self.type == list:
            return self.type(
                map(self.subtype, map(lambda x: x.strip(), value.split(',')))
            )
        elif self.type == dict:
            rv = {}
            for pair in value.split(','):
                key, val = pair.split(':')
                key = key.strip()
                val = val.strip()
                try:
                    rv[key] = self.subtype(val)
                except Exception:
                    rv[key] = val
            return rv
        return self.type(value)


class MetaConfig(type):
    """Config metaclass. Used to get the key name and set it on the value."""

    def __new__(mcs, classname, bases, classdict):
        """Get the name of the key and set it on the key"""
        for k, v in classdict.items():
            if isinstance(v, Key):
                v.name = k

        return type.__new__(mcs, classname, bases, classdict)


class BaseConfig(MetaConfig('ConfigBase', (object, ), {})):
    """
    This class holds the common method for configs.

    A config object can be instanciated with keyword arguments and
    updated on call with keyword arguments.
    """

    def __init__(self, **kwargs):
        """Can be instanciated with config kwargs"""
        for k in dir(self):
            v = getattr(self, k)
            if (k not in self.__dict__ and not k.startswith('_')
                    and not hasattr(v, '__call__')):
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
        """Update the config with the given dictionary"""
        from pygal.util import merge
        dir_self_set = set(dir(self))
        merge(
            self.__dict__,
            dict([(k, v) for (k, v) in kwargs.items()
                  if not k.startswith('_') and k in dir_self_set])
        )

    def to_dict(self):
        """Export a JSON serializable dictionary of the config"""
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
        """Copy this config object into another"""
        return deepcopy(self)


class CommonConfig(BaseConfig):
    """Class holding options used in both chart and serie configuration"""

    stroke = Key(
        True, bool, "Look", "Line dots (set it to false to get a scatter plot)"
    )

    show_dots = Key(True, bool, "Look", "Set to false to remove dots")

    show_only_major_dots = Key(
        False, bool, "Look",
        "Set to true to show only major dots according to their majored label"
    )

    dots_size = Key(2.5, float, "Look", "Radius of the dots")

    fill = Key(False, bool, "Look", "Fill areas under lines")

    stroke_style = Key(
        None, dict, "Look", "Stroke style of serie element.",
        "This is a dict which can contain a "
        "'width', 'linejoin', 'linecap', 'dasharray' "
        "and 'dashoffset'"
    )

    rounded_bars = Key(
        None, int, "Look",
        "Set this to the desired radius in px (for Bar-like charts)"
    )

    inner_radius = Key(
        0, float, "Look", "Piechart inner radius (donut), must be <.9"
    )

    allow_interruptions = Key(
        False, bool, "Look", "Break lines on None values"
    )

    formatter = Key(
        None, callable, "Value",
        "A function to convert raw value to strings for this chart or serie",
        "Default to value_formatter in most charts, it depends on dual charts."
        "(Can be overriden by value with the formatter metadata.)"
    )


class Config(CommonConfig):
    """Class holding config values"""

    style = Key(
        DefaultStyle, Style, "Style", "Style holding values injected in css"
    )

    css = Key(
        ('file://style.css', 'file://graph.css'), list, "Style",
        "List of css file",
        "It can be any uri from file:///tmp/style.css to //domain/style.css",
        str
    )

    classes = Key(('pygal-chart', ), list, "Style",
                  "Classes of the root svg node", str)

    defs = Key([], list, "Misc", "Extraneous defs to be inserted in svg",
               "Useful for adding gradients / patterns…", str)

    # Look #
    title = Key(
        None, str, "Look", "Graph title.", "Leave it to None to disable title."
    )

    x_title = Key(
        None, str, "Look", "Graph X-Axis title.",
        "Leave it to None to disable X-Axis title."
    )

    y_title = Key(
        None, str, "Look", "Graph Y-Axis title.",
        "Leave it to None to disable Y-Axis title."
    )

    width = Key(800, int, "Look", "Graph width")

    height = Key(600, int, "Look", "Graph height")

    show_x_guides = Key(
        False, bool, "Look", "Set to true to always show x guide lines"
    )

    show_y_guides = Key(
        True, bool, "Look", "Set to false to hide y guide lines"
    )

    show_legend = Key(True, bool, "Look", "Set to false to remove legend")

    legend_at_bottom = Key(
        False, bool, "Look", "Set to true to position legend at bottom"
    )

    legend_at_bottom_columns = Key(
        None, int, "Look", "Set to true to position legend at bottom"
    )

    legend_box_size = Key(12, int, "Look", "Size of legend boxes")

    rounded_bars = Key(
        None, int, "Look", "Set this to the desired radius in px"
    )

    stack_from_top = Key(
        False, bool, "Look", "Stack from top to zero, this makes the stacked "
        "data match the legend order"
    )

    spacing = Key(10, int, "Look", "Space between titles/legend/axes")

    margin = Key(20, int, "Look", "Margin around chart")

    margin_top = Key(None, int, "Look", "Margin around top of chart")

    margin_right = Key(None, int, "Look", "Margin around right of chart")

    margin_bottom = Key(None, int, "Look", "Margin around bottom of chart")

    margin_left = Key(None, int, "Look", "Margin around left of chart")

    tooltip_border_radius = Key(0, int, "Look", "Tooltip border radius")

    tooltip_fancy_mode = Key(
        True, bool, "Look", "Fancy tooltips",
        "Print legend, x label in tooltip and use serie color for value."
    )

    inner_radius = Key(
        0, float, "Look", "Piechart inner radius (donut), must be <.9"
    )

    half_pie = Key(False, bool, "Look", "Create a half-pie chart")

    x_labels = Key(
        None, list, "Label", "X labels, must have same len than data.",
        "Leave it to None to disable x labels display.", str
    )

    x_labels_major = Key(
        None,
        list,
        "Label",
        "X labels that will be marked major.",
        subtype=str
    )

    x_labels_major_every = Key(
        None, int, "Label", "Mark every n-th x label as major."
    )

    x_labels_major_count = Key(
        None, int, "Label", "Mark n evenly distributed labels as major."
    )

    show_x_labels = Key(True, bool, "Label", "Set to false to hide x-labels")

    show_minor_x_labels = Key(
        True, bool, "Label", "Set to false to hide x-labels not marked major"
    )

    y_labels = Key(
        None, list, "Label", "You can specify explicit y labels",
        "Must be a list of numbers", float
    )

    y_labels_major = Key(
        None,
        list,
        "Label",
        "Y labels that will be marked major. Default: auto",
        subtype=str
    )

    y_labels_major_every = Key(
        None, int, "Label", "Mark every n-th y label as major."
    )

    y_labels_major_count = Key(
        None, int, "Label", "Mark n evenly distributed y labels as major."
    )

    show_minor_y_labels = Key(
        True, bool, "Label", "Set to false to hide y-labels not marked major"
    )

    show_y_labels = Key(True, bool, "Label", "Set to false to hide y-labels")

    x_label_rotation = Key(
        0, int, "Label", "Specify x labels rotation angles", "in degrees"
    )

    y_label_rotation = Key(
        0, int, "Label", "Specify y labels rotation angles", "in degrees"
    )

    missing_value_fill_truncation = Key(
        "x", str, "Look",
        "Filled series with missing x and/or y values at the end of a series "
        "are closed at the first value with a missing "
        "'x' (default), 'y' or 'either'"
    )

    # Value #
    x_value_formatter = Key(
        formatters.default, callable, "Value",
        "A function to convert abscissa numeric value to strings "
        "(used in XY and Date charts)"
    )

    value_formatter = Key(
        formatters.default, callable, "Value",
        "A function to convert ordinate numeric value to strings"
    )

    logarithmic = Key(
        False, bool, "Value", "Display values in logarithmic scale"
    )

    interpolate = Key(
        None, str, "Value", "Interpolation",
        "May be %s" % ' or '.join(INTERPOLATIONS)
    )

    interpolation_precision = Key(
        250, int, "Value", "Number of interpolated points between two values"
    )

    interpolation_parameters = Key(
        {}, dict, "Value", "Various parameters for parametric interpolations",
        "ie: For hermite interpolation, you can set the cardinal tension with"
        "{'type': 'cardinal', 'c': .5}", int
    )

    box_mode = Key(
        'extremes', str, "Value", "Sets the mode to be used. "
        "(Currently only supported on box plot)", "May be %s" %
        ' or '.join(["1.5IQR", "extremes", "tukey", "stdev", "pstdev"])
    )

    order_min = Key(
        None, int, "Value", "Minimum order of scale, defaults to None"
    )

    min_scale = Key(
        4, int, "Value", "Minimum number of scale graduation for auto scaling"
    )

    max_scale = Key(
        16, int, "Value", "Maximum number of scale graduation for auto scaling"
    )

    range = Key(
        None, list, "Value", "Explicitly specify min and max of values",
        "(ie: (0, 100))", int
    )

    secondary_range = Key(
        None, list, "Value",
        "Explicitly specify min and max of secondary values", "(ie: (0, 100))",
        int
    )

    xrange = Key(
        None, list, "Value", "Explicitly specify min and max of x values "
        "(used in XY and Date charts)", "(ie: (0, 100))", int
    )

    include_x_axis = Key(False, bool, "Value", "Always include x axis")

    zero = Key(
        0, int, "Value", "Set the ordinate zero value",
        "Useful for filling to another base than abscissa"
    )

    # Text #
    no_data_text = Key(
        "No data", str, "Text", "Text to display when no data is given"
    )

    print_values = Key(False, bool, "Text", "Display values as text over plot")

    dynamic_print_values = Key(
        False, bool, "Text", "Show values only on hover"
    )

    print_values_position = Key(
        'center', str, "Text", "Customize position of `print_values`. "
        "(For bars: `top`, `center` or `bottom`)"
    )

    print_zeroes = Key(True, bool, "Text", "Display zero values as well")

    print_labels = Key(False, bool, "Text", "Display value labels")

    truncate_legend = Key(
        None, int, "Text", "Legend string length truncation threshold",
        "None = auto, Negative for none"
    )

    truncate_label = Key(
        None, int, "Text", "Label string length truncation threshold",
        "None = auto, Negative for none"
    )

    # Misc #
    js = Key(('//kozea.github.io/pygal.js/2.0.x/pygal-tooltips.min.js', ),
             list, "Misc", "List of js file",
             "It can be any uri from file:///tmp/ext.js to //domain/ext.js",
             str)

    disable_xml_declaration = Key(
        False, bool, "Misc",
        "Don't write xml declaration and return str instead of string",
        "useful for writing output directly in html"
    )

    force_uri_protocol = Key(
        'https', str, "Misc", "Default uri protocol",
        "Default protocol for external files. "
        "Can be set to None to use a // uri"
    )

    explicit_size = Key(
        False, bool, "Misc", "Write width and height attributes"
    )

    pretty_print = Key(False, bool, "Misc", "Pretty print the svg")

    strict = Key(
        False, bool, "Misc", "If True don't try to adapt / filter wrong values"
    )

    no_prefix = Key(False, bool, "Misc", "Don't prefix css")

    inverse_y_axis = Key(False, bool, "Misc", "Inverse Y axis direction")


class SerieConfig(CommonConfig):
    """Class holding serie config values"""

    title = Key(
        None, str, "Look", "Serie title.", "Leave it to None to disable title."
    )

    secondary = Key(
        False, bool, "Misc", "Set it to put the serie in a second axis"
    )
