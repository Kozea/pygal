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
Ghost container

It is used to delegate rendering to real objects but keeping config in place

"""

import io
import sys
from pygal.config import Config
from pygal.graph import CHARTS_NAMES
from pygal.util import prepare_values


REAL_CHARTS = {}
for NAME in CHARTS_NAMES:
    mod_name = 'pygal.graph.%s' % NAME.lower()
    __import__(mod_name)
    mod = sys.modules[mod_name]
    REAL_CHARTS[NAME] = getattr(mod, NAME)


class Ghost(object):

    def __init__(self, config=None, **kwargs):
        """Init config"""
        name = self.__class__.__name__
        self.cls = REAL_CHARTS[name]
        if config and isinstance(config, type):
            config = config()

        if config:
            config = config.copy()
        else:
            config = Config()

        config(**kwargs)
        self.config = config
        self.raw_series = []

    def add(self, title, values):
        """Add a serie to this graph"""
        if not hasattr(values, '__iter__') and not isinstance(values, dict):
            values = [values]
        self.raw_series.append((title, values))

    def make_series(self):
        return prepare_values(self.raw_series, self.config, self.cls)

    def make_instance(self):
        self.config(**self.__dict__)
        series = self.make_series()
        self._last__inst = self.cls(self.config, series)
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

    def render_to_png(self, filename):
        """Render the graph, convert it to png and write it to filename"""
        import cairosvg
        from io import BytesIO
        fakefile = BytesIO()
        fakefile.write(self.render())
        fakefile.seek(0)
        cairosvg.surface.PNGSurface.convert(
            file_obj=fakefile, write_to=filename)
