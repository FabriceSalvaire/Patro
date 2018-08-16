==========
 Features
==========

h2. Geometry Engine

h3. Vector

* dimension: 2D
* type: int, float
* normalisation
* homogeneous coordinate (x, y, w)
* math operations: + - * /
* equality test: == !=
* magnitude
* angle, tan, cos, sin
* rotation, normal, parity
* dot, cross
* geometric tests: parallel, orthogonal
* projection

h3. Transformation

* identity
* rotation, rotation at
* scale
* parity, x/y reflection
* translation
* composition

h3. Line

* dimension: 2D
* interpolation
* geometric tests: parallel, orthogonal
* shifted parallel line
* orthogonal line
* line intersection
* projection of a point
* distance to line

h3. Segment

* dimension: 2D
* length
* middle
* interpolation
* segment intersection test

h3. Triangle

* triangle orientation defined by three points : CW, CCW, degenerated

h3. Bezier Curve

h4. Quadratic Bezier Curve (defined by 3 points)

* dimension: 2D
* bounding box
* length
* interpolation
* split
* tangent and normal at extremity
* tangent at t

h4. Cubic Bezier Curve (defined by 4 points)

* dimension: 2D
* bounding box
* length
* interpolation
* split
* tangent extremity
* tangent at t

h3. Circle

* dimension: 2D

h3. Conic Curve

* dimension: 2D
* eccentricity
* matrix

h2. Pattern Engine

See in Valentina source code
* src/libs/ifc/schema/pattern/v0.6.2.xsd
* src/libs/ifc/xml/vpatternconverter.cpp
Notice XSD is not sufficient, there is no complete documentation of the Valentina format.

| point/alongLine                  | Y | Construct a point from two points defining a direction and a length |
| point/bisector                   | N |
| point/curveIntersectAxis         | N |
| point/cutArc                     | N |
| point/cutSpline                  | N |
| point/cutSplinePath              | N |
| point/endLine                    | Y | Construct a point from a base point and a vector defined by an angle and a length |
| point/height                     | N |
| point/lineIntersect              | Y | Construct a point from the intersection of two segments defined by four points |
| point/lineIntersectAxis          | N |
| point/normal                     | Y | Construct a point at a distance of the first point on the rotated normal of a line defined by two points |
| point/pointFromArcAndTangent     | N |
| point/pointFromCircleAndTangent  | N |
| point/pointOfContact             | N |
| point/pointOfIntersection        | Y | Construct a point from the x coordinate of a fist point and the y coordinate of a second point |
| point/pointOfIntersectionArcs    | N |
| point/pointOfIntersectionCircles | N |
| point/pointOfIntersectionCurves  | N |
| point/shoulder                   | N |
| point/single                     | Y | Construct a point from coordinate |
| point/triangle                   | N |
| point/trueDarts                  | N |
|                                  |   |
| line                             | Y | Construct a line defined by two points |
|                                  |   |
| spline/cubicBezier               | N |
| spline/cubicBezierPath           | N |
| spline/pathInteractive           | N |
| spline/simpleInteractive         | Y | Construct a quadratic Bezier curve from two extremity points and two control points |
|                                  |   |
| arc/arcWithLength                | N |
| arc/simple                       | N |
|                                  |   |
| elArc/simple                     | N |
|                                  |   |
| operation/flippingByAxis         | N |
| operation/flippingByLine         | N |
| operation/moving                 | N |
| operation/rotation               | N |

h2. Graphic Engine

h3. File Formats
