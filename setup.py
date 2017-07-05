#!/usr/bin/env python
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
import os
import sys

from setuptools import find_packages, setup
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = ['-x', 'build/lib/pygal']
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)


ROOT = os.path.dirname(__file__)


# Explicitly specify the encoding of pygal/__init__.py if we're on py3.
kwargs = {}
if sys.version_info[0] == 3:
    kwargs['encoding'] = 'utf-8'
    cairosvg = 'cairosvg'
else:
    cairosvg = 'cairosvg==0.5'

tests_requirements = [
    "pyquery", "flask", cairosvg, 'lxml', 'pygal_maps_world', 'pygal_maps_fr',
    'pygal_maps_ch', 'coveralls',
    'pytest-runner', 'pytest-cov', 'pytest-flake8', 'pytest-isort',
    'pytest'
]

about = {}
with open(os.path.join(
        os.path.dirname(__file__), "pygal", "__about__.py")) as f:
    exec(f.read(), about)

setup(
    name=about['__title__'],
    version=about['__version__'],
    description=about['__summary__'],
    url=about['__uri__'],
    author=about['__author__'],
    author_email=about['__email__'],
    license=about['__license__'],
    platforms="Any",
    packages=find_packages(),
    provides=['pygal'],
    scripts=["pygal_gen.py"],
    keywords=[
        "svg", "chart", "graph", "diagram", "plot", "histogram", "kiviat"],
    setup_requires=['pytest-runner'],
    test_requires=tests_requirements,
    cmdclass={'test': PyTest},
    package_data={'pygal': ['css/*', 'graph/maps/*.svg']},
    extras_require={
        'lxml': ['lxml'],
        'docs': ['sphinx', 'sphinx_rtd_theme', 'pygal_sphinx_directives'],
        'png': [cairosvg],
        'test': tests_requirements
    },
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
