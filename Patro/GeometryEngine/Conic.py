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

####################################################################################################

from math import sqrt, radians, cos, sin, fabs, pi

import numpy as np

from IntervalArithmetic import Interval

from Patro.Common.Math.Functions import sign
from .Line import Line2D
from .Primitive import Primitive, Primitive2DMixin
from .Segment import Segment2D
from .Vector import Vector2D

####################################################################################################

class DomainMixin:

    ##############################################

    @property
    def domain(self):
        return self._domain

    @domain.setter
    def domain(self, interval):
        if interval is not None and interval.length < 360:
            self._domain = Interval(interval)
        else:
            self._domain = None

    ##############################################

    @property
    def is_closed(self):
        return self._domain is None

    ##############################################

    def start_stop_point(self, start=True):

        if self._domain is not None:
            angle = self.domain.inf if start else self.domain.sup
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

class Circle2D(Primitive2DMixin, DomainMixin, Primitive):

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

    # Fixme: tangent constructs ...

    ##############################################

    def __init__(self, center, radius, domain=None, diameter=False):

        """Construct a 2D circle from a center point and a radius.

        If the circle is not closed, *domain* is an interval in degrees.
        """

        if diameter:
            radius /= 2
        self._radius = radius
        self.center = center
        self.domain = domain # Fixme: name ???

    ##############################################

    @property
    def center(self):
        return self._center

    @center.setter
    def center(self, value):
        self._center = Vector2D(value)

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
        return 2 * pi * self._radius

    @property
    def area(self):
        return pi * self._radius**2

    ##############################################

    def point_at_angle(self, angle):
        return Vector2D.from_polar(self._radius, angle) + self._center

    ##############################################

    def tangent_at_angle(self, angle):
        point = Vector2D.from_polar(self._radius, angle) + self._center
        tangent = (point - self._center).normal
        return Line2D(point, tangent)

    ##############################################

    @property
    def bounding_box(self):
        return self._center.bounding_box.enlarge(self._radius)

    ##############################################

    def is_point_inside(self, point):
        return (point - self._center).magnitude_square <= self._radius**2

    ##############################################

    def intersect_segment(self, segment):

        # Fixme: check domain !!!

        # http://mathworld.wolfram.com/Circle-LineIntersection.html
        # Reference: Rhoad et al. 1984, p. 429
        #            Rhoad, R.; Milauskas, G.; and Whipple, R. Geometry for Enjoyment and Challenge,
        #            rev. ed. Evanston, IL: McDougal, Littell & Company, 1984.

        # Definitions
        #   dx = x1 - x0
        #   dy = y1 - y0
        #   D = x0 * y1 - x1 * y0

        # Equations
        #   x**2 + y**2 = r**2
        #   dx * y = dy * x - D

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

class Conic2D(Primitive2DMixin, DomainMixin, Primitive):

    """Class to implements 2D Conic."""

    #######################################

    def __init__(self, center, x_radius, y_radius, angle, domain=None):

        self.center = center
        self._x_radius = x_radius
        self._y_radius = y_radius
        self._angle = angle
        self.domain = Interval(domain)

    ##############################################

    @property
    def center(self):
        return self._center

    @center.setter
    def center(self, value):
        self._center = Vector2D(value)

    @property
    def x_radius(self):
        return self._x_radius

    @x_radius.setter
    def x_radius(self, value):
        self._x_radius = value

    @property
    def y_radius(self):
        return self._y_radius

    @y_radius.setter
    def y_radius(self, value):
        self._y_radius = value

    @property
    def angle(self):
        return self._angle

    @angle.setter
    def angle(self, value):
        self._angle = value

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

        return np.array(((  A, B/2, D/2),
                         (B/2,   C, E/2),
                         (D/2, E/2,   F),
        ))

    ##############################################

    def point_at_angle(self, angle):
        raise NotImplementedError

    ##############################################

    @property
    def bounding_box(self):
        raise NotImplementedError

    ##############################################

    def is_point_inside(self, point):
        raise NotImplementedError

    ##############################################

    def intersect_segment(self, segment):
        raise NotImplementedError

    ##############################################

    def intersect_conic(self, conic):
        raise NotImplementedError
