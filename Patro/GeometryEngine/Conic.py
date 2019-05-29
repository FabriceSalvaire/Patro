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

"""Module to implement conic geometry like circle and ellipse.

For resources on conic see :ref:`this section <conic-geometry-ressources-page>`.

"""

####################################################################################################

__all__ = [
    'AngularDomain',
    'Circle2D',
    'Ellipse2D',
]

####################################################################################################

import logging

import math
from math import fabs, sqrt, radians, pi, cos, sin # , degrees

import numpy as np

from Patro.Common.Math.Functions import sign # , epsilon_float
from .Bezier import CubicBezier2D
from .BoundingBox import bounding_box_from_points
from .Line import Line2D
from .Mixin import AngularDomainMixin, CenterMixin, AngularDomain
from .Primitive import Primitive, Primitive2DMixin
from .Segment import Segment2D
from .Transformation import Transformation2D

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class PointNotOnCircleError(ValueError):
    pass

####################################################################################################

class Circle2D(Primitive2DMixin, CenterMixin, AngularDomainMixin, Primitive):

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

    def clone(self):
        return self.__class__(self._center, self._radius, self._domain)

    ##############################################

    def apply_transformation(self, transformation):
        self._center = transformation * self._center
        # Fixme: shear -> ellipse
        if self._radius is not None:
            self._radius = transformation * self._radius

    ##############################################

    def __repr__(self):
        return '{0}({1._center}, {1._radius}, {1._domain})'.format(self.__class__.__name__, self)

    ##############################################

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

    def point_in_circle_frame(self, point):
        return point - self._center

    ##############################################

    def angle_for_point(self, point):

        offset = self.point_in_circle_frame(point)
        # distance = offset.magnitude_square
        # if not epsilon_float(distance, self._radius**2):
        #     raise PointNotOnCircleError # ValueError('Point is not on circle')
        # Fixme:
        orientation = offset.orientation
        if orientation < 0:
            orientation = 360 + orientation
        return orientation

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
        # Fixme: wrong for arc
        return self._center.bounding_box.enlarge(self._radius)

    ##############################################

    def signed_distance_to_point(self, point):
        # d = |P - C| - R
        #   < 0 if inside
        #   = 0    on circle
        #   > 0 if outside
        return (point - self._center).magnitude - self._radius

    ##############################################

    def _circle_distance_to_point(self, point):
        return abs(self.signed_distance_to_point(point))

    ##############################################

    def distance_to_point(self, point):
        if self._domain is not None:
            # Fixme: check !!!
            # try:
            angle = self.angle_for_point(point)
            # print('distance_to_circle', point, angle)
            if self._domain.is_inside(angle):
                # print('point is inside')
                return self._circle_distance_to_point(point)
            # except PointNotOnCircleError:
            #     pass
            # print('point is outside')
            return min([(point - vertex).magnitude for vertex in (self.start_point, self.stop_point)])
        else:
            return self._circle_distance_to_point(point)

    ##############################################

    def is_point_inside(self, point):
        return (point - self._center).magnitude_square <= self._radius**2

    ##############################################

    def intersect_segment(self, segment):

        """Compute the intersection of a circle and a segment."""

        # Fixme: check domain !!!

        dx = segment.vector.x
        dy = segment.vector.y
        dr2 = dx**2 + dy**2

        p0 = segment.p0 - self.center
        p1 = segment.p1 - self.center
        D = p0.cross(p1) # Fixme: fixed typo _product ??

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

        v = circle.center - self.center
        d = sign(v.x) * v.magnitude

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
        raise NotImplementedError

####################################################################################################

class Ellipse2D(Primitive2DMixin, CenterMixin, AngularDomainMixin, Primitive):

    r"""Class to implements 2D Ellipse.


    """

    _logger = _module_logger.getChild('Ellipse2D')

    ##############################################

    @classmethod
    def svg_arc(cls, point1, point2, radius_x, radius_y, angle, large_arc, sweep):

        """Implement SVG Arc.

        Parameters

          * *point1* is the start point and *point2* is the end point.
          * *radius_x* and *radius_y* are the radii of the ellipse, also known as its semi-major and
            semi-minor axes.
          * *angle* is the angle from the x-axis of the current coordinate system to the x-axis of the ellipse.
          * if the *large arc* flag is unset then arc spanning less than or equal to 180 degrees is
            chosen, else an arc spanning greater than 180 degrees is chosen.
          * if the *sweep* flag is unset then the line joining centre to arc sweeps through decreasing
            angles, else if it sweeps through increasing angles.

        References

          * https://www.w3.org/TR/SVG/implnote.html#ArcConversionEndpointToCenter
          * https://www.w3.org/TR/SVG/implnote.html#ArcCorrectionOutOfRangeRadii

        """

        # Ensure radii are non-zero
        if radius_x == 0 or radius_y == 0:
            return Segment2D(point1, point2)

        # Ensure radii are positive
        radius_x = abs(radius_x)
        radius_y = abs(radius_y)

        # step 1

        radius_x2 = radius_x**2
        radius_y2 = radius_y**2

        # We define a new referential with the origin is set to the middle of P1 — P2
        origin_prime = (point1 + point2)/2

        # P1 is exprimed in this referential where the ellipse major axis line up with the x axis
        point1_prime = Transformation2D.Rotation(-angle) * (point1 - point2)/2

        # Ensure radii are large enough
        radii_scale = point1_prime.x**2/radius_x2 + point1_prime.y**2/radius_y2
        if radii_scale > 1:
            self._logger.warning('SVG Arc: radii must be scale')
            radii_scale = math.sqrt(radii_scale)
            radius_x = radii_scale * radius_x
            radius_y = radii_scale * radius_y
            radius_x2 = radius_x**2
            radius_y2 = radius_y**2

        # step 2

        den = radius_x2 * point1_prime.y**2 + radius_y2 * point1_prime.x**2
        num = radius_x2*radius_y2 - den

        ratio = radius_x/radius_y

        sign = 1 if large_arc != sweep else -1
        # print(point1_prime)
        # print(point1_prime.anti_normal)
        # print(ratio)
        # print(point1_prime.anti_normal.scale(ratio, 1/ratio))
        sign *= -1 # Fixme: solve mirroring artefacts for y-axis pointing to the top
        center_prime = sign * math.sqrt(num / den) * point1_prime.anti_normal.scale(ratio, 1/ratio)

        center = Transformation2D.Rotation(angle) * center_prime + origin_prime

        vector1 =   (point1_prime - center_prime).divide(radius_x, radius_y)
        vector2 = - (point1_prime + center_prime).divide(radius_x, radius_y)
        theta = cls.__vector_cls__(1, 0).angle_with(vector1)
        delta_theta = vector1.angle_with(vector2)
        # if theta < 0:
        #     theta = 180 + theta
        # if delta_theta < 0:
        #     delta_theta = 180 + delta_theta
        delta_theta = delta_theta % 360
        # print('theta', theta, delta_theta)
        if not sweep and delta_theta > 0:
            delta_theta -= 360
        elif sweep and delta_theta < 0:
            delta_theta += 360
        # print('theta', theta, delta_theta, theta + delta_theta)
        domain = domain = AngularDomain(theta, theta + delta_theta)

        return cls(center, radius_x, radius_y, angle, domain)

    #######################################

    def __init__(self, center, radius_x, radius_y, angle=0, domain=None):

        self.center = center
        self.radius_x = radius_x
        self.radius_y = radius_y
        self.angle = angle
        self.domain = domain

        self._bounding_box = None

    ##############################################

    def clone(self):
        return self.__class__(
            self._center,
            self._radius_x, self._radius_y,
            self._angle,
            self._domain,
        )

    ##############################################

    def apply_transformation(self, transformation):
        self._center = transformation * self._center
        self._radius_x = transformation * self._radius_x
        self._radius_y = transformation * self._radius_y
        self._bounding_box = None

    ##############################################

    def __repr__(self):
        return '{0}({1._center}, {1._radius_x}, {1._radius_x}, {1._angle})'.format(self.__class__.__name__, self)

    ##############################################

    @property
    def radius_x(self):
        return self._radius_x

    @radius_x.setter
    def radius_x(self, value):
        self._radius_x = float(value)

    @property
    def radius_y(self):
        return self._radius_y

    @radius_y.setter
    def radius_y(self, value):
        self._radius_y = float(value)

    @property
    def angle(self):
        return self._angle

    @angle.setter
    def angle(self, value):
        self._angle = float(value)

    @property
    def major_vector(self):
        # Fixme: x < y
        return self.__vector_cls__.from_polar(self._angle, self._radius_x)

    @property
    def minor_vector(self):
        # Fixme: x < y
        return self.__vector_cls__.from_polar(self._angle + 90, self._radius_y)

    ##############################################

    @property
    def eccentricity(self):
        # focal distance
        # c = sqrt(self._radius_x**2 - self._radius_y**2)
        # e = c / a
        return sqrt(1 - (self._radius_y/self._radius_x)**2)

    ##############################################

    def matrix(self):

        # unit circle -> scale(a, b) -> rotation -> translation(xc, yc)

        angle = radians(self._angle)
        c = cos(angle)
        s = sin(angle)
        c2 = c**2
        s2 = s**2

        a = self._radius_x
        b = self._radius_y
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
        # point = self.__vector_cls__.from_ellipse(self._radius_x, self._radius_y, angle)
        # return self.point_from_ellipse_frame(point)
        point = self.__vector_cls__.from_ellipse(self._radius_x, self._radius_y, angle)
        if self._angle != 0:
            point = point.rotate(self._angle)
        return self._center + point

    ##############################################

    @property
    def bounding_box(self):

        if self._bounding_box is None:
            radius_x, radius_y = self._radius_x, self._radius_y
            if self._angle == 0:
                bounding_box = self._center.bounding_box
                bounding_box.x.enlarge(radius_x)
                bounding_box.y.enlarge(radius_y)
                self._bounding_box = bounding_box
            else:
                angle_x = self._angle
                angle_y = angle_x + 90
                Vector2D = self.__vector_cls__
                points = [self._center + offset for offset in (
                    Vector2D.from_polar(angle_x,  radius_x),
                    Vector2D.from_polar(angle_x, -radius_x),
                    Vector2D.from_polar(angle_y,  radius_y),
                    Vector2D.from_polar(angle_y, -radius_y),
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
        e0, e1 = self._radius_x, self._radius_y

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
        y_scale = self._radius_x / self._radius_y
        points = [self.point_in_ellipse_frame(point) for point in segment.points]
        points = [self.__vector_cls__(point.x, point.y * y_scale) for point in points]
        segment_in_frame = Segment2D(*points)
        circle = Circle2D(self.__vector_cls__(0, 0), self._radius_x)

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

    ##############################################

    def to_bezier(self):

        """Convert an ellipse arc to a set of Quadratic Bézier curves."""

        if self._domain is not None:
            # Fixme: is_over_closer
            start_angle = self._domain.start
            angle_span = self._domain.span
        else:
            start_angle = 0
            angle_span = 360

        # make one segment by quarter
        number_of_segments = math.ceil(abs(angle_span / 90.001))
        angle_step = angle_span / number_of_segments

        curves = []
        for i in range(number_of_segments):
            angle1 = start_angle + i * angle_step
            angle2 = angle1 + angle_step
            curve = self._bezier_arc(angle1, angle2)
            curves.append(curve)

        return curves

    ##############################################

    def _bezier_arc(self, start_angle, stop_angle):

        # This algorithm comes from Qt qtsvg/src/svg/qsvghandler.cpp:pathArcSegment
        # need proof

        angle1 = math.radians(start_angle)
        angle2 = math.radians(stop_angle)

        half_delta_angle = (angle2 - angle1) / 2
        t = 8/3 * math.sin(half_delta_angle / 2)**2 / math.sin(half_delta_angle)

        p0 = self.point_at_angle(start_angle)
        p3 = self.point_at_angle(stop_angle)

        Vector2D = self.__vector_cls__
        offset1 = Vector2D(- self._radius_x * math.sin(angle1), self._radius_y * math.cos(angle1))
        offset2 = Vector2D(self._radius_x * math.sin(angle2), - self._radius_y * math.cos(angle2))
        if self._angle != 0:
            offset1 = offset1.rotate(self._angle)
            offset2 = offset2.rotate(self._angle)
        p1 = p0 + offset1 * t
        p2 = p3 + offset2 * t

        return CubicBezier2D(p0, p1, p2, p3)
