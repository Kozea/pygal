Chart configuration
===================

.. pygal::

  from pygal import Config
  config = Config()
  config.show_legend = False
  config.human_readable = True
  config.fill = True
  chart = pygal.XY(config)
  from math import cos, sin, pi
  a = 2 * pi / 5.
  chart.add('*', [(cos(i*a+pi/2.), sin(i*a+pi/2.)) for i in (0,2,4,1,3,0)])

How
---

pygal is customized at chart level with the help of the `Config class </_modules/pygal/config.html#Config>`_).


Instance
~~~~~~~~

The config class works this way:

.. code-block:: python

  from pygal import Config

  config = Config()
  config.show_legend = False
  config.human_readable = True
  config.fill = True
  chart = pygal.XY(config)
  ...

and you can share the config object between several charts. For one shot chart rendering several shorthand are available:


Attribute
~~~~~~~~~

Config values are settable on the chart object.

.. code-block:: python

  chart = pygal.XY(config)
  chart.show_legend = False
  chart.human_readable = True
  chart.fill = True
  ...


Keyword args
~~~~~~~~~~~~

Config values can be given as keyword args at init:

.. code-block:: python

  chart = pygal.XY(show_legend=False, human_readable=True, fill=True)


And at render:

.. code-block:: python

  chart = pygal.XY()
  chart.render(show_legend=False, human_readable=True, fill=True)


Options
-------

.. toctree::
   :maxdepth: 2

   sizing
   title
   label
   legend
   axis
   interpolations
   data
   tooltip
   rendering
   misc
   specific_options


