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
"""pygal public api functions"""

import base64
import io

from pygal._compat import _ellipsis, is_list_like, u
from pygal.graph.base import BaseGraph


class PublicApi(BaseGraph):

    """Chart public functions"""

    def add(self, title, values, **kwargs):
        """Add a serie to this graph, compat api"""
        if not is_list_like(values) and not isinstance(values, dict):
            values = [values]
        kwargs['title'] = title
        self.raw_series.append((values, kwargs))
        return self

    def __call__(self, *args, **kwargs):
        """Call api: chart(1, 2, 3, title='T')"""
        self.raw_series.append((args, kwargs))
        return self

    def add_xml_filter(self, callback):
        """Add an xml filter for in tree post processing"""
        self.xml_filters.append(callback)
        return self

    def render(self, is_unicode=False, **kwargs):
        """Render the graph, and return the svg string"""
        self.setup(**kwargs)
        svg = self.svg.render(
            is_unicode=is_unicode, pretty_print=self.pretty_print)
        self.teardown()
        return svg

    def render_tree(self, **kwargs):
        """Render the graph, and return (l)xml etree"""
        self.setup(**kwargs)
        svg = self.svg.root
        for f in self.xml_filters:
            svg = f(svg)
        self.teardown()
        return svg

    def render_table(self, **kwargs):
        """Render the data as a html table"""
        # Import here to avoid lxml import
        try:
            from pygal.table import Table
        except ImportError:
            raise ImportError('You must install lxml to use render table')
        return Table(self).render(**kwargs)

    def render_pyquery(self, **kwargs):
        """Render the graph, and return a pyquery wrapped tree"""
        from pyquery import PyQuery as pq
        return pq(self.render(**kwargs), parser='html')

    def render_in_browser(self, **kwargs):
        """Render the graph, open it in your browser with black magic"""
        try:
            from lxml.html import open_in_browser
        except ImportError:
            raise ImportError('You must install lxml to use render in browser')
        kwargs.setdefault('force_uri_protocol', 'https')
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

    def render_data_uri(self, **kwargs):
        """Output a base 64 encoded data uri"""
        # Force protocol as data uri have none
        kwargs.setdefault('force_uri_protocol', 'https')
        return "data:image/svg+xml;charset=utf-8;base64,%s" % (
            base64.b64encode(
                self.render(**kwargs)
            ).decode('utf-8').replace('\n', '')
        )

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
        values = list(self.raw_series[0][0])
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
        """Render a sparkline"""
        spark_options = dict(
            width=200,
            height=50,
            show_dots=False,
            show_legend=False,
            show_x_labels=False,
            show_y_labels=False,
            spacing=0,
            margin=5,
            min_scale=1,
            max_scale=2,
            explicit_size=True,
            no_data_text='',
            js=(),
            classes=(_ellipsis, 'pygal-sparkline')
        )
        spark_options.update(kwargs)
        return self.render(**spark_options)
