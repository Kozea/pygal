======================
 A SVG Charts Creator
======================

Presentation
============

pygal is a dynamic SVG charting library.


.. class:: thumbs
.. compound:: 

  .. pygal:: 300 200

     chart = pygal.HorizontalBar(y_label_rotation=-25)
     chart.x_labels = 'one', 'two', 'three', 'four', 'five'
     chart.add('red', [1, 2, 3, 1, 2])
     chart.add('green', [4, 3, 0, 1, 2])

  .. pygal:: 300 200

     chart = pygal.Line(x_label_rotation=25, fill=True, style=pygal.style.NeonStyle, interpolate='cubic')
     chart.x_labels = 'one', 'two', 'three', 'four', 'five'
     chart.add('red', [1, 2, 3, 1, 2])
     chart.add('green', [4, 3, 0, 1, 2])

  .. pygal:: 300 200

     chart = pygal.Pie()
     chart.x_labels = 'one', 'two', 'three', 'four', 'five'
     chart.add('red', [1, 2, 3, 1, 2])
     chart.add('green', [4, 3, 0, 1, 2])

  .. pygal:: 300 200

     chart = pygal.Radar(fill=True, style=pygal.style.NeonStyle)
     chart.x_labels = 'one', 'two', 'three', 'four', 'five'
     chart.add('red', [1, 2, 3, 1, 2])
     chart.add('green', [4, 3, 0, 1, 2])


It features various graph types:

- `Bar charts </chart_types/#bar-charts-histograms>`_

- `Line charts </chart_types/#line-charts>`_

- `XY charts </chart_types/#xy-charts>`_

- `Pie charts </chart_types/#pies>`_

- `Radar charts </chart_types/#radar-charts>`_


Python/Css styling with some packaged themes (`default </styles/#default>`_,
`light </styles/#light>`_,
`neon </styles/#neon>`_,
`clean </styles/#clean>`_,
`dark_solarized </styles/#dark-solarized>`_,
`light_solarized </styles/#light-solarized>`_)

`And a lot of options to customize the charts. </basic_customizations>`_

Technical Description
=====================

As of now pygal is known to work for python 2.7


Needed dependencies
-------------------

pygal uses `lxml <http://lxml.de/>`_ to generate the svg, this is the only needed dependency.

Optional dependencies
---------------------

Unit testing needs `py.test <http://pytest.org/latest/>`_ or `nosetests <http://readthedocs.org/docs/nose/en/latest/>`_.

Visual testing is based on `flask <http://flask.pocoo.org/>`_.
