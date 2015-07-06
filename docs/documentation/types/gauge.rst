Gauge charts
------------

Basic
~~~~~

Simple gauge chart:

.. pygal-code::

  gauge_chart = pygal.Gauge(human_readable=True)
  gauge_chart.title = 'DeltaBlue V8 benchmark results'
  gauge_chart.x_labels = ['Richards', 'DeltaBlue', 'Crypto', 'RayTrace', 'EarleyBoyer', 'RegExp', 'Splay', 'NavierStokes']
  gauge_chart.range = [0, 10000]
  gauge_chart.add('Chrome', 8212)
  gauge_chart.add('Firefox', 8099)
  gauge_chart.add('Opera', 2933)
  gauge_chart.add('IE', 41)
