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


import sys
import timeit
from random import sample

from pygal import CHARTS, CHARTS_BY_NAME
from pygal.etree import etree
from pygal.test import adapt

sizes = (1, 5, 10, 50, 100, 500, 1000)

rands = list(zip(
    sample(range(1000), 1000),
    sample(range(1000), 1000)))


def perf(chart_name, length, series):
    chart = CHARTS_BY_NAME.get(chart_name)()
    for i in range(series):
        chart.add('s %d' % i, adapt(chart, rands[:length]))
    return chart


if '--bench' in sys.argv:
    bench = True

    def prt(s):
        pass

    def cht(s):
        sys.stdout.write(s)
else:
    bench = False

    def prt(s):
        sys.stdout.write(s)
        sys.stdout.flush()

    def cht(s):
        pass

if '--profile' in sys.argv:
    import cProfile
    c = perf('Line', 500, 500)
    cProfile.run("c.render()")
    sys.exit(0)

if '--mem' in sys.argv:
    _TWO_20 = float(2 ** 20)
    import os
    import psutil
    import linecache
    pid = os.getpid()
    process = psutil.Process(pid)
    import gc
    gc.set_debug(
        gc.DEBUG_UNCOLLECTABLE | gc.DEBUG_INSTANCES | gc.DEBUG_OBJECTS)

    def print_mem():
        mem = process.get_memory_info()[0] / _TWO_20
        f = sys._getframe(1)
        line = linecache.getline(
            f.f_code.co_filename, f.f_lineno - 1).replace('\n', '')
        print('%s:%d \t| %.6f \t| %s' % (
            f.f_code.co_name, f.f_lineno, mem, line))

    c = perf('Line', 100, 500)
    print_mem()
    a = c.render()
    print_mem()
    import objgraph
    objgraph.show_refs([c], filename='sample-graph.png')
    gc.collect()
    print_mem()
    print(gc.garbage)
    print_mem()
    del a
    print_mem()
    del c
    print_mem()

    sys.exit(0)


charts = CHARTS if '--all' in sys.argv else 'Line',

for impl in ['lxml', 'etree']:
    if impl == 'lxml':
        etree.to_lxml()
    else:
        etree.to_etree()

    for chart in charts:
        prt('%s\n' % chart)
        prt('s\\l\t1\t10\t100')
        v = sys.version.split(' ')[0]
        if hasattr(sys, 'subversion'):
            v += ' ' + sys.subversion[0]
        v += ' ' + impl

        if len(charts) > 1:
            v += ' ' + chart

        cht('bench.add("%s", ' % v)
        diag = []
        for series in sizes:
            prt('\n%d\t' % series)
            for length in sizes:
                times = []
                if series == length or not bench:
                    time = timeit.timeit(
                        "c.render()",
                        setup="from __main__ import perf; "
                        "c = perf('%s', %d, %d)" % (
                            chart, length, series),
                        number=10)
                    if series == length:
                        diag.append(1000 * time)
                prt('%d\t' % (1000 * time))
        cht(repr(diag))
        cht(')\n')
        prt('\n')
