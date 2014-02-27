=============================
 A python SVG Charts Creator
=============================

Presentation
============

pygal 1.4.2 is a dynamic SVG charting library.


.. class:: thumbs
.. compound::

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

- `Bar charts </chart_types/#idbar-charts-histograms>`_

- `Line charts </chart_types/#idline-charts>`_

- `XY charts </chart_types/#idxy-charts>`_

- `Pie charts </chart_types/#idpies>`_

- `Radar charts </chart_types/#idradar-charts>`_

- `Box plot </chart_types/#idbox-plot>`_

- `Dot charts </chart_types/#iddot-charts>`_

- `Pyramid charts </chart_types/#idpyramid-charts>`_

- `Funnel charts </chart_types/#idfunnel-charts>`_

- `Gauge charts </chart_types/#idgauge-charts>`_

- `Worldmap charts </chart_types/#idworldmap-charts>`_

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

As of now pygal is known to work for python 2.6, 2.7 and 3.2, 3.3.


Needed dependencies
-------------------

pygal uses `lxml <http://lxml.de/>`_ to generate the svg, this is the only needed dependency.


Optional dependencies
---------------------

PNG output requires `CairoSVG <http://cairosvg.org/>`_, `tinycss <http://packages.python.org/tinycss/>`_ and `cssselect <http://packages.python.org/cssselect/>`_.
Install those with ``pip install CairoSVG tinycss cssselect``.

Unit testing needs `py.test <http://pytest.org/latest/>`_ or `nosetests <http://readthedocs.org/docs/nose/en/latest/>`_.

Visual testing is based on `flask <http://flask.pocoo.org/>`_.
