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
Solid Guage
For each series a solid guage is shown on the plot area.
"""
from math import pi, sqrt

from pygal.graph.graph import Graph
from pygal.util import alter, decorate


class SolidGauge(Graph):
    def gaugify(self, serie, squares, sq_dimensions, current_square):
        serie_node = self.svg.serie(serie)
        if self.half_pie:
            start_angle = 3 * pi / 2
            center = ((current_square[1] * sq_dimensions[0]) -
                      (sq_dimensions[0] / 2.),
                      (current_square[0] * sq_dimensions[1]) -
                      (sq_dimensions[1] / 4))
            end_angle = pi / 2
        else:
            start_angle = 0
            center = ((current_square[1] * sq_dimensions[0]) -
                      (sq_dimensions[0] / 2.),
                      (current_square[0] * sq_dimensions[1]) -
                      (sq_dimensions[1] / 2.))
            end_angle = 2 * pi

        max_value = serie.metadata.get(0, {}).get('max_value', 100)
        radius = min([sq_dimensions[0] / 2, sq_dimensions[1] / 2]) * .9
        small_radius = radius * serie.inner_radius

        self.svg.gauge_background(
            serie_node, start_angle, center, radius, small_radius, end_angle,
            self.half_pie, self._serie_format(serie, max_value)
        )

        sum_ = 0
        for i, value in enumerate(serie.values):
            if value is None:
                continue
            ratio = min(value, max_value) / max_value
            if self.half_pie:
                angle = 2 * pi * ratio / 2
            else:
                angle = 2 * pi * ratio

            val = self._format(serie, i)
            metadata = serie.metadata.get(i)

            gauge_ = decorate(
                self.svg, self.svg.node(serie_node['plot'], class_="gauge"),
                metadata
            )

            alter(
                self.svg.solid_gauge(
                    serie_node, gauge_, radius, small_radius, angle,
                    start_angle, center, val, i, metadata, self.half_pie,
                    end_angle, self._serie_format(serie, max_value)
                ), metadata
            )
            start_angle += angle
            sum_ += value

        x, y = center
        self.svg.node(
            serie_node['text_overlay'],
            'text',
            class_='value gauge-sum',
            x=x,
            y=y + self.style.value_font_size / 3,
            attrib={
                'text-anchor': 'middle'
            }
        ).text = self._serie_format(serie, sum_)

    def _compute_x_labels(self):
        pass

    def _compute_y_labels(self):
        pass

    def _plot(self):
        """Draw all the serie slices"""
        squares = self._squares()
        sq_dimensions = self.add_squares(squares)

        for index, serie in enumerate(self.series):
            current_square = self._current_square(squares, index)
            self.gaugify(serie, squares, sq_dimensions, current_square)

    def _squares(self):

        n_series_ = len(self.series)
        i = 2

        if sqrt(n_series_).is_integer():
            _x = int(sqrt(n_series_))
            _y = int(sqrt(n_series_))
        else:
            while i * i < n_series_:
                while n_series_ % i == 0:
                    n_series_ = n_series_ / i
                i = i + 1
            _y = int(n_series_)
            _x = int(len(self.series) / _y)
            if len(self.series) == 5:
                _x, _y = 2, 3
            if abs(_x - _y) > 2:
                _sq = 3
                while (_x * _y) - 1 < len(self.series):
                    _x, _y = _sq, _sq
                    _sq += 1
        return (_x, _y)

    def _current_square(self, squares, index):
        current_square = [1, 1]
        steps = index + 1
        steps_taken = 0
        for i in range(squares[0] * squares[1]):
            steps_taken += 1
            if steps_taken != steps and steps_taken % squares[0] != 0:
                current_square[1] += 1
            elif steps_taken != steps and steps_taken % squares[0] == 0:
                current_square[1] = 1
                current_square[0] += 1
            else:
                return tuple(current_square)
        raise Exception(
            'Something went wrong with the current square assignment.'
        )
