===============
 Documentation
===============


Other customizations
====================

.. contents::


Logarithmic
-----------

``logarithmic``

You can set the scale to be logarithmic:

.. pygal-code::

  chart = pygal.Line(logarithmic=True)
  values = [1, 3, 43, 123, 1231, 23192]
  chart.x_labels = map(str, values)
  chart.add('log example', values)

.. caution::

  Negative values are ignored


Custom css and js
-----------------

``css, js``

You can add or replace css/js files in pygal using the `css` and `js` array options.
These lists contain absolute filenames and/or external URI. (Relative filenames are relative to pygal internal files)

Default:

.. code-block::

    css = ['style.css', 'graph.css']
    js = [
        'http://kozea.github.com/pygal.js/javascripts/svg.jquery.js',
        'http://kozea.github.com/pygal.js/javascripts/pygal-tooltips.js'
    ]


Legend box size
---------------

``legend_box_size``

You can change the size of the rectangle next to the legend:

.. pygal-code::

  chart = pygal.Line(legend_box_size=50)
  values = [1, 3, 43, 123, 1231, 23192]
  chart.x_labels = map(str, values)
  chart.add('log example', values)


Rounded bars
------------

``rounded_bars``

You can add a round effect to bar diagrams with `rounded_bars`:

.. pygal-code::

  chart = pygal.Bar(rounded_bars=20)
  chart.add('values', [3, 10, 7, 2, 9, 7])


Pretty print
------------

``pretty_print``

You can enable pretty print if you want to edit the source at hand (look at this frame source):

.. pygal-code::

  chart = pygal.Bar(pretty_print=True)
  chart.add('values', [3, 10, 7, 2, 9, 7])


Static options
--------------

``print_values, print_zeroes``

By default, when the graph is viewed using a non javascript compatible
viewer or as an image, all the values are displayed on the graph.

It can be disabled by setting `print_values` to `False`.

`print_zeroes` can be enabled to display static values even if equal to zero.


Disable xml declaration
-----------------------

``disable_xml_declaration``

When you want to embed directly your SVG in your html,
this option disables the xml prolog in the output.

Since no encoding is declared, the result will be in unicode instead of bytes.



No prefix
---------

``no_prefix``

Normally pygal set an unique id to the chart and use it to style each chart to avoid collisions when svg are directly embedded in html. This can be a problem if you use external styling overriding the prefixed css. You can set this to True in order to prevent that behaviour.

