#!/usr/bin/env python
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
import argparse
import pygal

parser = argparse.ArgumentParser(
    description='Generate pygal chart in command line',
    prog='pygal_gen',
    version=pygal.__version__)

parser.add_argument('-t', '--type', dest='type', default='Line',
                    choices=map(lambda x: x.__name__, pygal.CHARTS),
                    help='Kind of chart to generate')

parser.add_argument('-o', '--output', dest='filename', default='pygal_out.svg',
                    help='Filename to write the svg to')

parser.add_argument('-s', '--serie', dest='series', nargs='+', action='append',
                    help='Add a serie in the form (title val1 val2...)')

for key, val in pygal.config.Config.__dict__.items():
    if not key.startswith('_') and not hasattr(val, '__call__'):
        opt_name = key
        opts = {'type': str}
        if val != None:
            opts['type'] = type(val)
        elif 'labels' in key:
            opts['nargs'] = '+'
        if opts['type'] == bool:
            del opts['type']
            opts['action'] = 'store_true' if not val else 'store_false'
            if val:
                opt_name = 'no-' + opt_name
        if key == 'interpolate':
            opts['choices'] = [
                'linear', 'nearest', 'zero', 'slinear', 'quadratic',
                'cubic', 'krogh', 'barycentric', 'univariate']
        parser.add_argument(
            '--%s' % opt_name, dest=key, default=val, **opts)

config = parser.parse_args()

chart = getattr(pygal, config.type)(**vars(config))

for serie in config.series:
    chart.add(serie[0], map(float, serie[1:]))

chart.render_to_file(config.filename)
