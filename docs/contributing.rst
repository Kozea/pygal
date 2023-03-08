============
Contributing
============


GitHub
======

Submit your bug reports and feature requests to the `github bug tracker <http://github.com/Kozea/pygal/issues>`_.


Code style
==========

The pygal code tries to respect the `pep8 <https://www.python.org/dev/peps/pep-0008/>`_ please keep that in mind when writing code for pygal. (The code style is checked along with the unit tests, see next paragraph).


Testing
=======

Before submitting a pull request, please check that all tests still pass.


To do this install ``py.test`` and them run ``py.test`` in the root of your pygal clone:

.. code-block:: bash

   [dev@dev pygal/]$ py.test --flake8


Even better if you have several python versions installed you can run ``tox``.


Continuous Integration
======================

The current build status can be seen at our `ymci <https://ymci.kozea.fr/project/view/12>`_


Contributing a New Graph Visualization
======================================

* Fork the pygal repository on GitHub
* Clone your own fork: ``git clone git@github.com:<Your_GH_User>/pygal.git``
* ``cd pygal``
* Create a virtual environment for development: ``python -m venv .pygal_dev``
* Activate the virtual environment ``source .pygal_dev/bin/activate`` (see <https://setuptools.pypa.io/en/latest/userguide/development_mode.html> for how to do that on Windows)
* Install pygal in development mode into the virtual environment ``pip install --editable ".[test]"``

The following steps are illustrated on reusing an existing graph, the Pie Graph. For your new visualization, adapt the names, the respective test code, and the actual visualization code accordingly.

* Add a test ``touch pygal/test/test_mypie.py``. For example, add the following code to it

.. code-block:: python

from pygal import MyPie

def test_donut():
    """Test a donut pie chart"""
    chart = MyPie(inner_radius=.3, pretty_print=True)
    chart.title = 'Browser usage in February 2012 (in %)'
    chart.add('IE', 19.5)
    chart.add('Firefox', 36.6)
    chart.add('Chrome', 36.3)
    chart.add('Safari', 4.5)
    chart.add('Opera', 2.3)
    chart.render_to_file('/tmp/chart.svg')
    assert chart.render()



* Create a new file for your new graph visualization: ``touch pygal/graph/my_viz.py``. (For this example: ``cp pygal/graph/pie.py pygal/graph/mypie.py``.)
* Add an import for your new visualization class to the ``__init__.py`` module. For this example, add ``from pygal.graph.mypie import MyPie`` to the block of imports at the top of this file.
* To manually test your new visualization: ``pytest pygal/test/test_mypie.py``.
* After the test completes, inspect the file that it generated (e.g., via ``open /tmp/chart.svg``) if it looks as intended.


Now, edit the code for the visualization and its respective test.
Once your visualization works as intended run the entire test suite as described above.
Thereafter, send a pull-request to the main branch of the original repository (Kozea/pygal).
