#!python

# $Id$

from ez_setup import use_setuptools
use_setuptools()
from setuptools import setup, find_packages

setup(name = "svg-chart",
	version = "1.2",
	description = "Python SVG Charting Library",
	author = "Jason R. Coombs",
	author_email = "jaraco@jaraco.com",
	url = "http://py-svg.sourceforge.net",
	packages = find_packages('lib'),
	package_dir = {'':'lib'},
	install_requires=[
		'python-dateutil>=1.4',
	],
	license = "MIT",
	long_description = """\
SVG Charting library based on the Ruby SVG::Graph

""",
	classifiers = [
		"Development Status :: 4 - Beta",
		"Intended Audience :: Developers",
		"Programming Language :: Python",
	],
	entry_points = {
	},
	tests_require=[
		'nose>=0.10',
	],
	test_suite = "nose.collector",
	
	)

