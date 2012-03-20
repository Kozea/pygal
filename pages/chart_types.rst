===============
 Documentation
===============


Chart types
===========

pygal provides 5 kind of charts:

.. contents::

Line charts
-----------

Basic
^^^^^

Basic simple line graph:

.. pygal-code::

  line_chart = pygal.Line()
  line_chart.title = 'Browser usage evolution (in %)'
  line_chart.x_labels = map(str, range(2002, 2013))
  line_chart.add('Firefox', [None, None, 0, 16.6,   25,   31, 36.4, 45.5, 46.3, 42.8, 37.1])
  line_chart.add('Chrome',  [None, None, None, None, None, None,    0,  3.9, 10.8, 23.8, 35.3])
  line_chart.add('IE',      [85.8, 84.6, 84.7, 74.5,   66, 58.6, 54.7, 44.8, 36.2, 26.6, 20.1])
  line_chart.add('Others',  [14.2, 15.4, 15.3,  8.9,    9, 10.4,  8.9,  5.8,  6.7,  6.8,  7.5])

Stacked
^^^^^^^

Same graph but with stacked values and filled rendering:

.. pygal-code::

  line_chart = pygal.StackedLine(fill=True)
  line_chart.title = 'Browser usage evolution (in %)'
  line_chart.x_labels = map(str, range(2002, 2013))
  line_chart.add('Firefox', [None, None, 0, 16.6,   25,   31, 36.4, 45.5, 46.3, 42.8, 37.1])
  line_chart.add('Chrome',  [None, None, None, None, None, None,    0,  3.9, 10.8, 23.8, 35.3])
  line_chart.add('IE',      [85.8, 84.6, 84.7, 74.5,   66, 58.6, 54.7, 44.8, 36.2, 26.6, 20.1])
  line_chart.add('Others',  [14.2, 15.4, 15.3,  8.9,    9, 10.4,  8.9,  5.8,  6.7,  6.8,  7.5])


Bar charts / Histograms
-----------------------

Basic
^^^^^

Basic simple bar graph:

.. pygal-code::

  line_chart = pygal.Bar()
  line_chart.title = 'Browser usage evolution (in %)'
  line_chart.x_labels = map(str, range(2002, 2013))
  line_chart.add('Firefox', [None, None, 0, 16.6,   25,   31, 36.4, 45.5, 46.3, 42.8, 37.1])
  line_chart.add('Chrome',  [None, None, None, None, None, None,    0,  3.9, 10.8, 23.8, 35.3])
  line_chart.add('IE',      [85.8, 84.6, 84.7, 74.5,   66, 58.6, 54.7, 44.8, 36.2, 26.6, 20.1])
  line_chart.add('Others',  [14.2, 15.4, 15.3,  8.9,    9, 10.4,  8.9,  5.8,  6.7,  6.8,  7.5])


Stacked
^^^^^^^

Same graph but with stacked values:

.. pygal-code::

  line_chart = pygal.StackedBar()
  line_chart.title = 'Browser usage evolution (in %)'
  line_chart.x_labels = map(str, range(2002, 2013))
  line_chart.add('Firefox', [None, None, 0, 16.6,   25,   31, 36.4, 45.5, 46.3, 42.8, 37.1])
  line_chart.add('Chrome',  [None, None, None, None, None, None,    0,  3.9, 10.8, 23.8, 35.3])
  line_chart.add('IE',      [85.8, 84.6, 84.7, 74.5,   66, 58.6, 54.7, 44.8, 36.2, 26.6, 20.1])
  line_chart.add('Others',  [14.2, 15.4, 15.3,  8.9,    9, 10.4,  8.9,  5.8,  6.7,  6.8,  7.5])


Horizontal
^^^^^^^^^^

Horizontal bar diagram:

.. pygal-code::

  line_chart = pygal.HorizontalBar()
  line_chart.title = 'Browser usage in February 2012 (in %)'
  line_chart.add('IE', 19.5)
  line_chart.add('Firefox', 36.6)
  line_chart.add('Chrome', 36.3)
  line_chart.add('Safari', 4.5)
  line_chart.add('Opera', 2.3)


XY charts
---------

Basic
^^^^^

Basic XY lines, drawing cosinus:

.. pygal-code::

  from math import cos
  xy_chart = pygal.XY()
  xy_chart.title = 'XY Cosinus'
  xy_chart.add('x = cos(y)', [(cos(x / 10.), x / 10.) for x in range(-50, 50, 5)])
  xy_chart.add('y = cos(x)', [(x / 10., cos(x / 10.)) for x in range(-50, 50, 5)])
  xy_chart.add('x = 1',  [(1, -5), (1, 5)])
  xy_chart.add('x = -1', [(-1, -5), (-1, 5)])
  xy_chart.add('y = 1',  [(-5, 1), (5, 1)])
  xy_chart.add('y = -1', [(-5, -1), (5, -1)])


Scatter Plot
^^^^^^^^^^^^

Disabling stroke make a good scatter plot

.. pygal-code::

  xy_chart = pygal.XY(stroke=False)
  xy_chart.title = 'Correlation'
  xy_chart.add('A', [(0, 0), (.1, .2), (.3, .1), (.5, 1), (.8, .6), (1, 1.08), (1.3, 1.1), (2, 3.23), (2.43, 2)])
  xy_chart.add('B', [(.1, .15), (.12, .23), (.4, .3), (.6, .4), (.21, .21), (.5, .3), (.6, .8), (.7, .8)])
  xy_chart.add('C', [(.05, .01), (.13, .02), (1.5, 1.7), (1.52, 1.6), (1.8, 1.63), (1.5, 1.82), (1.7, 1.23), (2.1, 2.23), (2.3, 1.98)])


Pies
----

Basic
^^^^^

Simple pie:


.. pygal-code::

  pie_chart = pygal.Pie()
  pie_chart.title = 'Browser usage in February 2012 (in %)'
  pie_chart.add('IE', 19.5)
  pie_chart.add('Firefox', 36.6)
  pie_chart.add('Chrome', 36.3)
  pie_chart.add('Safari', 4.5)
  pie_chart.add('Opera', 2.3)


Multi-series pie
^^^^^^^^^^^^^^^^

Same pie but divided in sub category:

.. pygal-code::

  pie_chart = pygal.Pie()
  pie_chart.title = 'Browser usage by version in February 2012 (in %)'
  pie_chart.add('IE', [5.7, 10.2, 2.6, 1])
  pie_chart.add('Firefox', [.6, 16.8, 7.4, 2.2, 1.2, 1, 1, 1.1, 4.3, 1])
  pie_chart.add('Chrome', [.3, .9, 17.1, 15.3, .6, .5, 1.6])
  pie_chart.add('Safari', [4.4, .1])
  pie_chart.add('Opera', [.1, 1.6, .1, .5])


Radar charts
------------

Basic
^^^^^

Simple Kiviat diagram:

.. pygal-code::

  radar_chart = pygal.Radar()
  radar_chart.title = 'V8 benchmark results'
  radar_chart.x_labels = ['Richards', 'DeltaBlue', 'Crypto', 'RayTrace', 'EarleyBoyer', 'RegExp', 'Splay', 'NavierStokes']
  radar_chart.add('Chrome', [4074, 3458, 12942, 3541, 10799, 1863, 657, 5918])
  radar_chart.add('Firefox', [3100, 2579, 3638, 2524, 3800, 552, 3675, 9043])


