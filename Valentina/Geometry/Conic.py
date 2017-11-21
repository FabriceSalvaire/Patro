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

from math import sqrt, radians, cos, sin

import numpy as np

from IntervalArithmetic import Interval, Interval2D

from .Primitive import Primitive2D
from .Vector import Vector2D

####################################################################################################

class Circle2D(Primitive2D):

    """ 2D Conic """

    #######################################

    def __init__(self, center, radius, domain):

        self._radius = radius
        self._center = Vector2D(center)
        self._domain = Interval(domain)

    ##############################################

    @property
    def center(self):
        return self._center

    @center.setter
    def center(self, value):
        self._center = value

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, value):
        self._radius = value

    @property
    def domain(self):
        return self._domain

    @domain.setter
    def domain(self, value):
        self._domain = value

    @property
    def eccentricity(self):
        return 1

    ##############################################

    def bounding_box(self):

        return self._center.bounding_box().enlarge(self._radius)

####################################################################################################

class Conic2D(Primitive2D):

    """ 2D Conic """

    #######################################

    def __init__(self, x_radius, y_radius, center, angle, domain):

        self._x_radius = x_radius
        self._y_radius = y_radius
        self._center = Vector2D(center)
        self._angle = angle
        self._domain = Interval(domain)

    ##############################################

    @property
    def center(self):
        return self._center

    @center.setter
    def center(self, value):
        self._center = value

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

    @property
    def domain(self):
        return self._domain

    @domain.setter
    def domain(self, value):
        self._domain = value

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
