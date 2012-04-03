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
from __future__ import division
import io
from pygal.serie import Serie
from pygal.view import Margin, Box
from pygal.util import round_to_scale, cut, rad, humanize
from pygal.svg import Svg
from pygal.config import Config
from pygal.util import cached_property
from math import log10, sin, cos, floor, ceil


class BaseGraph(object):
    """Graphs commons"""

    def __init__(self, config=None, **kwargs):
        """Init the graph"""
        self.config = config or Config()
        self.config(**kwargs)
        self.svg = Svg(self)
        self.series = []
        self._x_labels = self._y_labels = None

    def add(self, title, values):
        """Add a serie to this graph"""
        self.series.append(Serie(title, values, len(self.series)))

    def _init(self):
        """Init the graph"""
        self.margin = Margin(*([20] * 4))
        self._box = Box()

    def __getattr__(self, attr):
        """Search in config, then in self"""
        if attr in dir(self.config):
            return object.__getattribute__(self.config, attr)
        return object.__getattribute__(self, attr)

    @property
    def _format(self):
        """Return the value formatter for this graph"""
        return humanize if self.human_readable else str

    def _compute_logarithmic_scale(self, min_, max_):
        """Compute an optimal scale for logarithmic"""
        min_order = int(floor(log10(min_)))
        max_order = int(ceil(log10(max_)))
        positions = []
        amplitude = max_order - min_order
        if amplitude <= 1:
            return []
        detail = 10.
        while amplitude * detail < 20:
            detail *= 2
        while amplitude * detail > 50:
            detail /= 2
        for order in range(min_order, max_order + 1):
            for i in range(int(detail)):
                tick = (10 * i / detail or 1) * 10 ** order
                tick = round_to_scale(tick, tick)
                if min_ <= tick <= max_ and tick not in positions:
                    positions.append(tick)
        return positions

    def _compute_scale(self, min_, max_, min_scale=4, max_scale=20):
        """Compute an optimal scale between min and max"""
        if min_ == 0 and max_ == 0:
            return [0]
        if max_ - min_ == 0:
            return [min_]
        if self.logarithmic:
            log_scale = self._compute_logarithmic_scale(min_, max_)
            if log_scale:
                return log_scale
                # else we fallback to normal scalling
        order = round(log10(max(abs(min_), abs(max_)))) - 1
        while (max_ - min_) / (10 ** order) < min_scale:
            order -= 1
        step = float(10 ** order)
        while (max_ - min_) / step > max_scale:
            step *= 2.
        positions = []
        position = round_to_scale(min_, step)
        while position < (max_ + step):
            rounded = round_to_scale(position, step)
            if min_ <= rounded <= max_:
                if rounded not in positions:
                    positions.append(rounded)
            position += step
        if len(positions) < 2:
            return [min_, max_]
        return positions

    def _text_len(self, lenght, fs):
        """Approximation of text length"""
        return lenght * 0.6 * fs

    def _get_text_box(self, text, fs):
        """Approximation of text bounds"""
        return (fs, self._text_len(len(text), fs))

    def _get_texts_box(self, texts, fs):
        """Approximation of multiple texts bounds"""
        max_len = max(map(len, texts))
        return (fs, self._text_len(max_len, fs))

    def _compute(self):
        """Initial computations to draw the graph"""

    def _plot(self):
        """Actual plotting of the graph"""

    def _compute_margin(self):
        """Compute graph margins from set texts"""
        if self.show_legend:
            h, w = self._get_texts_box(
                cut(self.series, 'title'), self.legend_font_size)
            self.margin.right += 10 + w + self.legend_box_size

        if self.title:
            h, w = self._get_text_box(self.title, self.title_font_size)
            self.margin.top += 10 + h

        if self._x_labels:
            h, w = self._get_texts_box(
                cut(self._x_labels), self.label_font_size)
            self.margin.bottom += 10 + max(
                w * sin(rad(self.x_label_rotation)), h)
            if self.x_label_rotation:
                self.margin.right = max(
                    w * cos(rad(self.x_label_rotation)),
                    self.margin.right)
        if self._y_labels:
            h, w = self._get_texts_box(
                cut(self._y_labels), self.label_font_size)
            self.margin.left += 10 + max(
                w * cos(rad(self.y_label_rotation)), h)

    @cached_property
    def _legends(self):
        """Getter for series title"""
        return [serie.title for serie in self.series]

    @cached_property
    def _values(self):
        """Getter for series values (flattened)"""
        return [val
                for serie in self.series
                for val in serie.values
                if val != None]

    @cached_property
    def _len(self):
        """Getter for the maximum series size"""
        return max([len(serie.values) for serie in self.series])

    def _draw(self):
        """Draw all the things"""
        self._compute()
        self._compute_margin()
        self._decorate()
        self._plot()

    def _has_data(self):
        """Check if there is any data"""
        if len(self.series) == 0:
            return False
        for serie in self.series:
            if not hasattr(serie.values, '__iter__'):
                serie.values = [serie.values]
        if sum(map(len, map(lambda s: s.values, self.series))) == 0:
            return False
        return True

    def _render(self):
        """Make the graph internally"""
        self._init()
        self.svg._init()
        if self._has_data():
            self._draw()
            self.svg._pre_render(False)
        else:
            self.svg._pre_render(True)

    def render(self, is_unicode=False):
        """Render the graph, and return the svg string"""
        self._render()
        return self.svg.render(is_unicode=is_unicode)

    def render_tree(self):
        """Render the graph, and return lxml tree"""
        self._render()
        return self.svg.root

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
