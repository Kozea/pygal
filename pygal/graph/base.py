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
Base for pygal charts

"""

from __future__ import division
from pygal._compat import u, is_list_like, to_unicode
from pygal.view import Margin, Box
from pygal.config import Config
from pygal.state import State
from pygal.util import compose, ident
from pygal.svg import Svg
from pygal.serie import Serie
from pygal.config import SerieConfig
from pygal.adapters import (
    not_zero, positive, decimal_to_float)
from functools import reduce
from uuid import uuid4
import io


class BaseGraph(object):
    """Graphs commons"""

    _adapters = []

    def __init__(self, config=None, **kwargs):
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
        if name.startswith('__') or getattr(self, 'state', None) is None:
            super(BaseGraph, self).__setattr__(name, value)
        else:
            setattr(self.state, name, value)

    def __getattribute__(self, name):
        if name.startswith('__') or name == 'state' or getattr(
                self, 'state', None
        ) is None or name not in self.state.__dict__:
            return super(BaseGraph, self).__getattribute__(name)
        return getattr(self.state, name)

    def add(self, title, values, **kwargs):
        """Add a serie to this graph"""
        if not is_list_like(values) and not isinstance(values, dict):
            values = [values]
        if kwargs.get('secondary', False):
            self.raw_series2.append((title, values, kwargs))
        else:
            self.raw_series.append((title, values, kwargs))

    def add_xml_filter(self, callback):
        self.xml_filters.append(callback)

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
        adapter = reduce(compose, adapters) if not self.strict else ident
        x_adapter = reduce(
            compose, self._x_adapters) if getattr(
                self, '_x_adapters', None) else None
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
                        if k in self.x_labels:
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
                    value = list(map(adapter, value))
                elif self._dual:
                    if value is None:
                        value = (None, None)
                    elif not is_list_like(value):
                        value = (value, self.zero)
                    if x_adapter:
                        value = (x_adapter(value[0]), adapter(value[1]))
                    if isinstance(self, BaseMap):
                        value = (adapter(value[0]), value[1])
                    else:
                        value = list(map(adapter, value))
                else:
                    value = adapter(value)

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
        """Init the graph"""
        # Keep labels in case of map
        if getattr(self, 'x_labels', None) is not None:
            self.x_labels = list(map(to_unicode, self.x_labels))
        if getattr(self, 'y_labels', None) is not None:
            self.y_labels = list(self.y_labels)
        self.state = State(self, **kwargs)
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
        del self.state
        self.state = None

    def render(self, is_unicode=False, **kwargs):
        """Render the graph, and return the svg string"""
        self.setup(**kwargs)
        svg = self.svg.render(
            is_unicode=is_unicode, pretty_print=self.pretty_print)
        self.teardown()
        return svg

    def render_tree(self):
        """Render the graph, and return (l)xml etree"""
        self.setup()
        svg = self.svg.root
        for f in self.xml_filters:
            svg = f(svg)
        self.teardown()
        return svg

    def render_table(self, **kwargs):
        # Import here to avoid lxml import
        try:
            from pygal.table import Table
        except ImportError:
            raise ImportError('You must install lxml to use render table')
        return Table(self).render(**kwargs)

    def render_pyquery(self):
        """Render the graph, and return a pyquery wrapped tree"""
        from pyquery import PyQuery as pq
        return pq(self.render(), parser='html')

    def render_in_browser(self, **kwargs):
        """Render the graph, open it in your browser with black magic"""
        try:
            from lxml.html import open_in_browser
        except ImportError:
            raise ImportError('You must install lxml to use render in browser')
        open_in_browser(self.render_tree(**kwargs), encoding='utf-8')

    def render_response(self, **kwargs):
        """Render the graph, and return a Flask response"""
        from flask import Response
        return Response(self.render(**kwargs), mimetype='image/svg+xml')

    def render_django_response(self, **kwargs):
        """Render the graph, and return a Django response"""
        from django.http import HttpResponse
        return HttpResponse(
            self.render(**kwargs), content_type='image/svg+xml')

    def render_to_file(self, filename, **kwargs):
        """Render the graph, and write it to filename"""
        with io.open(filename, 'w', encoding='utf-8') as f:
            f.write(self.render(is_unicode=True, **kwargs))

    def render_to_png(self, filename=None, dpi=72, **kwargs):
        """Render the graph, convert it to png and write it to filename"""
        import cairosvg
        return cairosvg.svg2png(
            bytestring=self.render(**kwargs), write_to=filename, dpi=dpi)

    def render_sparktext(self, relative_to=None):
        """Make a mini text sparkline from chart"""
        bars = u('▁▂▃▄▅▆▇█')
        if len(self.raw_series) == 0:
            return u('')
        values = list(self.raw_series[0][1])
        if len(values) == 0:
            return u('')

        chart = u('')
        values = list(map(lambda x: max(x, 0), values))

        vmax = max(values)
        if relative_to is None:
            relative_to = min(values)

        if (vmax - relative_to) == 0:
            chart = bars[0] * len(values)
            return chart

        divisions = len(bars) - 1
        for value in values:
            chart += bars[int(divisions *
                              (value - relative_to) / (vmax - relative_to))]
        return chart

    def render_sparkline(self, **kwargs):
        spark_options = dict(
            width=200,
            height=50,
            show_dots=False,
            show_legend=False,
            show_x_labels=False,
            show_y_labels=False,
            spacing=0,
            margin=5,
            explicit_size=True
        )
        spark_options.update(kwargs)
        return self.render(**spark_options)

    def _repr_svg_(self):
        """Display svg in IPython notebook"""
        return self.render(disable_xml_declaration=True)

    def _repr_png_(self):
        """Display png in IPython notebook"""
        return self.render_to_png()
