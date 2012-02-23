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
from setuptools import setup, find_packages
import pygal

setup(
    name="pygal",
    version=pygal.__version__,
    description="A python svg graph plotting library",
    author="Kozea",
    author_email="florian.mounier@kozea.fr",
    license="GNU LGPL v3",
    platforms="Any",
    packages=find_packages(),
    provides=['pygal'],
    keywords=["svg", "graph", "diagram", "plot", "histogram", "kiviat"],
    tests_require=["pytest", "flask"],
    package_data={'pygal': ['css/*', 'js/*']},
    install_requires=['lxml'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: "
        "GNU Library or Lesser General Public License (LGPL)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2",
        "Topic :: Multimedia :: Graphics :: Presentation"])
