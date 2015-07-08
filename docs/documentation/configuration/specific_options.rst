Specific options
================

These options are specific for certain chart types.



rounded_bars
------------

You can add a round effect to bar diagrams with ``rounded_bars``:

.. pygal-code::

  chart = pygal.Bar(rounded_bars=20)
  chart.add('values', [3, 10, 7, 2, 9, 7])


half_pie
--------

.. pygal-code::

  pie_chart = pygal.Pie(half_pie=True)
  pie_chart.title = 'Browser usage in February 2012 (in %)'
  pie_chart.add('IE', 19.5)
  pie_chart.add('Firefox', 36.6)
  pie_chart.add('Chrome', 36.3)
  pie_chart.add('Safari', 4.5)
  pie_chart.add('Opera', 2.3)


inner_radius
------------

Donut like pies

.. pygal-code::

  pie_chart = pygal.Pie(inner_radius=.6)
  pie_chart.title = 'Browser usage in February 2012 (in %)'
  pie_chart.add('IE', 19.5)
  pie_chart.add('Firefox', 36.6)
  pie_chart.add('Chrome', 36.3)
  pie_chart.add('Safari', 4.5)
  pie_chart.add('Opera', 2.3)


box_mode
--------

box plot has several modes:

extremes
~~~~~~~~

.. pygal-code::

  box_plot = pygal.Box(box_mode="extremes")
  box_plot.title = 'V8 benchmark results'
  box_plot.add('Chrome', [6395, 8212, 7520, 7218, 12464, 1660, 2123, 8607])
  box_plot.add('Firefox', [7473, 8099, 11700, 2651, 6361, 1044, 3797, 9450])
  box_plot.add('Opera', [3472, 2933, 4203, 5229, 5810, 1828, 9013, 4669])
  box_plot.add('IE', [43, 41, 59, 79, 144, 136, 34, 102])

1.5IQR
~~~~~~

.. pygal-code::

  box_plot = pygal.Box(box_mode="1.5IQR")
  box_plot.title = 'V8 benchmark results'
  box_plot.add('Chrome', [6395, 8212, 7520, 7218, 12464, 1660, 2123, 8607])
  box_plot.add('Firefox', [7473, 8099, 11700, 2651, 6361, 1044, 3797, 9450])
  box_plot.add('Opera', [3472, 2933, 4203, 5229, 5810, 1828, 9013, 4669])
  box_plot.add('IE', [43, 41, 59, 79, 144, 136, 34, 102])

tukey
~~~~~

.. pygal-code::

  box_plot = pygal.Box(box_mode="tukey")
  box_plot.title = 'V8 benchmark results'
  box_plot.add('Chrome', [6395, 8212, 7520, 7218, 12464, 1660, 2123, 8607])
  box_plot.add('Firefox', [7473, 8099, 11700, 2651, 6361, 1044, 3797, 9450])
  box_plot.add('Opera', [3472, 2933, 4203, 5229, 5810, 1828, 9013, 4669])
  box_plot.add('IE', [43, 41, 59, 79, 144, 136, 34, 102])

stdev
~~~~~

.. pygal-code::

  box_plot = pygal.Box(box_mode="stdev")
  box_plot.title = 'V8 benchmark results'
  box_plot.add('Chrome', [6395, 8212, 7520, 7218, 12464, 1660, 2123, 8607])
  box_plot.add('Firefox', [7473, 8099, 11700, 2651, 6361, 1044, 3797, 9450])
  box_plot.add('Opera', [3472, 2933, 4203, 5229, 5810, 1828, 9013, 4669])
  box_plot.add('IE', [43, 41, 59, 79, 144, 136, 34, 102])

pstdev
~~~~~~

.. pygal-code::

  box_plot = pygal.Box(box_mode="pstdev")
  box_plot.title = 'V8 benchmark results'
  box_plot.add('Chrome', [6395, 8212, 7520, 7218, 12464, 1660, 2123, 8607])
  box_plot.add('Firefox', [7473, 8099, 11700, 2651, 6361, 1044, 3797, 9450])
  box_plot.add('Opera', [3472, 2933, 4203, 5229, 5810, 1828, 9013, 4669])
  box_plot.add('IE', [43, 41, 59, 79, 144, 136, 34, 102])


stack_from_top
--------------

You can reverse the stacking order for StackedBar and StackedLine

.. pygal-code::

  line_chart = pygal.StackedLine(fill=True)
  line_chart.title = 'Browser usage evolution (in %)'
  line_chart.x_labels = map(str, range(2002, 2013))
  line_chart.add('Firefox', [None, None, 0, 16.6,   25,   31, 36.4, 45.5, 46.3, 42.8, 37.1])
  line_chart.add('Chrome',  [None, None, None, None, None, None,    0,  3.9, 10.8, 23.8, 35.3])
  line_chart.add('IE',      [85.8, 84.6, 84.7, 74.5,   66, 58.6, 54.7, 44.8, 36.2, 26.6, 20.1])
  line_chart.add('Others',  [14.2, 15.4, 15.3,  8.9,    9, 10.4,  8.9,  5.8,  6.7,  6.8,  7.5])

.. pygal-code::

  line_chart = pygal.StackedLine(stack_from_top=True, fill=True)
  line_chart.title = 'Browser usage evolution (in %)'
  line_chart.x_labels = map(str, range(2002, 2013))
  line_chart.add('Firefox', [None, None, 0, 16.6,   25,   31, 36.4, 45.5, 46.3, 42.8, 37.1])
  line_chart.add('Chrome',  [None, None, None, None, None, None,    0,  3.9, 10.8, 23.8, 35.3])
  line_chart.add('IE',      [85.8, 84.6, 84.7, 74.5,   66, 58.6, 54.7, 44.8, 36.2, 26.6, 20.1])
  line_chart.add('Others',  [14.2, 15.4, 15.3,  8.9,    9, 10.4,  8.9,  5.8,  6.7,  6.8,  7.5])


.. pygal-code::

  line_chart = pygal.StackedBar()
  line_chart.title = 'Browser usage evolution (in %)'
  line_chart.x_labels = map(str, range(2002, 2013))
  line_chart.add('Firefox', [None, None, 0, 16.6,   25,   31, 36.4, 45.5, 46.3, 42.8, 37.1])
  line_chart.add('Chrome',  [None, None, None, None, None, None,    0,  3.9, 10.8, 23.8, 35.3])
  line_chart.add('IE',      [85.8, 84.6, 84.7, 74.5,   66, 58.6, 54.7, 44.8, 36.2, 26.6, 20.1])
  line_chart.add('Others',  [14.2, 15.4, 15.3,  8.9,    9, 10.4,  8.9,  5.8,  6.7,  6.8,  7.5])

.. pygal-code::

  line_chart = pygal.StackedBar(stack_from_top=True)
  line_chart.title = 'Browser usage evolution (in %)'
  line_chart.x_labels = map(str, range(2002, 2013))
  line_chart.add('Firefox', [None, None, 0, 16.6,   25,   31, 36.4, 45.5, 46.3, 42.8, 37.1])
  line_chart.add('Chrome',  [None, None, None, None, None, None,    0,  3.9, 10.8, 23.8, 35.3])
  line_chart.add('IE',      [85.8, 84.6, 84.7, 74.5,   66, 58.6, 54.7, 44.8, 36.2, 26.6, 20.1])
  line_chart.add('Others',  [14.2, 15.4, 15.3,  8.9,    9, 10.4,  8.9,  5.8,  6.7,  6.8,  7.5])


missing_value_fill_truncation
-----------------------------

Filled series with missing x and/or y values at the end of a series are closed at the first value with a missing.
'x' is default.
