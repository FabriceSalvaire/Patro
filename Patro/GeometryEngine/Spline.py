####################################################################################################
#
# Patro - A Python library to make patterns for fashion design
# Copyright (C) 2017 Fabrice Salvaire
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
####################################################################################################

r"""Module to implement Spline curve.

For resources on Spline curve see :ref:`this section <spline-geometry-ressources-page>`.

"""

####################################################################################################
#
# Notes: algorithm details are on spline.rst
#
####################################################################################################

####################################################################################################

__all__ = ['BSpline2D']

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
        points = np.dot(self.point_array, basis).transpose()
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
        points = np.dot(self.point_array, basis).transpose()
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

class BSpline2D(Primitive2DMixin, PrimitiveNP):

    """Class to implement a 2D B-Spline curve.

    """

    ##############################################

    @staticmethod
    def uniform_knots(degree, number_of_points):
        order = degree + 1
        if number_of_points < order:
            raise ValueError('Inconsistent degree and number of points')
        knots = list(range(number_of_points - degree +1))
        return [0]*degree + knots + [knots[-1]]*degree

    ##############################################

    @classmethod
    def check_for_unifom_knots(cls, degree, number_of_points, knots):
        return np.array_equal(cls.uniform_knots(degree, number_of_points), knots)

    ##############################################

    def __init__(self, points, degree, closed=False, knots=None):

        points = self.handle_points(points)
        PrimitiveNP.__init__(self, points)

        self._degree = int(degree)
        self._closed = bool(closed) # Fixme: not implemented

        if knots is not None:
            self._knots = list(knots)
            if not np.all(np.diff(self._knots) >= 0):
                raise ValueError('Invalid knots {}'.format(knots))
            # Fixme: check_for_unifom_knots
            self._uniform = False # Fixme:
        else:
            self._knots = self.uniform_knots(self._degree, self.number_of_points)
            self._uniform = True

        # self._number_of_points = len(self._knots) - self._degree - 1
        # assert (self.number_of_points >= self.order and
        #         (len(self._coefficients) >= self._number_of_points))

    ##############################################

    @property
    def degree(self):
        return self._degree

    @property
    def order(self):
        return self._degree +1

    @property
    def is_closed(self):
        return self._closed

    @property
    def uniform(self):
        return self._uniform

    @property
    def knots(self):
        return self._knots

    @property
    def start_knot(self):
        if self._uniform:
            return 0
        else:
            return self._knots[0]

    @property
    def end_knot(self):
        if self._uniform:
            return self.number_of_points - self._degree
        else:
            return self._knots[-1]

    @property
    def knot_iter(self):
        if self._uniform:
            return range(self.end_knot)
        else:
            return iter(self._knots)

    @property
    def number_of_spans(self):
        if self._uniform:
            count = self.number_of_points - self._degree
            if self._closed:
                count += 1
            return count
        else:
            # multiplicity
            raise NotImplementedError

    ##############################################

    def span(self, t):
        if not(self.start_knot <= t <= self.end_knot):
            raise ValueError('Invalid t {}'.format(t))
        if self._uniform:
            return int(t) + self._degree # start padding
        else:
            for i, t_span in enumerate(self._knots):
                if t < t_span:
                    return i-1

    ##############################################

    def knot_multiplicity(self, knot):
        count = 0
        for t in self._knots:
            if t == knot:
                count += 1
            elif t > knot:
                break
        return count

    ##############################################

    def basis_function(self, i, k, t):

        """De Boor-Cox recursion formula"""

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

    ##############################################

    def _deboor(self, t):

        """Compute point at t using De Boor algorithm"""

        # l_minus_degree = int(t) # span index
        # l = l_minus_degree + self._degree # knot index
        l = self.span(t)
        l_minus_degree = l - self._degree

        knots = self._knots

        points = [self._points[j + l_minus_degree] for j in range(self.order)]
        for r in range(1, self.order):
            for j in range(self._degree, r-1, -1):
                k = j + l_minus_degree
                d = knots[j+1+l-r] - knots[k]
                if d == 0:
                    alpha = 0
                else:
                    alpha = (t - knots[k]) / d
                if alpha == 0:
                    point = points[j-1]
                elif alpha == 1:
                    point = points[j]
                else:
                    point = points[j-1] * (1 - alpha) + points[j] * alpha
                points[j] = point

        return points[self._degree]

    ##############################################

    def _naive_point_at_t(self, t):

        """Compute point at t using a naive algorithm"""

        basis = np.array([self.basis_function(i, self._degree, t)
                          for i in range(self.number_of_points)])
        points = self.point_array
        return self.__vector_cls__(np.dot(basis, points))

    ##############################################

    def point_at_t(self, t, naive=False):

        # Spline curve as a Bézier span at start and end
        if self._uniform:
            if t == 0:
                return self.start_point
            elif t == self.end_knot:
                # else computation fail
                return self.end_point

        if naive:
            return self._naive_point_at_t(t)
        else:
            return self._deboor(t)

    ##############################################

    def insert_knot(self, t):

        # http://pages.mtu.edu/~shene/COURSES/cs3621/NOTES/spline/B-spline/single-insertion.html

        # t lie in the [t_l, t_{l+1}[ span
        # this span is only affected by the control points: P_l, ..., P_{l-degree}
        #   (number of points = degree + 1 = order)

        degree = self._degree
        points = self._points
        knots = self._knots
        l = self.span(t)

        new_points = []
        for i in range(self.number_of_points +1):
            # compute w
            if i <= l - degree:
                w = 1 # same point
            elif i > l:
                w = 0 # previous point
            else: # blend previous and current point
                ti = knots[i]
                d = knots[i + degree] - ti
                if d > 0:
                    w = (t - ti) / d
                else:
                    w = 0

            if w == 0:
                point = points[i-1]
            elif w == 1:
                point = points[i]
            else:
                point = points[i-1] * (1 - w) + points[i] * w
            new_points.append(point)

        # l += degree
        knots = self._knots[:l+1] + [t] + self._knots[l+1:]

        return self.__class__(new_points, self._degree, knots=knots)

    ##############################################

    def to_bezier_form(self, degree=None):

        if not self._uniform:
            raise ValueError('Must be uniform')

        if degree is None:
            degree = self._degree

        new_spline = self
        for t in range(1, self.end_knot):
            multiplicity = self.knot_multiplicity(t)
            for i in range(degree - multiplicity +1):
                new_spline = new_spline.insert_knot(t)

        return new_spline

    ##############################################

    def to_bezier(self):

        from . import Bezier

        if self._degree == 2:
            cls = Bezier.QuadraticBezier2D
        elif self._degree >= 3:
            cls = Bezier.CubicBezier2D
        else:
            not NotImplementedError

        # Fixme: degree > 3
        spline = self.to_bezier_form()

        bezier_curves = []
        order = spline.order
        for i in range(self.number_of_spans):
            i_inf = i * order
            i_sup = i_inf + order
            points = spline._points[i_inf:i_sup]
            bezier = cls(*points)
            bezier_curves.append(bezier)

        return bezier_curves
