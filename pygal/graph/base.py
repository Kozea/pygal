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

"""Base for pygal charts"""

from __future__ import division

import os
from functools import reduce
from uuid import uuid4

from pygal._compat import is_list_like
from pygal.adapters import decimal_to_float, not_zero, positive
from pygal.config import Config, SerieConfig
from pygal.serie import Serie
from pygal.state import State
from pygal.svg import Svg
from pygal.util import compose, ident
from pygal.view import Box, Margin


class BaseGraph(object):

    """Chart internal behaviour related functions"""

    _adapters = []

    def __init__(self, config=None, **kwargs):
        """Config preparation and various initialization"""
        if config:
            if isinstance(config, type):
                config = config()
            else:
                config = config.copy()
        else:
            config = Config()

        config(**kwargs)
        self.config = config
        self.state = None
        self.uuid = str(uuid4())
        self.raw_series = []
        self.raw_series2 = []
        self.xml_filters = []

    def __setattr__(self, name, value):
        """Set an attribute on the class or in the state if there is one"""
        if name.startswith('__') or getattr(self, 'state', None) is None:
            super(BaseGraph, self).__setattr__(name, value)
        else:
            setattr(self.state, name, value)

    def __getattribute__(self, name):
        """Get an attribute from the class or from the state if there is one"""
        if name.startswith('__') or name == 'state' or getattr(
                self, 'state', None
        ) is None or name not in self.state.__dict__:
            return super(BaseGraph, self).__getattribute__(name)
        return getattr(self.state, name)

    def prepare_values(self, raw, offset=0):
        """Prepare the values to start with sane values"""
        from pygal.graph.map import BaseMap
        from pygal import Histogram

        if self.zero == 0 and isinstance(self, BaseMap):
            self.zero = 1

        for key in ('x_labels', 'y_labels'):
            if getattr(self, key):
                setattr(self, key, list(getattr(self, key)))
        if not raw:
            return

        adapters = list(self._adapters) or [lambda x:x]
        if self.logarithmic:
            for fun in not_zero, positive:
                if fun in adapters:
                    adapters.remove(fun)
            adapters = adapters + [positive, not_zero]
        adapters = adapters + [decimal_to_float]

        self._adapt = reduce(compose, adapters) if not self.strict else ident
        self._x_adapt = reduce(
            compose, self._x_adapters) if not self.strict and getattr(
                self, '_x_adapters', None) else ident

        series = []

        raw = [(
            title,
            list(raw_values) if not isinstance(
                raw_values, dict) else raw_values,
            serie_config_kwargs
        ) for title, raw_values, serie_config_kwargs in raw]

        width = max([len(values) for _, values, _ in raw] +
                    [len(self.x_labels or [])])

        for title, raw_values, serie_config_kwargs in raw:
            metadata = {}
            values = []
            if isinstance(raw_values, dict):
                if isinstance(self, BaseMap):
                    raw_values = list(raw_values.items())
                else:
                    value_list = [None] * width
                    for k, v in raw_values.items():
                        if k in (self.x_labels or []):
                            value_list[self.x_labels.index(k)] = v
                    raw_values = value_list

            for index, raw_value in enumerate(
                    raw_values + (
                        (width - len(raw_values)) * [None]  # aligning values
                        if len(raw_values) < width else [])):
                if isinstance(raw_value, dict):
                    raw_value = dict(raw_value)
                    value = raw_value.pop('value', None)
                    metadata[index] = raw_value
                else:
                    value = raw_value

                # Fix this by doing this in charts class methods
                if isinstance(self, Histogram):
                    if value is None:
                        value = (None, None, None)
                    elif not is_list_like(value):
                        value = (value, self.zero, self.zero)
                    elif len(value) == 2:
                        value = (1, value[0], value[1])
                    value = list(map(self._adapt, value))
                elif self._dual:
                    if value is None:
                        value = (None, None)
                    elif not is_list_like(value):
                        value = (value, self.zero)
                    if self._x_adapt:
                        value = (
                            self._x_adapt(value[0]),
                            self._adapt(value[1]))
                    if isinstance(self, BaseMap):
                        value = (self._adapt(value[0]), value[1])
                    else:
                        value = list(map(self._adapt, value))
                else:
                    value = self._adapt(value)

                values.append(value)
            serie_config = SerieConfig()
            serie_config(**dict((k, v) for k, v in self.state.__dict__.items()
                                if k in dir(serie_config)))
            serie_config(**serie_config_kwargs)
            series.append(
                Serie(offset + len(series),
                      title, values, serie_config, metadata))
        return series

    def setup(self, **kwargs):
        """Set up the transient state prior rendering"""
        # Keep labels in case of map
        if getattr(self, 'x_labels', None) is not None:
            self.x_labels = list(self.x_labels)
        if getattr(self, 'y_labels', None) is not None:
            self.y_labels = list(self.y_labels)
        self.state = State(self, **kwargs)
        if isinstance(self.style, type):
            self.style = self.style()
        self.series = self.prepare_values(
            self.raw_series) or []
        self.secondary_series = self.prepare_values(
            self.raw_series2, len(self.series)) or []
        self.horizontal = getattr(self, 'horizontal', False)
        self.svg = Svg(self)
        self._x_labels = None
        self._y_labels = None
        self._x_2nd_labels = None
        self._y_2nd_labels = None
        self.nodes = {}
        self.margin_box = Margin(
            self.margin_top or self.margin,
            self.margin_right or self.margin,
            self.margin_bottom or self.margin,
            self.margin_left or self.margin)
        self._box = Box()
        self.view = None
        if self.logarithmic and self.zero == 0:
            # Explicit min to avoid interpolation dependency
            positive_values = list(filter(
                lambda x: x > 0,
                [val[1] or 1 if self._dual else val
                 for serie in self.series for val in serie.safe_values]))

            self.zero = min(positive_values or (1,)) or 1
        if self._len < 3:
            self.interpolate = None
        self._draw()
        self.svg.pre_render()

    def teardown(self):
        """Remove the transient state after rendering"""
        if os.getenv('PYGAL_KEEP_STATE'):
            return

        del self.state
        self.state = None

    def _repr_svg_(self):
        """Display svg in IPython notebook"""
        return self.render(disable_xml_declaration=True)

    def _repr_png_(self):
        """Display png in IPython notebook"""
        return self.render_to_png()
