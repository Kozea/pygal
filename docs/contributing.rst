============
Contributing
============


Github
======

Submit your bug reports and feature requests to the `github bug tracker <http://github.com/Kozea/pygal/issues>`_.


Code style
==========

The pygal code tries to respect the `pep8 <https://www.python.org/dev/peps/pep-0008/>`_ please keep that in mind when writing code for pygal. (The code style is checked along with the unit tests, see next paragraph).


Testing
=======

Before submiting a pull request, please check that linting and all tests still pass.


To do this launch `make install` and then run in the root of your pygal clone:

.. code-block:: bash

   [dev@dev pygal/]$ make check
   [dev@dev pygal/]$ make lint


Even better if you have several python versions installed you can run ``tox``.


Continuous Integration
======================

The current build status can be seen at our `ymci <https://ymci.kozea.fr/project/view/12>`_

