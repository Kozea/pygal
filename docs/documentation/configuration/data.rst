Data
====

value_formatter
---------------

You can specifiy how the values are displayed on the tooltip using a lambda function.
The code below shows the values to 2 decimal places.

.. pygal-code::

  chart = pygal.Line()
  chart.add('line', [.070106781, 1.414213562, 3.141592654])
  chart.value_formatter = lambda x: "%.2f" % x


x_value_formatter
-----------------

Same on x axis for xy like charts:

.. pygal-code::

  chart = pygal.XY()
  chart.add('line', [(12, 31), (8, 28), (89, 12)])
  chart.x_value_formatter = lambda x:  '%s%%' % x

print_values
------------

When using pygal to display static charts for printing for example you can chose to activate this option to print all values as text.

.. pygal-code::

  from pygal.style import DefaultStyle
  chart = pygal.Bar(print_values=True, style=DefaultStyle(
                    value_font_family='googlefont:Raleway',
                    value_font_size=30,
                    value_colors=('white',)))
  chart.add('line', [0, 12, 31, 8, -28, 0])

dynamic_print_values
--------------------

Show print_values only on legend hover.

.. pygal-code::

  from pygal.style import DefaultStyle
  chart = pygal.Bar(dynamic_print_values=True, style=DefaultStyle(
                    value_font_family='googlefont:Raleway',
                    value_font_size=30,
                    value_colors=('white',)))
  chart.add('line', [0, 12, 31, 8, -28, 0])


print_values_position
---------------------

Change print value position (in bar charts only).

  .. pygal-code::

    chart = pygal.Bar(print_values=True, print_values_position='top')
    chart.add('line', [0, 12, 31, 8, -28, 0])

  .. pygal-code::

    chart = pygal.Bar(print_values=True, print_values_position='bottom')
    chart.add('line', [0, 12, 31, 8, -28, 0])


print_zeroes
------------

zero values are shown by default but you can use this option to hide them.

.. pygal-code::

  chart = pygal.Bar(print_values=True, print_zeroes=False)
  chart.add('line', [0, 12, 31, 8, -28, 0])


print_labels
------------

You can activate value label display:

.. pygal-code::

  chart = pygal.Bar(print_labels=True)
  chart.add('line', [
    0,
    {'value': 12, 'label': 'Twelve'},
    31,
    {'value': 8, 'label': 'eight'},
    28,
    0
  ])


Displaying both is also possible:

.. pygal-code::

  chart = pygal.Bar(print_labels=True, print_values=True)
  chart.add('line', [
    0,
    {'value': 12, 'label': 'Twelve'},
    31,
    {'value': 8, 'label': 'eight'},
    28,
    0
  ])


human_readable
--------------

Display values in human readable form:

.. code-block:: c

  1 230 000 -> 1.23M
  .00 098 7 -> 987µ

.. pygal-code::

  chart = pygal.Line(human_readable=True)
  chart.add('line', [0, .0002, .0005, .00035])


no_data_text
------------

Text to display instead of the graph when no data is supplied:

.. pygal-code::

  chart = pygal.Line()
  chart.add('line', [])

.. pygal-code::

  from pygal.style import DefaultStyle
  chart = pygal.Line(no_data_text='No result found',
                     style=DefaultStyle(no_data_font_size=40))
  chart.add('line', [])
