Labels
======


You can specify x labels and y labels, depending on the graph type:


x_labels
--------

.. pygal-code::

  chart = pygal.Line()
  chart.x_labels = 'Red', 'Blue', 'Green'
  chart.add('line', [.0002, .0005, .00035])


y_labels
--------

.. pygal-code::

  chart = pygal.Line()
  chart.y_labels = .0001, .0003, .0004, .00045, .0005
  chart.add('line', [.0002, .0005, .00035])


show_x_labels
-------------

Set this to False to deactivate x labels:

.. pygal-code::

  chart = pygal.Line(show_x_labels=False)
  chart.x_labels = 'Red', 'Blue', 'Green'
  chart.add('line', [.0002, .0005, .00035])

show_y_labels
-------------

Set this to False to deactivate y labels:

.. pygal-code::

  chart = pygal.Line(show_y_labels=False)
  chart.x_labels = 'Red', 'Blue', 'Green'
  chart.add('line', [.0002, .0005, .00035])




Allow label rotation (in degrees) to avoid axis cluttering:

.. pygal-code::

  chart = pygal.Line()
  chart.x_labels = [
      'This is the first point !',
      'This is the second point !',
      'This is the third point !',
      'This is the fourth point !']
  chart.add('line', [0, .0002, .0005, .00035])


x_label_rotation
----------------

.. pygal-code::

  chart = pygal.Line(x_label_rotation=20)
  chart.x_labels = [
      'This is the first point !',
      'This is the second point !',
      'This is the third point !',
      'This is the fourth point !']
  chart.add('line', [0, .0002, .0005, .00035])


y_label_rotation
----------------

.. pygal-code::

  chart = pygal.Line(y_label_rotation=20)
  chart.add('line', [0, .0002, .0005, .00035])



You can alter major minor behaviour of axes thanks to `Arjen Stolk <https://github.com/simplyarjen>`_

x_labels_major
--------------

.. pygal-code::

  chart = pygal.Line(x_label_rotation=20)
  chart.x_labels = [
      'This is the first point !',
      'This is the second point !',
      'This is the third point !',
      'This is the fourth point !']
  chart.x_labels_major = ['This is the first point !', 'This is the fourth point !']
  chart.add('line', [0, .0002, .0005, .00035])


x_labels_major_every
--------------------

.. pygal-code::

  chart = pygal.Line(x_label_rotation=20, x_labels_major_every=3)
  chart.x_labels = [
      'This is the first point !',
      'This is the second point !',
      'This is the third point !',
      'This is the fourth point !']
  chart.add('line', [0, .0002, .0005, .00035])


x_labels_major_count
--------------------

.. pygal-code::

  chart = pygal.Line(x_label_rotation=20, x_labels_major_count=3)
  chart.x_labels = [
      'This is the first point !',
      'This is the second point !',
      'This is the third point !',
      'This is the fourth point !']
  chart.add('line', [0, .0002, .0005, .00035])


show_minor_x_labels
-------------------

.. pygal-code::

  chart = pygal.Line(x_label_rotation=20, show_minor_x_labels=False)
  chart.x_labels = [
      'This is the first point !',
      'This is the second point !',
      'This is the third point !',
      'This is the fourth point !']
  chart.x_labels_major = ['This is the first point !', 'This is the fourth point !']
  chart.add('line', [0, .0002, .0005, .00035])


y_labels_major
--------------

.. pygal-code::

  chart = pygal.Line(y_label_rotation=-20)
  chart.y_labels_major = []
  chart.add('line', [0, .0002, .0005, .00035])


.. pygal-code::

  chart = pygal.Line()
  chart.y_labels_major = [.0001, .0004]
  chart.add('line', [0, .0002, .0005, .00035])


y_labels_major_every
--------------------

.. pygal-code::

  chart = pygal.Line(y_label_rotation=20, y_labels_major_every=3)
  chart.add('line', [0, .0002, .0005, .00035])


y_labels_major_count
--------------------

.. pygal-code::

  chart = pygal.Line(y_labels_major_count=3)
  chart.add('line', [0, .0002, .0005, .00035])


show_minor_y_labels
-------------------

.. pygal-code::

  chart = pygal.Line(y_labels_major_every=2, show_minor_y_labels=False)
  chart.add('line', [0, .0002, .0005, .00035])


truncate_label
--------------


By default long labels are automatically truncated at reasonable length to fit in the graph.

You can override that by setting truncation lenght with ``truncate_label``.


.. pygal-code::

  chart = pygal.Line(truncate_label=17)
  chart.x_labels = [
      'This is the first point !',
      'This is the second point !',
      'This is the third point !',
      'This is the fourth point !']
  chart.add('line', [0, .0002, .0005, .00035])

or disable it by setting this to -1

.. pygal-code::

  chart = pygal.Line(truncate_label=-1)
  chart.x_labels = [
      'This is the first point !',
      'This is the second point !',
      'This is the third point !',
      'This is the fourth point !']
  chart.add('line', [0, .0002, .0005, .00035])

