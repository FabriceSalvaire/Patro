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

r"""Module to implement Bézier curve.

For resources on Bézier curve see :ref:`this section <bezier-geometry-ressources-page>`.

"""

####################################################################################################
#
# Notes: algorithm details are on bezier.rst
#
####################################################################################################

# Fixme:
#   max distance to the chord for linear approximation
#   fitting

# C0 = continuous
# G1 = geometric continuity
#    Tangents point to the same direction
# C1 = parametric continuity
#    Tangents are the same, implies G1
# C2 = curvature continuity
#    Tangents and their derivatives are the same

####################################################################################################

__all__ = [
    'QuadraticBezier2D',
    'CubicBezier2D',
]

####################################################################################################

import logging

from math import log, sqrt

import numpy as np

from Patro.Common.Math.Root import quadratic_root, cubic_root, fifth_root
from .Interpolation import interpolate_two_points
from .Line import Line2D
from .Primitive import Primitive3P, Primitive4P, PrimitiveNP, Primitive2DMixin
from .Transformation import AffineTransformation
from .Vector import Vector2D

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class BezierMixin2D(Primitive2DMixin):

    """Mixin to implements 2D Bezier Curve."""

    LineInterpolationPrecision = 0.05

    _logger = _module_logger.getChild('BezierMixin2D')

    ##############################################

    def interpolated_length(self, dt=None):

        """Length of the curve obtained via line interpolation"""

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

    _logger = _module_logger.getChild('QuadraticBezier2D')

    ##############################################

    def __init__(self, p0, p1, p2):
        Primitive3P.__init__(self, p0, p1, p2)

    ##############################################

    def __repr__(self):
        return self.__class__.__name__ + '({0._p0}, {0._p1}, {0._p2})'.format(self)

    ##############################################

    @property
    def length(self):

        r"""Compute the length of the curve.

        For more details see :ref:`this section <bezier-curve-length-section>`.

        """

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

        """Find the intersections of the curve with a line.

        For more details see :ref:`this section <bezier-curve-line-intersection-section>`.

        """

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

        """Return the closest point on the curve to the given *point*.

        For more details see :ref:`this section <bezier-curve-closest-point-section>`.

        """

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
            self._logger.warning("Found more than one root {} for {} and point {}".format(t, self, point))
            return None
        else:
            return self.point_at_t(t)

    ##############################################

    def to_cubic(self):

        r"""Elevate the quadratic Bézier curve to a cubic Bézier cubic with the same shape.

        For more details see :ref:`this section <bezier-curve-degree-elevation-section>`.

        """

        p1 = (self._p0 + self._p1 * 2) / 3
        p2 = (self._p2 + self._p1 * 2) / 3

        return CubicBezier2D(self._p0, p1, p2, self._p2)

####################################################################################################

_Sqrt3 = sqrt(3)
_Div18Sqrt3 = 18 / _Sqrt3
_OneThird = 1 / 3
_Sqrt3Div36 = _Sqrt3 / 36

class CubicBezier2D(BezierMixin2D, Primitive4P):

    """Class to implements 2D Cubic Bezier Curve."""

    InterpolationPrecision = 0.001

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

    _logger = _module_logger.getChild('CubicMixin2D')

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
        points = np.dot(self.point_array, basis).transpose()
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

        """Compute the intersection of two Bézier curves.

        Code inspired from

          *  https://github.com/paperjs/paper.js/blob/master/src/path/Curve.js
          *  http://nbviewer.jupyter.org/gist/hkrish/0a128f21a5b9e5a7a914 The Bezier Clipping Algorithm
          *  https://gist.github.com/hkrish/5ef0f2da7f9882341ee5 hkrish/bezclip_manual.py

        """

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

         r"""Determines if a curve is sufficiently flat, meaning it appears as a straight line and has
         curve-time that is enough linear, as specified by the given *flatness* parameter.

         For more details see :ref:`this section <bezier-curve-flatness-section>`.

         """

         u = 3*self._p1 - 2*self._p0 - self._p3
         v = 3*self._p2 - 2*self._p3 - self._p0

         criterion = max(u.x**2, v.x**2) + max(u.y**2, v.y**2)
         threshold = 16 * flatness**2

         self._logger.warning("is flat {} <= {} with flatness {}".format(criterion, threshold, flatness))

         return criterion <= threshold

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

        """Return the closest point on the curve to the given *point*.

        For more details see :ref:`this section <bezier-curve-closest-point-section>`.

        """

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
            # Fixme:
            # Found more than one root [0, 0.516373783749732]
            # for CubicBezier2D(
            #   Vector2D[1394.4334 1672.0004], Vector2D[1394.4334 1672.0004],
            #   Vector2D[1585.0004 1624.9634], Vector2D[1585.0004 1622.0004])
            # and point Vector2D[1495.11502887 1649.7386517 ]
            # raise NameError("Found more than one root: {}".format(t))
            self._logger.warning("Found more than one root {} for {} and point {}".format(t, self, point))
            # self._logger.warning("is flat {}".format(self.is_flat_enough(.1)))
            if len(t) == 2 and t[0] == 0:
                return self.point_at_t(t[1])
            else:
                return None
        else:
            return self.point_at_t(t[0])
