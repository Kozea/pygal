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
"""
Stacked Bar chart: Like a bar chart but with all series stacking
on top of the others instead of being displayed side by side.
"""

from pygal.adapters import none_to_zero
from pygal.graph.bar import Bar


class StackedBar(Bar):
    """Stacked Bar graph class"""

    _adapters = [none_to_zero]

    def _get_separated_values(self, secondary=False):
        """Separate values between positives and negatives stacked"""
        series = self.secondary_series if secondary else self.series
        transposed = list(zip(*[serie.values for serie in series]))
        positive_vals = [
            sum([val for val in vals if val is not None and val >= self.zero])
            for vals in transposed
        ]
        negative_vals = [
            sum([val for val in vals if val is not None and val < self.zero])
            for vals in transposed
        ]
        return positive_vals, negative_vals

    def _compute_box(self, positive_vals, negative_vals):
        """Compute Y min and max"""
        if self.range and self.range[0] is not None:
            self._box.ymin = self.range[0]
        else:
            self._box.ymin = negative_vals and min(
                min(negative_vals), self.zero
            ) or self.zero
        if self.range and self.range[1] is not None:
            self._box.ymax = self.range[1]
        else:
            self._box.ymax = positive_vals and max(
                max(positive_vals), self.zero
            ) or self.zero

    def _compute(self):
        """Compute y min and max and y scale and set labels"""
        positive_vals, negative_vals = self._get_separated_values()

        if self.logarithmic:
            positive_vals = list(
                filter(lambda x: x > self.zero, positive_vals)
            )
            negative_vals = list(
                filter(lambda x: x > self.zero, negative_vals)
            )

        self._compute_box(positive_vals, negative_vals)
        positive_vals = positive_vals or [self.zero]
        negative_vals = negative_vals or [self.zero]

        self._x_pos = [
            x / self._len for x in range(self._len + 1)
        ] if self._len > 1 else [0, 1]  # Center if only one value

        self._points(self._x_pos)

        self.negative_cumulation = [0] * self._len
        self.positive_cumulation = [0] * self._len

        if self.secondary_series:
            positive_vals, negative_vals = self._get_separated_values(True)
            positive_vals = positive_vals or [self.zero]
            negative_vals = negative_vals or [self.zero]
            self.secondary_negative_cumulation = [0] * self._len
            self.secondary_positive_cumulation = [0] * self._len
            self._pre_compute_secondary(positive_vals, negative_vals)

        self._x_pos = [(i + .5) / self._len for i in range(self._len)]

    def _pre_compute_secondary(self, positive_vals, negative_vals):
        """Compute secondary y min and max"""
        self._secondary_min = (
            negative_vals and min(min(negative_vals), self.zero)
        ) or self.zero
        self._secondary_max = (
            positive_vals and max(max(positive_vals), self.zero)
        ) or self.zero

    def _bar(self, serie, parent, x, y, i, zero, secondary=False):
        """Internal stacking bar drawing function"""
        if secondary:
            cumulation = (
                self.secondary_negative_cumulation
                if y < self.zero else self.secondary_positive_cumulation
            )
        else:
            cumulation = (
                self.negative_cumulation
                if y < self.zero else self.positive_cumulation
            )
        zero = cumulation[i]
        cumulation[i] = zero + y
        if zero == 0:
            zero = self.zero
            y -= self.zero
        y += zero

        width = (self.view.x(1) - self.view.x(0)) / self._len
        x, y = self.view((x, y))
        y = y or 0
        series_margin = width * self._series_margin
        x += series_margin
        width -= 2 * series_margin
        if self.secondary_series:
            width /= 2
            x += int(secondary) * width
            serie_margin = width * self._serie_margin
            x += serie_margin
            width -= 2 * serie_margin
        height = self.view.y(zero) - y
        r = serie.rounded_bars * 1 if serie.rounded_bars else 0
        self.svg.transposable_node(
            parent,
            'rect',
            x=x,
            y=y,
            rx=r,
            ry=r,
            width=width,
            height=height,
            class_='rect reactive tooltip-trigger'
        )
        return x, y, width, height

    def _plot(self):
        """Draw bars for series and secondary series"""
        for serie in self.series[::-1 if self.stack_from_top else 1]:
            self.bar(serie)
        for serie in self.secondary_series[::-1 if self.stack_from_top else 1]:
            self.bar(serie, True)
