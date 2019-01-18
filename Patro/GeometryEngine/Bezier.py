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

"""Module to implement Bézier curve.
"""

# C0 = continuous
# G1 = geometric continuity
#    Tangents point to the same direction
# C1 = parametric continuity
#    Tangents are the same, implies G1
# C2 = curvature continuity
#    Tangents and their derivatives are the same

####################################################################################################

from math import log, sqrt

import numpy as np

from Patro.Common.Math.Root import quadratic_root, cubic_root, fifth_root
from .Interpolation import interpolate_two_points
from .Line import Line2D
from .Primitive import Primitive3P, Primitive4P, PrimitiveNP, Primitive2DMixin
from .Transformation import AffineTransformation
from .Vector import Vector2D

####################################################################################################

# Fixme:
#   max distance to the chord for linear approximation
#   fitting

####################################################################################################

class BezierMixin2D(Primitive2DMixin):

    """Mixin to implements 2D Bezier Curve."""

    LineInterpolationPrecision = 0.05

    ##############################################

    def interpolated_length(self, dt=None):

        # Length of the curve obtained via line interpolation

        if dt is None:
            dt = self.LineInterpolationPrecision / (self.end_point - self.start_point).magnitude

        length = 0
        t = 0
        while t < 1:
            t0 = t
            t = min(t + dt, 1)
            length += (self.point_at_t(t) - self.point_at_t(t0)).magnitude

        return length

    ##############################################

    def length_at_t(self, t, cache=False):

        """Compute the length of the curve at *t*."""

        if cache: # lookup cache
            if not hasattr(self, '_length_cache'):
                self._length_cache = {}
            length = self._length_cache.get(t, None)
            if length is not None:
                return length

        length = self.split_at_t(t).length

        if cache: # save
            self._length_cache[t] = length

        return length

    ##############################################

    def t_at_length(self, length, precision=1e-6):

        """Compute t for the given length. Length must lie in [0, curve length] range]. """

        if length < 0:
            raise ValueError('Negative length')
        if length == 0:
            return 0
        curve_length = self.length # Fixme: cache ?
        if (curve_length - length) <= precision:
            return 1
        if length > curve_length:
            raise ValueError('Out of length')

        # Search t for length using dichotomy
        # convergence rate :
        #  10 iterations corresponds to curve length / 1024
        #  16                                        / 65536
        # start range
        inf = 0
        sup = 1
        while True:
            middle = (sup + inf) / 2
            length_at_middle = self.length_at_t(middle, cache=True) # Fixme: out of memory, use LRU ???
            # exit condition
            if abs(length_at_middle - length) <= precision:
                return middle
            elif length_at_middle < length:
                inf = middle
            else: # length < length_at_middle
                sup = middle

    ##############################################

    def split_at_two_t(self, t1, t2):

        if t1 == t2:
            return self.point_at_t(t1)

        if t2 < t1:
            # Fixme: raise ?
            t1, t2 = t2, t1

        # curve = self
        # if t1 > 0:
        curve = self.split_at_t(t1)[1] # right
        if t2 < 1:
            # Interpolate the parameter at t2 in the new curve
            t = (t2 - t1) / (1 - t1)
            curve = curve.split_at_t(t)[0] # left

        return curve

    ##############################################

    def _map_to_line(self, line):

        transformation = AffineTransformation.Rotation(-line.v.orientation)
        # Fixme: use __vector_cls__
        transformation *= AffineTransformation.Translation(Vector2D(0, -line.p.y))
        # Fixme: better API ?
        return self.clone().transform(transformation)

    ##############################################

    def non_parametric_curve(self, line):

        """Return the non-parametric Bezier curve D(ti, di(t)) where di(t) is the distance of the curve from
        the baseline of the fat-line, ti is equally spaced in [0, 1].

        """

        ts = np.arange(0, 1, 1/(self.number_of_points-1))
        distances = [line.distance_to_line(p) for p in self.points]
        points = [Vector2D(t, d) for t, f in zip(ts, distances)]
        return self.__class__(*points)

    ##############################################

    def distance_to_point(self, point):

        p = self.closest_point(point)
        if p is not None:
            return (point - p).magnitude
        else:
            return None

####################################################################################################

class QuadraticBezier2D(BezierMixin2D, Primitive3P):

    """Class to implements 2D Quadratic Bezier Curve."""

    # Q(t) = Transformation * Control * Basis * T(t)
    #
    #           / P1x P2x P3x \  / 1 -2  1 \ / 1    \
    # Q(t) = Tr | P1y P2x P3x |  | 0  2 -2 | | t    |
    #           \  1   1   1  /  \ 0  0  1 / \ t**2 /
    #
    # Q(t) =    P0 * (1 - 2*t + t**2) +
    #           P1 * (    2*t - t**2) +
    #           P2 *            t**2

    BASIS = np.array((
        (1, -2,  1),
        (0,  2, -2),
        (0,  0,  1),
    ))

    INVERSE_BASIS = np.array((
        (-2,  1, -2),
        (-1, -3,  1),
        (-1, -1, -2),
    ))

    ##############################################

    def __init__(self, p0, p1, p2):
        Primitive3P.__init__(self, p0, p1, p2)

    ##############################################

    def __repr__(self):
        return self.__class__.__name__ + '({0._p0}, {0._p1}, {0._p2})'.format(self)

    ##############################################

    @property
    def length(self):

        # Algorithm:
        #
        # http://www.gamedev.net/topic/551455-length-of-a-generalized-quadratic-bezier-curve-in-3d
        # Dave Eberly Posted October 25, 2009
        #
        # The quadratic Bezier is
        #   (x(t),y(t)) = (1-t)^2*(x0,y0) + 2*t*(1-t)*(x1,y1) + t^2*(x2,y2)
        #
        # The derivative is
        #   (x'(t),y'(t)) = -2*(1-t)*(x0,y0) + (2-4*t)*(x1,y1) + 2*t*(x2,y2)
        #
        # The length of the curve for 0 <= t <= 1 is
        #   Integral[0,1] sqrt((x'(t))^2 + (y'(t))^2) dt
        # The integrand is of the form sqrt(c*t^2 + b*t + a)
        #
        # You have three separate cases: c = 0, c > 0, or c < 0.
        # * The case c = 0 is easy.
        # * For the case c > 0, an antiderivative is
        #     (2*c*t+b)*sqrt(c*t^2+b*t+a)/(4*c) + (0.5*k)*log(2*sqrt(c*(c*t^2+b*t+a)) + 2*c*t + b)/sqrt(c)
        #   where k = 4*c/q with q = 4*a*c - b*b.
        # * For the case c < 0, an antiderivative is
        #    (2*c*t+b)*sqrt(c*t^2+b*t+a)/(4*c) - (0.5*k)*arcsin((2*c*t+b)/sqrt(-q))/sqrt(-c)

        A0 = self._p1 - self._p0
        A1 = self._p0 - self._p1 * 2 + self._p2
        if A1.magnitude_square != 0:
            c = 4 * A1.dot(A1)
            b = 8 * A0.dot(A1)
            a = 4 * A0.dot(A0)
            q = 4 * a * c - b * b
            two_cb = 2 * c + b
            sum_cba = c + b + a
            m0 = 0.25 / c
            m1 = q / (8 * c**1.5)
            return (m0 * (two_cb * sqrt(sum_cba) - b * sqrt(a)) +
                    m1 * (log(2 * sqrt(c * sum_cba) + two_cb) - log(2 * sqrt(c * a) + b)))
        else:
            return 2 * A0.magnitude

    ##############################################

    def point_at_t(self, t):
        # if 0 < t or 1 < t:
        #     raise ValueError()
        u = 1 - t
        return self._p0 * u**2 + self._p1 * 2 * t * u + self._p2 * t**2

    ##############################################

    def split_at_t(self, t):

        """Split the curve at given position"""

        if t <= 0:
            return None, self
        elif t >= 1:
            return self, None
        else:
            p01 = interpolate_two_points(self._p0, self._p1, t)
            p12 = interpolate_two_points(self._p1, self._p2, t)
            p = interpolate_two_points(p01, p12, t) # p = p012
            # p = self.point_at_t(t)
            return (QuadraticBezier2D(self._p0, p01, p), QuadraticBezier2D(p, p12, self._p2))

   ##############################################

    @property
    def tangent0(self):
        return (self._p1 - self._p0).normalise()

    ##############################################

    @property
    def tangent1(self):
        return (self._p2 - self._p1).normalise()

    ##############################################

    @property
    def normal0(self):
        return self.tangent0.normal()

    ##############################################

    @property
    def tangent1(self):
        return self.tangent1.normal()

    ##############################################

    def tangent_at(self, t):
        u = 1 - t
        return (self._p1 - self._p0) * u + (self._p2 - self._p1) * t

    ##############################################

    def intersect_line(self, line):

        """Find the intersections of the curve with a line."""

        # Algorithm:
        #   Apply a transformation to the curve that maps the line onto the X-axis.
        #   Then we only need to test the Y-values for a zero.

        # t, p0, p1, p2, p3 = symbols('t p0 p1 p2 p3')
        # u = 1 - t
        # B = p0 * u**2  +  p1 * 2*t*u  +  p2 * t**2
        # collect(expand(B), t)
        # solveset(B, t)

        curve = self._map_to_line(line)

        p0 = curve.p0.y
        p1 = curve.p1.y
        p2 = curve.p2.y

        return quadratic_root(
            p2 - 2*p1 + p0, # t**2
            2*(p1 - p0),    # t
            p0,
        )

        ### a = p0 - 2*p1 + p2 # t**2
        ### # b = 2*(-p0 + p1) # t
        ### b = -p0 + p1 # was / 2 !!!
        ### c = p0
        ###
        ### # discriminant = b**2 - 4*a*c
        ### # discriminant = 4 * (p1**2 - p0*p2)
        ### discriminant = p1**2 - p0*p2 # was / 4 !!!
        ###
        ### if discriminant < 0:
        ###     return None
        ### elif discriminant == 0:
        ###     return -b / a # dropped 2
        ### else:
        ###      # dropped 2
        ###     y1 = (-b - sqrt(discriminant)) / a
        ###     y2 = (-b + sqrt(discriminant)) / a
        ###     return y1, y2

    ##############################################

    def fat_line(self):

        line = Line2D.from_two_points(self._p0, self._p3)
        d1 = line.distance_to_line(self._p1)
        d_min = min(0, d1 / 2)
        d_max = max(0, d1 / 2)

        return (line, d_min, d_max)

    ##############################################

    def closest_point(self, point):

        # Reference:
        #   https://hal.archives-ouvertes.fr/inria-00518379/document
        #   Improved Algebraic Algorithm On Point Projection For Bézier Curves
        #   Xiao-Diao Chen, Yin Zhou, Zhenyu Shu, Hua Su, Jean-Claude Paul

        # Condition:
        #   (P - B(t)) . B'(t) = 0   where t in [0,1]
        #
        #   P. B'(t) - B(t). B'(t) = 0

        # A = P1 - P0
        # B = P2 - P1 - A
        # M = P0 - P

        # Q(t)  = P0*(1-t)**2 + P1*2*t*(1-t) + P2*t**2
        # Q'(t) = -2*P0*(1 - t) + 2*P1*(1 - 2*t) + 2*P2*t
        #       = 2*(A + B*t)

        # P0, P1, P2, P, t = symbols('P0 P1 P2 P t')
        # Q = P0 * (1-t)**2  +  P1 * 2*t*(1-t)  +  P2 * t**2
        # Qp = simplify(Q.diff(t))
        # collect(expand((P*Qp - Q*Qp)/-2), t)

        # (P0**2 - 4*P0*P1 + 2*P0*P2 + 4*P1**2 - 4*P1*P2 + P2**2) * t**3
        # (-3*P0**2 + 9*P0*P1 - 3*P0*P2 - 6*P1**2 + 3*P1*P2) * t**2
        # (-P*P0 + 2*P*P1 - P*P2 + 3*P0**2 - 6*P0*P1 + P0*P2 + 2*P1**2) * t
        # P*P0 - P*P1 - P0**2 + P0*P1

        # factorisation
        # (P0 - 2*P1 + P2)**2 * t**3
        # 3*(P1 - P0)*(P0 - 2*P1 + P2) * t**2
        # ...
        # (P0 - P)*(P1 - P0)

        # B**2 * t**3
        # 3*A*B * t**2
        # (2*A**2 + M*B) * t
        # M*A

        A = self._p1 - self._p0
        B = self._p2 - self._p1 - A
        M = self._p0 - point

        roots = cubic_root(
            B.magnitude_square,
            3*A.dot(B),
            2*A.magnitude_square + M.dot(B),
            M.dot(A),
        )
        t = [root for root in roots if 0 <= root <= 1]
        if not t:
            return None
        elif len(t) > 1:
            raise NameError("Found more than on root")
        else:
            return self.point_at_t(t)

####################################################################################################

_Sqrt3 = sqrt(3)
_Div18Sqrt3 = 18 / _Sqrt3
_OneThird = 1 / 3
_Sqrt3Div36 = _Sqrt3 / 36

class CubicBezier2D(BezierMixin2D, Primitive4P):

    """Class to implements 2D Cubic Bezier Curve."""

    InterpolationPrecision = 0.001

    # Q(t) = Transformation * Control * Basis * T(t)
    #
    #           / P1x P2x P3x P4x \  / 1 -3  3 -1 \ / 1    \
    # Q(t) = Tr | P1y P2x P3x P4x |  | 0  3 -6  3 | | t    |
    #           |  0   0   0   0  |  | 0  0  3 -3 | | t**2 |
    #           \  1   1   1   1  /  \ 0  0  0  1 / \ t**3 /

    BASIS = np.array((
        (1, -3,  3, -1),
        (0,  3, -6,  3),
        (0,  0,  3, -3),
        (0,  0,  0,  1),
    ))

    INVERSE_BASIS = np.array((
        (1,    1,   1, 1),
        (0,  1/3, 2/3, 1),
        (0,    0, 1/3, 1),
        (0,    0,   0, 1),
    ))

    #######################################

    def __init__(self, p0, p1, p2, p3):
        Primitive4P.__init__(self, p0, p1, p2, p3)

    ##############################################

    def __repr__(self):
        return self.__class__.__name__ + '({0._p0}, {0._p1}, {0._p2}, {0._p3})'.format(self)

    ##############################################

    def to_spline(self):
        from .Spline import CubicUniformSpline2D
        basis = np.dot(self.BASIS, CubicUniformSpline2D.INVERSE_BASIS)
        points = np.dot(self.geometry_matrix, basis).transpose()
        return CubicUniformSpline2D(*points)

    ##############################################

    @property
    def length(self):
        return self.adaptive_length_approximation()

    ##############################################

    def point_at_t(self, t):
        # if 0 < t or 1 < t:
        #     raise ValueError()
        return (self._p0 +
                (self._p1 - self._p0) * 3 * t  +
                (self._p2 - self._p1*2 + self._p0) * 3 * t**2 +
                (self._p3 - self._p2*3 + self._p1*3 - self._p0) * t**3)

    # interpolate = point_at_t

    ##############################################

    def _q_point(self):
        """Return the control point for mid-point quadratic approximation"""
        return (self._p2*3 - self._p3 + self._p1*3 - self._p0) / 4

    ##############################################

    def mid_point_quadratic_approximation(self):
        """Return the mid-point quadratic approximation"""
        p1 = self._q_point()
        return QuadraticBezier2D(self._p0, p1, self._p3)

    ##############################################

    def split_at_t(self, t):

        """Split the curve at given position"""

        p01 = interpolate_two_points(self._p0, self._p1, t)
        p12 = interpolate_two_points(self._p1, self._p2, t)
        p23 = interpolate_two_points(self._p2, self._p3, t)
        p012 = interpolate_two_points(p01, p12, t)
        p123 = interpolate_two_points(p12, p23, t)
        p = interpolate_two_points(p012, p123, t) # p = p0123
        # p = self.point_at_t(t)

        return (CubicBezier2D(self._p0, p01, p012, p), CubicBezier2D(p, p123, p23, self._p3))

    ##############################################

    def _d01(self):
        """Return the distance between 0 and 1 quadratic aproximations"""
        return (self._p3 - self._p2 * 3 + self._p1 * 3 - self._p0).magnitude / 2

    ##############################################

    def _t_max(self):
        """Return the split point for adaptive quadratic approximation"""
        return (_Div18Sqrt3 * self.InterpolationPrecision / self._d01())**_OneThird

    ##############################################

    def q_length(self):
        """Return the length of the mid-point quadratic approximation"""
        return self.mid_point_quadratic_approximation().length

    ##############################################

    def adaptive_length_approximation(self):

        """Return the length of the adaptive quadratic approximation"""

        segments = []
        segment = self
        t_max = segment._t_max()
        while t_max < 1:
            split = segment.split_at_t(t_max)
            segments.append(split[0])
            segment = split[1]
            t_max = segment._t_max()
        segments.append(segment)

        return sum([segment.q_length() for segment in segments])

    ##############################################

    @property
    def tangent1(self):
        return (self._p3 - self._p2).normalise()

    ##############################################

    def tangent_at(self, t):
        u = 1 - t
        return (self._p1 - self._p0) * u**2 + (self._p2 - self._p1) * 2 * t * u + (self._p3 - self._p2) * t**2

    ##############################################

    def intersect_line(self, line):

        """Find the intersections of the curve with a line."""

        # Algorithm: same as for quadratic

        # t, p0, p1, p2, p3, p4 = symbols('t p0 p1 p2 p3 p4')
        # u = 1 - t
        # B = p0 *     u**3        +
        #     p1 * 3 * u**2 * t    +
        #     p2 * 3 * u    * t**2 +
        #     p3 *            t**3
        # B = p0 +
        #    (p1 - p0) * 3 * t  +
        #    (p2 - p1 * 2 + p0) * 3 * t**2 +
        #    (p3 - p2 * 3 + p1 * 3 - p0) * t**3
        # solveset(B, t)

        curve = self._map_to_line(line)

        p0 = curve.p0.y
        p1 = curve.p1.y
        p2 = curve.p2.y
        p3 = curve.p3.y

        return cubic_root(
            p3 - 3*p2 + 3*p1 - p0,
            3 * (p2 - p1 * 2 + p0),
            3 * (p1 - p0),
            p0,
        )

    ##############################################

    def fat_line(self):

        line = Line2D.from_two_points(self._p0, self._p3)
        d1 = line.distance_to_line(self._p1)
        d2 = line.distance_to_line(self._p2)
        if d1*d2 > 0:
            factor = 3 / 4
        else:
            factor = 4 / 9
        d_min = factor * min(0, d1, d2)
        d_max = factor * max(0, d1, d2)

        return (line, d_min, d_max)

    ##############################################

    def _clipping_convex_hull(self):

        line_03 = Line2D(self._p0, self._p3)
        d1 = line_03.distance_to_line(self._p1)
        d2 = line_03.distance_to_line(self._p2)

        # Check if p1 and p2 are on the same side of the line [p0, p3]
        if d1 * d2 < 0:
            # p1 and p2 lie on different sides of [p0, p3].
            # The hull is a quadrilateral and line [p0, p3] is not part of the hull.
            # The top part includes p1, we will reverse it later if that is not the case.
            hull = [
                [self._p0, self._p1, self._p3], # top part
                [self._p0, self._p2, self._p3]  # bottom part
            ]
            flip = d1 < 0
        else:
            # p1 and p2 lie on the same sides of [p0, p3]. The hull can be a triangle or a
            # quadrilateral and line [p0, p3] is part of the hull.  Check if the hull is a triangle
            # or a quadrilateral.  Also, if at least one of the distances for p1 or p2, from line
            # [p0, p3] is zero then hull must at most have 3 vertices.
             # Fixme: check cross product
            y0, y1, y2, y3 = [p.y for p in self.points]
            if abs(d1) < abs(d2):
                pmax = p2;
                # apex is y0 in this case, and the other apex point is y3
                # vector yapex -> yapex2 or base vector which is already part of the hull
                # V30xV10 * V10xV20
                cross_product = ((y1 - y0) - (y3 - y0)/3) * (2*(y1 - y0) - (y2 - y0)) /3
            else:
                pmax = p1;
                # apex is y3 and the other apex point is y0
                # vector yapex -> yapex2 or base vector which is already part of the hull
                # V32xV30 * V32xV31
                cross_product = ((y3 - y2) - (y3 - y0)/3) * (2*(y3 - y2) - (y3 + y1)) /3

            # Compare cross products of these vectors to determine if the point is in the triangle
            # [p3, pmax, p0], or if it is a quadrilateral.
            has_null_distance = d1 == 0 or d2 == 0 # Fixme: don't need to compute cross_product
            if cross_product < 0 or has_null_distance:
                # hull is a triangle
                hull = [
                    [self._p0, pmax, self._p3], # top part is a triangle
                    [self._p0, self._p3],       # bottom part is just an edge
                ]
            else:
                hull = [
                    [self._p0, self._p1, self._p2, self._p3], # top part is a quadrilateral
                    [self._p0, self._p3],                     # bottom part is just an edge
                ]
            flip =  d1 < 0 if d1 else d2 < 0

        if flip:
            hull.reverse()

        return hull

    ##############################################

    @staticmethod
    def _clip_convex_hull(hull_top, hull_bottom, d_min, d_max) :


        #              Top   /----
        #                   /     ---/
        #                  /        /
        # d_max -------------------*---
        #                /        / t_max
        #         t_min /        /
        # d_min -------*---------------
        #             /        /
        #            /    ----/   Bottom
        #        p0 /----

        if (hull_top[0].y < d_min):
            # Left of hull is below d_min,
            # walk through the hull until it enters the region between d_min and d_max
            return self._clip_convex_hull_part(hull_top, True, d_min);
        elif (hull_bottom[0].y > d_max) :
            # Left of hull is above d_max,
            # walk through the hull until it enters the region between d_min and d_max
            return self._clip_convex_hull_part(hull_bottom, False, d_max);
        else :
            # Left of hull is between d_min and d_max, no clipping possible
            return hull_top[0].x; # Fixme: 0 ???

    ##############################################

    @staticmethod
    def _clip_convex_hull_part(part, top, threshold) :

        """Clip the bottom or top part of the convex hull.

        *part* is a list of points, *top* is a boolean flag to indicate if it corresponds to the top
        part, *threshold* is d_min if top part else d_max.

        """

        # Walk on the edges
        px = part[0].x;
        py = part[0].y;
        for i in range(1, len(part)):
            qx = part[i].x;
            qy = part[i].y;
            if (qy >= threshold if top else qy <= threshold):
                # compute a linear interpolation
                #   threshold = s * (t - px) + py
                #   t = (threshold - py) / s + px
                return px + (threshold - py) * (qx - px) / (qy - py);
            px = qx;
            py = qy;

        return None; # no intersection

    ##############################################

    @staticmethod
    def _instersect_curve(
            curve1, curve2,
            t_min=0, t_max=1,
            u_min=0, u_max=1,
            old_delta_t=1,
            reverse=False, # flag to indicate that 1 <-> 2 when we store locations
            recursion=0, # number of recursions
            recursion_limit=32,
            t_limit=0.8,
            locations=[],
    ) :

        # Code inspired from
        #   https://github.com/paperjs/paper.js/blob/master/src/path/Curve.js
        #   http://nbviewer.jupyter.org/gist/hkrish/0a128f21a5b9e5a7a914 The Bezier Clipping Algorithm
        #   https://gist.github.com/hkrish/5ef0f2da7f9882341ee5 hkrish/bezclip_manual.py

        # Note:
        #   see https://github.com/paperjs/paper.js/issues/565
        #   It was determined that more than 20 recursions are needed sometimes, depending on the
        #   delta_t threshold values further below when determining which curve converges the
        #   least. He also recommended a threshold of 0.5 instead of the initial 0.8

        if recursion > recursion_limit:
            return

        tolerance = 1e-5
        epsilon = 1e-10

        # t_min_new = 0.
        # t_max_new = 0.
        # delta_t = 0.

        # NOTE: the recursion threshold of 4 is needed to prevent this issue from occurring:
        #       https://github.com/paperjs/paper.js/issues/571
        #       when two curves share an end point
        if curve1.p0.x == curve1.p3.x and u_max - u_min <= epsilon and recursion > 4:
            # The fat-line of curve1 has converged to a point, the clipping is not reliable.
            # Return the value we have even though we will miss the precision.
            t_max_new = t_min_new = (t_max + t_min) / 2
            delta_t = 0
        else :
            # Compute the fat-line for curve1:
            #  a baseline and two offsets which completely encloses the curve
            fatline, d_min, d_max = curve1.fat_line()

            # Calculate a non-parametric bezier curve D(ti, di(t)) where di(t) is the distance of curve2 from
            # the baseline, ti is equally spaced in [0, 1]
            non_parametric_curve = curve2.non_parametric_curve(fatline)

            # Get the top and bottom parts of the convex-hull
            top, bottom = non_parametric_curve._clip_convex_hull()
            # Clip the convex-hull with d_min and d_max
            t_min_clip = self.clip_convex_hull(top, bottom, d_min, d_max);
            top.reverse()
            bottom.reverse()
            t_max_clip = clipConvexHull(top, bottom, d_min, d_max);

            # No intersections if one of the t values is None
            if t_min_clip is None or t_max_clip is None:
                return

            # Clip curve2 with the fat-line for curve1
            curve2 = curve2.split_at_two_t(t_min_clip, t_max_clip)
            delta_t = t_max_clip - t_min_clip
            # t_min and t_max are within the range [0, 1]
            # We need to project it to the original parameter range
            t_min_new = t_max * t_min_clip + t_min * (1 - t_min_clip)
            t_max_new = t_max * t_max_clip + t_min * (1 - t_max_clip)
            delta_t_new = t_max_new - t_min_new

        delta_u = u_max - u_min

        # Check if we need to subdivide the curves
        if old_delta_t > t_limit and delta_t > t_limit:
            # Subdivide the curve which has converged the least.
            args = (delta_t, not reverse, recursion+1, recursion_limit, t_limit, locations)
            if delta_u < delta_t_new: # curve2 < curve1
                parts = curve1.split_at_t(0.5)
                t = t_min_new + delta_t_new / 2
                self._intersect_curve(curve2, parts[0], u_min, u_max, t_min_new, t, *args)
                self._intersect_curve(curve2, parts[1], u_min, u_max, t, t_max_new, *args)
            else :
                parts = curve2.split_at_t(0.5)
                t = u_min + delta_u / 2
                self._intersect_curve(parts[0], curve1, u_min, t, t_min_new, t_max_new, *args)
                self._intersect_curve(parts[1], curve1, t, u_max, t_min_new, t_max_new, *args)

        elif max(delta_u, delta_t_new) < tolerance:
            # We have isolated the intersection with sufficient precision
            t1 = t_min_new + delta_t_new / 2
            t2 = u_min + delta_u / 2
            if reverse:
                t1, t2 = t2, t1
            p1 = curve1.point_at_t(t1)
            p2 = curve2.point_at_t(t2)
            locations.append([t1, point1, t2, point2])

        else:
            args = (delta_t, not reverse, recursion+1, recursion_limit, t_limit)
            self._intersect_curve(curve2, curve1, locations, u_min, u_max, t_min_new, t_max_new, *args)

    ##############################################

    def is_flat_enough(self, flatness):

         """Determines if a curve is sufficiently flat, meaning it appears as a straight line and has
         curve-time that is enough linear, as specified by the given *flatness* parameter.

         *flatness* is the maximum error allowed for the straight line to deviate from the curve.

         """

         # Reference:
         #  Kaspar Fischer and Roger Willcocks  http://hcklbrrfnn.files.wordpress.com/2012/08/bez.pdf
         #  PostScript Language Reference. Addison- Wesley, third edition, 1999

         # We define the flatness of the curve as the argmax of the distance from the curve to the
         # line passing by the start and stop point.
         #
         # flatness = argmax(d(t)) for t in [0, 1] where d(t) = | B(t) - L(t) |
         #
         # L = (1-t)*P0 + t*P1
         #
         # Let
         #   u = 3*P1 - 2*P0 - P3
         #   v = 3*P2 - P0 - 2*P3
         #
         # d(t) = (1-t)**2 * t * (3*P1 - 2*P0 - P3)  +  (1-t) * t**2 * (3*P2 - P0 - 2*P3)
         #      = (1-t)**2 * t * u  +  (1-t) * t**2 * v
         #
         # d(t)**2 = (1 - t)**2 * t**2 * (((1 - t)*ux + t*vx)**2 + ((1 - t)*uy + t*vy)**2
         #
         # argmax((1 - t)**2 * t**2) = 1/16
         # argmax((1 - t)*a + t*b)   = argmax(a, b)
         #
         # flatness**2 = argmax(d(t)**2) <= 1/16 * (argmax(ux**2, vx**2) + argmax(uy**2, vy**2))
         #
         # argmax(ux**2, vx**2) + argmax(uy**2, vy**2) is thus an upper bound of 16 * flatness**2

         # x0, y0 = list(self._p0)
         # x1, y1 = list(self._p1)
         # x2, y2 = list(self._p2)
         # x3, y3 = list(self._p3)

         # ux = 3*x1 - 2*x0 - x3
         # uy = 3*y1 - 2*y0 - y3
         # vx = 3*x2 - 2*x3 - x0
         # vy = 3*y2 - 2*y3 - y0

         u = 3*P1 - 2*P0 - P3
         v = 3*P2 - 2*P3 - P0

         return max(u.x**2, v.x**2) + max(u.y**2, v.y**2) <= 16 * flatness**2

    ##############################################

    @property
    def area(self):

        """Compute the area delimited by the curve and the segment across the start and stop point."""

        # Reference: http://objectmix.com/graphics/133553-area-closed-bezier-curve.html BUT DEAD LINK
        # Proof using divergence theorem ???
        # Fixme: any proof !

        x0, y0 = list(self._p0)
        x1, y1 = list(self._p1)
        x2, y2 = list(self._p2)
        x3, y3 = list(self._p3)

        return (3 * ((y3 - y0) * (x1 + x2) - (x3 - x0) * (y1 + y2)
                     + y1 * (x0 - x2) - x1 * (y0 - y2)
                     + y3 * (x2 + x0 / 3) - x3 * (y2 + y0 / 3)) / 20)

    ##############################################

    def closest_point(self, point):

        # Q(t) = (P3 - 3*P2 + 3*P1 - P0) * t**3 +
        #        3*(P2 - 2*P1 + P0) * t**2 +
        #        3*(P1 - P0) * t  +
        #        P0

        # n = P3 - 3*P2 + 3*P1 - P0
        # r = 3*(P2 - 2*P1 + P0
        # s = 3*(P1 - P0)
        # v = P0

        # Q(t)  = n*t**3 + r*t**2 + s*t + v
        # Q'(t) = 3*n*t**2 + 2*r*t + s

        # P0, P1, P2, P3, P, t = symbols('P0 P1 P2 P3 P t')
        # n, r, s, v = symbols('n r s v')
        # Q = n*t**3 + r*t**2 + s*t + v
        # Qp = simplify(Q.diff(t))
        # collect(expand((P*Qp - Q*Qp)), t)

        # -3*n**2 * t**5
        # -5*n*r * t**4
        # -2*(2*n*s + r**2) * t**3
        # 3*(P*n - n*v - r*s) * t**2
        # (2*P*r - 2*r*v - s**2) * t
        # P*s - s*v

        n = self._p3 - self._p2*3 + self._p1*3 - self._p0
        r = (self._p2 - self._p1*2 + self._p0)*3
        s = (self._p1 - self._p0)*3
        v = self._p0

        roots = fifth_root(
            -3 * n.magnitude_square,
            -5 * n.dot(r),
            -2 * (2*n.dot(s) + r.magnitude_square),
            3 * (point.dot(n) - n.dot(v) - r.dot(s)),
            2*point.dot(r) - 2*r.dot(v) - s.magnitude_square,
            point.dot(s) - s.dot(v),
        )
        # Fixme: to func
        t = [root for root in roots if 0 <= root <= 1]
        if not t:
            return None
        elif len(t) > 1:
            raise NameError("Found more than on root")
        else:
            return self.point_at_t(t[0])
