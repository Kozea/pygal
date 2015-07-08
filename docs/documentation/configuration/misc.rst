Misc
====

pretty_print
------------

You can enable pretty print if you want to edit the source by hand (look at this frame source):

.. pygal-code::

  chart = pygal.Bar(pretty_print=True)
  chart.add('values', [3, 10, 7, 2, 9, 7])



disable_xml_declaration
-----------------------

When you want to embed directly your SVG in your html,
this option disables the xml prolog in the output.

Since no encoding is declared, the result will be in unicode instead of bytes.


no_prefix
---------

Normally pygal set an unique id to the chart and use it to style each chart to avoid collisions when svg are directly embedded in html. This can be a problem if you use external styling overriding the prefixed css. You can set this to True in order to prevent that behaviour.


strict
------

This activates strict value mode which disable some data adapting and filters.
This will make a logarithmic chart crash on negative values for example.
