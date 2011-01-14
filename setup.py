#!python

# $Id$

import os
from setuptools import find_packages

from distutils.cmd import Command

class DisabledTestCommand(Command):
	user_options = []
	def __init__(self, dist):
		raise RuntimeError("test command not supported on svg.charts. Use setup.py nosetests instead")

_this_dir = os.path.dirname(__file__)
_long_description = open('readme.txt').read().strip()

setup_params = dict(
	name = "svg.charts",
	version = "2.0.5",
	description = "Python SVG Charting Library",
	long_description = _long_description,
	author = "Jason R. Coombs",
	author_email = "jaraco@jaraco.com",
	url = "http://py-svg.sourceforge.net",
	packages = find_packages(),
	zip_safe=True,
	namespace_packages=['svg'],
	include_package_data = True,
	install_requires=[
		'python-dateutil>=1.4',
		'cssutils>=0.9.6b3',
		'lxml>=2.0',
	],
	license = "MIT",
	classifiers = [
		"Development Status :: 5 - Production/Stable",
		"Intended Audience :: Developers",
		"Intended Audience :: Science/Research",
		"Programming Language :: Python",
		"License :: OSI Approved :: MIT License",
	],
	entry_points = {
	},
	# Don't use setup.py test - nose doesn't support it
	# see http://code.google.com/p/python-nose/issues/detail?id=219
	cmdclass=dict(
		test=DisabledTestCommand,
	),
	setup_requires=[
		'nose>=0.11',
	],
	)

if __name__ == '__main__':
	from setuptools import setup
	setup(**setup_params)
