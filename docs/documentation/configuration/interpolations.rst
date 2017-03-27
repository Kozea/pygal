Interpolations
==============

pygal allow you to interpolate most of line charts. Take this chart for instance:

.. pygal-code::

  chart = pygal.Line()
  chart.add('line', [1, 5, 17, 12, 5, 10])


interpolate
-----------

cubic
~~~~~

You can set the cubic interpolation:

.. pygal-code::

  chart = pygal.Line(interpolate='cubic')
  chart.add('line', [1, 5, 17, 12, 5, 10])


quadratic
~~~~~~~~~

.. pygal-code::

  chart = pygal.Line(interpolate='quadratic')
  chart.add('line', [1, 5, 17, 12, 5, 10])


lagrange
~~~~~~~~

.. pygal-code::

  chart = pygal.Line(interpolate='lagrange')
  chart.add('line', [1, 5, 17, 12, 5, 10])


trigonometric
~~~~~~~~~~~~~

.. pygal-code::

  chart = pygal.Line(interpolate='trigonometric')
  chart.add('line', [1, 5, 17, 12, 5, 10])


hermite
~~~~~~~

.. pygal-code::

  chart = pygal.Line(interpolate='hermite')
  chart.add('line', [1, 5, 17, 12, 5, 10])


interpolation_parameters
------------------------

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


interpolation_precision
-----------------------

You can change the resolution of the interpolation with the help of ``interpolation_precision``:


.. pygal-code::

  chart = pygal.Line(interpolate='quadratic')
  chart.add('line', [1, 5, 17, 12, 5, 10])

.. pygal-code::

  chart = pygal.Line(interpolate='quadratic', interpolation_precision=3)
  chart.add('line', [1, 5, 17, 12, 5, 10])

