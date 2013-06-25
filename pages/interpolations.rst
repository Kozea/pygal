===============
 Documentation
===============


Interpolations
==============


.. contents::


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


With quadratic interpolation:
-----------------------------

``interpolate``

.. pygal-code::

  chart = pygal.Line(interpolate='quadratic')
  chart.add('line', [1, 5, 17, 12, 5, 10])


With lagrange interpolation:
----------------------------

``interpolate``

.. pygal-code::

  chart = pygal.Line(interpolate='lagrange')
  chart.add('line', [1, 5, 17, 12, 5, 10])


With trigonometric interpolation:
---------------------------------

``interpolate``

.. pygal-code::

  chart = pygal.Line(interpolate='trigonometric')
  chart.add('line', [1, 5, 17, 12, 5, 10])


With hermite interpolation:
---------------------------

``interpolate``

.. pygal-code::

  chart = pygal.Line(interpolate='hermite')
  chart.add('line', [1, 5, 17, 12, 5, 10])


For hermite you can also pass additionnal parameters to configure tangent behaviour:


.. pygal-code::

  chart = pygal.Line(interpolate='hermite', interpolation_parameters={'type': 'finite_difference'})
  chart.add('line', [1, 5, 17, 12, 5, 10])


.. pygal-code::

  chart = pygal.Line(interpolate='hermite', interpolation_parameters={'type': 'cardinal', 'c': .75})
  chart.add('line', [1, 5, 17, 12, 5, 10])


.. pygal-code::

  chart = pygal.Line(interpolate='hermite', interpolation_parameters={'type': 'kochanek_bartels', 'b': -1, 'c': 1, 't': 1})
  chart.add('line', [1, 5, 17, 12, 5, 10])

For more information see the `wikipedia article <http://en.wikipedia.org/wiki/Cubic_Hermite_spline#Finite_difference>`_


Interpolation precision
-----------------------

``interpolation_precision``

You can change the resolution of the interpolation with the help of `interpolation_precision`:


.. pygal-code::

  chart = pygal.Line(interpolate='quadratic')
  chart.add('line', [1, 5, 17, 12, 5, 10])

.. pygal-code::

  chart = pygal.Line(interpolate='quadratic', interpolation_precision=3)
  chart.add('line', [1, 5, 17, 12, 5, 10])


Next: `Sparklines </sparklines>`_
