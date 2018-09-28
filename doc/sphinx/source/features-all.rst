.. include:: abbreviation.txt

.. _features-page:

==========
 Features
==========

Geometry Engine
===============

The geometry engine implements:

* 2D vector and usual transformations
* usual 2D primitives:

 * point, segment, line
 * triangle, rectangle, polygon
 * circle and conic
 * quadratic and cubic Bézier curve

* perimeter and area
* primitive intersection

Pattern Engine
==============

Graphic Engine
==============

* show drawing on screen with : |Matplotlib|_
* export drawing to : PDF, SVG, LaTeX Tikz
* export tiled pattern on A4 sheets : PDF, LaTeX Tikz
* **DXF is not yet supported**
* PDF export is implemented with the help of the |Reportlab|_ package

Note the PDF and SVG format are convertible to each other without data loss (font handling require
more attention), using the free software |Inkscape|_ for example.

Pattern Format Support
======================

* |Valentina|_ format: read/write *.val* and *.vit* file, but partially implemented, cf. supra for details

Pattern Format Compatibility
----------------------------

For more details on pattern format support, see :

.. toctree::
  :maxdepth: 1

  valentina-compatibility/index.rst

Digitalisation
==============

* import pattern from SVG (PDF can be converted to SVG using the free software |Inkscape| for
  example)
* import pattern from camera image **ACTUALLY NOT RELEASED WITH OPEN SOURCE LICENCE**
