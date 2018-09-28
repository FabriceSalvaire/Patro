.. _valentina-compatibility-page:

=========================
 Valentina Compatibility
=========================

.. warning:: To be completed

To learn more on Valentina format, see the source code:

* src/libs/ifc/schema/pattern/v0.6.2.xsd
* src/libs/ifc/xml/vpatternconverter.cpp

Notice the XSD is not sufficient, there is no complete documentation of the Valentina format.

Math Expressions
================

`QMuParser <http://beltoforion.de/article.php?a=muparser>`_ expressions are translated to Python and evaluated on the fly.

* ...

Measurements
============

Calculations
============

=================================== === ========================================================================================================================
 Feature                                 Description
=================================== === ========================================================================================================================
arc/arcWithLength                    N
arc/simple                           N
elArc/simple                         N
line                                 Y    Construct a line defined by two points
operation/flippingByAxis             N
operation/flippingByLine             N
operation/moving                     N
operation/rotation                   N
point/alongLine                      Y    Construct a point from two points defining a direction and a length
point/bisector                       N
point/curveIntersectAxis             N
point/cutArc                         N
point/cutSpline                      N
point/cutSplinePath                  N
point/endLine                        Y    Construct a point from a base point and a vector defined by an angle and a length
point/height                         N
point/lineIntersect                  Y    Construct a point from the intersection of two segments defined by four points
point/lineIntersectAxis              N
point/normal                         Y    Construct a point at a distance of the first point on the rotated normal of a line defined by two points
point/pointFromArcAndTangent         N
point/pointFromCircleAndTangent      N
point/pointOfContact                 N
point/pointOfIntersection            Y    Construct a point from the x coordinate of a fist point and the y coordinate of a second point
point/pointOfIntersectionArcs        N
point/pointOfIntersectionCircles     N
point/pointOfIntersectionCurves      N
point/shoulder                       N
point/single                         Y    Construct a point from coordinate
point/triangle                       N
point/trueDarts                      N
spline/cubicBezier                   N
spline/cubicBezierPath               N
spline/pathInteractive               N
spline/simpleInteractive             Y    Construct a quadratic Bezier curve from two extremity points and two control points
=================================== === ========================================================================================================================

Graphic Properties
==================

* line styles
* colors

Detail
======

* ...

Valentina File Examples
=======================

Measurements .vit Example
-------------------------

.. literalinclude:: example.vit
    :language: xml

Pattern .val Example
--------------------

.. literalinclude:: operations-demo.val
    :language: xml

.. literalinclude:: detail-demo.val
    :language: xml
