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
Projection and bounding helpers
"""

from __future__ import division
from math import sin, cos, log10, pi


class Margin(object):
    """Graph margin"""
    def __init__(self, top, right, bottom, left):
        self.top = top
        self.right = right
        self.bottom = bottom
        self.left = left

    @property
    def x(self):
        """Helper for total x margin"""
        return self.left + self.right

    @property
    def y(self):
        """Helper for total y margin"""
        return self.top + self.bottom


class Box(object):
    """Chart boundings"""
    margin = .02

    def __init__(self, xmin=0, ymin=0, xmax=1, ymax=1):
        self._xmin = xmin
        self._ymin = ymin
        self._xmax = xmax
        self._ymax = ymax

    def set_polar_box(self, rmin=0, rmax=1, tmin=0, tmax=2 * pi):
        self._rmin = rmin
        self._rmax = rmax
        self._tmin = tmin
        self._tmax = tmax
        self.xmin = self.ymin = rmin - rmax
        self.xmax = self.ymax = rmax - rmin

    @property
    def xmin(self):
        return self._xmin

    @xmin.setter
    def xmin(self, value):
        if value:
            self._xmin = value

    @property
    def ymin(self):
        return self._ymin

    @ymin.setter
    def ymin(self, value):
        if value:
            self._ymin = value

    @property
    def xmax(self):
        return self._xmax

    @xmax.setter
    def xmax(self, value):
        if value:
            self._xmax = value

    @property
    def ymax(self):
        return self._ymax

    @ymax.setter
    def ymax(self, value):
        if value:
            self._ymax = value

    @property
    def width(self):
        """Helper for box width"""
        return self.xmax - self.xmin

    @property
    def height(self):
        """Helper for box height"""
        return self.ymax - self.ymin

    def swap(self):
        """Return the box (for horizontal graphs)"""
        self.xmin, self.ymin = self.ymin, self.xmin
        self.xmax, self.ymax = self.ymax, self.xmax

    def fix(self, with_margin=True):
        """Correct box when no values and take margin in account"""
        if not self.width:
            self.xmax = self.xmin + 1
        if not self.height:
            self.ymin -= .5
            self.ymax = self.ymin + 1
        xmargin = self.margin * self.width
        self.xmin -= xmargin
        self.xmax += xmargin
        if with_margin:
            ymargin = self.margin * self.height
            self.ymin -= ymargin
            self.ymax += ymargin


class View(object):
    """Projection base class"""
    def __init__(self, width, height, box):
        self.width = width
        self.height = height
        self.box = box
        self.box.fix()

    def x(self, x):
        """Project x"""
        if x is None:
            return None
        return self.width * (x - self.box.xmin) / self.box.width

    def y(self, y):
        """Project y"""
        if y is None:
            return None
        return (self.height - self.height *
                (y - self.box.ymin) / self.box.height)

    def __call__(self, xy):
        """Project x and y"""
        x, y = xy
        return (self.x(x), self.y(y))


class HorizontalView(View):
    def __init__(self, width, height, box):
        self._force_vertical = None
        self.width = width
        self.height = height

        self.box = box
        self.box.fix()
        self.box.swap()

    def x(self, x):
        """Project x"""
        if x is None:
            return None
        if self._force_vertical:
            return super(HorizontalView, self).x(x)
        return super(HorizontalView, self).y(x)

    def y(self, y):
        if y is None:
            return None
        if self._force_vertical:
            return super(HorizontalView, self).y(y)
        return super(HorizontalView, self).x(y)


class PolarView(View):
    """Polar projection for pie like graphs"""

    def __call__(self, rhotheta):
        """Project rho and theta"""
        if None in rhotheta:
            return None, None
        rho, theta = rhotheta
        return super(PolarView, self).__call__(
            (rho * cos(theta), rho * sin(theta)))


class PolarLogView(View):
    """Logarithmic polar projection"""

    def __init__(self, width, height, box):
        super(PolarLogView, self).__init__(width, height, box)
        if not hasattr(box, '_rmin') or not hasattr(box, '_rmax'):
            raise Exception(
                'Box must be set with set_polar_box for polar charts')

        self.log10_rmax = log10(self.box._rmax)
        self.log10_rmin = log10(self.box._rmin)
        if self.log10_rmin == self.log10_rmax:
            self.log10_rmax = self.log10_rmin + 1

    def __call__(self, rhotheta):
        """Project rho and theta"""
        if None in rhotheta:
            return None, None
        rho, theta = rhotheta
        # Center case
        if rho == 0:
            return super(PolarLogView, self).__call__((0, 0))
        rho = (self.box._rmax - self.box._rmin) * (
            log10(rho) - self.log10_rmin) / (
            self.log10_rmax - self.log10_rmin)
        return super(PolarLogView, self).__call__(
            (rho * cos(theta), rho * sin(theta)))


class PolarThetaView(View):
    """Logarithmic polar projection"""

    def __init__(self, width, height, box):
        super(PolarThetaView, self).__init__(width, height, box)
        if not hasattr(box, '_tmin') or not hasattr(box, '_tmax'):
            raise Exception(
                'Box must be set with set_polar_box for polar charts')

    def __call__(self, rhotheta):
        """Project rho and theta"""
        if None in rhotheta:
            return None, None
        rho, theta = rhotheta
        aperture = pi / 3
        if theta > self.box._tmax:
            theta = (3 * pi - aperture / 2) / 2
        elif theta < self.box._tmin:
            theta = (3 * pi + aperture / 2) / 2
        else:
            start = 3 * pi / 2 + aperture / 2
            theta = start + (2 * pi - aperture) * (
                theta - self.box._tmin) / (
                self.box._tmax - self.box._tmin)
        return super(PolarThetaView, self).__call__(
            (rho * cos(theta), rho * sin(theta)))


class PolarThetaLogView(View):
    """Logarithmic polar projection"""

    def __init__(self, width, height, box):
        super(PolarThetaLogView, self).__init__(width, height, box)
        if not hasattr(box, '_tmin') or not hasattr(box, '_tmax'):
            raise Exception(
                'Box must be set with set_polar_box for polar charts')
        self.log10_tmax = log10(self.box._tmax) if self.box._tmax > 0 else 0
        self.log10_tmin = log10(self.box._tmin) if self.box._tmin > 0 else 0
        if self.log10_tmin == self.log10_tmax:
            self.log10_tmax = self.log10_tmin + 1

    def __call__(self, rhotheta):
        """Project rho and theta"""
        if None in rhotheta:
            return None, None
        rho, theta = rhotheta
        # Center case
        if theta == 0:
            return super(PolarThetaLogView, self).__call__((0, 0))
        theta = self.box._tmin + (self.box._tmax - self.box._tmin) * (
            log10(theta) - self.log10_tmin) / (
            self.log10_tmax - self.log10_tmin)
        aperture = pi / 3
        if theta > self.box._tmax:
            theta = (3 * pi - aperture / 2) / 2
        elif theta < self.box._tmin:
            theta = (3 * pi + aperture / 2) / 2
        else:
            start = 3 * pi / 2 + aperture / 2
            theta = start + (2 * pi - aperture) * (
                theta - self.box._tmin) / (
                self.box._tmax - self.box._tmin)

        return super(PolarThetaLogView, self).__call__(
            (rho * cos(theta), rho * sin(theta)))


class LogView(View):
    """Logarithmic projection """
    # Do not want to call the parent here
    def __init__(self, width, height, box):
        self.width = width
        self.height = height
        self.box = box
        self.log10_ymax = log10(self.box.ymax) if self.box.ymax > 0 else 0
        self.log10_ymin = log10(self.box.ymin) if self.box.ymin > 0 else 0
        if self.log10_ymin == self.log10_ymax:
            self.log10_ymax = self.log10_ymin + 1
        self.box.fix(False)

    def y(self, y):
        """Project y"""
        if y is None or y <= 0 or self.log10_ymax - self.log10_ymin == 0:
            return 0
        return (self.height - self.height *
                (log10(y) - self.log10_ymin)
                / (self.log10_ymax - self.log10_ymin))


class XLogView(View):
    """Logarithmic projection """
    # Do not want to call the parent here
    def __init__(self, width, height, box):
        self.width = width
        self.height = height
        self.box = box
        self.log10_xmax = log10(self.box.xmax) if self.box.xmax > 0 else 0
        self.log10_xmin = log10(self.box.xmin) if self.box.xmin > 0 else 0
        self.box.fix(False)

    def x(self, x):
        """Project x"""
        if x is None or x <= 0 or self.log10_xmax - self.log10_xmin == 0:
            return None
        return (self.width *
                (log10(x) - self.log10_xmin)
                / (self.log10_xmax - self.log10_xmin))


class XYLogView(XLogView, LogView):
    def __init__(self, width, height, box):
        self.width = width
        self.height = height
        self.box = box
        self.log10_ymax = log10(self.box.ymax) if self.box.ymax > 0 else 0
        self.log10_ymin = log10(self.box.ymin) if self.box.ymin > 0 else 0
        self.log10_xmax = log10(self.box.xmax) if self.box.xmax > 0 else 0
        self.log10_xmin = log10(self.box.xmin) if self.box.xmin > 0 else 0
        self.box.fix(False)


class HorizontalLogView(XLogView):
    """Logarithmic projection """
    # Do not want to call the parent here
    def __init__(self, width, height, box):
        self._force_vertical = None
        self.width = width
        self.height = height
        self.box = box
        self.log10_xmax = log10(self.box.ymax) if self.box.ymax > 0 else 0
        self.log10_xmin = log10(self.box.ymin) if self.box.ymin > 0 else 0
        if self.log10_xmin == self.log10_xmax:
            self.log10_xmax = self.log10_xmin + 1
        self.box.fix(False)
        self.box.swap()

    def x(self, x):
        """Project x"""
        if x is None:
            return None
        if self._force_vertical:
            return super(HorizontalLogView, self).x(x)
        return super(XLogView, self).y(x)

    def y(self, y):
        if y is None:
            return None
        if self._force_vertical:
            return super(XLogView, self).y(y)
        return super(HorizontalLogView, self).x(y)
