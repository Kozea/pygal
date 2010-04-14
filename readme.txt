``svg.charts`` - Package for generating SVG Charts in Python
============================================================

.. contents::

Status and License
------------------

``svg.charts`` is a port of the SVG::Graph Ruby package by Sean E. Russel.

``svg.charts`` supercedes ``svg_charts`` 1.1 and 1.2.

``svg.charts`` is written by Jason R. Coombs.  It is licensed under an
`MIT-style permissive license
<https://py-svg.svn.sourceforge.net/svnroot/py-svg/trunk/docs/license.txt>`_.

You can install it with ``easy_install svg.charts``, or from the
`subversion repository
<https://py-svg.svn.sourceforge.net/svnroot/py-svg/trunk#egg=svg.charts-dev>`_ with
``easy_install svg.charts==dev``.

Getting Started
---------------

``svg.charts`` has some examples (taken directly from the reference implementation)
in `tests/testing.py <https://py-svg.svn.sourceforge.net/svnroot/py-svg/trunk/tests/testing.py>`_.
These examples show sample usage of the various chart types. They should provide a
good starting point for learning the usage of the library.

Upgrade Notes
-------------

Upgrading from 1.x to 2.0

I suggest removing SVG 1.0 from the python installation.  This involves removing the SVG directory (or svg_chart*) from site-packages.

Change import statements to import from the new namespace.

from SVG import Bar
Bar.VerticalBar(...)
becomes
from svg.charts.bar import VerticalBar
VerticalBar(...)

More To-Dos
-----------

-  Implement javascript-based animation (See JellyGraph for a Silverlight example of what simple animation can do for a charting library).

Changes
-------

2.0.3
~~~~~

* Fix IndexError in ``svg.charts.plot.Plot.field_size`` when there are
  only two values returned by float_range (in the case there are only
  two different 'y' values in the data) and scale_y_integers == True.
  Credit to `Jean Schurger <http://schurger.org/>`_ for the patch.
* Fixed problem in setup.py installing on Unix OS (case sensitivity of 
  readme.txt). Credit to Luke Miller and Jean Schurger for supplying
  a patch for this issue.

2.0.2
~~~~~

* Updated cssutils dependency to 0.9.6 (currently in beta) to require the CSS profiles support.
* Completed an SVG CSS profile according to the SVG 1.1 spec.

2.0.1
~~~~~

* Added preliminary SVG CSS profile, suitable for stock CSS properties.

2.0
~~~~~

* First major divergence from the Ruby reference implementation
* Now implemented as a namespace package (svg.charts instead of svg_charts)
* Changed XML processor to lxml
* Enabled extensible css support using cssutils, greatly reducing static CSS
* Renamed modules and methods to be more consistent with PEP-8 naming convention

1.2
~~~

* Bug fixes

1.1
~~~

* First public release
