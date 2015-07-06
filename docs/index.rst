=====
Pygal
=====

Sexy python charting
====================


.. pygal:: 300 200

   chart = pygal.HorizontalBar(y_label_rotation=-25)
   chart.x_labels = 'one', 'two', 'three', 'four', 'five'
   chart.add('alpha', [1, 2, 3, 1, 2])
   chart.add('beta', [4, 3, 0, 1, 2])

.. pygal:: 300 200

   chart = pygal.Line(x_label_rotation=25, fill=True, style=pygal.style.NeonStyle, interpolate='cubic')
   chart.x_labels = 'one', 'two', 'three', 'four', 'five'
   chart.add('alpha', [1, 2, 3, 1, 2])
   chart.add('beta', [4, 3, 0, 1, 2])

.. pygal:: 300 200

   chart = pygal.Pie()
   chart.x_labels = 'one', 'two', 'three', 'four', 'five'
   chart.add('alpha', [1, 2, 3, 1, 2])
   chart.add('beta', [4, 3, 0, 1, 2])

.. pygal:: 300 200

   chart = pygal.Radar(fill=True, style=pygal.style.NeonStyle)
   chart.x_labels = 'one', 'two', 'three', 'four', 'five'
   chart.add('alpha', [1, 2, 3, 1, 2])
   chart.add('beta', [4, 3, 0, 1, 2])


Simple python charting
======================

.. pygal-code::

   chart = pygal.Bar()
   chart.add('First', [1, 3, 3, 7])


Index
=====

.. toctree::
   :maxdepth: 1

   documentation/index
   installing
   contributing
   changelog
   api

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
