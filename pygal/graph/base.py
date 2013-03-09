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
Base for pygal charts

"""

from __future__ import division
from pygal.view import Margin, Box
from pygal.util import (
    get_text_box, get_texts_box, cut, rad, humanize, truncate)
from pygal.svg import Svg
from pygal.util import cached_property, reverse_text_len
from math import sin, cos, sqrt


class BaseGraph(object):
    """Graphs commons"""

    _adapters = []

    def __init__(self, config, series, secondary_series):
        """Init the graph"""
        self.config = config
        self.series = series or []
        self.secondary_series = secondary_series or []
        self.horizontal = getattr(self, 'horizontal', False)
        self.svg = Svg(self)
        self._x_labels = None
        self._y_labels = None
        self._x_2nd_labels = None
        self._y_2nd_labels = None
        self.nodes = {}
        self.margin = Margin(*([20] * 4))
        self._box = Box()
        self.view = None
        if self.logarithmic and self.zero == 0:
            # Explicit min to avoid interpolation dependency
            positive_values = filter(
                lambda x: x > 0,
                [val for serie in self.series for val in serie.safe_values])
            self.zero = min(positive_values) if positive_values else 0
        self._draw()
        self.svg.pre_render()

    def __getattr__(self, attr):
        """Search in config, then in self"""
        if attr in dir(self.config):
            return object.__getattribute__(self.config, attr)
        return object.__getattribute__(self, attr)

    def _split_title(self):
        if not self.title:
            self.title = []
            return
        size = reverse_text_len(self.width, self.title_font_size * 1.1)
        title = self.title.strip()
        self.title = []
        while len(title) > size:
            title_part = title[:size]
            i = title_part.rfind(' ')
            if i == -1:
                i = len(title_part)
            self.title.append(title_part[:i])
            title = title[i:].strip()
        self.title.append(title)

    @property
    def all_series(self):
        return self.series + self.secondary_series

    @property
    def _format(self):
        """Return the value formatter for this graph"""
        return self.value_formatter or (
            humanize if self.human_readable else str)

    def _compute(self):
        """Initial computations to draw the graph"""

    def _plot(self):
        """Actual plotting of the graph"""

    def _compute_margin(self):
        """Compute graph margins from set texts"""
        for series_group in (self.series, self.secondary_series):
            if self.show_legend and series_group:
                h, w = get_texts_box(
                    map(lambda x: truncate(x, self.truncate_legend or 15),
                        cut(series_group, 'title')),
                    self.legend_font_size)
                if self.legend_at_bottom:
                    h_max = max(h, self.legend_box_size)
                    self.margin.bottom += 10 + h_max * round(
                        sqrt(self._order) - 1) * 1.5 + h_max
                else:
                    if series_group is self.series:
                        self.margin.left += 10 + w + self.legend_box_size
                    else:
                        self.margin.right += 10 + w + self.legend_box_size

        if self.title:
            h, _ = get_text_box(self.title[0], self.title_font_size)
            self.margin.top += len(self.title) * (10 + h)

        for xlabels in (self._x_labels, self._x_2nd_labels):
            if xlabels:
                h, w = get_texts_box(
                    cut(xlabels), self.label_font_size)
                self._x_labels_height = 10 + max(
                    w * sin(rad(self.x_label_rotation)), h)
                if xlabels is self._x_labels:
                    self.margin.bottom += self._x_labels_height
                else:
                    self.margin.top += self._x_labels_height
                if self.x_label_rotation:
                    self.margin.right = max(
                        w * cos(rad(self.x_label_rotation)),
                        self.margin.right)
        if not self._x_labels:
            self._x_labels_height = 0

        for ylabels in (self._y_labels, self._y_2nd_labels):
            if ylabels:
                h, w = get_texts_box(
                    cut(ylabels), self.label_font_size)
                if ylabels is self._y_labels:
                    self.margin.left += 10 + max(
                        w * cos(rad(self.y_label_rotation)), h)
                else:
                    self.margin.right += 10 + max(
                        w * cos(rad(self.y_label_rotation)), h)

    @cached_property
    def _legends(self):
        """Getter for series title"""
        return [serie.title for serie in self.series]

    @cached_property
    def _secondary_legends(self):
        """Getter for series title on secondary y axis"""
        return [serie.title for serie in self.secondary_series]

    @cached_property
    def _values(self):
        """Getter for series values (flattened)"""
        return [val
                for serie in self.series
                for val in serie.values
                if val is not None]

    @cached_property
    def _secondary_values(self):
        """Getter for secondary series values (flattened)"""
        return [val
                for serie in self.secondary_series
                for val in serie.values
                if val is not None]

    @cached_property
    def _len(self):
        """Getter for the maximum series size"""
        return max([
            len(serie.values)
            for serie in self.all_series] or [0])

    @cached_property
    def _secondary_min(self):
        """Getter for the minimum series value"""
        return (self.range and self.range[0]) or (
            min(self._secondary_values) if self._secondary_values else None)

    @cached_property
    def _min(self):
        """Getter for the minimum series value"""
        return (self.range and self.range[0]) or (
            min(self._values) if self._values else None)

    @cached_property
    def _max(self):
        """Getter for the maximum series value"""
        return (self.range and self.range[1]) or (
            max(self._values) if self._values else None)

    @cached_property
    def _secondary_max(self):
        """Getter for the maximum series value"""
        return (self.range and self.range[1]) or (
            max(self._secondary_values) if self._secondary_values else None)

    @cached_property
    def _order(self):
        """Getter for the maximum series value"""
        return len(self.all_series)

    def _draw(self):
        """Draw all the things"""
        self._compute()
        self._compute_secondary()
        self._post_compute()
        self._split_title()
        self._compute_margin()
        self._decorate()
        if self.series and self._has_data():
            self._plot()
        else:
            self.svg.draw_no_data()

    def _has_data(self):
        """Check if there is any data"""
        return sum(
            map(len, map(lambda s: s.safe_values, self.series))) != 0 and (
                sum(map(abs, self._values)) != 0)

    def render(self, is_unicode):
        """Render the graph, and return the svg string"""
        return self.svg.render(
            is_unicode=is_unicode, pretty_print=self.pretty_print)

    def render_tree(self):
        """Render the graph, and return lxml tree"""
        return self.svg.root
