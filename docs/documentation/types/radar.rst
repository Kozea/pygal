Radar
-----

Basic
~~~~~

Simple Kiviat diagram:

.. pygal-code:: 600 500

  radar_chart = pygal.Radar()
  radar_chart.title = 'V8 benchmark results'
  radar_chart.x_labels = ['Richards', 'DeltaBlue', 'Crypto', 'RayTrace', 'EarleyBoyer', 'RegExp', 'Splay', 'NavierStokes']
  radar_chart.add('Chrome', [6395, 8212, 7520, 7218, 12464, 1660, 2123, 8607])
  radar_chart.add('Firefox', [7473, 8099, 11700, 2651, 6361, 1044, 3797, 9450])
  radar_chart.add('Opera', [3472, 2933, 4203, 5229, 5810, 1828, 9013, 4669])
  radar_chart.add('IE', [43, 41, 59, 79, 144, 136, 34, 102])
