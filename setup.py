#!python

# $Id$

import os
from setuptools import find_packages

_this_dir = os.path.dirname(__file__)
_long_description = open(os.path.join(_this_dir, 'README.txt')).read().strip()

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
	tests_require=[
		'nose>=0.10',
	],
	test_suite = "nose.collector",
	
	)

if __name__ == '__main__':
	from setuptools import setup
	setup(**setup_params)
