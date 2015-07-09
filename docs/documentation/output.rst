Output
======

pygal can generate multiple output formats.


SVG
---

String
~~~~~~

The obvious output is the vectorial output in svg format:

.. code-block:: python

   chart = pygal.Line()
   ...
   chart.render()  # Return the svg as bytes


It can be rendered as unicode when specifying ``is_unicode=True`` or when ``disable_xml_declaration`` is used

.. code-block:: python

   chart = pygal.Line()
   ...
   chart.render(is_unicode=True)  # Return the svg as a unicode string


File
~~~~


You can also write the chart to a file using ``render_to_file``:

.. code-block:: python

   chart = pygal.Line()
   ...
   chart.render_to_file('/tmp/chart.svg')  # Write the chart in the specified file


PNG
---

With cairosvg installed you can directly get the png file using ``render_to_png``:

.. code-block:: python

   chart = pygal.Line()
   ...
   chart.render_to_png('/tmp/chart.png')  # Write the chart in the specified file


Etree
-----


It is possible to get the xml etree root element of the chart (or lxml etree node if lxml is installed) by calling the ``render_tree`` method:


.. code-block:: python

   chart = pygal.Line()
   ...
   chart.render_tree()  # Return the svg root etree node


Browser
-------

With lxml installed you can use the ``render_in_browser`` method to magically make your chart appear in you default browser.

.. code-block:: python

   chart = pygal.Line()
   ...
   chart.render_in_browser()


PyQuery
-------

If pyquery is installed you can get the pyquery object wrapping the chart by calling ``render_pyquery``:

(This is mainly used for testing)

.. code-block:: python

   chart = pygal.Line()
   ...
   chart.render_pyquery()  # Return pyquery object


Flask response
--------------

If you are using pygal in a flask app the ``render_response`` may come in handy:

.. code-block:: python

   @app.route('/charts/line.svg')
   def line_route():
     chart = pygal.Line()
     ...
     return chart.render_response()


Django response
---------------

Same thing for django with ``render_django_response``.



Table
-----

pygal also supports a html table export of given data using the ``render_table`` option:


.. pygal-code::

  line_chart = pygal.Bar()
  line_chart.title = 'Browser usage evolution (in %)'
  line_chart.x_labels = map(str, range(2002, 2013))
  line_chart.add('Firefox', [None, None, 0, 16.6,   25,   31, 36.4, 45.5, 46.3, 42.8, 37.1])
  line_chart.add('Chrome',  [None, None, None, None, None, None,    0,  3.9, 10.8, 23.8, 35.3])
  line_chart.add('IE',      [85.8, 84.6, 84.7, 74.5,   66, 58.6, 54.7, 44.8, 36.2, 26.6, 20.1])
  line_chart.add('Others',  [14.2, 15.4, 15.3,  8.9,    9, 10.4,  8.9,  5.8,  6.7,  6.8,  7.5])
  line_chart.value_formatter = lambda x: '%.2f%%' % x if x is not None else '∅'


Default
~~~~~~~

.. pygal-table-code::

  line_chart = pygal.Bar()
  line_chart.title = 'Browser usage evolution (in %)'
  line_chart.x_labels = map(str, range(2002, 2013))
  line_chart.add('Firefox', [None, None, 0, 16.6,   25,   31, 36.4, 45.5, 46.3, 42.8, 37.1])
  line_chart.add('Chrome',  [None, None, None, None, None, None,    0,  3.9, 10.8, 23.8, 35.3])
  line_chart.add('IE',      [85.8, 84.6, 84.7, 74.5,   66, 58.6, 54.7, 44.8, 36.2, 26.6, 20.1])
  line_chart.add('Others',  [14.2, 15.4, 15.3,  8.9,    9, 10.4,  8.9,  5.8,  6.7,  6.8,  7.5])
  line_chart.value_formatter = lambda x: '%.2f%%' % x if x is not None else '∅'
  line_chart.render_table()


Style
~~~~~

.. pygal-table-code::

  line_chart = pygal.Bar()
  line_chart.title = 'Browser usage evolution (in %)'
  line_chart.x_labels = map(str, range(2002, 2013))
  line_chart.add('Firefox', [None, None, 0, 16.6,   25,   31, 36.4, 45.5, 46.3, 42.8, 37.1])
  line_chart.add('Chrome',  [None, None, None, None, None, None,    0,  3.9, 10.8, 23.8, 35.3])
  line_chart.add('IE',      [85.8, 84.6, 84.7, 74.5,   66, 58.6, 54.7, 44.8, 36.2, 26.6, 20.1])
  line_chart.add('Others',  [14.2, 15.4, 15.3,  8.9,    9, 10.4,  8.9,  5.8,  6.7,  6.8,  7.5])
  line_chart.value_formatter = lambda x: '%.2f%%' % x if x is not None else '∅'
  line_chart.render_table(style=True)


Total
~~~~~

.. pygal-table-code::

  line_chart = pygal.Bar()
  line_chart.title = 'Browser usage evolution (in %)'
  line_chart.x_labels = map(str, range(2002, 2013))
  line_chart.add('Firefox', [None, None, 0, 16.6,   25,   31, 36.4, 45.5, 46.3, 42.8, 37.1])
  line_chart.add('Chrome',  [None, None, None, None, None, None,    0,  3.9, 10.8, 23.8, 35.3])
  line_chart.add('IE',      [85.8, 84.6, 84.7, 74.5,   66, 58.6, 54.7, 44.8, 36.2, 26.6, 20.1])
  line_chart.add('Others',  [14.2, 15.4, 15.3,  8.9,    9, 10.4,  8.9,  5.8,  6.7,  6.8,  7.5])
  line_chart.value_formatter = lambda x: '%.2f%%' % x if x is not None else '∅'
  line_chart.render_table(style=True, total=True)


Transposed
~~~~~~~~~~

.. pygal-table-code::

  line_chart = pygal.Bar()
  line_chart.title = 'Browser usage evolution (in %)'
  line_chart.x_labels = map(str, range(2002, 2013))
  line_chart.add('Firefox', [None, None, 0, 16.6,   25,   31, 36.4, 45.5, 46.3, 42.8, 37.1])
  line_chart.add('Chrome',  [None, None, None, None, None, None,    0,  3.9, 10.8, 23.8, 35.3])
  line_chart.add('IE',      [85.8, 84.6, 84.7, 74.5,   66, 58.6, 54.7, 44.8, 36.2, 26.6, 20.1])
  line_chart.add('Others',  [14.2, 15.4, 15.3,  8.9,    9, 10.4,  8.9,  5.8,  6.7,  6.8,  7.5])
  line_chart.value_formatter = lambda x: '%.2f%%' % x if x is not None else '∅'
  line_chart.render_table(style=True, total=True, transpose=True)

