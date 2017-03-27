Box
---


Extremes (default)
~~~~~~~~~~~~~~~~~~

By default, the extremes mode is used that is the whiskers are the extremes of the data set, the box goes from the first quartile to the third and the middle line is the median.

.. pygal-code::

  box_plot = pygal.Box()
  box_plot.title = 'V8 benchmark results'
  box_plot.add('Chrome', [6395, 8212, 7520, 7218, 12464, 1660, 2123, 8607])
  box_plot.add('Firefox', [7473, 8099, 11700, 2651, 6361, 1044, 3797, 9450])
  box_plot.add('Opera', [3472, 2933, 4203, 5229, 5810, 1828, 9013, 4669])
  box_plot.add('IE', [43, 41, 59, 79, 144, 136, 34, 102])


1.5 interquartile range
~~~~~~~~~~~~~~~~~~~~~~~

Same as above except the whiskers are the first quartile minus 1.5 times the interquartile range and the third quartile plus 1.5 times the interquartile range.

.. pygal-code::

  box_plot = pygal.Box(box_mode="1.5IQR")
  box_plot.title = 'V8 benchmark results'
  box_plot.add('Chrome', [6395, 8212, 7520, 7218, 12464, 1660, 2123, 8607])
  box_plot.add('Firefox', [7473, 8099, 11700, 2651, 6361, 1044, 3797, 9450])
  box_plot.add('Opera', [3472, 2933, 4203, 5229, 5810, 1828, 9013, 4669])
  box_plot.add('IE', [43, 41, 59, 79, 144, 136, 34, 102])


Tukey
~~~~~

The whiskers are the lowest datum whithin the 1.5 IQR of the lower quartile and the highest datum still within 1.5 IQR of the upper quartile. The outliers are shown too.

.. pygal-code::

  box_plot = pygal.Box(box_mode="tukey")
  box_plot.title = 'V8 benchmark results'
  box_plot.add('Chrome', [6395, 8212, 7520, 7218, 12464, 1660, 2123, 8607])
  box_plot.add('Firefox', [7473, 8099, 11700, 2651, 6361, 1044, 3797, 9450])
  box_plot.add('Opera', [3472, 2933, 4203, 5229, 5810, 1828, 9013, 4669])
  box_plot.add('IE', [43, 41, 59, 79, 144, 136, 34, 102])


Standard deviation
~~~~~~~~~~~~~~~~~~

The whiskers are defined here by the standard deviation of the data.

.. pygal-code::

  box_plot = pygal.Box(box_mode="stdev")
  box_plot.title = 'V8 benchmark results'
  box_plot.add('Chrome', [6395, 8212, 7520, 7218, 12464, 1660, 2123, 8607])
  box_plot.add('Firefox', [7473, 8099, 11700, 2651, 6361, 1044, 3797, 9450])
  box_plot.add('Opera', [3472, 2933, 4203, 5229, 5810, 1828, 9013, 4669])
  box_plot.add('IE', [43, 41, 59, 79, 144, 136, 34, 102])


Population standard deviation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The whiskers are defined here by the population standard deviation of the data.

.. pygal-code::

  box_plot = pygal.Box(box_mode="pstdev")
  box_plot.title = 'V8 benchmark results'
  box_plot.add('Chrome', [6395, 8212, 7520, 7218, 12464, 1660, 2123, 8607])
  box_plot.add('Firefox', [7473, 8099, 11700, 2651, 6361, 1044, 3797, 9450])
  box_plot.add('Opera', [3472, 2933, 4203, 5229, 5810, 1828, 9013, 4669])
  box_plot.add('IE', [43, 41, 59, 79, 144, 136, 34, 102])
