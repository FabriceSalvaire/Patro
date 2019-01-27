.. include:: /abbreviation.txt

.. _bezier-geometry-ressources-page:

===============
 Bézier Curves
===============

.. contents:: :local:




Definitions
-----------

A Bézier curve is defined by a set of control points :math:`\mathbf{P}_0` through
:math:`\mathbf{P}_n`, where :math:`n` is called its order (:math:`n = 1` for linear, 2 for
quadratic, 3 for cubic etc.). The first and last control points are always the end points of the
curve;

In the following :math:`0 \le t \le 1` and :math:`u = 1 - t`



Linear Bézier Curves
--------------------

Given distinct points :math:`\mathbf{P}_0` and :math:`\mathbf{P}_1`, a linear Bézier curve is simply
a straight line between those two points. The curve is given by

.. math::
    \begin{align}
    \mathbf{B}(t) &= \mathbf{P}_0 + t (\mathbf{P}_1 - \mathbf{P}_0) \\[.5em]
                  &= (1-t) \mathbf{P}_0 + t \mathbf{P}_1 \\[.5em]
                  &= u \mathbf{P}_0 + t \mathbf{P}_1
    \end{align}

and is equivalent to linear interpolation.



Quadratic Bézier Curves
-----------------------

A quadratic Bézier curve is the path traced by the function :math:`\mathbf{B}(t)`, given points
:math:`\mathbf{P}_0`, :math:`\mathbf{P}_1`, and :math:`\mathbf{P}_2`,

.. math::
    \begin{align}
    \mathbf{B}(t) &= (1-t)[(1-t) \mathbf{P}_0 + t \mathbf{P}_1] + t [(1-t) \mathbf{P}_1 + t \mathbf{P}_2] \\[.5em]
                  &= u[u \mathbf{P}_0 + t \mathbf{P}_1] + t [u \mathbf{P}_1 + t \mathbf{P}_2]
    \end{align}

which can be interpreted as the linear interpolant of corresponding points on the linear Bézier
curves from :math:`\mathbf{P}_0` to :math:`\mathbf{P}_1` and from :math:`\mathbf{P}_1` to
:math:`\mathbf{P}_2` respectively.

Rearranging the preceding equation yields:

.. math::
    \begin{align}
    \mathbf{B}(t) &= (1-t)^2 \mathbf{P}_0 + 2(1-t)t \mathbf{P}_1 + t^2 \mathbf{P}_2 \\[.5em]
                  &= u^2 \mathbf{P}_0 + 2ut \mathbf{P}_1 + t^2 \mathbf{P}_2 \\[.5em]
                  &= (\mathbf{P}_0 - 2\mathbf{P}_1 + \mathbf{P}_2) t^2 +
                     2(-\mathbf{P}_0 + \mathbf{P}_1) t +
                     \mathbf{P}_0
    \end{align}

This can be written in a way that highlights the symmetry with respect to :math:`\mathbf{P}_1`:

.. math::
    \begin{align}
    \mathbf{B}(t) &= \mathbf{P}_1 + (1-t)^2 ( \mathbf{P}_0 - \mathbf{P}_1) + t^2 (\mathbf{P}_2 - \mathbf{P}_1) \\[.5em]
                  &= \mathbf{P}_1 + u^2 ( \mathbf{P}_0 - \mathbf{P}_1) + t^2 (\mathbf{P}_2 - \mathbf{P}_1)
    \end{align}

Which immediately gives the derivative of the Bézier curve with respect to `t`:

.. math::
    \begin{align}
    \mathbf{B}'(t) &= 2(1-t) (\mathbf{P}_1 - \mathbf{P}_0) + 2t (\mathbf{P}_2 - \mathbf{P}_1) \\[.5em]
                   &= 2 (\mathbf{P}_1 - \mathbf{P}_0) + 2(\mathbf{P}_0 - 2\mathbf{P}_1 + \mathbf{P}_2) t \\[.5em]
                   &= 2u (\mathbf{P}_1 - \mathbf{P}_0) + 2t (\mathbf{P}_2 - \mathbf{P}_1)
    \end{align}

from which it can be concluded that the tangents to the curve at :math:`\mathbf{P}_0` and
:math:`\mathbf{P}_2` intersect at :math:`\mathbf{P}_1`. As :math:`t` increases from 0 to 1, the
curve departs from :math:`\mathbf{P}_0` in the direction of :math:`\mathbf{P}_1`, then bends to
arrive at :math:`\mathbf{P}_2` from the direction of :math:`\mathbf{P}_1`.

The second derivative of the Bézier curve with respect to :math:`t` is

.. math::
    \mathbf{B}''(t) = 2 (\mathbf{P}_2 - 2 \mathbf{P}_1 + \mathbf{P}_0)



Cubic Bézier Curves
-------------------

Four points :math:`\mathbf{P}_0`, :math:`\mathbf{P}_1`, :math:`\mathbf{P}_2` and
:math:`\mathbf{P}_3` in the plane or in higher-dimensional space define a cubic Bézier curve.  The
curve starts at :math:`\mathbf{P}_0` going toward :math:`\mathbf{P}_1` and arrives at
:math:`\mathbf{P}_3` coming from the direction of :math:`\mathbf{P}_2`. Usually, it will not pass
through :math:`\mathbf{P}_1` or :math:`\mathbf{P}_2`; these points are only there to provide
directional information. The distance between :math:`\mathbf{P}_1` and :math:`\mathbf{P}_2`
determines "how far" and "how fast" the curve moves towards :math:`\mathbf{P}_1` before turning
towards :math:`\mathbf{P}_2`.

Writing :math:`\mathbf{B}_{\mathbf P_i,\mathbf P_j,\mathbf P_k}(t)` for the quadratic Bézier curve
defined by points :math:`\mathbf{P}_i`, :math:`\mathbf{P}_j`, and :math:`\mathbf{P}_k`, the cubic
Bézier curve can be defined as an affine combination of two quadratic Bézier curves:

.. math::
    \mathbf{B}(t) = (1-t) \mathbf{B}_{\mathbf P_0,\mathbf P_1,\mathbf P_2}(t) +
                        t \mathbf{B}_{\mathbf P_1,\mathbf P_2,\mathbf P_3}(t)

The explicit form of the curve is:

.. math::
    \begin{align}
    \mathbf{B}(t) &= (1-t)^3 \mathbf{P}_0 + 3(1-t)^2t \mathbf{P}_1 + 3(1-t)t^2 \mathbf{P}_2 + t^3\mathbf{P}_3 \\[.5em]
                  &= u^3 \mathbf{P}_0 + 3u^2t \mathbf{P}_1 + 3ut^2 \mathbf{P}_2 + t^3\mathbf{P}_3 \\[.5em]
                  &= (\mathbf{P}_3 - 3\mathbf{P}_2 + 3\mathbf{P}_1 - \mathbf{P}_0) t^3 +
                     3(\mathbf{P}_2 - 2\mathbf{P}_1 + \mathbf{P}_0) t^2 +
                     3(\mathbf{P}_1 - \mathbf{P}_0) t  +
                     \mathbf{P}_0
    \end{align}

For some choices of :math:`\mathbf{P}_1` and :math:`\mathbf{P}_2` the curve may intersect itself, or
contain a cusp.

The derivative of the cubic Bézier curve with respect to :math:`t` is

.. math::
    \begin{align}
    \mathbf{B}'(t) &= 3(1-t)^2 (\mathbf{P}_1 - \mathbf{P}_0) + 6(1-t)t (\mathbf{P}_2 - \mathbf{P}_1) + 3t^2 (\mathbf{P}_3 - \mathbf{P}_2) \\[.5em]
	           &= 3u^2 (\mathbf{P}_1 - \mathbf{P}_0) + 6ut (\mathbf{P}_2 - \mathbf{P}_1) + 3t^2 (\mathbf{P}_3 - \mathbf{P}_2)
    \end{align}

The second derivative of the Bézier curve with respect to :math:`t` is

.. math::
    \begin{align}
    \mathbf{B}''(t) &= 6(1-t) (\mathbf{P}_2 - 2 \mathbf{P}_1 + \mathbf{P}_0) +  6t (\mathbf{P}_3 - 2 \mathbf{P}_2 + \mathbf{P}_1) \\[.5em]
                    &= 6u (\mathbf{P}_2 - 2 \mathbf{P}_1 + \mathbf{P}_0) +  6t (\mathbf{P}_3 - 2 \mathbf{P}_2 + \mathbf{P}_1)
    \end{align}



Recursive definition
--------------------

A recursive definition for the Bézier curve of degree :math:`n` expresses it as a point-to-point
linear combination of a pair of corresponding points in two Bézier curves of degree :math:`n-1`.

Let :math:`\mathbf{B}_{\mathbf{P}_0\mathbf{P}_1\ldots\mathbf{P}_n}` denote the Bézier curve
determined by any selection of points :math:`\mathbf{P}_0`, :math:`\mathbf{P}_1`, :math:`\ldots`,
:math:`\mathbf{P}_{n-1}`.

The recursive definition is

.. math::
    \begin{align}
    \mathbf{B}_{\mathbf{P}_0}(t) &= \mathbf{P}_0 \\[1em]
    \mathbf{B}(t) &= \mathbf{B}_{\mathbf{P}_0\mathbf{P}_1\ldots\mathbf{P}_n}(t) \\[.5em]
                  &= (1-t) \mathbf{B}_{\mathbf{P}_0\mathbf{P}_1\ldots\mathbf{P}_{n-1}}(t) +
                         t \mathbf{B}_{\mathbf{P}_1\mathbf{P}_2\ldots\mathbf{P}_n}(t)
    \end{align}

The formula can be expressed explicitly as follows:

.. math::
    \begin{align}
    \mathbf{B}(t) &= \sum_{i=0}^n b_{i,n}(t) \mathbf{P}_i \\[.5em]
                  &= \sum_{i=0}^n {n\choose i}(1-t)^{n - i}t^i \mathbf{P}_i \\[.5em]
                  &= (1-t)^n \mathbf{P}_0 +
                     {n\choose 1}(1-t)^{n - 1}t \mathbf{P}_1 +
                     \cdots +
                     {n\choose n - 1}(1-t)t^{n - 1} \mathbf{P}_{n - 1} +
                     t^n \mathbf{P}_n
    \end{align}

where :math:`b_{i,n}(t)` are the Bernstein basis polynomials of degree :math:`n` and :math:`n
\choose i` are the binomial coefficients.



.. _bezier-curve-degree-elevation-section:

Degree elevation
----------------

A Bézier curve of degree :math:`n` can be converted into a Bézier curve of degree :math:`n + 1` with
the same shape.

To do degree elevation, we use the equality

.. math::
       \mathbf{B}(t) = (1-t) \mathbf{B}(t) + t \mathbf{B}(t)

Each component :math:`\mathbf{b}_{i,n}(t) \mathbf{P}_i` is multiplied by :math:`(1-t)` and
:math:`t`, thus increasing a degree by one, without changing the value.

For arbitrary :math:`n`, we have

.. math::
    \begin{align}
    \mathbf{B}(t) &= (1-t) \sum_{i=0}^n \mathbf{b}_{i,n}(t) \mathbf{P}_i +
                           t \sum_{i=0}^n \mathbf{b}_{i,n}(t) \mathbf{P}_i \\[.5em]
                  &= \sum_{i=0}^n \frac{n + 1 - i}{n + 1} \mathbf{b}_{i, n + 1}(t) \mathbf{P}_i +
                     \sum_{i=0}^n \frac{i + 1}{n + 1} \mathbf{b}_{i + 1, n + 1}(t) \mathbf{P}_i \\[.5em]
                  &= \sum_{i=0}^{n + 1} \mathbf{b}_{i, n + 1}(t)
                                        \left(\frac{i}{n + 1}         \mathbf{P}_{i - 1} +
                                              \frac{n + 1 - i}{n + 1} \mathbf{P}_i\right) \\[.5em]
                  &= \sum_{i=0}^{n + 1} \mathbf{b}_{i, n + 1}(t) \mathbf{P'}_i
    \end{align}

Therefore the new control points are

.. math::
      \mathbf{P'}_i = \frac{i}{n + 1} \mathbf{P}_{i - 1} + \frac{n + 1 - i}{n + 1} \mathbf{P}_i

It introduces two arbitrary points :math:`\mathbf{P}_{-1}` and :math:`\mathbf{P}_{n+1}` which are
cancelled in :math:`\mathbf{P'}_i`.

Example for a quadratic Bézier curve:

.. math::
   \begin{align}
   \mathbf{P'}_0 &= \mathbf{P}_0 \\[.5em]
   \mathbf{P'}_1 &= \mathbf{P}_0 + \frac{2}{3} (\mathbf{P}_1 - \mathbf{P}_0) \\[.5em]
   \mathbf{P'}_1 &= \mathbf{P}_2 + \frac{2}{3} (\mathbf{P}_1 - \mathbf{P}_2) \\[.5em]
   \mathbf{P'}_2 &= \mathbf{P}_2
   \end{align}



Matrix Forms
------------

.. math::
     \mathbf{B}(t) = \mathbf{Transformation} \; \mathbf{Control} \; \mathbf{Basis} \; \mathbf{T}(t)

.. math::
     \begin{align}
     \mathbf{B^2}(t) &= \mathbf{Tr}
                        \begin{pmatrix}
                          P_{1x} & P_{2x} & P_{3x} \\
                          P_{1y} & P_{2x} & P_{3x} \\
                          1      & 1      & 1
                        \end{pmatrix}
                        \begin{pmatrix}
                          1 & -2 &  1 \\
                          0 &  2 & -2 \\
                          0 &  0 &  1
                        \end{pmatrix}
                        \begin{pmatrix}
                          1 \\
                          t \\
                          t^2
                        \end{pmatrix} \\[1em]
     \mathbf{B^3}(t) &= \mathbf{Tr}
                        \begin{pmatrix}
                          P_{1x} & P_{2x} & P_{3x} & P_{4x} \\
                          P_{1y} & P_{2x} & P_{3x} & P_{4x} \\
                          0      & 0      & 0      & 0      \\
                          1      & 1      & 1      & 1
                        \end{pmatrix}
                        \begin{pmatrix}
                          1 & -3 &  3 & -1 \\
                          0 &  3 & -6 &  3 \\
                          0 &  0 &  3 & -3 \\
                          0 &  0 &  0 &  1
                        \end{pmatrix}
                        \begin{pmatrix}
                          1 \\
                          t \\
                          t^2 \\
                          t^3
                        \end{pmatrix}
    \end{align}

.. B(t) = P0 (1 - 2t + t^2) +
          P1 (    2t - t^2) +
          P2           t^2



Symbolic Calculation
--------------------

.. code-block:: py3

    >>> from sympy import *

    >>> P0, P1, P2, P3, P, t = symbols('P0 P1 P2 P3 P t')

    >>> B2 = (1-t)*((1-t)*P0 + t*P1) + t*((1-t)*P1 + t*P2)
    >>> collect(expand(B2), t)
    P0 + t**2*(P0 - 2*P1 + P2) + t*(-2*P0 + 2*P1)

    >>> B2_012 = (1-t)*((1-t)*P0 + t*P1) + t*((1-t)*P1 + t*P2)
    >>> B2_123 = (1-t)*((1-t)*P1 + t*P2) + t*((1-t)*P2 + t*P3)
    >>> B3 = (1-t)*B2_012 + t*B2_123
    >>> collect(expand(B3), t)
    P0 + t**3*(-P0 + 3*P1 - 3*P2 + P3) + t**2*(3*P0 - 6*P1 + 3*P2) + t*(-3*P0 + 3*P1)

    # Compute derivative
    >>> B2p = collect(simplify(B2.diff(t)), t)
    -2*P0 + 2*P1 + t*(2*P0 - 4*P1 + 2*P2)

    >>> B3p = collect(simplify(B3.diff(t)), t)
    -3*P0 + 3*P1 + t**2*(-3*P0 + 9*P1 - 9*P2 + 3*P3) + t*(6*P0 - 12*P1 + 6*P2)



.. _bezier-curve-length-section:

Curve Length
------------

Reference

  * http://www.gamedev.net/topic/551455-length-of-a-generalized-quadratic-bezier-curve-in-3d
  * Dave Eberly Posted October 25, 2009

The quadratic Bézier is

.. math::
    \mathbf{B}(t) = (1-t)^2 \mathbf{P}_0 + 2t(1-t) \mathbf{P}_1 + t^2 \mathbf{P}_2

The derivative is

.. math::
    \mathbf{B'}(t) = -2(1-t) \mathbf{P}_0 + (2-4t) \mathbf{P}_1 + 2t \mathbf{P}_2

The length of the curve for :math:`0 <= t <= 1` is

.. math::
    \int_0^1 \sqrt{(x'(t))^2 + (y'(t))^2} dt

The integrand is of the form :math:`\sqrt{c t^2 + b t + a}`

You have three separate cases: :math:`c = 0`, :math:`c > 0`, or :math:`c < 0`.

The case :math:`c = 0` is easy.

For the case :math:`c > 0`, an antiderivative is

.. math::
    \frac{2ct + b}{4c} \sqrt{ct^2 + bt + a}  +  \frac{k}{2\sqrt{c}} \ln{\left(2\sqrt{c(ct^2 + bt + a)} + 2ct + b\right)}

For the case :math:`c < 0`, an antiderivative is

.. math::
    \frac{2ct + b}{4c} \sqrt{ct^2 + bt + a}  -  \frac{k}{2\sqrt{-c}} \arcsin{\frac{2ct + b}{\sqrt{-q}}}

where :math:`k = \frac{4c}{q}` with :math:`q = 4ac - b^2`.



.. _bezier-curve-flatness-section:

Determine the curve flatness
----------------------------

Reference

  * Kaspar Fischer and Roger Willcocks  http://hcklbrrfnn.files.wordpress.com/2012/08/bez.pdf
  * PostScript Language Reference. Addison- Wesley, third edition, 1999

*flatness* is the maximum error allowed for the straight line to deviate from the curve.

Algorithm

We define the flatness of the curve as the argmax of the distance from the curve to the
line passing by the start and stop point.

:math:`\mathrm{flatness} = argmax(d(t))` for :math:`t \in [0, 1]` where :math:`d(t) = \vert B(t) - L(t) \vert`

The line equation is

.. math::
    L = (1-t) \mathbf{P}_0 + t \mathbf{P}_1

Let

.. math::
    \begin{align}
    U &= 3\mathbf{P}_1 - 2\mathbf{P}_0 - \mathbf{P}_3 \\[.5em]
    V &= 3\mathbf{P}_2 - \mathbf{P}_0 - 2\mathbf{P}_3
    \end{align}

The distance is

.. math::
    \begin{align}
    d(t) &= (1-t)^2 t \left(3\mathbf{P}_1 - 2\mathbf{P}_0 - \mathbf{P}_3\right)  +  (1-t) t^2 (3\mathbf{P}_2 - \mathbf{P}_0 - 2\mathbf{P}_3) \\[.5em]
         &= (1-t)^2 t u  +  (1-t) t^2 v
    \end{align}

The square of the distance is

.. math::
    d(t)^2 = (1-t)^2 t^2 (((1-t) U_x + t V_x)^2 + ((1-t) U_y + t V_y)^2

From

.. math::
    \begin{align}
    argmax((1-t)^2 t^2)   &= \frac{1}{16} \\[.5em]
    argmax((1-t) a + t b) &= argmax(a, b)
    \end{align}

we can express a bound on the flatness

.. math::
    \mathrm{flatness}^2 = argmax(d(t)^2) \leq \frac{1}{16} (argmax(U_x^2, V_x^2) + argmax(U_y^2, V_y^2))

Thus an upper bound of :math:`16\,\mathrm{flatness}^2` is

.. math::
    argmax(U_x^2, V_x^2) + argmax(U_y^2, V_y^2)



.. _bezier-curve-line-intersection-section:

Intersection of Bézier Curve with a Line
----------------------------------------

Algorithm

  * Apply a transformation to the curve that maps the line onto the X-axis.
  * Then we only need to test the Y-values for a zero.



.. _bezier-curve-closest-point-section:

Closest Point
-------------

Reference

  * https://hal.archives-ouvertes.fr/inria-00518379/document
    Improved Algebraic Algorithm On Point Projection For Bézier Curves
    Xiao-Diao Chen, Yin Zhou, Zhenyu Shu, Hua Su, Jean-Claude Paul

Let a point :math:`\mathbf{P}` and the closest point :math:`\mathbf{B}(t)` on the curve, we have this
condition:

.. math::
    (\mathbf{P} - \mathbf{B}(t)) \cdot \mathbf{B}'(t) = 0 \\[.5em]
    \mathbf{P} \cdot \mathbf{B}'(t) - \mathbf{B}(t) \cdot \mathbf{B}'(t) = 0

Quadratic Bézier Curve
~~~~~~~~~~~~~~~~~~~~~~

Let

.. math::
    \begin{align}
       \mathbf{A} &= \mathbf{P}_1 - \mathbf{P}_0 \\[.5em]
       \mathbf{B} &= \mathbf{P}_2 - \mathbf{P}_1 -\mathbf{A} \\[.5em]
       \mathbf{M} &= \mathbf{P}_0 - \mathbf{P}
    \end{align}

We have

.. math::
    \mathbf{B}'(t) = 2(\mathbf{A} + \mathbf{B} t)

.. factorisation
   (P0 - 2*P1 + P2)**2 * t**3
   3*(P1 - P0)*(P0 - 2*P1 + P2) * t**2
   ...
   (P0 - P)*(P1 - P0)

The condition can be expressed as

.. math::
    \mathbf{B}^2 t^3 + 3\mathbf{A}\mathbf{B} t^2 + (2\mathbf{A}^2 + \mathbf{M}\mathbf{B}) t + \mathbf{M}\mathbf{A} = 0

.. code-block:: py3

    >>> C = collect(expand((P*B2p - B2*B2p)/-2), t)
    P*P0 - P*P1 - P0**2 + P0*P1 +
    t**3 * (P0**2 - 4*P0*P1 + 2*P0*P2 + 4*P1**2 - 4*P1*P2 + P2**2) +
    t**2 * (-3*P0**2 + 9*P0*P1 - 3*P0*P2 - 6*P1**2 + 3*P1*P2) +
    t    * (-P*P0 + 2*P*P1 - P*P2 + 3*P0**2 - 6*P0*P1 + P0*P2 + 2*P1**2)
    >>> A = P1 - P0
        B = P2 - P1 - A
        M = P0 - P
    >>> C2 = B**2 * t**3 + 3*A*B * t**2 + (2*A**2 + M*B) * t + M*A
    >>> expand(C - C2)
    0

Cubic Bézier Curve
~~~~~~~~~~~~~~~~~~

Let

.. math::
    \begin{align}
     n &= \mathbf{P}_3 - 3\mathbf{P}_2 + 3\mathbf{P}_1 - \mathbf{P}_0 \\[.5em]
     r &= 3(\mathbf{P}_2 - 2\mathbf{P}_1 + \mathbf{P}_0 \\[.5em]
     s &= 3(\mathbf{P}_1 - \mathbf{P}_0) \\[.5em]
     v &= \mathbf{P}_0
     \end{align}

We have

.. math::
    \begin{align}
    \mathbf{B}^3(t)  &= nt^3 + rt^2 + st + v \\[.5em]
    \mathbf{B}'(t) &= 3nt^2 + 2rt + s
    \end{align}

    .. n = P3 - 3*P2 + 3*P1 - P0
   r = 3*(P2 - 2*P1 + P0
   s = 3*(P1 - P0)
   v = P0

.. code-block:: py3

    >>> n, r, s, v = symbols('n r s v')
    >>> B3 = n*t**3 + r*t**2 + s*t + v
    >>> B3p = simplify(B3.diff(t))
    >>> C = collect(expand((P*B3p - B3*B3p)), t)
    -3*n**2 * t**5 +
    -5*n*r * t**4 +
    -2*(2*n*s + r**2) * t**3 +
    3*(P*n - n*v - r*s) * t**2 +
    (2*P*r - 2*r*v - s**2) * t +
    P*s - s*v
