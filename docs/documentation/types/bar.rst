Bar
---

Basic
~~~~~

Basic simple bar graph:

.. pygal-code::

  bar_chart = pygal.Bar()
  bar_chart.title = 'Browser usage evolution (in %)'
  bar_chart.x_labels = map(str, range(2002, 2013))
  bar_chart.add('Firefox', [None, None, 0, 16.6,   25,   31, 36.4, 45.5, 46.3, 42.8, 37.1])
  bar_chart.add('Chrome',  [None, None, None, None, None, None,    0,  3.9, 10.8, 23.8, 35.3])
  bar_chart.add('IE',      [85.8, 84.6, 84.7, 74.5,   66, 58.6, 54.7, 44.8, 36.2, 26.6, 20.1])
  bar_chart.add('Others',  [14.2, 15.4, 15.3,  8.9,    9, 10.4,  8.9,  5.8,  6.7,  6.8,  7.5])


Stacked
~~~~~~~

Same graph but with stacked values:

.. pygal-code::

  bar_chart = pygal.StackedBar()
  bar_chart.title = 'Browser usage evolution (in %)'
  bar_chart.x_labels = map(str, range(2002, 2013))
  bar_chart.add('Firefox', [None, None, 0, 16.6,   25,   31, 36.4, 45.5, 46.3, 42.8, 37.1])
  bar_chart.add('Chrome',  [None, None, None, None, None, None,    0,  3.9, 10.8, 23.8, 35.3])
  bar_chart.add('IE',      [85.8, 84.6, 84.7, 74.5,   66, 58.6, 54.7, 44.8, 36.2, 26.6, 20.1])
  bar_chart.add('Others',  [14.2, 15.4, 15.3,  8.9,    9, 10.4,  8.9,  5.8,  6.7,  6.8,  7.5])


Horizontal
~~~~~~~~~~

Horizontal bar diagram:

.. pygal-code::

  bar_chart = pygal.HorizontalBar()
  bar_chart.title = 'Browser usage in February 2012 (in %)'
  bar_chart.add('IE', 19.5)
  bar_chart.add('Firefox', 36.6)
  bar_chart.add('Chrome', 36.3)
  bar_chart.add('Safari', 4.5)
  bar_chart.add('Opera', 2.3)
