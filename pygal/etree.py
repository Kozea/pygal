# -*- coding: utf-8 -*-
# This file is part of pygal
#
# A python svg graph plotting library
# Copyright © 2012-2015 Kozea
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
Wrapper for seemless lxml.etree / xml.etree usage
depending on whether lxml is installed or not.
"""

import os


class Etree(object):

    """Etree wrapper using lxml.etree or standard xml.etree"""

    def __init__(self):
        """Create the wrapper"""
        from xml.etree import ElementTree as _py_etree
        self._py_etree = _py_etree
        try:
            from lxml import etree as _lxml_etree
            self._lxml_etree = _lxml_etree
        except ImportError:
            self._lxml_etree = None

        if os.getenv('NO_LXML', None):
            self._etree = self._py_etree
        else:
            self._etree = self._lxml_etree or self._py_etree
        self.lxml = self._etree is self._lxml_etree

    def __getattribute__(self, attr):
        """Retrieve attr from current active etree implementation"""
        if (attr not in object.__getattribute__(self, '__dict__') and
                attr not in Etree.__dict__):
            return object.__getattribute__(self._etree, attr)
        return object.__getattribute__(self, attr)

    def to_lxml(self):
        """Force lxml.etree to be used"""
        self._etree = self._lxml_etree
        self.lxml = True

    def to_etree(self):
        """Force xml.etree to be used"""
        self._etree = self._py_etree
        self.lxml = False

etree = Etree()
