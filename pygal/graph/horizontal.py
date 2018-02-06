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
"""Horizontal graph mixin"""

from pygal.graph.graph import Graph
from pygal.view import HorizontalLogView, HorizontalView


class HorizontalGraph(Graph):
    """Horizontal graph mixin"""

    def __init__(self, *args, **kwargs):
        """Set the horizontal flag to True"""
        self.horizontal = True
        super(HorizontalGraph, self).__init__(*args, **kwargs)

    def _post_compute(self):
        """After computations transpose labels"""
        self._x_labels, self._y_labels = self._y_labels, self._x_labels
        self._x_labels_major, self._y_labels_major = (
            self._y_labels_major, self._x_labels_major
        )
        self._x_2nd_labels, self._y_2nd_labels = (
            self._y_2nd_labels, self._x_2nd_labels
        )
        self.show_y_guides, self.show_x_guides = (
            self.show_x_guides, self.show_y_guides
        )

    def _axes(self):
        """Set the _force_vertical flag when rendering axes"""
        self.view._force_vertical = True
        super(HorizontalGraph, self)._axes()
        self.view._force_vertical = False

    def _set_view(self):
        """Assign a horizontal view to current graph"""
        if self.logarithmic:
            view_class = HorizontalLogView
        else:
            view_class = HorizontalView

        self.view = view_class(
            self.width - self.margin_box.x, self.height - self.margin_box.y,
            self._box
        )

    def _get_x_label(self, i):
        """Convenience function to get the x_label of a value index"""
        if not self.x_labels or not self._y_labels or len(self._y_labels) <= i:
            return
        return self._y_labels[i][0]
