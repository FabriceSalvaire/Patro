.. include:: ../../abbreviation.txt

.. _bezier-geometry-ressources-page:

===============
 Bézier Curves
===============

Definitions
-----------

A Bézier curve is defined by a set of control points :math:`\mathbf{P}_0` through
:math:`\mathbf{P}_n`, where :math:`n` is called its order (:math:`n = 1` for linear, 2 for
quadratic, 3 for cubic etc.). The first and last control points are always the end points of the
curve;

In the following :math:`0 \le t \le 1`.

Linear Bézier Curves
---------------------

Given distinct points :math:`\mathbf{P}_0` and :math:`\mathbf{P}_1`, a linear Bézier curve is simply
a straight line between those two points. The curve is given by

.. math::
    \begin{align}
    \mathbf{B}(t) &= \mathbf{P}_0 + t (\mathbf{P}_1 - \mathbf{P}_0) \\
                  &= (1-t) \mathbf{P}_0 + t \mathbf{P}_1
    \end{align}

and is equivalent to linear interpolation.

Quadratic Bézier Curves
-----------------------

A quadratic Bézier curve is the path traced by the function :math:`\mathbf{B}(t)`, given points
:math:`\mathbf{P}_0`, :math:`\mathbf{P}_1`, and :math:`\mathbf{P}_2`,

.. math::
    \mathbf{B}(t) = (1 - t)[(1 - t) \mathbf{P}_0 + t \mathbf{P}_1] + t [(1 - t) \mathbf{P}_1 + t \mathbf{P}_2]

which can be interpreted as the linear interpolant of corresponding points on the linear Bézier
curves from :math:`\mathbf{P}_0` to :math:`\mathbf{P}_1` and from :math:`\mathbf{P}_1` to
:math:`\mathbf{P}_2` respectively.

Rearranging the preceding equation yields:

.. math::
    \begin{align}
    \mathbf{B}(t) &= (1 - t)^{2} \mathbf{P}_0 + 2(1 - t)t \mathbf{P}_1 + t^{2} \mathbf{P}_2 \\
                  &= (\mathbf{P}_0 - 2\mathbf{P}_1 + \mathbf{P}_2) t^2 +
                     (-2\mathbf{P}_0 + 2\mathbf{P}_1) t +
                     \mathbf{P}_0
    \end{align}

This can be written in a way that highlights the symmetry with respect to :math:`\mathbf{P}_1`:

.. math::
    \mathbf{B}(t) = \mathbf{P}_1 + (1 - t)^{2} ( \mathbf{P}_0 - \mathbf{P}_1) + t^{2} (\mathbf{P}_2 - \mathbf{P}_1)

Which immediately gives the derivative of the Bézier curve with respect to `t`:

.. math::
    \mathbf{B}'(t) = 2(1 - t) (\mathbf{P}_1 - \mathbf{P}_0) + 2t (\mathbf{P}_2 - \mathbf{P}_1)

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
    \mathbf{B}(t) &= (1-t)^3 \mathbf{P}_0 + 3(1-t)^2t \mathbf{P}_1 + 3(1-t)t^2 \mathbf{P}_2 + t^3\mathbf{P}_3 \\
                  &= (\mathbf{P}_3 - 3\mathbf{P}_2 + 3\mathbf{P}_1 - \mathbf{P}_0) t^3 +
                     3(\mathbf{P}_2 - 2\mathbf{P}_1 + \mathbf{P}_0) t^2 +
                     3(\mathbf{P}_1 - \mathbf{P}_0) t  +
                     \mathbf{P}_0
    \end{align}

For some choices of :math:`\mathbf{P}_1` and :math:`\mathbf{P}_2` the curve may intersect itself, or
contain a cusp.

The derivative of the cubic Bézier curve with respect to :math:`t` is

.. math::
    \mathbf{B}'(t) = 3(1-t)^2 (\mathbf{P}_1 - \mathbf{P}_0) + 6(1-t)t (\mathbf{P}_2 - \mathbf{P}_1) + 3t^2 (\mathbf{P}_3 - \mathbf{P}_2)

The second derivative of the Bézier curve with respect to :math:`t` is

.. math::
    \mathbf{B}''(t) = 6(1-t) (\mathbf{P}_2 - 2 \mathbf{P}_1 + \mathbf{P}_0) +  6t (\mathbf{P}_3 - 2 \mathbf{P}_2 + \mathbf{P}_1)

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
    \mathbf{B}(t) &= \mathbf{B}_{\mathbf{P}_0\mathbf{P}_1\ldots\mathbf{P}_n}(t) \\
                  &= (1-t) \mathbf{B}_{\mathbf{P}_0\mathbf{P}_1\ldots\mathbf{P}_{n-1}}(t) +
                         t \mathbf{B}_{\mathbf{P}_1\mathbf{P}_2\ldots\mathbf{P}_n}(t)
    \end{align}

The formula can be expressed explicitly as follows:

.. math::
    \begin{align}
    \mathbf{B}(t) &= \sum_{i=0}^n b_{i,n}(t) \mathbf{P}_i \\
                  &= \sum_{i=0}^n {n\choose i}(1 - t)^{n - i}t^i \mathbf{P}_i \\
                  &= (1 - t)^n \mathbf{P}_0 +
                     {n\choose 1}(1 - t)^{n - 1}t \mathbf{P}_1 +
                     \cdots +
                     {n\choose n - 1}(1 - t)t^{n - 1} \mathbf{P}_{n - 1} +
                     t^n \mathbf{P}_n
    \end{align}

where :math:`b_{i,n}(t)` are the Bernstein basis polynomials of degree :math:`n` and :math:`n
\choose i` are the binomial coefficients.

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
    \mathbf{B}(t) &= (1 - t) \sum_{i=0}^n \mathbf{b}_{i,n}(t) \mathbf{P}_i +
                           t \sum_{i=0}^n \mathbf{b}_{i,n}(t) \mathbf{P}_i \\
                  &= \sum_{i=0}^n \frac{n + 1 - i}{n + 1} \mathbf{b}_{i, n + 1}(t) \mathbf{P}_i +
                     \sum_{i=0}^n \frac{i + 1}{n + 1} \mathbf{b}_{i + 1, n + 1}(t) \mathbf{P}_i \\
                  &= \sum_{i=0}^{n + 1} \mathbf{b}_{i, n + 1}(t)
                                        \left(\frac{i}{n + 1}         \mathbf{P}_{i - 1} +
                                              \frac{n + 1 - i}{n + 1} \mathbf{P}_i\right) \\
                  &= \sum_{i=0}^{n + 1} \mathbf{b}_{i, n + 1}(t) \mathbf{P'}_i
    \end{align}

Therefore the new control points are

.. math::
      \mathbf{P'}_i = \frac{i}{n + 1} \mathbf{P}_{i - 1} + \frac{n + 1 - i}{n + 1} \mathbf{P}_i

It introduces two arbitrary points :math:`\mathbf{P}_{-1}` and :math:`\mathbf{P}_{n+1}` which are
cancelled in :math:`\mathbf{P'}_i`.

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
    >>> collect(expand(B2), t)
    P0 + t**3*(-P0 + 3*P1 - 3*P2 + P3) + t**2*(3*P0 - 6*P1 + 3*P2) + t*(-3*P0 + 3*P1)
