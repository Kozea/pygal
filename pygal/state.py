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
"""Class holding state during render"""

from pygal.util import merge


class State(object):
    """
    Class containing config values
    overriden by chart values
    overriden by keyword args
    """

    def __init__(self, graph, **kwargs):
        """Create the transient state"""
        merge(self.__dict__, graph.config.__class__.__dict__)
        merge(self.__dict__, graph.config.__dict__)
        merge(self.__dict__, graph.__dict__)
        merge(self.__dict__, kwargs)
