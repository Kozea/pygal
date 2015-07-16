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


css
---

Default:

.. code-block:: python

    css = ['file://style.css', 'file://graph.css']


Css can also specified inline by prepending `inline:` to the css:

.. code-block:: python

   css = ['inline:.rect { fill: blue; }']


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
