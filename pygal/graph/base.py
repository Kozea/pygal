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
from pygal.view import Margin, Box
from pygal.util import (
    get_text_box, get_texts_box, cut, rad, humanize, truncate, split_title)
from pygal.svg import Svg
from pygal.util import cached_property, majorize
from math import sin, cos, sqrt, ceil


class BaseGraph(object):
    """Graphs commons"""

    _adapters = []

    def __init__(self, config, series, secondary_series, uuid, xml_filters):
        """Init the graph"""
        self.uuid = uuid
        self.__dict__.update(config.to_dict())
        self.config = config
        self.series = series or []
        self.secondary_series = secondary_series or []
        self.xml_filters = xml_filters or []
        self.horizontal = getattr(self, 'horizontal', False)
        self.svg = Svg(self)
        self._x_labels = None
        self._y_labels = None
        self._x_2nd_labels = None
        self._y_2nd_labels = None
        self.nodes = {}
        self.margin = Margin(self.margin_top or self.margin,
                             self.margin_right or self.margin,
                             self.margin_bottom or self.margin,
                             self.margin_left or self.margin)
        self._box = Box()
        self.view = None
        if self.logarithmic and self.zero == 0:
            # Explicit min to avoid interpolation dependency
            if self._dual:
                get = lambda x: x[1] or 1
            else:
                get = lambda x: x

            positive_values = list(filter(
                lambda x: x > 0,
                [get(val)
                 for serie in self.series for val in serie.safe_values]))

            self.zero = min(positive_values or (1,)) or 1
        if self._len < 3:
            self.interpolate = None
        self._draw()
        self.svg.pre_render()

    @property
    def all_series(self):
        return self.series + self.secondary_series

    @property
    def _x_format(self):
        """Return the value formatter for this graph"""
        return self.config.x_value_formatter or (
            humanize if self.human_readable else str)

    @property
    def _format(self):
        """Return the value formatter for this graph"""
        return self.config.value_formatter or (
            humanize if self.human_readable else str)

    def _compute(self):
        """Initial computations to draw the graph"""

    def _compute_margin(self):
        """Compute graph margins from set texts"""
        self._legend_at_left_width = 0
        for series_group in (self.series, self.secondary_series):
            if self.show_legend and series_group:
                h, w = get_texts_box(
                    map(lambda x: truncate(x, self.truncate_legend or 15),
                        cut(series_group, 'title')),
                    self.legend_font_size)
                if self.legend_at_bottom:
                    h_max = max(h, self.legend_box_size)
                    cols = (self._order // self.legend_at_bottom_columns
                            if self.legend_at_bottom_columns
                            else ceil(sqrt(self._order)) or 1)
                    self.margin.bottom += self.spacing + h_max * round(
                        cols - 1) * 1.5 + h_max
                else:
                    if series_group is self.series:
                        legend_width = self.spacing + w + self.legend_box_size
                        self.margin.left += legend_width
                        self._legend_at_left_width += legend_width
                    else:
                        self.margin.right += (
                            self.spacing + w + self.legend_box_size)

        self._x_labels_height = 0
        if (self._x_labels or self._x_2nd_labels) and self.show_x_labels:
            for xlabels in (self._x_labels, self._x_2nd_labels):
                if xlabels:
                    h, w = get_texts_box(
                        map(lambda x: truncate(x, self.truncate_label or 25),
                            cut(xlabels)),
                        self.label_font_size)
                    self._x_labels_height = self.spacing + max(
                        w * sin(rad(self.x_label_rotation)), h)
                    if xlabels is self._x_labels:
                        self.margin.bottom += self._x_labels_height
                    else:
                        self.margin.top += self._x_labels_height
                    if self.x_label_rotation:
                        self.margin.right = max(
                            w * cos(rad(self.x_label_rotation)),
                            self.margin.right)

        if self.show_y_labels:
            for ylabels in (self._y_labels, self._y_2nd_labels):
                if ylabels:
                    h, w = get_texts_box(
                        cut(ylabels), self.label_font_size)
                    if ylabels is self._y_labels:
                        self.margin.left += self.spacing + max(
                            w * cos(rad(self.y_label_rotation)), h)
                    else:
                        self.margin.right += self.spacing + max(
                            w * cos(rad(self.y_label_rotation)), h)

        self.title = split_title(
            self.title, self.width, self.title_font_size)

        if self.title:
            h, _ = get_text_box(self.title[0], self.title_font_size)
            self.margin.top += len(self.title) * (self.spacing + h)

        self.x_title = split_title(
            self.x_title, self.width - self.margin.x, self.title_font_size)

        self._x_title_height = 0
        if self.x_title:
            h, _ = get_text_box(self.x_title[0], self.title_font_size)
            height = len(self.x_title) * (self.spacing + h)
            self.margin.bottom += height
            self._x_title_height = height + self.spacing

        self.y_title = split_title(
            self.y_title, self.height - self.margin.y, self.title_font_size)

        self._y_title_height = 0
        if self.y_title:
            h, _ = get_text_box(self.y_title[0], self.title_font_size)
            height = len(self.y_title) * (self.spacing + h)
            self.margin.left += height
            self._y_title_height = height + self.spacing

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
        return (self.range[0] if (self.range and self.range[0] is not None)
                else (min(self._secondary_values)
                      if self._secondary_values else None))

    @cached_property
    def _min(self):
        """Getter for the minimum series value"""
        return (self.range[0] if (self.range and self.range[0] is not None)
                else (min(self._values)
                      if self._values else None))

    @cached_property
    def _max(self):
        """Getter for the maximum series value"""
        return (self.range[1] if (self.range and self.range[1] is not None)
                else (max(self._values) if self._values else None))

    @cached_property
    def _secondary_max(self):
        """Getter for the maximum series value"""
        return (self.range[1] if (self.range and self.range[1] is not None)
                else (max(self._secondary_values)
                      if self._secondary_values else None))

    @cached_property
    def _order(self):
        """Getter for the number of series"""
        return len(self.all_series)

    @cached_property
    def _x_major_labels(self):
        """Getter for the x major label"""
        if self.x_labels_major:
            return self.x_labels_major
        if self.x_labels_major_every:
            return [self._x_labels[i][0] for i in range(
                0, len(self._x_labels), self.x_labels_major_every)]
        if self.x_labels_major_count:
            label_count = len(self._x_labels)
            major_count = self.x_labels_major_count
            if (major_count >= label_count):
                return [label[0] for label in self._x_labels]

            return [self._x_labels[
                    int(i * (label_count - 1) / (major_count - 1))][0]
                    for i in range(major_count)]

        return []

    @cached_property
    def _y_major_labels(self):
        """Getter for the y major label"""
        if self.y_labels_major:
            return self.y_labels_major
        if self.y_labels_major_every:
            return [self._y_labels[i][1] for i in range(
                0, len(self._y_labels), self.y_labels_major_every)]
        if self.y_labels_major_count:
            label_count = len(self._y_labels)
            major_count = self.y_labels_major_count
            if (major_count >= label_count):
                return [label[1] for label in self._y_labels]

            return [self._y_labels[
                int(i * (label_count - 1) / (major_count - 1))][1]
                for i in range(major_count)]

        return majorize(
            cut(self._y_labels, 1)
        )

    def _draw(self):
        """Draw all the things"""
        self._compute()
        self._compute_secondary()
        self._post_compute()
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

    def render(self, is_unicode=False):
        """Render the graph, and return the svg string"""
        return self.svg.render(
            is_unicode=is_unicode, pretty_print=self.pretty_print)

    def render_tree(self):
        """Render the graph, and return (l)xml etree"""
        svg = self.svg.root
        for f in self.xml_filters:
            svg = f(svg)
        return svg
