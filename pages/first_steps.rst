===============
 Documentation
===============


First steps
===========

First you need to download the pygal package, see the `download page </download>`_.

When it's done, you are ready to make your first chart:

.. code-block:: python

  import pygal                                                       # First import pygal
  bar_chart = pygal.Bar()                                            # Then create a bar graph object
  bar_chart.add('Fibonacci', [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55])  # Add some values
  bar_chart.render_to_file('bar_chart.svg')                          # Save the svg to a file

Now you have a svg file called `bar_chart.svg` in your current directory.

You can open it with various programs such as your web browser, inkscape or any svg compatible viewer.



