Line
----

Basic
~~~~~

Basic simple line graph:

.. pygal-code::

  line_chart = pygal.Line()
  line_chart.title = 'Browser usage evolution (in %)'
  line_chart.x_labels = map(str, range(2002, 2013))
  line_chart.add('Firefox', [None, None,    0, 16.6,   25,   31, 36.4, 45.5, 46.3, 42.8, 37.1])
  line_chart.add('Chrome',  [None, None, None, None, None, None,    0,  3.9, 10.8, 23.8, 35.3])
  line_chart.add('IE',      [85.8, 84.6, 84.7, 74.5,   66, 58.6, 54.7, 44.8, 36.2, 26.6, 20.1])
  line_chart.add('Others',  [14.2, 15.4, 15.3,  8.9,    9, 10.4,  8.9,  5.8,  6.7,  6.8,  7.5])


Horizontal Line
~~~~~~~~~~~~~~~

Same graph but horizontal and with a range of 0-100.

.. pygal-code::

  line_chart = pygal.HorizontalLine()
  line_chart.title = 'Browser usage evolution (in %)'
  line_chart.x_labels = map(str, range(2002, 2013))
  line_chart.add('Firefox', [None, None,    0, 16.6,   25,   31, 36.4, 45.5, 46.3, 42.8, 37.1])
  line_chart.add('Chrome',  [None, None, None, None, None, None,    0,  3.9, 10.8, 23.8, 35.3])
  line_chart.add('IE',      [85.8, 84.6, 84.7, 74.5,   66, 58.6, 54.7, 44.8, 36.2, 26.6, 20.1])
  line_chart.add('Others',  [14.2, 15.4, 15.3,  8.9,    9, 10.4,  8.9,  5.8,  6.7,  6.8,  7.5])
  line_chart.range = [0, 100]


Stacked
~~~~~~~

Same graph but with stacked values and filled rendering:

.. pygal-code::

  line_chart = pygal.StackedLine(fill=True)
  line_chart.title = 'Browser usage evolution (in %)'
  line_chart.x_labels = map(str, range(2002, 2013))
  line_chart.add('Firefox', [None, None, 0, 16.6,   25,   31, 36.4, 45.5, 46.3, 42.8, 37.1])
  line_chart.add('Chrome',  [None, None, None, None, None, None,    0,  3.9, 10.8, 23.8, 35.3])
  line_chart.add('IE',      [85.8, 84.6, 84.7, 74.5,   66, 58.6, 54.7, 44.8, 36.2, 26.6, 20.1])
  line_chart.add('Others',  [14.2, 15.4, 15.3,  8.9,    9, 10.4,  8.9,  5.8,  6.7,  6.8,  7.5])


Time
~~~~

For time related plots, just format your labels or use `one variant of xy charts <xy.html#dates>`_:

.. pygal-code::

  from datetime import datetime, timedelta
  date_chart = pygal.Line(x_label_rotation=20)
  date_chart.x_labels = map(lambda d: d.strftime('%Y-%m-%d'), [
   datetime(2013, 1, 2),
   datetime(2013, 1, 12),
   datetime(2013, 2, 2),
   datetime(2013, 2, 22)])
  date_chart.add("Visits", [300, 412, 823, 672])


None values
~~~~~~~~~~~

None values will be skipped. It is also possible to `break lines <../configuration/serie.html#allow-interruptions>`_.
