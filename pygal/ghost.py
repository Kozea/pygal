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
Ghost container

It is used to delegate rendering to real objects but keeping config in place

"""

from __future__ import division
import io
import sys
from pygal.config import Config
from pygal.lineconfig import LineConfig
from pygal._compat import u, is_list_like
from pygal.graph import CHARTS_NAMES
from pygal.util import prepare_values
from uuid import uuid4


class ChartCollection(object):
    pass


REAL_CHARTS = {}
for NAME in CHARTS_NAMES:
    mod_name = 'pygal.graph.%s' % NAME.lower()
    __import__(mod_name)
    mod = sys.modules[mod_name]
    chart = getattr(mod, NAME)
    if issubclass(chart, ChartCollection):
        for name, chart in chart.__dict__.items():
            if name.startswith('_'):
                continue
            REAL_CHARTS['%s_%s' % (NAME, name)] = chart
    else:
        REAL_CHARTS[NAME] = chart


class Ghost(object):

    def __init__(self, config=None, **kwargs):
        """Init config"""
        name = self.__class__.__name__
        self.cls = REAL_CHARTS[name]
        self.uuid = str(uuid4())
        if config and isinstance(config, type):
            config = config()

        if config:
            config = config.copy()
        else:
            config = Config()

        config(**kwargs)
        self.config = config
        self.raw_series = []
        self.raw_series2 = []
        self.xml_filters = []

    def add(self, title, values, secondary=False, lineConfig=None):
        """Add a serie to this graph"""
        if not is_list_like(values) and not isinstance(values, dict):
            values = [values]
        if lineConfig is None:
            lineConfig = LineConfig()
        if secondary:
            self.raw_series2.append((title, values, lineConfig))
        else:
            self.raw_series.append((title, values, lineConfig))

    def add_xml_filter(self, callback):
        self.xml_filters.append(callback)

    def make_series(self, series):
        return prepare_values(series, self.config, self.cls)

    def make_instance(self, overrides={}):
        self.config(**self.__dict__)
        self.config.__dict__.update(overrides)
        series = self.make_series(self.raw_series)
        secondary_series = self.make_series(self.raw_series2)
        self._last__inst = self.cls(
            self.config, series, secondary_series, self.uuid,
            self.xml_filters)
        return self._last__inst

    # Rendering
    def render(self, is_unicode=False):
        return self.make_instance().render(is_unicode=is_unicode)

    def render_tree(self):
        return self.make_instance().render_tree()

    def render_pyquery(self):
        """Render the graph, and return a pyquery wrapped tree"""
        from pyquery import PyQuery as pq
        return pq(self.render_tree())

    def render_in_browser(self):
        """Render the graph, open it in your browser with black magic"""
        from lxml.html import open_in_browser
        open_in_browser(self.render_tree(), encoding='utf-8')

    def render_response(self):
        """Render the graph, and return a Flask response"""
        from flask import Response
        return Response(self.render(), mimetype='image/svg+xml')

    def render_to_file(self, filename):
        """Render the graph, and write it to filename"""
        with io.open(filename, 'w', encoding='utf-8') as f:
            f.write(self.render(is_unicode=True))

    def render_to_png(self, filename=None, dpi=72):
        """Render the graph, convert it to png and write it to filename"""
        import cairosvg
        return cairosvg.svg2png(
            bytestring=self.render(), write_to=filename, dpi=dpi)

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
            show_y_labels=False,
            spacing=0,
            margin=5,
            explicit_size=True
        )
        spark_options.update(kwargs)
        return self.make_instance(spark_options).render()

    def _repr_png_(self):
        """Display png in IPython notebook"""
        return self.render_to_png()
