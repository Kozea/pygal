#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Public Domain
from setuptools import setup, find_packages


setup(
    name="pygal",
    packages=find_packages(),
    tests_require=["pytest"],
    install_requires=['lxml'])
