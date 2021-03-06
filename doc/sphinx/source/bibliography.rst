.. _bibliography-page:

==============
 Bibliography
==============

.. related-projects vs bibliography : ???

Geometry Engine
---------------

* `CGAL Computational Geometry Algorithms Library <http://www.cgal.org>`_

  **A major library for computational geometry algorithms.**

.. rst hack

* `lib2geom <https://gitlab.com/inkscape/lib2geom>`_ is a C++ 2D geometry library geared towards
  robust processing of computational geometry data associated with vector graphics.  It is
  dual-licensed under LGPL 2.1 and MPL 1.1.  The library is descended from a set of geometric
  routines present in **Inkscape**. **Due to this legacy, not all parts of the API form a coherent
  whole.**

  **Interesting and coded by peoples having good mathematical skills, but this project lacks a good
  documentation, references, and code cleanup.**

  It implements polynomial s-power basis, cf. `Javier Sánchez-Reyes publications
  <https://dblp.uni-trier.de/pers/hd/s/S=aacute=nchez=Reyes:Javier>`_.

.. J. Sánchez-Reyes. The symmetric analogue of the polynomial power basis. ACM Trans. Graph.,
   16(3):319–357, 1997.

.. J. Sánchez-reyes. Inversion approximations for functions via s-power series. Comput. Aided
   Geom. Des., 18(6):587–608, 2001.

.. J. Sánchez-Reyes and J. M. Chacón. s-power series: an alternative to poisson expansions for
   representing analytic functions. Comput. Aided Geom. Des., 22(2):103–119, 2005.

.. Javier Sánchez-Reyes. Applications of the polynomial s-power basis in geometry processing. ACM
   Trans. Graph., 19(1):27–55, 2000.

* `David Eberly Geometric Tools web site <https://www.geometrictools.com/index.html>`_

  **A good source of documentation on geometry on the web.**

.. rst hack

* `Clipper <http://www.angusj.com/delphi/clipper.php>`_ an open source library for clipping and
  offsetting lines and polygons.  The Clipper library performs line & polygon clipping -
  intersection, union, difference & exclusive-or, and line & polygon offsetting. The library is
  based on Vatti's clipping algorithm.  Licensed under Boost Software License.  Authored by Angus
  Johnson in 2014.

  **A major clipping library.**

.. rst hack

* `Open Cascade Framework <https://www.opencascade.com>`_ an open-source software development
  platform for 3D CAD, CAM, CAE.

  **A major framework for CAD.**

.. rst hack

* `Shapely <https://github.com/Toblerity/Shapely>`_ is a BSD-licensed Python package for
  manipulation and analysis of planar geometric objects.  It is based on the widely deployed
  **GEOS** and `JTS <https://locationtech.github.io/jts>`_ (from which GEOS
  is ported) libraries.  Shapely is not concerned with data formats or coordinate systems, but can
  be readily integrated with packages that are.

  * `Shapely Documentaion <https://shapely.readthedocs.io/en/latest>`_

.. rst hack

* `GEOS <http://trac.osgeo.org/geos>`_ — **the engine of PostGIS**

  * Geometries: Point, LineString, Polygon, MultiPoint, MultiLineString, MultiPolygon, GeometryCollection
  * Predicates: Intersects, Touches, Disjoint, Crosses, Within, Contains, Overlaps, Equals, Covers
  * Operations: Union, Distance, Intersection, Symmetric Difference, Convex Hull, Envelope, Buffer, Simplify, Polygon Assembly, Valid, Area, Length,
  * Prepared geometries (pre-spatially indexed)
  * STR spatial index
  * C and C++ API (C API gives long term ABI stability)
  * Thread safe (using the reentrant API)

JavaScript Vector Graphics Libraries
------------------------------------

* `Paper.js <http://paperjs.org>`_ is an open source vector graphics scripting framework that runs
  on top of the HTML5 Canvas. It offers a clean Scene Graph / Document Object Model and a lot of
  powerful functionality to create and work with vector graphics and bezier curves, all neatly
  wrapped up in a well designed, consistent and clean programming interface.

  **A major JavaScript implementation.**

  * `Example <http://paperjs.org/examples/>`_
  * `Reference Manual <http://paperjs.org/reference/global/>`_
  * `Source code <https://github.com/paperjs/paper.js>`_ 10k stars
  * http://assets.paperjs.org/boolean
  * `Revamp Boolean Operations #761 <https://github.com/paperjs/paper.js/issues/761>`_



.. `Two.js <https://two.js.org>`_ is a two-dimensional drawing api geared towards modern web
   browsers. It is renderer agnostic enabling the same api to draw in multiple contexts: svg,
   canvas, and webgl.
   https://github.com/jonobr1/two.js 6k stars

.. https://pixijs.io

.. https://www.createjs.com

.. https://fabricjs.com 12k stars

.. https://docs.google.com/spreadsheets/d/1JYEGMN2jJtmwyjB4DMw3uaYLVMkduf61suKpiOzo0hc/edit#gid=0

.. http://p5js.org a JavaScript port of Processing (in Java) for experimental works

.. http://dmitrybaranovskiy.github.io/raphael
   https://github.com/DmitryBaranovskiy/raphael 10k

.. http://snapsvg.io

.. https://threejs.org

.. https://github.com/andreaferretti/paths-js 1.5k
