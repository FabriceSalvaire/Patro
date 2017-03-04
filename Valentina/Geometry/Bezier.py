####################################################################################################
#
# PyValentina - A Python implementation of Valentina Pattern Drafting Software
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

####################################################################################################

from math import log, sqrt # pow

from .Primitive import Primitive2D, ReversablePrimitiveMixin, bounding_box_from_points
from .Segment import Segment2D, interpolate_two_points
from .Vector import Vector2D

####################################################################################################

class QuadraticBezier2D(Primitive2D, ReversablePrimitiveMixin):

    """ 2D Quadratic Bezier Curve """

    LineInterpolationPrecision = 0.05

    ##############################################

    def __init__(self, p0, p1, p2):

        """ Construct a :class:`Segment2D` from three points. """

        self._p0 = Vector2D(p0)
        self._p1 = Vector2D(p1)
        self._p2 = Vector2D(p2)

    ##############################################

    def clone(self):

        return self.__class__(self._p0, self._p1, self._p2)

    ##############################################

    def bounding_box(self):

        return bounding_box_from_points((self._p0, self._p1, self._p2))

    ##############################################

    def reverse(self):

        return self.__class__(self._p2, self._p1, self._p0)

    ##############################################

    def __repr__(self):

        return self.__class__.__name__ + '({0._p0}, {0._p1}, {0._p2})'.format(self)

    ##############################################

    @property
    def p0(self):
        return self._p0

    @p0.setter
    def p0(self, value):
        self._p0 = value

    @property
    def p1(self):
        return self._p1

    @p1.setter
    def p1(self, value):
        self._p1 = value

    @property
    def p2(self):
        return self._p2

    @p2.setter
    def p2(self, value):
        self._p2 = value

    @property
    def start_point(self):
        return self._p0

    @property
    def end_point(self):
        return self._p2

    ##############################################

    @property
    def length(self):

        # calculation by Dave Eberly
        #   http://www.gamedev.net/topic/551455-length-of-a-generalized-quadratic-bezier-curve-in-3d
        A0 = self._p1 - self._p0
        A1 = self._p0 - self._p1 * 2 + self._p2
        if A1.magnitude_square() != 0:
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
            return 2 * A0.magnitude()

    ##############################################

    def interpolated_length(self):

        # Length of the curve obtained via line interpolation

        dt = self.LineInterpolationPrecision / (self.end_point - self.start_point).magnitude()
        length = 0
        t = 0
        while t < 1:
            t0 = t
            t = min(t + dt, 1)
            length += (self.point_at_t(t) - self.point_at_t(t0)).magnitude()

        return length

    ##############################################

    def point_at_t(self, t):

        # if 0 < t or 1 < t:
        #     raise ValueError()

        u = 1 - t

        return self._p0 * u**2 + self._p1 * 2 * t * u + self._p2 * t**2

    ##############################################

    def split_at_t(self, t):

        # Splits the curve at given position

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

####################################################################################################

_Sqrt3 = sqrt(3)
_Div18Sqrt3 = 18 / _Sqrt3
_OneThird = 1 / 3
_Sqrt3Div36 = _Sqrt3 / 36

class CubicBezier2D(QuadraticBezier2D):

    """ 2D Cubic Bezier Curve """

    InterpolationPrecision = 0.001

    #######################################

    def __init__(self, p0, p1, p2, p3):

        """ Construct a :class:`Segment2D` from three points. """

        QuadraticBezier2D.__init__(self, p0, p1, p2)
        self._p3 = Vector2D(p3)

    ##############################################

    def clone(self):

        return self.__class__(self._p0, self._p1, self._p2, self._p3)

    ##############################################

    def bounding_box(self):

        return bounding_box_from_points((self._p0, self._p1, self._p2, self._p3))

    ##############################################

    def reverse(self):

        return self.__class__(self._p3, self._p2, self._p1, self._p0)

    ##############################################

    def __repr__(self):

        return self.__class__.__name__ + '({0._p0}, {0._p1}, {0._p2}, {0._p3})'.format(self)

    ##############################################

    @property
    def p3(self):
        return self._p3

    @p3.setter
    def p3(self, value):
        self._p3 = value

    @property
    def end_point(self):
        return self._p3

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
                (self._p2 - self._p1 * 2 + self._p0) * 3 * t**2 +
                (self._p3 - self._p2 * 3 + self._p1 * 3 - self._p0) * t**3)

    ##############################################

    def _q_point(self):
        # Control point for mid-point quadratic approximation
        return (self._p2 * 3 - self._p3 + self._p1 * 3 - self._p0) / 4

    ##############################################

    def mid_point_quadratic_approximation(self):

        # Mid-point quadratic approximation
        p1 = self._q_point()
        return QuadraticBezier2D(self._p0, p1, self._p3)

    ##############################################

    def split_at_t(self, t):

        # Splits the curve at given position

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
        # The distance between 0 and 1 quadratic aproximations
        return (self._p3 - self._p2 * 3 + self._p1 * 3 - self._p0).magnitude() / 2

    ##############################################

    def _t_max(self):
        # Split point for adaptive quadratic approximation
        return (_Div18Sqrt3 * self.InterpolationPrecision / self._d01())**_OneThird

    ##############################################

    def q_length(self):

        #  length of the mid-point quadratic approximation
        return self.mid_point_quadratic_approximation().length

    ##############################################

    def adaptive_length_approximation(self):

        # Calculated length of adaptive quadratic approximation
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
