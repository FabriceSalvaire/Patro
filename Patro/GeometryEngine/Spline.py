####################################################################################################
#
# Patro - A Python library to make patterns for fashion design
# Copyright (C) 2017 Fabrice Salvaire
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
####################################################################################################

r"""Module to implement Spline curve.

B-spline Basis
--------------

A nonuniform, nonrational B-spline of order `k` is a piecewise polynomial function of degree
:math:`k - 1` in a variable `t`.

.. check: k+1 knots ???

.. It is defined over :math:`k + 1` locations :math:`t_i`, called knots, which must be in
   non-descending order :math:`t_i \leq t_{i+1}`. This series defines a knot vector :math:`T = (t_0,
   \ldots, t_{k})`.

A set of non-descending breaking points, called knot, :math:`t_0 \le t_1 \le \ldots \le t_m` defines
a knot vector :math:`T = (t_0, \ldots, t_{m})`.

If each knot is separated by the same distance `h` (where :math:`h = t_{i+1} - t_i`) from its
predecessor, the knot vector and the corresponding B-splines are called "uniform".

Given a knot vector `T`, the associated B-spline basis functions, :math:`B_i^k(t)` are defined as:

.. t \in [t_i, t_{i+1}[

.. math::
    B_i^1(t) =
    \left\lbrace
    \begin{array}{l}
       1 \;\textrm{if}\; t_i \le t < t_{i+1} \\
       0 \;\textrm{otherwise}
    \end{array}
    \right.

.. math::
   \begin{split}
    B_i^k(t) &= \frac{t - t_i}{t_{i+k-1} - t_i} B_i^{k-1}(t)
              + \frac{t_{i+k} - t}{t_{i+k} - t_{i+1}} B_{i+1}^{k-1}(t) \\
             &= w_i^{k-1}(t) B_i^{k-1}(t) + [1 - w_{i+1}^{k-1}(t)] B_{i+1}^{k-1}(t)
   \end{split}

where

.. math::
    w_i^k(t) =
    \left\lbrace
    \begin{array}{l}
       \frac{t - t_i}{t_{i+k} - t_i} \;\textrm{if}\; t_i < t_{i+k} \\
       0 \;\textrm{otherwise}
    \end{array}
    \right.

These equations have the following properties, for :math:`k > 1` and :math:`i = 0, 1, \ldots, n` :

* Positivity: :math:`B_i^k(t) > 0`, for :math:`t_i < t < t_{i+k}`
* Local Support: :math:`B_i^k(t) = 0`, for :math:`t_0 \le t \le t_i` and :math:`t_{i+k} \le t \le t_{n+k}`
* Partition of unity: :math:`\sum_{i=0}^n B_i^k(t)= 1`, for :math:`t \in [t_0, t_m]`
* Continuity: :math:`B_i^k(t)` as :math:`C^{k-2}` continuity at each simple knot

.. The B-spline contributes only in the range between the first and last of these knots and is zero
   elsewhere.

B-spline Curve
--------------

A B-spline curve of order `k` is defined as a linear combination of control points :math:`p_i` and
B-spline basis functions :math:`B_i^k(t)` given by

.. math::
    S^k(t) = \sum_{i=0}^{n} p_i\; B_i^k(t) ,\quad n \ge k - 1,\; t \in [t_{k-1}, t_{n+1}]

In this context the control points are called De Boor points. The basis functions :math:`B_i^k(t)`
is defined on a knot vector

.. math::
    T = (t_0, t_1, \ldots, t_{k-1}, t_k, t_{k+1}, \ldots, t_{n-1}, t_n, t_{n+1}, \ldots, t_{n+k})

where there are :math:`n+k+1` elements, i.e. the number of control points :math:`n+1` plus the order
of the curve `k`.  Each knot span :math:`t_i \le t \le t_{i+1}` is mapped onto a polynomial curve
between two successive joints :math:`S(t_i)` and :math:`S(t_{i+1})`.

Unlike Bézier curves, B-spline curves do not in general pass through the two end control points.
Increasing the multiplicity of a knot reduces the continuity of the curve at that knot.
Specifically, the curve is :math:`(k-p-1)` times continuously differentiable at a knot with
multiplicity :math:`p (\le k)`, and thus has :math:`C^{k-p-1}` continuity.  Therefore, the control
polygon will coincide with the curve at a knot of multiplicity :math:`k-1`, and a knot with
multiplicity `k` indicates :math:`C^{-1}` continuity, or a discontinuous curve.  Repeating the knots
at the end `k` times will force the endpoints to coincide with the control polygon.  Thus the first
and the last control points of a curve with a knot vector described by

.. math::
    \begin{eqnarray}
    T = (
    \underbrace{t_0, t_1, \ldots, t_{k-1},}_{\mbox{$k$ equal knots}}
    \quad
    \underbrace{t_k, t_{k+1}, \ldots, t_{n-1}, t_n,}_{\mbox{$n$-$k$+1 internal knots}}
    \quad
    \underbrace{t_{n+1}, \ldots, t_{n+k}}_{\mbox{$k$ equal knots}})
    \end{eqnarray}

coincide with the endpoints of the curve.  Such knot vectors and curves are known as *clamped*. In
other words, *clamped/unclamped* refers to whether both ends of the knot vector have multiplicity
equal to `k` or not.

**Local support property**: A single span of a B-spline curve is controlled only by `k` control
points, and any control point affects `k` spans.  Specifically, changing :math:`p_i` affects the
curve in the parameter range :math:`t_i < t < t_{i+k}` and the curve at a point where :math:`t_r < t
< t_{r+1}` is determined completely by the control points :math:`p_{r-(k-1)}, \ldots, p_r`.

**B-spline to Bézier property**: From the discussion of end points geometric property, it can be
seen that a Bézier curve of order `k` (degree :math:`k-1`) is a B-spline curve with no internal
knots and the end knots repeated `k` times.  The knot vector is thus

.. math::
 \begin{eqnarray}
    T = (
    \underbrace{t_0, t_1, \ldots, t_{k-1}}_{\mbox{$k$ equal knots}}
    ,\quad
    \underbrace{t_{n+1}, \ldots, t_{n+k}}_{\mbox{$k$ equal knots}}
    )
    \end{eqnarray}

where :math:`n+k+1 = 2k` or :math:`n = k-1`.

Algorithms for B-spline curves
------------------------------

Evaluation and subdivision algorithm
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A B-spline curve can be evaluated at a specific parameter value `t` using the de Boor algorithm,
which is a generalization of the de Casteljau algorithm.  The repeated substitution of the recursive
definition of the B-spline basis function into the previous definition and re-indexing leads to the
following de Boor algorithm:

..  math::
   S(t) = \sum_{i=0}^{n+j} p_i^j B_i^{k-j}(t) ,\quad j = 0, 1, \ldots, k-1

where

.. math::
   p_i^j = \Big[1 - w_i^j\Big] p_{i-1}^{j-1} + w_i^j p_i^{j-1}, \; j > 0

with

.. math::

  w_i^j = \frac{t - t_i}{t_{i+k-j} - t_i} \quad \textrm{and} \; p_j^0 = p_j

For :math:`j = k-1`, the B-spline basis function reduces to :math:`B_l^1` for :math:`t \in [t_l,
t_{l+1}]`, and :math:`p_l^{k-1}` coincides with the curve :math:`S(t) = p_l^{k-1}`.

The de Boor algorithm is a generalization of the de Casteljau algorithm. The de Boor algorithm also
permits the subdivision of the B-spline curve into two segments of the same order.

De Boor Algorithm
~~~~~~~~~~~~~~~~~

Let the index `l` define the knot interval that contains the position, :math:`t \in [t_l ,
t_{l+1}]`.  We can see in the recursion formula that only B-splines with :math:`i = l-K, \dots, l`
are non-zero for this knot interval, where :math:`K = k - 1` is the degree.  Thus, the sum is
reduced to:

.. math::
    S^k(t) = \sum _{i=l-K}^{l} p_{i} B_i^k(t)

The algorithm does not compute the B-spline functions :math:`B_i^k(t)` directly.  Instead it
evaluates :math:`S(t)` through an equivalent recursion formula.

Let :math:`d _i^r` be new control points with :math:`d_i^0 = p_i` for :math:`i = l-K, \dots, l`.

For :math:`r = 1, \dots, K` the following recursion is applied:

.. math::
    d_i^r = (1 - w_i^r) d_{i-1}^{r-1} + w_i^r d_i^{r-1} \quad i = l-K+r, \dots, l

    w_i^r = \frac{t - t_i}{t_{i+1+l-r} - t_{i}}

Once the iterations are complete, we have :math:`S^k(t) = d_l^k`.

.. , meaning that :math:`d_l^k` is the desired result.

De Boor's algorithm is more efficient than an explicit calculation of B-splines :math:`B_i^k(t)`
with the Cox-de Boor recursion formula, because it does not compute terms which are guaranteed to be
multiplied by zero.

..
    :math:`S(t) = p_j^k` for :math:`t \in [t_j , t_{j+1}[` for :math:`k \le j \le n` with the following relation:
    .. math::
        \begin{split}
        p_i^{r+1} &= \frac{t - t_i}{t_{i+k-r} - t} p_i^r + \frac{t_{i+k-r} - t_i}{t_{i+k-r} - t_i} p_{i-1}^r \\
                  &= w_i^{k-r}(t) p_i^r +  (1 - w_i^{k-r}(t)) p_{i-1}^r
        \end{split}

Knot insertion
~~~~~~~~~~~~~~

A knot can be inserted into a B-spline curve without changing the
geometry of the curve.  The new curve is identical to

.. math::
    \begin{array}{lcl}
    \sum_{i=0}^n p_i B_i^k(t) & \textrm{becomes} & \sum_{i=0}^{n+1} \bar{p}_i \bar B_i^k(t) \\
    \mbox{over}\; T = (t_0, t_1, \ldots, t_l, t_{l+1}, \ldots) & &
    \mbox{over}\; T = (t_0, t_1, \ldots, t_l, \bar t, t_{l+1}, \ldots) & &
    \end{array}

when a new knot :math:`\bar t` is inserted between knots :math:`t_l` and :math:`t_{l+1}`.  The new
de Boor points are given by

.. math::
    \bar{p}_i = (1 - w_i) p_{i-1} + w_i p_i

where

.. math::
    w_i =
    \left\{ \begin{array}{ll}
    1 & i \le l-k+1 \\
    0 & i \ge l+1 \\
    \frac{\bar{t} - t_i}{t_{l+k-1} - t_i} & l-k+2 \le i \leq l
    \end{array}
    \right.

The above algorithm is also known as **Boehm's algorithm**.  A more general (but also more complex)
insertion algorithm permitting insertion of several (possibly multiple) knots into a B-spline knot
vector, known as the Oslo algorithm, was developed by Cohen et al.

A B-spline curve is :math:`C^{\infty}` continuous in the interior of a span.  Within exact
arithmetic, inserting a knot does not change the curve, so it does not change the continuity.
However, if any of the control points are moved after knot insertion, the continuity at the knot
will become :math:`C^{k-p-1}`, where `p` is the multiplicity of the knot.

The B-spline curve can be subdivided into Bézier segments by knot insertion at each internal knot
until the multiplicity of each internal knot is equal to `k`.

References
----------

* Computer Graphics, Principle and Practice, Foley et al., Adison Wesley
* http://web.mit.edu/hyperbook/Patrikalakis-Maekawa-Cho/node15.html

"""

# The DeBoor-Cox algorithm permits to evaluate recursively a B-Spline in a similar way to the De
# Casteljaud algorithm for Bézier curves.
#
# Given `k` the degree of the B-spline, `n + 1` control points :math:`p_0, \ldots, p_n`, and an
# increasing series of scalars :math:`t_0 \le t_1 \le \ldots \le t_m` with :math:`m = n + k + 1`,
# called knots.
#
# The number of points must respect the condition :math:`n + 1 \le k`, e.g. a B-spline of degree 3
# must have 4 control points.

####################################################################################################

__all__ = ['BSpline']

####################################################################################################

# from math import log, sqrt

import numpy as np

from .Bezier import QuadraticBezier2D, CubicBezier2D
from .Primitive import Primitive3P, Primitive4P, PrimitiveNP, Primitive2DMixin

####################################################################################################

class QuadraticUniformSpline2D(Primitive2DMixin, Primitive3P):

    """Class to implements 2D Quadratic Spline Curve."""

    BASIS = np.array((
        (1, -2,  1),
        (1,  2, -2),
        (0,  0,  1),
    ))

    INVERSE_BASIS = np.array((
        (-2,  1, -2),
        (-2, -3,  1),
        (-1, -1, -2),
    ))

    #######################################

    def __init__(self, p0, p1, p2):
        Primitive3P.__init__(self, p0, p1, p2)

    ##############################################

    def __repr__(self):
        return self.__class__.__name__ + '({0._p0}, {0._p1}, {0._p2})'.format(self)

    ##############################################

    def to_bezier(self):
        basis = np.dot(self.BASIS, QuadraticBezier2D.INVERSE_BASIS)
        points = np.dot(self.geometry_matrix, basis).transpose()
        return QuadraticBezier2D(*points)

    ##############################################

    def point_at_t(self, t):

        # Q(t) = (
        #          P0 *  (1-t)**3                      +
        #          P1 * (  3*t**3 - 6*t**2       + 4 ) +
        #          P2 * ( -3*t**3 + 3*t**2 + 3*t + 1 ) +
        #          P3 *      t**3
        #        ) / 6
        #
        #     = P0*(1-t)**3/6 + P1*(3*t**3 - 6*t**2 + 4)/6 + P2*(-3*t**3 + 3*t**2 + 3*t + 1)/6 + P3*t**3/6

        return (self._p0/6 + self._p1*2/3 + self._p2/6 +
                (-self._p0/2 + self._p2/2)*t +
                (self._p0/2 - self._p1 + self._p2/2)*t**2 +
                (-self._p0/6 + self._p1/2 - self._p2/2 + self._p3/6)*t**3)

####################################################################################################

class CubicUniformSpline2D(Primitive2DMixin, Primitive4P):

    """Class to implements 2D Cubic Spline Curve."""

    # T = (1 t t**2 t**3)
    # P = (Pi Pi+2 Pi+2 Pi+3)
    # Q(t) = T M Pt
    #      = P Mt Tt
    # Basis = Mt
    BASIS = np.array((
        (1, -3,  3, -1),
        (4,  0, -6,  3),
        (1,  3,  3, -3),
        (0,  0,  0,  1),
    )) / 6

    INVERSE_BASIS = np.array((
        (  1,    1,    1,     1),
        ( -1,    0,    1,     2),
        (2/3, -1/3,  2/3,  11/3),
        (  0,    0,    0,     6),
    ))

    #######################################

    def __init__(self, p0, p1, p2, p3):
        Primitive4P.__init__(self, p0, p1, p2, p3)

    ##############################################

    def __repr__(self):
        return self.__class__.__name__ + '({0._p0}, {0._p1}, {0._p2}, {0._p3})'.format(self)

    ##############################################

    def to_bezier(self):
        basis = np.dot(self.BASIS, CubicBezier2D.INVERSE_BASIS)
        points = np.dot(self.geometry_matrix, basis).transpose()
        if self._start:
            # list(self.points)[:2]
            points[:2] = self._p0, self._p1
        elif self._stop:
            # list(self.points)[-2:]
            points[-2:] = self._p2, self._p3
        return CubicBezier2D(*points)

    ##############################################

    def point_at_t(self, t):

        # Q(t) = (
        #          P0 *  (1-t)**3                      +
        #          P1 * (  3*t**3 - 6*t**2       + 4 ) +
        #          P2 * ( -3*t**3 + 3*t**2 + 3*t + 1 ) +
        #          P3 *      t**3
        #        ) / 6
        #
        #     = P0*(1-t)**3/6 + P1*(3*t**3 - 6*t**2 + 4)/6 + P2*(-3*t**3 + 3*t**2 + 3*t + 1)/6 + P3*t**3/6

        return (self._p0/6 + self._p1*2/3 + self._p2/6 +
                (-self._p0/2 + self._p2/2)*t +
                (self._p0/2 - self._p1 + self._p2/2)*t**2 +
                (-self._p0/6 + self._p1/2 - self._p2/2 + self._p3/6)*t**3)

####################################################################################################

class BSpline:

    """Class to implement B-Spline curve.

    """

    ##############################################

    def __init__(self, degree, knots, coefficients):

        self._degree = int(degree)
        self._knots = list(knots)
        self._coefficients = list(coefficients)

        self._number_of_points = len(self._knots) - self._degree - 1
        assert ((self._number_of_points >= self._degree+1) and
                (len(self._coefficients) >= self._number_of_points))

    ##############################################

    @property
    def degree(self):
        return self._degree

    @property
    def knots(self):
        return self._knots

    @property
    def coefficients(self):
        return self._coefficients

    @property
    def number_of_points(self):
        return self._number_of_points

    ##############################################

    def eval(self, t):
        return sum(coefficients[i] * self.basis_function(i, self._degree, t)
                   for i in range(self._number_of_points))

    ##############################################

    def basis_function(self, i, k, t):

        """Cox-de Boor recursion formula"""

        if k == 0:
            return 1 if self._knots[i] <= t < self._knots[i+1] else 0

        ki = self._knots[i]
        kik = self._knots[i+k]
        if kik == ki:
            c1 = 0
        else:
            c1 = (t - ki)/(kik - ki) * self.basis_function(i, k-1, t)

        ki = self._knots[i+1]
        kik = self._knots[i+k+1]
        if kik == ki:
            c2 = 0
        else:
            c2 =  (kik - t)/(kik - ki) * self.basis_function(i+1, k-1, t)

        return c1 + c2
