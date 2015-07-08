Pie
---

Basic
~~~~~

Simple pie:


.. pygal-code::

  pie_chart = pygal.Pie()
  pie_chart.title = 'Browser usage in February 2012 (in %)'
  pie_chart.add('IE', 19.5)
  pie_chart.add('Firefox', 36.6)
  pie_chart.add('Chrome', 36.3)
  pie_chart.add('Safari', 4.5)
  pie_chart.add('Opera', 2.3)


Multi-series pie
~~~~~~~~~~~~~~~~

Same pie but divided in sub category:

.. pygal-code::

  pie_chart = pygal.Pie()
  pie_chart.title = 'Browser usage by version in February 2012 (in %)'
  pie_chart.add('IE', [5.7, 10.2, 2.6, 1])
  pie_chart.add('Firefox', [.6, 16.8, 7.4, 2.2, 1.2, 1, 1, 1.1, 4.3, 1])
  pie_chart.add('Chrome', [.3, .9, 17.1, 15.3, .6, .5, 1.6])
  pie_chart.add('Safari', [4.4, .1])
  pie_chart.add('Opera', [.1, 1.6, .1, .5])


Donut
~~~~~

It is possible to specify an inner radius to get a donut:

.. pygal-code::

  pie_chart = pygal.Pie(inner_radius=.4)
  pie_chart.title = 'Browser usage in February 2012 (in %)'
  pie_chart.add('IE', 19.5)
  pie_chart.add('Firefox', 36.6)
  pie_chart.add('Chrome', 36.3)
  pie_chart.add('Safari', 4.5)
  pie_chart.add('Opera', 2.3)

or a ring:

.. pygal-code::

  pie_chart = pygal.Pie(inner_radius=.75)
  pie_chart.title = 'Browser usage in February 2012 (in %)'
  pie_chart.add('IE', 19.5)
  pie_chart.add('Firefox', 36.6)
  pie_chart.add('Chrome', 36.3)
  pie_chart.add('Safari', 4.5)
  pie_chart.add('Opera', 2.3)


Half pie
~~~~~~~~

.. pygal-code::

  pie_chart = pygal.Pie(half_pie=True)
  pie_chart.title = 'Browser usage in February 2012 (in %)'
  pie_chart.add('IE', 19.5)
  pie_chart.add('Firefox', 36.6)
  pie_chart.add('Chrome', 36.3)
  pie_chart.add('Safari', 4.5)
  pie_chart.add('Opera', 2.3)
