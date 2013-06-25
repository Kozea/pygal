===============
 Documentation
===============


Interpolations
==============


.. contents::

To enable interpolation, just specify the interpolation type to:

- quadratic
- cubic


Without interpolation:
----------------------

``interpolate``

.. pygal-code::

  chart = pygal.Line()
  chart.add('line', [1, 5, 17, 12, 5, 10])

With cubic interpolation:
-------------------------

``interpolate``

.. pygal-code::

  chart = pygal.Line(interpolate='cubic')
  chart.add('line', [1, 5, 17, 12, 5, 10])

With krogh interpolation:
-------------------------

``interpolate``

.. pygal-code::

  chart = pygal.Line(interpolate='quadratic')
  chart.add('line', [1, 5, 17, 12, 5, 10])


Interpolation precision
-----------------------

``interpolation_precision``

You can change the resolution of the interpolation with the help of `interpolation_precision`:


.. pygal-code::

  chart = pygal.Line(interpolate='quadratic')
  chart.add('line', [1, 5, 17, 12, 5, 10])

.. pygal-code::

  chart = pygal.Line(interpolate='quadratic', interpolation_precision=50)
  chart.add('line', [1, 5, 17, 12, 5, 10])


Next: `Sparklines </sparklines>`_
