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

  Negative values are ignored, interpolation might be broken if it goes below zero...


Custom css and js
-----------------

``base_css, base_js``

You can specify a css/js file to replace the one by default using `base_css` and `base_js` options.
These options take a filename in parameter.


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
---------------

``rounded_bars``

You can add a round effect to bar diagrams with `rounded_bars`:

.. pygal-code::

  chart = pygal.Bar(rounded_bars=20)
  chart.add('rounded', [3, 10, 7, 2, 9, 7])


Static options
--------------

``print_values, print_zeroes``

By default, when the graph is viewed using a non javascript compatible
viewer or as an image, all the values are displayed on the graph.

It can be disabled by setting `print_values` to `False`.

``print_zeroes`` can be enabled to display static values even if equal to zero.


Tooltip animation
-----------------

``animation_steps``

.. caution::
   Experimental (might be slow acconding to particular conditions)

If you want some smoothing in tooltip display you can set animation_steps to a number.
The greater the number the slowest but detailed the animation:


.. pygal-code::

  chart = pygal.Line(animation_steps=20)
  values = [1, 3, 43, 123, 1231, 23192]
  chart.x_labels = map(str, values)
  chart.add('log example', values)


Disable xml declaration
-----------------------

``disable_xml_declaration``

When you want to embed directly your SVG in your html,
this option disables the xml prolog in the output.

Since no encoding is declared, the result will be in unicode instead of bytes.


