Embedding in a web page
=======================


Within an embed tag
-------------------

First set up an url entry point for your svg: ``/mysvg.svg`` don't forget to set the mime-type to ``image/svg+xml``. (If you are using flask you can use the ``render_response`` method.)

Then in your html put an embed tag like this:

.. code-block:: html

  <!DOCTYPE html>
  <html>
    <head>
      <!-- ... -->
    </head>
    <body>
      <figure>
        <embed type="image/svg+xml" src="/mysvg.svg" />
      </figure>
    </body>
  </html>

You can also use an iframe tag, but automatic sizing with ``width: 100%`` will not work.


Directly in the html
--------------------

You can insert it directly in a html page with the use of ``disable_xml_declaration``.
You have to put the javascript manually in you webpage, for instance:


.. code-block:: html

  <!DOCTYPE html>
  <html>
    <head>
    <script type="text/javascript" src="http://kozea.github.com/pygal.js/latest/pygal-tooltips.min.js"></script>
      <!-- ... -->
    </head>
    <body>
      <figure>
        <!-- Pygal render() result: -->
        <svg
          xmlns:xlink="http://www.w3.org/1999/xlink"
          xmlns="http://www.w3.org/2000/svg"
          id="chart-e6700c90-7a2b-4602-961c-83ccf5e59204"
          class="pygal-chart"
          viewBox="0 0 800 600">
          <!--Generated with pygal 1.0.0 ©Kozea 2011-2013 on 2013-06-25-->
          <!--http://pygal.org-->
          <!--http://github.com/Kozea/pygal-->
          <defs>
            <!-- ... -->
          </defs>
          <title>Pygal</title>
          <g class="graph bar-graph vertical">
            <!-- ... -->
          </g>
        </svg>
        <!-- End of Pygal render() result: -->
      </figure>
    </body>
  </html>

You can use ``explicit_size`` to set the svg size from the ``width``, ``height`` properties.

