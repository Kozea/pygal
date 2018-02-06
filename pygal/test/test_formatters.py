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
"""Test formatters"""

from pygal import formatters
from pygal._compat import u


def test_human_readable():
    """Test human_readable formatter"""
    f = formatters.human_readable

    assert f(1) == '1'
    assert f(1.) == '1'
    assert f(10) == '10'
    assert f(12.5) == '12.5'
    assert f(1000) == '1k'
    assert f(5000) == '5k'
    assert f(100000) == '100k'
    assert f(1253) == '1.253k'
    assert f(1250) == '1.25k'

    assert f(0.1) == '100m'
    assert f(0.01) == '10m'
    assert f(0.001) == '1m'
    assert f(0.002) == '2m'
    assert f(0.0025) == '2.5m'
    assert f(0.0001) == u('100µ')
    assert f(0.000123) == u('123µ')
    assert f(0.00001) == u('10µ')
    assert f(0.000001) == u('1µ')
    assert f(0.0000001) == u('100n')
    assert f(0.0000000001) == u('100p')

    assert f(0) == '0'
    assert f(0.) == '0'
    assert f(-1337) == '-1.337k'
    assert f(-.000000042) == '-42n'


def test_human_readable_custom():
    """Test human_readable formatter option"""
    f = formatters.HumanReadable()
    assert f(None) == u('∅')
    f = formatters.HumanReadable(none_char='/')
    assert f(None) == '/'


def test_significant():
    """Test significant formatter"""
    f = formatters.significant
    assert f(1) == '1'
    assert f(1.) == '1'
    assert f(-1.) == '-1'
    assert f(10) == '10'
    assert f(10000000000) == '1e+10'
    assert f(100000000000) == '1e+11'
    assert f(120000000000) == '1.2e+11'

    assert f(.1) == '0.1'
    assert f(.01) == '0.01'
    assert f(.0000000001) == '1e-10'
    assert f(-.0000000001) == '-1e-10'
    assert f(.0000000001002) == '1.002e-10'

    assert f(.0000000001002) == '1.002e-10'

    assert f(.12345678912345) == '0.1234567891'
    assert f(.012345678912345) == '0.01234567891'

    assert f(12345678912345) == '1.234567891e+13'
