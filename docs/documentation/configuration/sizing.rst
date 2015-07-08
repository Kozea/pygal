Sizing
======

Svg size is configurable with ``width`` and ``height`` parameter.


width
-----

.. pygal-code:: 200 400

  chart = pygal.Bar(width=200)
  chart.add('1', 1)
  chart.add('2', 2)


height
------

.. pygal-code:: 600 100

  chart = pygal.Bar(height=100)
  chart.add('1', 1)
  chart.add('2', 2)


explicit_size
-------------

Size can be written directly to the svg tag to force display of the requested size using ``explicit_size``.


spacing
-------

Spacing determines the space between all elements:

.. pygal-code::

  chart = pygal.Bar(spacing=50)
  chart.x_labels = u'αβγδ'
  chart.add('line 1', [5, 15, 10, 8])
  chart.add('line 2', [15, 20, 8, 11])

margin
------

Margin is the external chart margin:

.. pygal-code::

  chart = pygal.Bar(margin=50)
  chart.x_labels = u'αβγδ'
  chart.add('line 1', [5, 15, 10, 8])
  chart.add('line 2', [15, 20, 8, 11])


Individual margins can also be specified

margin_top
----------

.. pygal-code::

  chart = pygal.Bar(margin_top=50)
  chart.x_labels = u'αβγδ'
  chart.add('line 1', [5, 15, 10, 8])
  chart.add('line 2', [15, 20, 8, 11])

margin_right
------------

.. pygal-code::

  chart = pygal.Bar(margin_right=50)
  chart.x_labels = u'αβγδ'
  chart.add('line 1', [5, 15, 10, 8])
  chart.add('line 2', [15, 20, 8, 11])

margin_bottom
-------------

.. pygal-code::

  chart = pygal.Bar(margin_bottom=50)
  chart.x_labels = u'αβγδ'
  chart.add('line 1', [5, 15, 10, 8])
  chart.add('line 2', [15, 20, 8, 11])

margin_left
-----------

.. pygal-code::

  chart = pygal.Bar(margin_left=50)
  chart.x_labels = u'αβγδ'
  chart.add('line 1', [5, 15, 10, 8])
  chart.add('line 2', [15, 20, 8, 11])
