# -*- coding: UTF-8 -*-

""" Setup script for building SVG distribution

Copyright © 2005 Jason R. Coombs
"""

from distutils.core import setup

__author__ = 'Jason R. Coombs <jaraco@sandia.gov>'
__version__ = '$Rev:  $'[6:-2]
__svnauthor__ = '$Author:  $'[9:-2]
__date__ = '$Date:  $'[7:-2]

setup ( name = 'SVGChart',
		version = '1.0',
		description = 'Python SVG Charting Support',
		author = 'Jason R. Coombs',
		author_email = 'jaraco@sandia.gov',
		packages = ['SVG'],
		package_dir = { 'SVG':'.' },
		script_args = ( 'bdist_wininst', )
		)
