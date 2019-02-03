.. include:: /abbreviation.txt

.. _conic-geometry-ressources-page:

=======
 Conic
=======

----------------------
Valentina Requirements
----------------------

  * circle with angular domain
  * circle with start angle and arc length
  * curvilinear distance on circle
  * line-circle intersection
  * circle-circle intersection
  * point constructed from a virtual circle and a point on a tangent : right triangle
  * point from tangent circle and segment ???
  * ellipse with angular domain and rotation

------
Circle
------

Intersection of a Circle and a Segment
--------------------------------------

Reference

  * http://mathworld.wolfram.com/Circle-LineIntersection.html
  * Rhoad et al. 1984, p. 429
  * Rhoad, R.; Milauskas, G.; and Whipple, R. Geometry for Enjoyment and Challenge,
  * rev. ed. Evanston, IL: McDougal, Littell & Company, 1984.

System of equations

.. math::
   \begin{align}
   x^2 + y^2 &= r^2 \\
   dx \times y &= dy \times x - D
   \end{align}

where

.. math::
   \begin{align}
    dx &= x1 - x0 \\
    dy &= y1 - y0 \\
    D  &= x0 \times y1 - x1 \times y0
   \end{align}

Intersection of a Circle and a Circle
--------------------------------------

Reference

  * http://mathworld.wolfram.com/Circle-CircleIntersection.html

System of equations

.. math::
    \begin{align}
    x^2     + y^2 &= R^2 \\
    (x-d)^2 + y^2 &= r^2
   \end{align}

Bezier Approximation
--------------------

Reference

  * http://spencermortensen.com/articles/bezier-circle/
  * http://www.spaceroots.org/documents/ellipse/index.html

.. see also https://pomax.github.io/bezierinfo/#circles

**First approximation:**

  #. The endpoints of the cubic Bézier curve must coincide with the endpoints of the circular arc,
     and their first derivatives must agree there.
  #. The midpoint of the cubic Bézier curve must lie on the circle.

A Cubic Bézier curve is parameterised by

.. math::
    \mathbf{B}(t) = (1-t)^3  \mathbf{P}_0 + 3(1-t)^2t  \mathbf{P}_1 + 3(1-t)t^2  \mathbf{P}_2 + t^3  \mathbf{P}_3

and its first derivative by

.. math::
    \begin{align}
    \mathbf{B}'(t) &= 3(1-t)^2 (\mathbf{P}_1 - \mathbf{P}_0) + 6(1-t)t (\mathbf{P}_2 - \mathbf{P}_1) + 3t^2 (\mathbf{P}_3 - \mathbf{P}_2) \\[.5em]
    \mathbf{B}'(t=0) &= 3 (\mathbf{P}_1 - \mathbf{P}_0) \\
    \mathbf{B}'(t=1) &= 3 (\mathbf{P}_3 - \mathbf{P}_2)
    \end{align}

The first constraint yields for an unitary circle:

.. math::
    \begin{align}
    \mathbf{P}_0 &= (0, 1) \\
    \mathbf{P}_1 &= (c, 1) \\
    \mathbf{P}_2 &= (1, c) \\
    \mathbf{P}_3 &= (1, 0)
    \end{align}

The second constraint provides the value of :math:`c = \frac{4}{3} (\sqrt{2} - 1) \approx 0.552`

The maximum radial drift is 0.027253 % with this approximation.

In this approximation, the Bézier curve always falls outside the circle, except momentarily when it
dips in to touch the circle at the midpoint and endpoints.

**Better approximation:**

2) The maximum radial distance from the circle to the Bézier curve must be as small as possible.

The first constraint yields the parametric form of the Bézier curve :math:`\mathbf{B}(t) = (x,y)`:

.. math::
    \begin{align}
    x(t) &= 3c(1-t)^2t + 3(1-t)t^2 + t^3 \\
    y(t) &= 3ct^2(1-t) + 3t(1-t)^2 + (1-t)^3
    \end{align}

The radial distance from the arc to the Bézier curve is:

.. math::
    d(t) = \sqrt{x^2 + y^2} - 1

The Bézier curve touches the right circular arc at its initial endpoint, then drifts outside the
arc, inside, outside again, and finally returns to touch the arc at its endpoint.

.. The roots of `d` are: :math:`0, 3c \pm \frac{\sqrt{-9c^2 - 24c + 16} - 2}{6c - 4}, 1`

This radial distance function, d(t), has minima at :math:`t = 0, \frac{1}{2}, 1`, and maxima at
:math:`t = \frac{1}{2} \pm \frac{\sqrt{12 - 20c - 3c^2}}{4 - 6c}`

Because the Bézier curve is symmetric about :math:`t = \frac{1}{2}`, the two maxima have the same
value. The radial deviation is minimized when the magnitude of this maximum is equal to the
magnitude of the minimum at :math:`t = \frac{1}{2}`.

This gives the ideal value for c = 0.551915024494

The maximum radial drift is 0.019608 % with this approximation.

A complete unit circle is approximated by these fours curves:

  * :math:`\mathbf{P}_0 = (0,1)   \quad\mathbf{P}_1 = (c,1)   \quad\mathbf{P}_2 = (1,c)   \quad\mathbf{P}_3 = (1,0)`
  * :math:`\mathbf{P}_0 = (1,0)   \quad\mathbf{P}_1 = (1,-c)  \quad\mathbf{P}_2 = (c,-1)  \quad\mathbf{P}_3 = (0,-1)`
  * :math:`\mathbf{P}_0 = (0,-1)  \quad\mathbf{P}_1 = (-c,-1) \quad\mathbf{P}_2 = (-1,-c) \quad\mathbf{P}_3 = (-1,0)`
  * :math:`\mathbf{P}_0 = (-1,0)  \quad\mathbf{P}_1 = (-1,c)  \quad\mathbf{P}_2 = (-c,1)  \quad\mathbf{P}_3 = (0,1)`

-------
Ellipse
-------

A general ellipse in 2D is represented by a center point `C`, an orthonormal set of
axis-direction vectors :math:`{U_0 , U_1 }`, and associated extents :math:`e_i` with :math:`e_0
\ge e_1 > 0`. The ellipse points are

.. math::
    \begin{equation}
    P = C + x_0 U_0 + x_1 U_1
    \end{equation}

where

.. math::
    \begin{equation}
    \left(\frac{x_0}{e_0}\right)^2 + \left(\frac{x_1}{e_1}\right)^2 = 1
    \end{equation}

If :math:`e_0 = e_1`, then the ellipse is a circle with center `C` and radius :math:`e_0`.

The orthonormality of the axis directions and Equation (1) imply :math:`x_i = U_i \dot (P −
C)`. Substituting this into Equation (2) we obtain

.. math::
    (P − C)^T M (P − C) = 1

where :math:`M = R D R^T`, `R` is an orthogonal matrix whose columns are :math:`U_0` and
:math:`U_1` , and `D` is a diagonal matrix whose diagonal entries are :math:`1/e_0^2` and
:math:`1/e_1^2`.

An ellipse can also be parameterised by an angle :math:`\theta`

.. math::
    \begin{pmatrix} x \\ y \end{pmatrix} =
    \begin{bmatrix}
    \cos\phi & \sin\phi \\
    -\sin\phi & \cos\phi
    \end{bmatrix}
    \begin{pmatrix} r_x \cos\theta \\ r_y \sin\theta \end{pmatrix}
    + \begin{pmatrix} C_x \\ C_y \end{pmatrix}

where :math:`\phi` is the angle from the x-axis, :math:`r_x` is the semi-major and :math:`r_y`
semi-minor axes.
