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

"""Dual chart base. Dual means a chart with 2 scaled axis like xy"""

from pygal._compat import is_str
from pygal.graph.graph import Graph
from pygal.util import compute_scale, cut


class Dual(Graph):
    _dual = True

    def _value_format(self, value):
        """
        Format value for dual value display.
        """
        return '%s: %s' % (
            self._x_format(value[0]),
            self._y_format(value[1]))

    def _compute_x_labels(self):
        x_pos = compute_scale(
            self._box.xmin, self._box.xmax, self.logarithmic,
            self.order_min, self.min_scale, self.max_scale
        )
        if self.x_labels:
            self._x_labels = []
            for i, x_label in enumerate(self.x_labels):
                if isinstance(x_label, dict):
                    pos = self._x_adapt(x_label.get('value'))
                    title = x_label.get('label', self._x_format(pos))
                elif is_str(x_label):
                    pos = self._x_adapt(x_pos[i % len(x_pos)])
                    title = x_label
                else:
                    pos = self._x_adapt(x_label)
                    title = self._x_format(pos)

                self._x_labels.append((title, pos))
            self._box.xmin = min(self._box.xmin, min(cut(self._x_labels, 1)))
            self._box.xmax = max(self._box.xmax, max(cut(self._x_labels, 1)))

        else:
            self._x_labels = list(zip(map(self._x_format, x_pos), x_pos))

    def _compute_x_labels_major(self):
        # In case of dual, x labels must adapters and so majors too
        self.x_labels_major = self.x_labels_major and list(
            map(self._x_adapt, self.x_labels_major))
        super(Dual, self)._compute_x_labels_major()

    def _get_x_label(self, i):
        """Convenience function to get the x_label of a value index"""
        return
