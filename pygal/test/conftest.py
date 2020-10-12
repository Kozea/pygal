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
"""pytest fixtures"""

import sys

import pytest

import pygal
from pygal.etree import etree

from . import get_data


@pytest.fixture
def etreefx(request):
    """Fixture allowing to test with builtin etree and lxml"""
    if request.param == 'etree':
        etree.to_etree()
    if request.param == 'lxml':
        etree.to_lxml()


def pytest_generate_tests(metafunc):
    """Generate the tests for etree and lxml"""
    if etree._lxml_etree:
        metafunc.fixturenames.append('etreefx')
        metafunc.parametrize('etreefx', ['lxml', 'etree'], indirect=True)

    if not hasattr(sys, 'pypy_version_info'):
        etree.to_lxml()

    if hasattr(sys, 'pypy_version_info'):
        etree.to_etree()

    if "Chart" in metafunc.fixturenames:
        metafunc.parametrize("Chart", pygal.CHARTS)
    if "datas" in metafunc.fixturenames:
        metafunc.parametrize(
            "datas", [[("Serie %d" % i, get_data(i)) for i in range(s)]
                      for s in (5, 1, 0)]
        )
