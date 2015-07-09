Sparklines
==========

pygal provides a simple way to get beautiful sparklines.


Basic
-----

.. pygal-code:: sparkline

  chart = pygal.Line()
  chart.add('', [1, 3,  5, 16, 13, 3,  7])
  chart.render_sparkline()


Options
-------

Sparklines support the same options as normal charts but for those that are overriden by sparkline settings, pass them to the ``render_sparkline`` method:

.. pygal-code:: sparkline

  chart = pygal.Line(interpolate='cubic')
  chart.add('', [1, 3, 5, 16, 13, 3, 7])
  chart.render_sparkline()

.. pygal-code:: sparkline

  from pygal.style import LightSolarizedStyle
  chart = pygal.Line(style=LightSolarizedStyle)
  chart.add('', [1, 3, 5, 16, 13, 3, 7, 9, 2, 1, 4, 9, 12, 10, 12, 16, 14, 12, 7, 2])
  chart.render_sparkline(width=500, height=25, show_dots=True)

With labels:

.. pygal-code:: sparkline

  chart = pygal.Line()
  chart.add('', [1, 3, 5, 16, 13, 3, 7])
  chart.x_labels = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
  chart.render_sparkline(show_x_labels=True, show_y_labels=True)


Sparktext
---------

If you want to get a simple spartext, use the render_sparktext function:

.. code-block:: python

  chart = pygal.Line()
  chart.add('', [1, 3,  5, 16, 13, 3,  7])
  chart.render_sparktext()

→ ``▁▁▂█▆▁▃``

You can also specify an explicit minimum for the values:

.. code-block:: python

  chart = pygal.Line()
  chart.add('', [1, 3,  5, 16, 13, 3,  7])
  chart.render_sparktext(relative_to=0)

→ ``▁▂▃█▆▂▄``


