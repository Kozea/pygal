===============
 Documentation
===============


Interpolations
==============


.. contents::

Interpolations need the `scipy python module <http://www.scipy.org/>`_.
To enable it just specify the interpolation type to:

- linear
- nearest
- zero
- slinear
- quadratic
- cubic
- krogh
- barycentric
- univariate
- or an integer representing the order of the spline interpolator

For more info see `interp1d definition on scipy <http://docs.scipy.org/doc/scipy/reference/generated/scipy.interpolate.interp1d.html#scipy.interpolate.interp1d>`_


Without interpolation:
----------------------

`interpolation`

.. pygal-code::

  chart = pygal.Line()
  chart.add('line', [1, 5, 17, 12, 5, 10])

With cubic interpolation:
-------------------------

`interpolation`

.. pygal-code::

  chart = pygal.Line(interpolate='cubic')
  chart.add('line', [1, 5, 17, 12, 5, 10])

With krogh interpolation:
-------------------------

`interpolation`

.. pygal-code::

  chart = pygal.Line(interpolate='krogh')
  chart.add('line', [1, 5, 17, 12, 5, 10])


Interpolation precision
-----------------------

`interpolation_precision`

You can change the resolution of the interpolation with the help of `interpolation_precision`:


.. pygal-code::

  chart = pygal.Line(interpolate='krogh', interpolation_precision=15)
  chart.add('line', [1, 5, 17, 12, 5, 10])

.. pygal-code::

  chart = pygal.Line(interpolate='krogh', interpolation_precision=50)
  chart.add('line', [1, 5, 17, 12, 5, 10])
