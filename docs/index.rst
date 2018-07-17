=====
Pygal
=====

Sexy python charting
====================


.. pygal:: 300 200

   chart = pygal.HorizontalBar(y_label_rotation=-25)
   chart.title = 'Horizontal Bar Chart with Rotated Y Labels'
   chart.x_labels = 'one', 'two', 'three', 'four', 'five'
   chart.add('alpha', [1, 2, 3, 1, 2])
   chart.add('beta', [4, 3, 0, 1, 2])

.. pygal:: 300 200

   chart = pygal.Line(x_label_rotation=25, fill=True, interpolate='cubic')
   chart.title = 'Line Chart with Rotated X Labels, Fill, and Cubic Interpolation'
   chart.x_labels = 'one', 'two', 'three', 'four', 'five'
   chart.add('alpha', [1, 2, 3, 1, 2])
   chart.add('beta', [4, 3, 0, 1, 2])

.. pygal:: 300 200

   chart = pygal.Pie()
   chart.title = 'An Ordinary Pie Chart'
   chart.x_labels = 'one', 'two', 'three', 'four', 'five'
   chart.add('alpha', [1, 2, 3, 1, 2])
   chart.add('beta', [4, 3, 0, 1, 2])

.. pygal:: 300 200

   chart = pygal.Radar(fill=True)
   chart.title = 'Radar Chart with Fill'
   chart.x_labels = 'one', 'two', 'three', 'four', 'five'
   chart.add('alpha', [1, 2, 3, 1, 2])
   chart.add('beta', [4, 3, 0, 1, 2])


Simple python charting
======================

.. pygal-code:: inline

   pygal.Bar()(1, 3, 3, 7)(1, 6, 6, 4).render()


Index
=====

.. toctree::
   :maxdepth: 1

   documentation/index
   installing
   contributing
   changelog
   api/modules

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


Credits
=======

`A Kozea Community Project <https://community.kozea.fr/>`_
