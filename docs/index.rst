=====
Pygal
=====

Presentation
============

pygal is a SVG charting library written in python.

.. pygal:: 300 200

   chart = pygal.HorizontalBar(y_label_rotation=-25)
   chart.x_labels = 'one', 'two', 'three', 'four', 'five'
   chart.add('red', [1, 2, 3, 1, 2])
   chart.add('green', [4, 3, 0, 1, 2])

.. pygal:: 300 200

   chart = pygal.Line(x_label_rotation=25, fill=True, style=pygal.style.NeonStyle, interpolate='cubic')
   chart.x_labels = 'one', 'two', 'three', 'four', 'five'
   chart.add('red', [1, 2, 3, 1, 2])
   chart.add('green', [4, 3, 0, 1, 2])

.. pygal:: 300 200

   chart = pygal.Pie()
   chart.x_labels = 'one', 'two', 'three', 'four', 'five'
   chart.add('red', [1, 2, 3, 1, 2])
   chart.add('green', [4, 3, 0, 1, 2])

.. pygal:: 300 200

   chart = pygal.Radar(fill=True, style=pygal.style.NeonStyle)
   chart.x_labels = 'one', 'two', 'three', 'four', 'five'
   chart.add('red', [1, 2, 3, 1, 2])
   chart.add('green', [4, 3, 0, 1, 2])

It features various graph types:

- `Bar charts </chart_types/#bar-charts-histograms>`_

- `Line charts </chart_types/#line-charts>`_

- `XY charts </chart_types/#xy-charts>`_

- `Pie charts </chart_types/#pies>`_

- `Radar charts </chart_types/#radar-charts>`_

- `Box plot </chart_types/#box-plot>`_

- `Dot charts </chart_types/#dot-charts>`_

- `Pyramid charts </chart_types/#pyramid-charts>`_

- `Funnel charts </chart_types/#funnel-charts>`_

- `Gauge charts </chart_types/#gauge-charts>`_

- `Worldmap charts </chart_types/#worldmap-charts>`_

- `Country charts </chart_types/#country-charts>`_


Python/Css styling with some pre-defined themes. See `styling </styles/>`_.

And a lot of options to `customize the charts. </basic_customizations>`_


Get it !
========

- Get the package on `pypi <http://pypi.python.org/pypi/pygal/>`_
- Fork me on `github <http://github.com/Kozea/pygal>`_

More information in the `download page </download>`_


Get started
===========

Start `here </first_steps/>`_ to make your first steps.


Technical Description
=====================

As of now pygal is known to work for python 2.6, 2.7 and 3.2, 3.3, 3.4.


Needed dependencies
-------------------

pygal uses `lxml <http://lxml.de/>`_ to generate the svg, this is the only needed dependency.


Optional dependencies
---------------------

PNG output requires `CairoSVG <http://cairosvg.org/>`_, `tinycss <http://packages.python.org/tinycss/>`_ and `cssselect <http://packages.python.org/cssselect/>`_.
Install those with ``pip install CairoSVG tinycss cssselect``.

Unit testing needs `py.test <http://pytest.org/latest/>`_ or `nosetests <http://readthedocs.org/docs/nose/en/latest/>`_.

Visual testing is based on `flask <http://flask.pocoo.org/>`_.

Contents:

.. toctree::
   :maxdepth: 2



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
