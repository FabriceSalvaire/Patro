.. -*- Mode: rst -*-

.. image:: https://badge.fury.io/py/PyValentina.svg
	   :target: https://badge.fury.io/py/PyValentina

.. image:: https://img.shields.io/pypi/dm/PyValentina.svg
	   :target: https://pypi.python.org/pypi/PyValentina

.. image:: https://img.shields.io/pypi/status/PyValentina.svg
	   :target: https://pypi.python.org/pypi/PyValentina

.. image:: https://img.shields.io/pypi/pyversions/PyValentina.svg
	   :target: https://pypi.python.org/pypi/PyValentina

.. image:: https://img.shields.io/pypi/l/PyValentina.svg
	   :target: https://raw.githubusercontent.com/FabriceSalvaire/PyValentina/master/LICENSE.txt

.. -*- Mode: rst -*-

..
   |PyValentinaUrl|
   |PyValentinaHomePage|_
   |PyValentinaDoc|_
   |PyValentina@github|_
   |PyValentina@readthedocs|_
   |PyValentina@readthedocs-badge|
   |PyValentina@pypi|_

.. |ohloh| image:: https://www.openhub.net/accounts/230426/widgets/account_tiny.gif
   :target: https://www.openhub.net/accounts/fabricesalvaire
   :alt: Fabrice Salvaire's Ohloh profile
   :height: 15px
   :width:  80px

.. |PyValentinaUrl| replace:: http://fabricesalvaire.github.io/PyValentina

.. |PyValentinaHomePage| replace:: PyValentina Home Page
.. _PyValentinaHomePage: http://fabricesalvaire.github.io/PyValentina

.. |PyValentinaDoc| replace:: PyValentina Documentation
.. _PyValentinaDoc: http://pyvalentina.readthedocs.org/en/latest

.. |PyValentina@readthedocs-badge| image:: https://readthedocs.org/projects/pyvalentina/badge/?version=latest
   :target: http://pyvalentina.readthedocs.org/en/latest

.. |PyValentina@github| replace:: https://github.com/FabriceSalvaire/PyValentina
.. .. _PyValentina@github: https://github.com/FabriceSalvaire/PyValentina

.. |PyValentina@readthedocs| replace:: http://pyvalentina.readthedocs.org
.. .. _PyValentina@readthedocs: http://pyvalentina.readthedocs.org

.. |PyValentina@pypi| replace:: https://pypi.python.org/pypi/PyValentina
.. .. _PyValentina@pypi: https://pypi.python.org/pypi/PyValentina

.. |Build Status| image:: https://travis-ci.org/FabriceSalvaire/PyValentina.svg?branch=master
   :target: https://travis-ci.org/FabriceSalvaire/PyValentina
   :alt: PyValentina build status @travis-ci.org

.. |Pypi Download| image:: https://img.shields.io/pypi/dm/PyValentina.svg
   :target: https://pypi.python.org/pypi/PyValentina
   :alt: PyValentina Download per month

.. |Pypi Version| image:: https://img.shields.io/pypi/v/PyValentina.svg
   :target: https://pypi.python.org/pypi/PyValentina
   :alt: PyValentina last version

.. |Pypi License| image:: https://img.shields.io/pypi/l/PyValentina.svg
   :target: https://pypi.python.org/pypi/PyValentina
   :alt: PyValentina license

.. |Pypi Format| image:: https://img.shields.io/pypi/format/PyValentina.svg
   :target: https://pypi.python.org/pypi/PyValentina
   :alt: PyValentina format

.. |Pypi Python Version| image:: https://img.shields.io/pypi/pyversions/PyValentina.svg
   :target: https://pypi.python.org/pypi/PyValentina
   :alt: PyValentina python version

..  coverage test
..  https://img.shields.io/pypi/status/Django.svg
..  https://img.shields.io/github/stars/badges/shields.svg?style=social&label=Star

.. End
.. -*- Mode: rst -*-

.. |Python| replace:: Python
.. _Python: http://python.org

.. |PyPI| replace:: PyPI
.. _PyPI: https://pypi.python.org/pypi

.. |Numpy| replace:: Numpy
.. _Numpy: http://www.numpy.org

.. |Sphinx| replace:: Sphinx
.. _Sphinx: http://sphinx-doc.org

.. End

============
 PyValentina
============

PyValentina Home Page is located at |PyValentinaUrl|

The latest documentation build from the git repository is available at readthedocs.org |PyValentina@readthedocs-badge|

Authored by `Fabrice Salvaire <http://fabrice-salvaire.pagesperso-orange.fr>`_.

.. -*- Mode: rst -*-

==========
 Features
==========

The features of PyValentina are :

* read/write *.val* and *.vit* file
* `QMuParser <http://beltoforion.de/article.php?a=muparser>`_ expressions are translated to Python and evaluated on the fly
* API to define patterns
* compute the detail of a pattern
* export the detail to latex/pgf as A0 or tiled A4 paper

Missing features:

* full operation support
* direct PDF export
* SVG export

.. image:: https://raw.github.com/FabriceSalvaire/PyValentina/master/test/output/pattern-a0.png
 :height: 600px

.. image:: https://raw.github.com/FabriceSalvaire/PyValentina/master/test/output/pattern-a4.png
 :height: 600px

.. -*- Mode: rst -*-

=============
 Introduction
=============

PyValentina is a python implementation of the `Valentina <http://valentina-project.org/>`_ Pattern
Making software, which only focus to implement the core engine and not the graphical user interface.

A pattern in flat pattern design is build from geometrical operations which can be turned to a
computer program and is thus a field of applications of Computer Aided Design.  It corresponds more
precisely to parametric modelling with dedicated features to fashion modelling and manufacturing.

What is the requirements of a pattern drafting software ?
---------------------------------------------------------

The core functionality of a CAD system for pattern drafting consists of these two software components :

* an **open** file format to store and exchange the pattern,
* a geometrical engine to compute the pattern, e.g. to generate the layout of each fabric's piece of a clothe.

The XML language is a natural candidate to define an open file format to store and exchange the
pattern. Valentina uses XML to sore measurements in *.vit* files and patterns in *.val* files.

Another solution to define and store a pattern is to use a programming language, it can be a
dedicated language or any programming language associated to a dedicated API.  Many graphical
languages was invented for specific usages, e.g. PostScript for printer, Metafont and MetaPost for
publishing, G-code for machining etc.

Usually the geometrical operations of a pattern are simple in comparison to the requirements of a
mechanical or electronic CAD software.  In first hand it is only 2D and the number of operations
should be handled smoothly by a computer of these days, whereas it is still challenging for other
domains.

.. A pattern drafting software only need a good geometrical engine to be designed efficiently.

Finally, a pattern drafting software requires an efficient graphical user interface so as to be used
by fashion designers and not only by hackers.  This software component is more challenging in therms
of software engineering, i.e. in therms of design and cost.

Why Python is a good language for this library ?
------------------------------------------------

The Python language has a large audience in engineering, due to its canonical syntax and richness of
its ecosystem (scientific libraries).

Python is a high level language and thus more productive.

Python is used as scripting language to extend many softwares, in particular the famous open source
3D creation suite `Blender <https://www.blender.org>`_, the parametric 3D modeller `FreeCad
<http://freecadweb.org>`_ as well as the SVG editor `Inkscape <https://inkscape.org/>`_.  Moreover
the 3D human model generator `MakeHuman <http://www.makehuman.org>`_ is written in Python.

Python can be easily extended by C libraries using `CFFI <http://cffi.readthedocs.io/en/latest>`_
and C++ libraries using `SWIG <http://www.swig.org>`_.

Python as other dynamic languages is able to evaluate code on the fly which provide an expression
evaluator for free.  And this feature is even more pertinent in our case because of the canonical
nature of the syntax of Python which is natural to somebody initiated to a basic mathematical
language level.

What is the purpose of this library ?
-------------------------------------

This library could serve several purposes :

* help to experiment core features for pattern drafting,
* plug Valentina to software featuring a Python plugin mechanism like Blender, FreeCad etc.

Could we implement a full software using Python ?
-------------------------------------------------

The answer is *yes we can!* since `Qt <https://www.qt.io>`_ has as a nice binding so called
`PyQt <https://riverbankcomputing.com/software/pyqt/intro>`_.

..  (if we consider Qt is superior to GTK and WxWidgets)

But up to now Python has of course some drawbacks!

Its main drawback is due to the fact the standard interpreter cannot execute more than one *Python
bytecode* thread at once, this limitation so called Global Interpreter Lock is required for
implementation simplicity.

..  in true parallelism (multi-core)
.. Consequently we can do multi-threading, even on multi-core in some cases, but less easily than in Java or Cxx11.

Despite a GUI implemented in PyQt is almost of the time more faster than the human perception on a
computer of these days.  It can be sometime difficult to overcome latency arising from the software
stack.  Thus yes we can do it, but it could requires some tricks to achieve the performance of a C++
application.

How to generate drawings in standard format like PDF or SVG ?
-------------------------------------------------------------

SVG is not difficult to generate from Python since it is based on XML.  However the PDF format is
more challenging, for efficiency reason PDF is a binary format and is thus much more complicated
than PostScript which is a true programming language.

There is several possibilities to generate PDF.

The most disturbing one is to use the `LaTeX <https://en.wikipedia.org/wiki/LaTeX>`_ publishing
system in combination with the `PGF <http://www.texample.net/tikz/examples>`_ package which provide
an amazing graphical language on top of LaTeX.  This solution could terrify many peoples, but it do
the job very well for text and graphics.  However user must install a LaTeX environment from their
Linux distribution or using the `TexLive <https://www.tug.org/texlive>`_ distribution.

A more conventional solution requires a library that can generate PDF from standard graphical
operations.  Some libraries featuring that are :

* Qt using QPainter API, Valentina solution, see https://wiki.qt.io/Handling_PDF
* `Cairo <https://www.cairographics.org/manual/cairo-PDF-Surfaces.html>`_
* `ReportLab <http://www.reportlab.com/opensource>`_  open-source PDF Toolkit (more commercial and less known)
* `Matplotlib <http://matplotlib.org>`_ (but more oriented to plot)
* and ???

.. -*- Mode: rst -*-

.. _installation-page:


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

.. _bibliography-page:

==============
 Bibliography
==============

* `CGAL Computational Geometry Algorithms Library <http://www.cgal.org>`_
* `Open Cascade Framework <https://www.opencascade.com>`_
* `David Eberly Geometric Tools web site <https://www.geometrictools.com/index.html>`_

.. End

