.. include:: abbreviation.txt

.. _features-page:

==========
 Features
==========

Patro implements several components:

* a 2D Geometry Engine
* a Pattern Engine
* a Graphic Engine to export drawing to screen display, SVG and PDF file
* a submodule to read/write SVG file
* import/export of the |Valentina|_ file format
* import of SVG pattern (as well as PDF using a conversion tools like |Inkscape|_)
* digitalisation of patterns acquired with a camera **ACTUALLY NOT RELEASED WITH OPEN SOURCE LICENCE**

.. note:: Patro is just a core engine actually. It doesn't implement a GUI similar to |Valentina|_.

.. note:: Patro doesn't implement 3D feature actually, like automatic clothe fitting on avatar and tension map.

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
* thanks to |Sympy|_, Patro could implement symbolic computations when it is feasible

Pattern Engine
==============

* Measurements can be imported from Valentina *.vit* or a YAML file.  We can merge several files to a measurement set.
* Measurements are lazily evaluated using |Sympy|_ symbolic computation, which means we can compute
  exact values and the order of definition doesn't matter.

Graphic Engine
==============

* show drawing on screen with : |Matplotlib|_
* export drawing to : PDF, SVG, DXF, LaTeX Tikz
* export tiled pattern on A4 sheets : PDF, LaTeX Tikz
* PDF export is implemented with the help of the |Reportlab|_ package

Pattern Format Support
======================

* |Valentina|_ format: read/write *.val* and *.vit* file, but partially implemented, cf. supra for details
* import pattern from SVG
* **DXF is not yet supported**

.. note:: PDF and SVG format are convertible to each other without data loss
          (font handling require more attention).

.. note:: The |Inkscape|_ free software is able to import a lot of file formats like PDF, DXF and to save it to SVG.

Pattern Format Compatibility
----------------------------

For more details on pattern format support, see :

.. toctree::
  :maxdepth: 1

  valentina-compatibility/index.rst

Digitalisation
==============

* digitalise pattern acquired with a camera **ACTUALLY NOT RELEASED WITH OPEN SOURCE LICENCE**
