.. include:: abbreviation.txt

.. _features-page:

==========
 Features
==========

Patro implements several components:

* a 2D Geometry Engine
* a Pattern Engine
* a Graphic Engine to export drawing to screen display, SVG, PDF and DXF file
* a submodule to read/write SVG file
* import/export of the |Valentina|_ file format
* import of SVG pattern (as well as PDF using a conversion tools like |Inkscape|_)
* digitalisation of patterns acquired with a camera **ACTUALLY NOT RELEASED WITH OPEN SOURCE LICENCE**

.. note:: Patro is just a core engine actually. It doesn't implement a full featured GUI similar to
          |Valentina|_.

.. note:: Patro doesn't implement 3D feature actually, like automatic clothe fitting on avatar and
          tension map.

Geometry Engine
===============

The geometry engine implements:

* 2D vector and usual transformations
* usual 2D primitives:

 * point, segment, line, polyline
 * triangle, rectangle, polygon
 * circle and ellipse
 * quadratic and cubic Bézier curve
 * B-spline curve
 * path made of linear segments with an optional bulge at breaks, as well as quadratic and cubic
   Bézier curve segments.

* perimeter and area
* primitive intersection
* thanks to |Sympy|_, Patro could implement symbolic computations when it is feasible

Pattern Engine
==============

* Measurements can be imported from Valentina *.vit* or a YAML file.  We can merge several files to
  a measurement set.
* Measurements are lazily evaluated using |Sympy|_ symbolic computation, which means we can compute
  exact values and the order of definition doesn't matter.

Graphic Engine
==============

Patro features a basic |Qt|_ user interface which can display a graphic scene and features item
selection so as to provide the minimum to work with.

The graphic engine implement a 2D graphic scene which is rendered by a painter.  A scene contains
graphic items like text, image line, circle and Bézier curve.

A painter is responsible to render the scene on the screen or a graphic file format. The graphic
engine is able to render on the following:

* show drawing on screen with : |Matplotlib|_, |Qt|_
* export drawing to : SVG, PDF, DXF, LaTeX |Tikz|_
* export tiled pattern on A4 sheets : PDF, LaTeX |Tikz|_

.. duplicated note

.. note:: PDF and SVG format are convertible to each other without data loss
          (font handling require more attention).

.. note:: The |Inkscape|_ free software is able to import from / export to a lot of file formats
          like SVG, PDF, DXF and to render the drawing to an image format.  This job can be done in
          batch from command line.

Also the graphic engine is able to render a DXF made of these graphic items: line, circle, arc,
ellipse, lwpolyline and spline.

For expert, the LaTeX output can be used to modify the drawing using the power of the |Tikz|_ (PGF)
graphic package.

Implementation details:

* SVG can be rendered using the SVG and Qt painter
* PDF export is implemented with the help of the |Reportlab|_ package
* DXF import/export is implemented with the help of the |ezdxf|_ package of `Manfred Moitzi
  <https://github.com/mozman>`_

Pattern Format Support
======================

* |Valentina|_ format: read/write *.val* and *.vit* file, but partially implemented, cf. supra for details
* import pattern from SVG and DXF (**partially implemented**)

.. note:: PDF and SVG format are convertible to each other without data loss
          (font handling require more attention).

.. note:: The |Inkscape|_ free software is able to import a lot of file formats like PDF, DXF and to
          save it to SVG.

Pattern Format Compatibility
----------------------------

For more details on pattern format support, see :

.. toctree::
  :maxdepth: 1

  valentina-compatibility/index.rst

Digitalisation
==============

* digitalise pattern acquired with a camera **ACTUALLY NOT RELEASED WITH OPEN SOURCE LICENCE**
