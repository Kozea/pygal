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