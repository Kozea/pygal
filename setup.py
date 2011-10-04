#!python

import os
import sys
from setuptools import find_packages

from distutils.cmd import Command


class DisabledTestCommand(Command):
    user_options = []

    def __init__(self, dist):
        raise RuntimeError(
            "test command not supported on pygal."
            " Use setup.py nosetests instead")


setup_params = dict(
    name="pygal",
    description="Python svg graph abstract layer",
    author="Jason R. Coombs, Kozea",
    author_email="jaraco@jaraco.com, gayoub@kozea.fr",
    url="https://github.com/Kozea/pygal",
    packages=find_packages(),
    zip_safe=True,
    include_package_data=True,
    install_requires=[
        'lxml>=2.0',
    ],
    license="MIT",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    entry_points={
    },
    # Don't use setup.py test - nose doesn't support it
    # see http://code.google.com/p/python-nose/issues/detail?id=219
    cmdclass=dict(
        test=DisabledTestCommand,
    ),
    use_2to3=True,
)

if __name__ == '__main__':
    from setuptools import setup
    setup(**setup_params)
