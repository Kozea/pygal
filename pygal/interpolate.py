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
from pygal.util import ident
try:
    import scipy
    from scipy import interpolate
except:
    scipy = None


def interpolation(x, y, kind):
    assert scipy != None, 'You must have scipy installed to use interpolation'
    order = None
    if len(x) < 2:
        return ident
    if isinstance(kind, int):
        order = kind
    elif kind in ['zero', 'slinear', 'quadratic', 'cubic']:
        order = {'nearest': 0, 'zero': 0, 'slinear': 1,
                 'quadratic': 2, 'cubic': 3}[kind]
    if order and len(x) <= order:
        kind = len(x) - 1
    if kind == 'krogh':
        return interpolate.KroghInterpolator(x, y)
    elif kind == 'barycentric':
        return interpolate.BarycentricInterpolator(x, y)
    elif kind == 'univariate':
        return interpolate.InterpolatedUnivariateSpline(x, y)
    return interpolate.interp1d(x, y, kind=kind)
