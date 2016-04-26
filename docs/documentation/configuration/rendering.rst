Rendering
=========

stroke
------

On line graphs you can disable line stroking:

.. pygal-code::

  chart = pygal.Line(stroke=False)
  chart.add('line', [.0002, .0005, .00035])


fill
----

And enable line filling:

.. pygal-code::

  chart = pygal.Line(fill=True)
  chart.add('line', [.0002, .0005, .00035])


zero
----

To fill to an other reference than zero:

.. pygal-code::

  chart = pygal.Line(fill=True, zero=.0004)
  chart.add('line', [.0002, .0005, .00035])


show_dots
---------

You can remove dots by setting ``show_dots`` at ``False```

.. pygal-code::

  chart = pygal.Line(show_dots=False)
  chart.add('line', [.0002, .0005, .00035])


show_only_major_dots
--------------------

You can remove minor x-labelled dots by setting ``show_only_major_dots`` at ``True``

.. pygal-code::

  chart = pygal.Line(show_only_major_dots=True)
  chart.add('line', range(12))
  chart.x_labels = map(str, range(12))
  chart.x_labels_major = ['2', '4', '8', '11']


dots_size
---------

You can change the dot size

.. pygal-code::

  chart = pygal.Line(dots_size=5)
  chart.add('line', [.0002, .0005, .00035])


stroke_style
------------

It is possible to set a default style for lines with the ``stroke_style`` dictionary.

.. pygal-code::

  chart = pygal.Line(stroke_style={'width': 5, 'dasharray': '3, 6', 'linecap': 'round', 'linejoin': 'round'})
  chart.add('line', [.0002, .0005, .00035])



show_x_guides
-------------

You can force the display of x guides

.. pygal-code::

  chart = pygal.Line(show_x_guides=True)
  chart.x_labels = ['alpha', 'beta', 'gamma']
  chart.add('line', [.0002, .0005, .00035])


show_y_guides
-------------

Or disable y guides:

.. pygal-code::

  chart = pygal.Line(show_y_guides=False)
  chart.x_labels = ['alpha', 'beta', 'gamma']
  chart.add('line', [.0002, .0005, .00035])


style
-----

see `styles <../styles.html>`_


You can add or replace css/js files in pygal using the `css` and `js` array options.
These lists contain absolute filenames and/or external URI. (Relative filenames are relative to pygal internal files)

All config lists now support the use of ellipsis as an extender. For instance:

.. code-block:: python

  config = Config()
  config.css.append('style.css')
  chart = pygal.Line(config)

can now be replaced with:

.. code-block:: python

  chart = pygal.Line(css=(..., 'style.css'))

or if you are still using python from the last decade:

.. code-block:: python

  from pygal._compat import _ellipsis
  chart = pygal.Line(css=(_ellipsis, 'style.css'))


css
---

Default:

.. code-block:: python

    css = ['file://style.css', 'file://graph.css']


Css can also specified inline by prepending `inline:` to the css:

.. code-block:: python

   css = ['inline:.rect { fill: blue; }']


classes
-------

You can alter pygal svg node classes with the classes option:

.. code-block:: python

  chart = pygal.Line(classes=(..., 'flex'))


defs
----

You can add defs like linearGradient, radialGradient, pattern to the defs config:


.. pygal-code::

    config = pygal.Config()
    config.style = pygal.style.DarkStyle
    config.defs.append('''
      <linearGradient id="gradient-0" x1="0" x2="0" y1="0" y2="1">
        <stop offset="0%" stop-color="#ff5995" />
        <stop offset="100%" stop-color="#feed6c" />
      </linearGradient>
    ''')
    config.defs.append('''
      <linearGradient id="gradient-1" x1="0" x2="0" y1="0" y2="1">
        <stop offset="0%" stop-color="#b6e354" />
        <stop offset="100%" stop-color="#8cedff" />
      </linearGradient>
    ''')
    config.css.append('''inline:
      .color-0 {
        fill: url(#gradient-0) !important;
        stroke: url(#gradient-0) !important;
      }''')
    config.css.append('''inline:
      .color-1 {
        fill: url(#gradient-1) !important;
        stroke: url(#gradient-1) !important;
      }''')
    chart = pygal.Line(config)
    chart.add('1', [1, 3, 12, 3, 4, None, 9])
    chart.add('2', [7, -4, 10, None, 8, 3, 1])
    chart.x_labels = ('a', 'b', 'c', 'd', 'e', 'f', 'g')
    chart.legend_at_bottom = True
    chart.interpolate = 'cubic'


js
--

.. code-block:: python

    js = [
        '//kozea.github.io/pygal.js/2.0.x/pygal-tooltips.min.js'
    ]

See `pygal.js <https://github.com/Kozea/pygal.js/>`_


force_uri_protocol
------------------

In case of rendering the svg as a data uri, it is mandatory to specify a protocol.

It can be set to http or https and will be used for '//domain/' like uri.

It is used along with ``render_data_uri``.
