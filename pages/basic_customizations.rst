===============
 Documentation
===============


Basic customizations
====================


.. contents::


How to customize:
-----------------

pygal is customized with the help of the `Config` class (see `config.py <https://github.com/Kozea/pygal/blob/master/pygal/config.py>`_). It can be changed in several ways:

.. pygal::

  from pygal import Config
  config = Config()
  config.show_legend = False
  config.human_readable = True
  config.fill = True
  config.x_scale = config.y_scale = 0.25
  chart = pygal.XY(config)
  from math import cos, sin, pi
  a = 2 * pi / 5.
  chart.add('*', [(cos(i*a+pi/2.), sin(i*a+pi/2.)) for i in (0,2,4,1,3,0)])


By instanciating it
^^^^^^^^^^^^^^^^^^^

Just import the `Config` class and instanciate it:

.. code-block::

  from pygal import Config

  config = Config()
  config.show_legend = False
  config.human_readable = True
  config.fill = True
  config.x_scale = .25
  config.y_scale = .25
  chart = pygal.XY(config)
  ...

By inheriting it
^^^^^^^^^^^^^^^^

Import the `Config` class and override it:

.. code-block::

  from pygal import Config

  class StarConfig(Config):
      show_legend = False
      human_readable = True
      fill = True
      x_scale = .25
      y_scale = .25

  chart = pygal.XY(StarConfig())
  ...


Using keyword args
^^^^^^^^^^^^^^^^^^

As a shorthand for a one shot config, you can specify all config arguments as keyword args:

.. code-block::

  chart = pygal.XY(show_legend=False, human_readable=True, fill=True, x_scale=.25, y_scale=.25)
  ...


Size
----

``width, height, explicit_size``


The simplest and usefull customizations is the svg size to render.
It indicates the desired size of the svg.


.. pygal-code:: 200 100

  chart = pygal.Bar(width=200, height=100)
  chart.add('1', 1)
  chart.add('2', 2)

You can also set `explicit_size` to True to add size attributes to the svg tag.

Scaling
-------

``include_x_axis``

Scales are computed automaticaly between the min and the max values.

You may want to always have the absissa in your graph:

.. pygal-code::

  chart = pygal.Line(include_x_axis=True)
  chart.add('line', [.0002, .0005, .00035])


Title
-----

``title``

You can add a title to the chart by setting the `title` option:

.. pygal-code::

  chart = pygal.Line(title=u'Some points')
  chart.add('line', [.0002, .0005, .00035])


Labels
------

``x_labels, y_labels``

You can specify x labels and y labels, depending on the graph type:

.. pygal-code::

  chart = pygal.Line()
  chart.x_labels = 'Red', 'Blue', 'Green'
  chart.y_labels = .0001, .0003, .0004, .00045, .0005
  chart.add('line', [.0002, .0005, .00035])


Display
-------

``show_legend, show dots``

You can remove legend and dots by setting these at `False`

.. pygal-code::

  chart = pygal.Line(show_legend=False)
  chart.add('line', [.0002, .0005, .00035])


.. pygal-code::

  chart = pygal.Line(show_dots=False)
  chart.add('line', [.0002, .0005, .00035])

Rendering
---------

``fill, stroke, zero``

You can disable line stroking:

.. pygal-code::

  chart = pygal.Line(stroke=False)
  chart.add('line', [.0002, .0005, .00035])

And enable line filling:

.. pygal-code::

  chart = pygal.Line(fill=True)
  chart.add('line', [.0002, .0005, .00035])

To fill to an other reference than zero:

.. pygal-code::

  chart = pygal.Line(fill=True, zero=.0004)
  chart.add('line', [.0002, .0005, .00035])


Font sizes
----------

``label_font_size, value_font_size, tooltip_font_size, title_font_size, legend_font_size``


Set the various font size

.. pygal-code::

  chart = pygal.Line(label_font_size=34, legend_font_size=8)
  chart.add('line', [0, .0002, .0005, .00035])


Label rotation
--------------

``x_label_rotation, y_label_rotation``


Allow label rotation (in degrees) to avoid axis cluttering:

.. pygal-code::

  chart = pygal.Line()
  chart.x_labels = ['This is the first point !', 'This is the second point !', 'This is the third point !', 'This is the fourth point !']
  chart.add('line', [0, .0002, .0005, .00035])


.. pygal-code::

  chart = pygal.Line(x_label_rotation=20)
  chart.x_labels = ['This is the first point !', 'This is the second point !', 'This is the third point !', 'This is the fourth point !']
  chart.add('line', [0, .0002, .0005, .00035])


Human readable
--------------

``human_readable``


Display values in human readable form:

1 230 000 -> 1.23M
.00 098 7 -> 987µ

.. pygal-code::

  chart = pygal.Line(human_readable=True, y_scale=.0001)
  chart.add('line', [0, .0002, .0005, .00035])


No data text
------------

``no_data_text``


Text to display instead of the graph when no data is supplied:

.. pygal-code::

  chart = pygal.Line()
  chart.add('line', [])

.. pygal-code::

  chart = pygal.Line(no_data_text='No result found')
  chart.add('line', [])
