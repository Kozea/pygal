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
"""Serie property holder"""

from pygal.util import cached_property


class Serie(object):
    """Serie class containing title, values and the graph serie index"""

    def __init__(self, index, values, config, metadata=None):
        """Create the serie with its options"""
        self.index = index
        self.values = values
        self.config = config
        self.__dict__.update(config.__dict__)
        self.metadata = metadata or {}

    @cached_property
    def safe_values(self):
        """Property containing all values that are not None"""
        return list(filter(lambda x: x is not None, self.values))
