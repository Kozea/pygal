#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of pygal
#
# A python svg graph plotting library
# Copyright © 2012-2013 Kozea
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
import os, sys
import re

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True
    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)


ROOT = os.path.dirname(__file__)
with open(os.path.join(ROOT, 'pygal', '__init__.py')) as fd:
    __version__ = re.search("__version__ = '([^']+)'", fd.read()).group(1)

setup(
    name="pygal",
    version=__version__,
    description="A python svg graph plotting library",
    author="Kozea",
    url="http://pygal.org/",
    author_email="florian.mounier@kozea.fr",
    license="GNU LGPL v3+",
    platforms="Any",
    packages=find_packages(),
    provides=['pygal'],
    scripts=["pygal_gen.py"],
    keywords=[
        "svg", "chart", "graph", "diagram", "plot", "histogram", "kiviat"],
    tests_require=["pytest", "pyquery", "flask", "cairosvg"],
    cmdclass = {'test': PyTest},
    package_data={'pygal': ['css/*', 'graph/worldmap.svg']},
    install_requires=['lxml'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: "
        "GNU Lesser General Public License v3 or later (LGPLv3+)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Topic :: Multimedia :: Graphics :: Presentation"])
