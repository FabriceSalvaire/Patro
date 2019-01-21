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

"""Module to implement conic geometry like circle and ellipse.

Valentina Requirements

* circle with angular domain
* circle with start angle and arc length
* curvilinear distance on circle
* line-circle intersection
* circle-circle intersection
* point constructed from a virtual circle and a point on a tangent : right triangle
* point from tangent circle and segment ???
* ellipse with angular domain and rotation

"""

####################################################################################################

__all__ = [
    'AngularDomain',
    'Circle2D',
    'Ellipse2D',
]

####################################################################################################

import math
from math import fabs, sqrt, radians, pi, cos, sin # , degrees

import numpy as np

from IntervalArithmetic import Interval2D

from Patro.Common.Math.Functions import sign
from .BoundingBox import bounding_box_from_points
from .Line import Line2D
from .Primitive import Primitive, Primitive2DMixin
from .Segment import Segment2D

####################################################################################################

class AngularDomain:

    """Class to define an angular domain"""

    ##############################################

    def __init__(self, start=0, stop=360, degrees=True):

        if not degrees:
            start = math.degrees(start)
            stop = math.degrees(stop)

        self.start = start
        self.stop = stop

    ##############################################

    def __clone__(self):
        return self.__class__(self._start, self._stop)

    ##############################################

    @property
    def start(self):
        return self._start

    @start.setter
    def start(self, value):
        self._start = float(value)

    @property
    def stop(self):
        return self._stop

    @stop.setter
    def stop(self, value):
        self._stop = float(value)

    @property
    def start_radians(self):
        return radians(self._start)

    @property
    def stop_radians(self):
        return radians(self._stop)

    ##############################################

    @property
    def is_null(self):
        return self._stop == self._start

    @property
    def is_closed(self):
        return abs(self._stop - self._start) >= 360

    @property
    def is_over_closed(self):
        return abs(self._stop - self._start) > 360

    @property
    def is_counterclockwise(self):
        """Return True if start <= stop, e.g. 10 <= 300"""
        # Fixme: name ???
        return self.start <= self.stop

    @property
    def is_clockwise(self):
        """Return True if stop < start, e.g. 300 < 10"""
        return self.stop < self.start

    ##############################################

    @property
    def length(self):
        """Return the length for an unitary circle"""
        if self.is_closed:
            return 2*pi
        else:
            length = self.stop_radians - self.start_radians
            if self.is_counterclockwise:
                return length
            else:
                return 2*pi - length

####################################################################################################

class AngularDomainMixin:

    ##############################################

    @property
    def domain(self):
        return self._domain

    @domain.setter
    def domain(self, value):
        if value is not None:
            self._domain = value # Fixme: AngularDomain() ??
        else:
            self._domain = None

    ##############################################

    @property
    def is_closed(self):
        return self._domain is None

    ##############################################

    def start_stop_point(self, start=True):

        if self._domain is not None:
            angle = self.domain.start if start else self.domain.stop
            return self.point_at_angle(angle)
        else:
            return None

    ##############################################

    @property
    def start_point(self):
        return self.start_stop_point(start=True)

    ##############################################

    @property
    def stop_point(self):
        return self.start_stop_point(start=False)

####################################################################################################

class Circle2D(Primitive2DMixin, AngularDomainMixin, Primitive):

    """Class to implements 2D Circle."""

    ##############################################

    @classmethod
    def from_two_points(cls, center, point):
        """Construct a circle from a center point and passing by another point"""
        return cls(center, (point - center).magnitude)

    ##############################################

    @classmethod
    def from_triangle_circumcenter(cls, triangle):
        """Construct a circle passing by three point"""
        return cls.from_two_points(triangle.circumcenter, triangle.p0)

    ##############################################

    @classmethod
    def from_triangle_in_circle(cls, triangle):
        """Construct the in circle of a triangle"""
        return triangle.in_circle

    ##############################################

    # @classmethod
    # def from_start_angle_distance(cls, center, radius, start_angle, distance):
    #     """Construct a circle from a center point, a starting angle and a distance point"""
    #     if distance > 2*pi*radius:
    #         domain = None
    #     else:
    #         stop_angle = start_angle + math.degrees(distance / radius)
    #         domain = AngularDomain(start_angle, stop_angle)
    #     return cls(center, radius, domain)

    ##############################################

    # Fixme: tangent constructs ...

    ##############################################

    def __init__(self, center, radius,
                 domain=None,
                 diameter=False,
                 start_angle=None,
                 distance=None,
    ):

        """Construct a 2D circle from a center point and a radius.

        If the circle is not closed, *domain* is a an :class:`AngularDomain` instance in degrees.
        If *start_angle and *distance* is given then the stop angle is computed from them.

        """

        if diameter:
            radius /= 2
        self._radius = radius
        self.center = center

        if start_angle is not None and distance is not None:
            if distance > 2*pi*radius:
                self._domain = None
            else:
                stop_angle = start_angle + math.degrees(distance / radius)
                self._domain = AngularDomain(start_angle, stop_angle)
        else:
            self.domain = domain # Fixme: name ???

    ##############################################

    def __repr__(self):
        return '{0}({1._center}, {1._radius})'.format(self.__class__.__name__, self)

    ##############################################

    @property
    def center(self):
        return self._center

    @center.setter
    def center(self, value):
        self._center = self.__vector_cls__(value)

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, value):
        self._radius = value

    @property
    def diameter(self):
        return self._radius * 2

    ##############################################

    @property
    def eccentricity(self):
        return 1

    @property
    def perimeter(self):
        if self._domain is not None:
            return 2*pi * self._radius
        else:
            return self._radius * self._domain.length

    @property
    def area(self):
        # Fixme: domain
        return pi * self._radius**2

    ##############################################

    def point_at_angle(self, angle):
        return self.__vector_cls__.from_polar(self._radius, angle) + self._center

    ##############################################

    def point_at_distance(self, distance):
        angle = math.degrees(distance / self._radius)
        return self.point_at_angle(angle)

    ##############################################

    def tangent_at_angle(self, angle):
        point = self.__vector_cls__.from_polar(self._radius, angle) + self._center
        tangent = (point - self._center).normal
        return Line2D(point, tangent)

    ##############################################

    @property
    def bounding_box(self):
        return self._center.bounding_box.enlarge(self._radius)

    ##############################################

    def signed_distance_to_point(self, point):
        # d = |P - C| - R
        #   < 0 if inside
        #   = 0    on circle
        #   > 0 if outside
        return (point - self._center).magnitude - self._radius

    ##############################################

    def distance_to_point(self, point):
        return abs(self.signed_distance_to_point(point))

    ##############################################

    def is_point_inside(self, point):
        return (point - self._center).magnitude_square <= self._radius**2

    ##############################################

    def intersect_segment(self, segment):

        r"""Compute the intersection of a circle and a segment.

        Reference

             * http://mathworld.wolfram.com/Circle-LineIntersection.html
             * Rhoad et al. 1984, p. 429
             * Rhoad, R.; Milauskas, G.; and Whipple, R. Geometry for Enjoyment and Challenge,
             * rev. ed. Evanston, IL: McDougal, Littell & Company, 1984.

        System of equations

        .. math::
           \begin{split}
           x^2 + y^2 = r^2 \\
           dx \times y = dy \times x - D
           \end{split}

        where

        .. math::
           \begin{align}
            dx &= x1 - x0 \\
            dy &= y1 - y0 \\
            D  &= x0 \times y1 - x1 \times y0
           \end{align}

        """

        # Fixme: check domain !!!

        dx = segment.vector.x
        dy = segment.vector.y
        dr2 = dx**2 + dy**2

        p0 = segment.p0 - self.center
        p1 = segment.p1 - self.center
        D = p0.cross_product(p1)

        # from sympy import *
        # x, y, dx, dy, D, r = symbols('x y dx dy D r')
        # system = [x**2 + y**2 - r**2, dx*y - dy*x + D]
        # vars = [x, y]
        # solution = nonlinsolve(system, vars)
        # solution.subs(dx**2 + dy**2, dr**2)

        Vector2D = self.__vector_cls__
        discriminant = self.radius**2 * dr2 - D**2
        if discriminant < 0:
            return None
        elif discriminant == 0: # tangent line
            x = (  D * dy ) / dr2
            y = (- D * dx ) / dr2
            return Vector2D(x, y) + self.center
        else: # intersection
            x_a =  D * dy
            y_a = -D * dx
            x_b = sign(dy) * dx * sqrt(discriminant)
            y_b = fabs(dy) * sqrt(discriminant)
            x0 = (x_a - x_b) / dr2
            y0 = (y_a - y_b) / dr2
            x1 = (x_a + x_b) / dr2
            y1 = (y_a + y_b) / dr2
            p0 = Vector2D(x0, y0) + self.center
            p1 = Vector2D(x1, y1) + self.center
            return p0, p1

    ##############################################

    def intersect_circle(self, circle):

        # Fixme: check domain !!!

        # http://mathworld.wolfram.com/Circle-CircleIntersection.html

        v = circle.center - self.center
        d = sign(v.x) * v.magnitude

        # Equations
        #       x**2 + y**2 = R**2
        #   (x-d)**2 + y**2 = r**2

        x = (d**2 - circle.radius**2 + self.radius**2) / (2*d)
        y2 = self.radius**2 - x**2

        if y2 < 0:
            return None
        else:
            p = self.center + v.normalise() * x
            if y2 == 0:
                return p
            else:
                n = v.normal() * sqrt(y2)
                return p - n, p - n

    ##############################################

    def bezier_approximation(self):

        # http://spencermortensen.com/articles/bezier-circle/

        # > First approximation:
        #
        # 1) The endpoints of the cubic Bézier curve must coincide with the endpoints of the
        #    circular arc, and their first derivatives must agree there.
        #
        # 2) The midpoint of the cubic Bézier curve must lie on the circle.
        #
        # B(t) = (1-t)**3 * P0 + 3*(1-t)**2*t * P1 + 3*(1-t)*t**2 * P2 + t**3 * P3
        #
        # For an unitary circle : P0 = (0,1)  P1 = (c,1)  P2 = (1,c)  P3 = (1, 0)
        #
        # The second constraint provides the value of c = 4/3 * (sqrt(2) - 1)
        #
        # The maximum radial drift is 0.027253 % with this approximation.
        # In this approximation, the Bézier curve always falls outside the circle, except
        # momentarily when it dips in to touch the circle at the midpoint and endpoints.
        #
        # >Better approximation:
        #
        # 2) The maximum radial distance from the circle to the Bézier curve must be as small as
        #    possible.
        #
        # The first constraint yields the parametric form of the Bézier curve:
        # B(t) = (x,y), where:
        # x(t) = 3*c*(1-t)**2*t + 3*(1-t)*t**2 + t**3
        # y(t) = 3*c*t**2*(1-t) + 3*t*(1-t)**2 + (1-t)**3
        #
        # The radial distance from the arc to the Bézier curve is: d(t) = sqrt(x**2 + y**2) - 1
        #
        # The Bézier curve touches the right circular arc at its initial endpoint, then drifts
        # outside the arc, inside, outside again, and finally returns to touch the arc at its
        # endpoint.
        #
        # roots of d : 0, (3*c +- sqrt(-9*c**2 - 24*c + 16) - 2)/(6*c - 4), 1
        #
        # This radial distance function, d(t), has minima at t = 0, 1/2, 1,
        # and maxima at t = 1/2 +- sqrt(12 - 20*c - 3*c**22)/(4 - 6*c)
        #
        # Because the Bézier curve is symmetric about t = 1/2 , the two maxima have the same
        # value. The radial deviation is minimized when the magnitude of this maximum is equal to
        # the magnitude of the minimum at t = 1/2.
        #
        # This gives the ideal value for c = 0.551915024494
        # The maximum radial drift is 0.019608 % with this approximation.

        # P0 = (0,1)   P1 = (c,1)   P2 = (1,c)   P3 = (1,0)
        # P0 = (1,0)   P1 = (1,-c)  P2 = (c,-1)  P3 = (0,-1)
        # P0 = (0,-1)  P1 = (-c,-1) P2 = (-1,-c) P3 = (-1,0)
        # P0 = (-1,0)  P1 = (-1,c)  P2 = (-c,1)  P3 = (0,1)

        raise NotImplementedError

####################################################################################################

class Ellipse2D(Primitive2DMixin, AngularDomainMixin, Primitive):

    r"""Class to implements 2D Ellipse.

    A general ellipse in 2D is represented by a center point `C`, an orthonormal set of
    axis-direction vectors :math:`{U_0 , U_1 }`, and associated extents :math:`e_i` with :math:`e_0
    \ge e_1 > 0`. The ellipse points are

    .. math::
         P = C + x_0 U_0 + x_1 U_1

    where

    .. math::

        \left(\frac{x_0}{e_0}\right)^2 + \left(\frac{x_1}{e_1}\right)^2 = 1

    If :math:`e_0 = e_1`, then the ellipse is a circle with center `C` and radius :math:`e_0`. The
    orthonormality of the axis directions and Equation (1) imply :math:`x_i = U_i \dot (P −
    C)`. Substituting this into Equation (2) we obtain

    .. math::

        (P − C)^T M (P − C) = 1

    where :math:`M = R D R^T`, `R` is an orthogonal matrix whose columns are :math:`U_0` and
    :math:`U_1` , and `D` is a diagonal matrix whose diagonal entries are :math:`1/e_0^2` and
    :math:`1/e_1^2`.

    """

    #######################################

    def __init__(self, center, x_radius, y_radius, angle, domain=None):

        self.center = center
        self.x_radius = x_radius
        self.y_radius = y_radius
        self.angle = angle
        self.domain = domain

        self._bounding_box = None

    ##############################################

    def __repr__(self):
        return '{0}({1._center}, {1._x_radius}, {1._x_radius}, {1._angle})'.format(self.__class__.__name__, self)

    ##############################################

    @property
    def center(self):
        return self._center

    @center.setter
    def center(self, value):
        self._center = self.__vector_cls__(value)

    @property
    def x_radius(self):
        return self._x_radius

    @x_radius.setter
    def x_radius(self, value):
        self._x_radius = float(value)

    @property
    def y_radius(self):
        return self._y_radius

    @y_radius.setter
    def y_radius(self, value):
        self._y_radius = float(value)

    @property
    def angle(self):
        return self._angle

    @angle.setter
    def angle(self, value):
        self._angle = float(value)

    @property
    def major_vector(self):
        # Fixme: x < y
        return self.__vector_cls__.from_polar(self._angle, self._x_radius)

    @property
    def minor_vector(self):
        # Fixme: x < y
        return self.__vector_cls__.from_polar(self._angle + 90, self._y_radius)

    ##############################################

    @property
    def eccentricity(self):
        # focal distance
        # c = sqrt(self._x_radius**2 - self._y_radius**2)
        # e = c / a
        return sqrt(1 - (self._y_radius/self._x_radius)**2)

    ##############################################

    def matrix(self):

        # unit circle -> scale(a, b) -> rotation -> translation(xc, yc)

        angle = radians(self._angle)
        c = cos(angle)
        s = sin(angle)
        c2 = c**2
        s2 = s**2

        a = self._x_radius
        b = self._y_radius
        a2 = a**2
        b2 = b**2

        xc = self._center.x
        yc = self._center.y
        xc2 = xc**2
        yc2 = yc**2

        A = a2*s + b2*c2
        B = 2*(b2 - a2)*c*s
        C = a2*c2 * b2*s2
        D = -2*A*xc - B*yc
        E = -B*xc - 2*C*yc
        F = A*xc2 + B*xc*yc + C*yc2 - a2*b2

        return np.array((
            (  A, B/2, D/2),
            (B/2,   C, E/2),
            (D/2, E/2,   F),
        ))

    ##############################################

    def point_in_ellipse_frame(self, point):
        return (point - self._center).rotate(-self._angle)

    def point_from_ellipse_frame(self, point):
        return self._center + point.rotate(self._angle)

    ##############################################

    def point_at_angle(self, angle):
        # point = self.__vector_cls__.from_ellipse(self._x_radius, self._y_radius, angle)
        # return self.point_from_ellipse_frame(point)
        point = self.__vector_cls__.from_ellipse(self._x_radius, self._y_radius, self._angle + angle)
        return self._center + point

    ##############################################

    @property
    def bounding_box(self):

        if self._bounding_box is None:
            x_radius, y_radius = self._x_radius, self._y_radius
            if self._angle == 0:
                bounding_box = self._center.bounding_box
                bounding_box.x.enlarge(x_radius)
                bounding_box.y.enlarge(y_radius)
                self._bounding_box = bounding_box
            else:
                angle_x = self._angle
                angle_y = angle_x + 90
                Vector2D = self.__vector_cls__
                points = [self._center + offset for offset in (
                    Vector2D.from_polar(angle_x,  x_radius),
                    Vector2D.from_polar(angle_x, -x_radius),
                    Vector2D.from_polar(angle_y,  y_radius),
                    Vector2D.from_polar(angle_y, -y_radius),
                )]
                self._bounding_box = bounding_box_from_points(points)

        return self._bounding_box

    ##############################################

    @staticmethod
    def _robust_length(x, y):
        if x < y:
            x, y = y, x
        return abs(x) * math.sqrt(1 + (y/x)**2)

    ##############################################

    def _distance_point_bisection(self, r0,  z0,  z1,  g):

        n0 = r0 * z0
        s0 = z1 - 1
        if g < 0:
            s1 = 0
        else:
            s1 = self._robust_length(n0 , z1) - 1

        s = 0
        MAX_ITERATION = 1074 # for double
        for i in range(MAX_ITERATION):
            s = (s0 + s1) / 2
            if s == s0 or s == s1:
                break
            ratio0 = n0 / (s + r0)
            ratio1 = z1 / (s + 1)
            g = ratio0**2 + ratio1**2 -1
            if g > 0:
                s0 = s
            elif g < 0:
                s1 = s
            else:
                break

        return s

    ##############################################

    def _eberly_distance(self, point):

        """Compute distance to point using the algorithm described in

            Distance from a Point to an Ellipse, an Ellipsoid, or a Hyperellipsoid
            David Eberly, Geometric Tools, Redmond WA 98052
            September 28, 2018
            https://www.geometrictools.com/Documentation/Documentation.html
            https://www.geometrictools.com/Documentation/DistancePointEllipseEllipsoid.pdf

        The point is expressed in the ellipse coordinate system.
        The preconditions are e0 ≥ e1 > 0, y0 ≥ 0, and y1 ≥ 0.

        """

        # Fixme: make a 3D plot to check the algorithm on a 2D grid and rotated ellipse

        y0, y1 = point
        e0, e1 = self._x_radius, self._y_radius

        if y1 > 0:
            if  y0 > 0:
                z0 = y0 / e0
                z1 = y1 / e1
                g = z0**2 + z1**2 - 1
                if g != 0:
                    r0 = (e0 / e1)**2
                    sbar = self._distance_point_bisection(r0, z0, z1, g)
                    x0 = r0 * y0 / (sbar + r0)
                    x1 = y1 / (sbar + 1)
                    distance = math.sqrt((x0 - y0)**2 + (x1 - y1)**2)
                else:
                    x0 = y0
                    x1 = y1
                    distance = 0
            else:
                # y0 == 0
                x0 = 0
                x1 = e1
                distance = abs(y1 - e1)
        else:
            # y1 == 0
            numer0 = e0 * y0
            denom0 = e0**2 - e1**2
            if numer0 < denom0:
                xde0 = numer0 / denom0
                x0 = e0 * xde0
                x1 = e1 * math.sqrt(1 - xde0**2)
                distance = math.sqrt((x0 - y0)**2 + x1**2)
            else:
                x0 = e0
                x1 = 0
                distance = abs(y0 - e0)

        return distance, self.__vector_cls__(x0, x1)

    ##############################################

    def distance_to_point(self, point, return_point=False, is_inside=False):

        # Fixme: can be transform the problem to a circle using transformation ???

        point_in_frame = self.point_in_ellipse_frame(point)
        point_in_frame_abs = self.__vector_cls__(abs(point_in_frame.x), abs(point_in_frame.y))
        distance, point_in_ellipse = self._eberly_distance(point_in_frame_abs)

        if is_inside:
            # Fixme: right ???
            return (
                (point_in_frame_abs - self._center).magnitude_square
                <=
                (point_in_ellipse - self._center).magnitude_square
            )
        elif return_point:
            point_in_ellipse = self.__vector_cls__(
                sign(point_in_frame.x)*(point_in_ellipse.x),
                sign(point_in_frame.y)*(point_in_ellipse.y),
            )
            point_in_ellipse = self.point_from_ellipse_frame(point_in_ellipse)
            return distance, point_in_ellipse
        else:
            return distance

    ##############################################

    def is_point_inside(self, point):
        return self.distance_to_point(point, is_inside=True)

    ##############################################

    def intersect_segment(self, segment):

        # Fixme: to be checked

        # Map segment in ellipse frame and scale y axis so as to transform the ellipse to a circle
        y_scale = self._x_radius / self._y_radius
        points = [self.point_in_ellipse_frame(point) for point in segment.points]
        points = [self.__vector_cls__(point.x, point.y * y_scale) for point in points]
        segment_in_frame = Segment2D(*points)
        circle = Circle2D(self.__vector_cls__(0, 0), self._x_radius)

        points = circle.intersect_segment(segment_in_frame)
        points = [self.__vector_cls__(point.x, point.y / y_scale) for point in points]
        points = [self.point_from_ellipse_frame(point) for point in points]

        return points

    ##############################################

    def intersect_conic(self, conic):

        """
        Reference

            * Intersection of Ellipses
            * David Eberly, Geometric Tools, Redmond WA 98052
            * June 23, 2015
            * https://www.geometrictools.com/
            * https://www.geometrictools.com/Documentation/IntersectionOfEllipses.pdf

        """

        raise NotImplementedError
