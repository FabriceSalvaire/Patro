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

"""Module to implement Spline curve.
"""

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

    r"""B-Spline

    A nonuniform, nonrational B-spline of order `n` is a piecewise polynomial function of degree
    :math:`n - 1` in a variable `t`. It is defined over :math:`n + 1` locations :math:`t_j`, called
    knots, which must be in non-descending order :math:`t_j \leq t_{j+1}`.  The B-spline contributes
    only in the range between the first and last of these knots and is zero elsewhere.

    If each knot is separated by the same distance `h` (where :math:`h = t_{j+1} - t_j`) from its
    predecessor, the knot vector and the corresponding B-splines are called "uniform".

    A spline function of order `n` on a given set of knots `K` can be expressed as a linear combination
    of B-splines:

    .. math::
        S_{n,K}(t) = \sum_{i=0}^{n-1} p_i  B_i^n(t)

    where :math:`B_{i, n}` are B-spline basis functions defined by the Cox-de Boor recursion formula:

    .. math::
        B_i^0(t) = 1, \textrm{if $t_i \le t < t_{i+1}$, otherwise $0$,}

        B_i^k(t) = \frac{t - t_i}{t_{i+k} - t_i} B_i^{k-1}(t)
                 + \frac{t_{i+k+1} - t}{t_{i+k+1} - t_{i+1}} B_{i+1}^{k-1}(t)



    The DeBoor-Cox algorithm permits to evaluate recursively a B-Spline in a similar way to the De
    Casteljaud algorithm for Bézier curves.

    Given `k` the degree of the B-spline, `n + 1` control points :math:`p_0, \ldots, p_n`, and an
    increasing series of scalars :math:`t_0 \le t_1 \le \ldots \le t_m` with :math:`m = n + k + 1`,
    called knots.

    The number of points must respect the condition :math:`n + 1 \le k`, e.g. a B-spline of degree 3
    must have 4 control points.

    A B-spline :math:`S(t)` curve is defined by:

    .. math::
        S(t) = \sum_{i=0}^n p_i B_i^k(t) \;\textrm{with}\; t \in [t_k , t_{n+1}]

    The functions :math:`B_i^k(t)` are B-splines functions defined by:

    .. math::
        B_i^0(t) =
        \left\lbrace
        \begin{array}{l}
           1 \;\textrm{if}\; t \in [t_i, t_{i+1}] \\
           0 \;\textrm{else}
        \end{array}
        \right.

    .. math::
       B_i^k(t) = w_i^k(t) B_i^{k-1}(t) + [1 - w_{i+1}^k(t)] B_{i+1}^{k-1}(t)

    with

    .. math::
        w_i^k(t) =
        \left\lbrace
        \begin{array}{l}
           \frac{t - t_i}{t_{i+k} - t_i} \;\textrm{if}\; t_i < t_{i+k} \\
           0 \;\textrm{else}
        \end{array}
        \right.

    DeBoor-Cox Algorithm (1972)

    :math:`S(t) = p_j^k` for :math:`t \in [t_j , t_{j+1}[` for :math:`k \le j \le n` with the following relation:

    .. math::
        \begin{split}
        p_i^{r+1} &= \frac{t - t_i}{t_{i+k-r} - t} p_i^r + \frac{t_{i+k-r} - t_i}{t_{i+k-r} - t_i} p_{i-1}^r \\
                  &= w_i^{k-r}(t) p_i^r +  (1 - w_i^{k-r}(t)) p_{i-1}^r
        \end{split}

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
