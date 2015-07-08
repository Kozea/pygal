Swiss map
---------


Installing
~~~~~~~~~~

The swiss map plugin can be installed by doing a:

.. code-block:: bash

  pip install pygal_maps_ch


Canton
~~~~~~

Then you will have access to the ``pygal.maps.ch`` module.

You can now plot cantons (see below for the list):

.. pygal-code::

  ch_chart = pygal.maps.ch.Cantons()
  ch_chart.title = 'Some cantons'
  ch_chart.add('Cantons 1', ['kt-zh', 'kt-be', 'kt-nw'])
  ch_chart.add('Cantons 2', ['kt-ow', 'kt-bs', 'kt-ne'])


Canton list
~~~~~~~~~~~

=====  ======
code   Canton
=====  ======
kt-zh  ZH
kt-be  BE
kt-lu  LU
kt-ju  JH
kt-ur  UR
kt-sz  SZ
kt-ow  OW
kt-nw  NW
kt-gl  GL
kt-zg  ZG
kt-fr  FR
kt-so  SO
kt-bl  BL
kt-bs  BS
kt-sh  SH
kt-ar  AR
kt-ai  AI
kt-sg  SG
kt-gr  GR
kt-ag  AG
kt-tg  TG
kt-ti  TI
kt-vd  VD
kt-vs  VS
kt-ne  NE
kt-ge  GE
=====  ======
