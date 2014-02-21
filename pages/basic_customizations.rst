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
~~~~~~~~~~~~~~~~~~~

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
~~~~~~~~~~~~~~~~

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
~~~~~~~~~~~~~~~~~~

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


Spacing
-------

``spacing, margin``

Spacing determines the space between all elements:

.. pygal-code::

  chart = pygal.Bar(spacing=50)
  chart.x_labels = u'αβγδ'
  chart.add('line 1', [5, 15, 10, 8])
  chart.add('line 2', [15, 20, 8, 11])


Margin is the external chart margin:

.. pygal-code::

  chart = pygal.Bar(margin=50)
  chart.x_labels = u'αβγδ'
  chart.add('line 1', [5, 15, 10, 8])
  chart.add('line 2', [15, 20, 8, 11])



Scaling
-------

``include_x_axis``

Scales are computed automaticaly between the min and the max values.

You may want to always have the absissa in your graph:

.. pygal-code::

  chart = pygal.Line(include_x_axis=True)
  chart.add('line', [.0002, .0005, .00035])


``range``

You may also want to explicitly set a range, `range` takes a tuple containing min and max:

.. pygal-code::

  chart = pygal.Line(range=(.0001, .001))
  chart.add('line', [.0002, .0005, .00035])


``order_min``

Finaly you can tell at which precision pygal should stop scaling (in log10):

.. pygal-code::

  chart = pygal.Line(order_min=-4)
  chart.add('line', [.0002, .0005, .00035])



Titles
------

Chart title
~~~~~~~~~~~

``title``

You can add a title to the chart by setting the `title` option:

.. pygal-code::

  chart = pygal.Line(title=u'Some points')
  chart.add('line', [.0002, .0005, .00035])


X title
~~~~~~~

``x_title``

You can add a title to the x axis by setting the `x_title` option:

.. pygal-code::

  chart = pygal.Line(title=u'Some points', x_title='X Axis')
  chart.add('line', [.0002, .0005, .00035])


Y title
~~~~~~~

``y_title``

You can add a title to the y axis by setting the `y_title` option:

.. pygal-code::

  chart = pygal.Line(title=u'Some points', y_title='Y Axis')
  chart.add('line', [.0002, .0005, .00035])


Font size
~~~~~~~~~

``title_font_size``

.. pygal-code::

  chart = pygal.Line(title=u'Some points', x_title='X Axis', y_title='Y Axis',
       title_font_size=24)
  chart.add('line', [.0002, .0005, .00035])


Labels
------

Add labels
~~~~~~~~~~

``x_labels, y_labels``

You can specify x labels and y labels, depending on the graph type:

.. pygal-code::

  chart = pygal.Line()
  chart.x_labels = 'Red', 'Blue', 'Green'
  chart.y_labels = .0001, .0003, .0004, .00045, .0005
  chart.add('line', [.0002, .0005, .00035])


Remove y labels
~~~~~~~~~~~~~~~

``show_y_labels``

Set this to False to deactivate y labels:

.. pygal-code::

  chart = pygal.Line(show_y_labels=False)
  chart.add('line', [.0002, .0005, .00035])


Rotate labels
~~~~~~~~~~~~~

``x_label_rotation, y_label_rotation``


Allow label rotation (in degrees) to avoid axis cluttering:

.. pygal-code::

  chart = pygal.Line()
  chart.x_labels = [
      'This is the first point !',
      'This is the second point !',
      'This is the third point !',
      'This is the fourth point !']
  chart.add('line', [0, .0002, .0005, .00035])


.. pygal-code::

  chart = pygal.Line(x_label_rotation=20)
  chart.x_labels = [
      'This is the first point !',
      'This is the second point !',
      'This is the third point !',
      'This is the fourth point !']
  chart.add('line', [0, .0002, .0005, .00035])


Change minor/major labels
~~~~~~~~~~~~~~~~~~~~~~~~~

``x_labels_major, x_labels_major_every, x_labels_major_count, show_minor_x_labels, y_labels_major, y_labels_major_every, y_labels_major_count, show_minor_y_labels``

You can alter major minor behaviour of axes thanks to `Arjen Stolk <https://github.com/simplyarjen>`_

.. pygal-code::

  chart = pygal.Line(x_label_rotation=20)
  chart.x_labels = [
      'This is the first point !',
      'This is the second point !',
      'This is the third point !',
      'This is the fourth point !']
  chart.x_labels_major = ['This is the first point !', 'This is the fourth point !']
  chart.add('line', [0, .0002, .0005, .00035])


.. pygal-code::

  chart = pygal.Line(x_label_rotation=20, x_labels_major_every=3)
  chart.x_labels = [
      'This is the first point !',
      'This is the second point !',
      'This is the third point !',
      'This is the fourth point !']
  chart.add('line', [0, .0002, .0005, .00035])


.. pygal-code::

  chart = pygal.Line(x_label_rotation=20, x_labels_major_count=3)
  chart.x_labels = [
      'This is the first point !',
      'This is the second point !',
      'This is the third point !',
      'This is the fourth point !']
  chart.add('line', [0, .0002, .0005, .00035])


.. pygal-code::

  chart = pygal.Line(x_label_rotation=20, show_minor_x_labels=False)
  chart.x_labels = [
      'This is the first point !',
      'This is the second point !',
      'This is the third point !',
      'This is the fourth point !']
  chart.x_labels_major = ['This is the first point !', 'This is the fourth point !']
  chart.add('line', [0, .0002, .0005, .00035])


.. pygal-code::

  chart = pygal.Line(y_label_rotation=-20)
  chart.y_labels_major = []
  chart.add('line', [0, .0002, .0005, .00035])


.. pygal-code::

  chart = pygal.Line()
  chart.y_labels_major = [.0001, .0004]
  chart.add('line', [0, .0002, .0005, .00035])


.. pygal-code::

  chart = pygal.Line(y_label_rotation=20, y_labels_major_every=3)
  chart.add('line', [0, .0002, .0005, .00035])


.. pygal-code::

  chart = pygal.Line(y_labels_major_count=3)
  chart.add('line', [0, .0002, .0005, .00035])


.. pygal-code::

  chart = pygal.Line(y_labels_major_every=2, show_minor_y_labels=False)
  chart.add('line', [0, .0002, .0005, .00035])


Font size
~~~~~~~~~

``label_font_size, major_label_font_size``

.. pygal-code::

  chart = pygal.Line(x_label_rotation=20, label_font_size=8, major_label_font_size=12)
  chart.x_labels = [
      'This is the first point !',
      'This is the second point !',
      'This is the third point !',
      'This is the fourth point !']
  chart.x_labels_major = ['This is the first point !', 'This is the fourth point !']
  chart.add('line', [0, .0002, .0005, .00035])


Dots
----

Removing
~~~~~~~~

``show_dots``

You can remove dots by setting `show_dots` at `False`


.. pygal-code::

  chart = pygal.Line(show_dots=False)
  chart.add('line', [.0002, .0005, .00035])

Size
~~~~

``dots_size``

.. pygal-code::

  chart = pygal.Line(dots_size=5)
  chart.add('line', [.0002, .0005, .00035])


Legends
-------

Removing
~~~~~~~~

``show_legend``

You can remove legend by setting these at `False`

.. pygal-code::

  chart = pygal.Line(show_legend=False)
  chart.add('line', [.0002, .0005, .00035])


Legend at bottom
~~~~~~~~~~~~~~~~

``legend_at_bottom``

You can put legend at bottom by setting `legend_at_bottom` at True:


.. pygal-code::

  chart = pygal.Line(legend_at_bottom=True)
  chart.add('line', [.0002, .0005, .00035])


Legend box size
~~~~~~~~~~~~~~~

``legend_box_size``

.. pygal-code::

  chart = pygal.Line(legend_box_size=18)
  chart.add('line', [.0002, .0005, .00035])


Font size
~~~~~~~~~

``legend_font_size``

.. pygal-code::

  chart = pygal.Line(legend_font_size=20)
  chart.add('line', [.0002, .0005, .00035])


Tooltip
-------

Rounded corner
~~~~~~~~~~~~~~

``tooltip_border_radius``

.. pygal-code::

  chart = pygal.Line(tooltip_border_radius=10)
  chart.add('line', [.0002, .0005, .00035])


Font size
~~~~~~~~~

``tooltip_font_size``


.. pygal-code::

  chart = pygal.Line(tooltip_font_size=24)
  chart.add('line', [.0002, .0005, .00035])


Two y axes
----------

``secondary``

You can plot your values to 2 separate axes, thanks to `wiktorn <https://github.com/wiktorn>`_

.. pygal-code::

  chart = pygal.Line(title=u'Some different points')
  chart.add('line', [.0002, .0005, .00035])
  chart.add('other line', [1000, 2000, 7000], secondary=True)


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

``value_font_size, tooltip_font_size``


Set the various font size

.. pygal-code::

  chart = pygal.Line(label_font_size=34, legend_font_size=8)
  chart.add('line', [0, .0002, .0005, .00035])


Text truncation
---------------

``truncate_legend, truncate_label``

By default long text are automatically truncated at reasonable length which fit in the graph.

You can override that by setting truncation lenght with `truncate_legend` and `truncate_label`.


.. pygal-code::

  chart = pygal.Line(truncate_legend=3, truncate_label=17)
  chart.x_labels = [
      'This is the first point !',
      'This is the second point !',
      'This is the third point !',
      'This is the fourth point !']
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


Next: `Interpolations </interpolations>`_
