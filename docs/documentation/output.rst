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

In case of rendered image turning up black, installing lxml, tinycss and cssselect should fix the issue.


Etree
-----


It is possible to get the xml etree root element of the chart (or lxml etree node if lxml is installed) by calling the ``render_tree`` method:


.. code-block:: python

   chart = pygal.Line()
   ...
   chart.render_tree()  # Return the svg root etree node


Base 64 data URI
----------------

You can directly output a base 64 encoded data uri for <embed> or <image> inclusion:


.. code-block:: python

   chart = pygal.Line()
   ...
   chart.render_data_uri()  # Return `data:image/svg+xml;charset=utf-8;base64,...`


Browser
-------

With lxml installed you can use the ``render_in_browser`` method to magically make your chart appear in your default browser.

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


Flask App
--------------

If you are using pygal in a flask app the ``render_response`` may come in handy:

.. code-block:: python

   @app.route('/charts/line.svg')
   def line_route():
     chart = pygal.Line()
     ...
     return chart.render_response()

An other way is to use a Base 64 data URI for your flask app. 

In python file:

.. code-block:: python

   @app.route('/charts/')
   def line_route():
      chart = pygal.Line()
      ...
      chart = chart.render_data_uri()
      
      return render_template( 'charts.html', chart = chart)
      
In HTML file:

.. code-block:: html

   <!-- Don't forget the "|safe"! -->
   <div id="chart">
      <embed type="image/svg+xml" src= {{ chart|safe }} />
   </div>
   
   


Django response
---------------

Same thing for django with ``render_django_response``.
