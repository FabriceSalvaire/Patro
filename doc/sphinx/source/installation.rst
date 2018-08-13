.. -*- Mode: rst -*-

.. _installation-page:

.. include:: project-links.txt
.. include:: abbreviation.txt

==============
 Installation
==============

The installation of Patro by itself is quite simple. However it will be easier to get the
dependencies on a Linux desktop.

Dependencies
------------

Patro requires the following dependencies:

 * |Python|_ 3
 * |Numpy|_

Also it is recommanded to have these Python modules:

 * pip
 * virtualenv

For development, you will need in addition:

 * |Sphinx|_

Installation from PyPi Repository
---------------------------------

Patro is made available on the |Pypi|_ repository at |Patro@pypi|

Run this command to install the last release:

.. code-block:: sh

  pip install Patro

Installation from Source
------------------------

The Patro source code is hosted at |Patro@github|

To clone the Git repository, run this command in a terminal:

.. code-block:: sh

  git clone git@github.com:FabriceSalvaire/Patro.git

Then to build and install Patro run these commands:

.. code-block:: sh

  python setup.py build
  python setup.py install

.. End
