Axis
====


include_x_axis
--------------

Scales are computed automaticaly between the min and the max values.

You may want to always have the absissa in your graph:

.. pygal-code::

  chart = pygal.Line(include_x_axis=True)
  chart.add('line', [.0002, .0005, .00035])


inverse_y_axis
--------------

.. pygal-code::

  chart = pygal.Line(inverse_y_axis=True)
  chart.add('line', [.0002, .0005, .00035])


range
-----

In pygal you can override automatic scaling by setting ``y_labels`` to the values you want, but if you want to change the scaling range and keep auto scaling in it, you can set a ``range`` which is a tuple containing the desired min and max:

.. pygal-code::

  chart = pygal.Line(range=(.0001, .001))
  chart.add('line', [.0002, .0005, .00035])


xrange
------

For xy graph xrange can be used for the x axis.

.. pygal-code::

  chart = pygal.XY(xrange=(10, 30))
  chart.add('line', [(10, .0002), (15, .0005), (12, .00035)])


secondary_range
---------------

For chart with two axis, the ``secondary_range`` defines the range for the secondary axis.

.. pygal-code::

  chart = pygal.Line(secondary_range=(10, 25))
  chart.add('primary', [.0002, .0005, .00035])
  chart.add('secondary', [10, 15, 12], secondary=True)


logarithmic
-----------

You can set the scale to be logarithmic:

.. pygal-code::

  chart = pygal.Line(logarithmic=True)
  values = [1, 3, 43, 123, 1231, 23192]
  chart.x_labels = map(str, values)
  chart.add('log example', values)

.. caution::

  Negative values are ignored


min_scale
---------

You can specify the minimum number of scale graduation to generate with auto scaling if possible.

.. pygal-code::

  chart = pygal.Line(min_scale=12)
  chart.add('line', [1, 10, 100, 50, 25])


max_scale
---------

You can specify the maximum number of scale graduation to generate with auto scaling if possible.

.. pygal-code::

  chart = pygal.Line(max_scale=6)
  chart.add('line', [1, 10, 100, 50, 25])



order_min
---------

You can specify at which precision pygal should stop scaling (in log10) usefull in conjuction of the two previous properties:

.. pygal-code::

  chart = pygal.Line(order_min=1)
  chart.add('line', [1, 10, 100, 50, 25])
