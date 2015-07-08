Titles
======


title
-----

You can add a title to the chart by setting the ``title`` option:

.. pygal-code::

  chart = pygal.Line(title=u'Some points')
  chart.add('line', [.0002, .0005, .00035])


x_title
-------

You can add a title to the x axis by setting the ``x_title`` option:

.. pygal-code::

  chart = pygal.Line(title=u'Some points', x_title='X Axis')
  chart.add('line', [.0002, .0005, .00035])


y_title
-------


You can add a title to the y axis by setting the ``y_title`` option:

.. pygal-code::

  chart = pygal.Line(title=u'Some points', y_title='Y Axis')
  chart.add('line', [.0002, .0005, .00035])


title_font_size
---------------

.. pygal-code::

  chart = pygal.Line(title=u'Some points', x_title='X Axis', y_title='Y Axis',
       title_font_size=24)
  chart.add('line', [.0002, .0005, .00035])
