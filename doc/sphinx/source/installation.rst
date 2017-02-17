.. -*- Mode: rst -*-

.. _installation-page:

.. include:: project-links.txt
.. include:: abbreviation.txt

==============
 Installation
==============

The installation of PyValentina by itself is quite simple. However it will be easier to get the
dependencies on a Linux desktop.

Dependencies
------------

PyValentina requires the following dependencies:

 * |Python|_ 3
 * |Numpy|_

Also it is recommanded to have these Python modules:

 * pip
 * virtualenv

For development, you will need in addition:

 * |Sphinx|_

Installation from PyPi Repository
---------------------------------

PyValentina is made available on the |Pypi|_ repository at |PyValentina@pypi|

Run this command to install the last release:

.. code-block:: sh

  pip install PyValentina

Installation from Source
------------------------

The PyValentina source code is hosted at |PyValentina@github|

To clone the Git repository, run this command in a terminal:

.. code-block:: sh

  git clone git@github.com:FabriceSalvaire/PyValentina.git

Then to build and install PyValentina run these commands:

.. code-block:: sh

  python setup.py build
  python setup.py install

.. End
