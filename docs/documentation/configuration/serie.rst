Serie configuration
===================

How
---

Series are customized using keyword args set in the ``add`` or call function:

.. code-block:: python

   chart = pygal.Line()
   chart(1, 2, 3, fill=True)
   chart.add('', [3, 2, 1], dot=False)



Options
-------

.. contents::
   :local:


secondary
~~~~~~~~~

You can plot your values to 2 separate axes, thanks to `wiktorn <https://github.com/wiktorn>`_
This is the only serie only option.

.. pygal-code::

  chart = pygal.Line(title=u'Some different points')
  chart.x_labels = ('one', 'two', 'three')
  chart.add('line', [.0002, .0005, .00035])
  chart.add('other line', [1000, 2000, 7000], secondary=True)


stroke
~~~~~~

.. pygal-code::

  xy_chart = pygal.XY(stroke=False)
  xy_chart.title = 'Correlation'
  xy_chart.add('A', [(0, 0), (.1, .2), (.3, .1), (.5, 1), (.8, .6), (1, 1.08), (1.3, 1.1), (2, 3.23), (2.43, 2)])
  xy_chart.add('B', [(.1, .15), (.12, .23), (.4, .3), (.6, .4), (.21, .21), (.5, .3), (.6, .8), (.7, .8)])
  xy_chart.add('C', [(.05, .01), (.13, .02), (1.5, 1.7), (1.52, 1.6), (1.8, 1.63), (1.5, 1.82), (1.7, 1.23), (2.1, 2.23), (2.3, 1.98)])
  xy_chart.add('Correl', [(0, 0), (2.8, 2.4)], stroke=True)


fill
~~~~

.. pygal-code::

  chart = pygal.Line()
  chart.add('line', [.0002, .0005, .00035], fill=True)
  chart.add('line', [.0004, .0009, .001])


show_dots
~~~~~~~~~

.. pygal-code::

  chart = pygal.Line()
  chart.add('line', [.0002, .0005, .00035], show_dots=False)
  chart.add('line', [.0004, .0009, .001])


show_only_major_dots
~~~~~~~~~~~~~~~~~~~~


.. pygal-code::

  chart = pygal.Line()
  chart.add('line', range(12))
  chart.add('line', range(12)[::-1], show_only_major_dots=True)
  chart.x_labels = map(str, range(12))
  chart.x_labels_major = ['2', '4', '8', '11']


dots_size
~~~~~~~~~


.. pygal-code::

  chart = pygal.Line()
  chart.add('line', [.0002, .0005, .00035], dots_size=4)
  chart.add('line', [.0004, .0009, .001], dots_size=12)


stroke_style
~~~~~~~~~~~~

.. pygal-code::

  chart = pygal.Line()
  chart.add('line', [.0002, .0005, .00035], stroke_style={'width': 5, 'dasharray': '3, 6', 'linecap': 'round', 'linejoin': 'round'})
  chart.add('line', [.0004, .0009, .001], stroke_style={'width': 2, 'dasharray': '3, 6, 12, 24'})


rounded_bars
~~~~~~~~~~~~


.. pygal-code::

   chart = pygal.Bar()
   for i in range(10):
     chart.add(str(i), i, rounded_bars=2 * i)


inner_radius
~~~~~~~~~~~~


.. pygal-code::

   chart = pygal.Pie()
   for i in range(10):
     chart.add(str(i), i, inner_radius=(10 - i) / 10)



allow_interruptions
~~~~~~~~~~~~~~~~~~~

You can set `allow_interruptions` to True in order to break lines on None values.

.. pygal-code::

  interrupted_chart = pygal.Line()
  interrupted_chart.add(
    'Temperature', [22, 34, 43, 12, None, 12, 55, None, 56],
    allow_interruptions=True)
  interrupted_chart.add(
    'Temperature', [11, 17, 21.5, 6, None, 6, 27.5, None, 28])


formatter
~~~~~~~~~

You can add a `formatter` function for this serie values.
It will be used for value printing and tooltip. (Not for axis.)


.. pygal-code::

  chart = pygal.Bar(print_values=True, value_formatter=lambda x: '{}$'.format(x))
  chart.add('bar', [.0002, .0005, .00035], formatter=lambda x: '<%s>' % x)
  chart.add('bar', [.0004, .0009, .001])
