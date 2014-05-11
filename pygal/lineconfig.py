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
Line Config module - with available line options
"""
#This class is used to control individual line configurations
#The unspecified items are taken from the global configuration
#Set the default values to None, then it it clear which values need to take the defaults
class LineConfig(object):
    show_dots = None
    show_only_major_dots = None
    dots_size = None
    stroke = None
    dashed_line = None
    fill = None

    def __init__(self, **kwargs):
        """Can be instanciated with config kwargs"""
        for k in dir(self):
            v = getattr(self, k)
            if (k not in self.__dict__ and not
                    k.startswith('_') and not
                    hasattr(v, '__call__')):
                setattr(self, k, v)
        self._update(kwargs)

    def _update(self, kwargs):
        self.__dict__.update(
            dict([(k, v) for (k, v) in kwargs.items()
                  if not k.startswith('_') and k in dir(self)]))
    
    def populateDefault(self, config):
        #Populate the default values with those from the main/global config
        for k in self.__dict__:
            v = getattr(self, k)
            if v is None:
                setattr(self, k, getattr(config, k))
        return self