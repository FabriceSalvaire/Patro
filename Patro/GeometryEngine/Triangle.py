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

"""Module to implement triangle.

"""

####################################################################################################

__all__ = ['Triangle2D']

####################################################################################################

import math

from .Primitive import Primitive3P, ClosedPrimitiveMixin, PathMixin, PolygonMixin, Primitive2DMixin
from .Line import Line2D

####################################################################################################

def triangle_orientation(p0, p1, p2):

    """Return the triangle orientation defined by the three points."""

    dx1 = p1.x - p0.x
    dy1 = p1.y - p0.y
    dx2 = p2.x - p0.x
    dy2 = p2.y - p0.y

    # second slope is greater than the first one --> counter-clockwise
    if dx1 * dy2 > dx2 * dy1:
        return 1
    # first slope is greater than the second one --> clockwise
    elif dx1 * dy2 < dx2 * dy1:
        return -1
    # both slopes are equal --> collinear line segments
    else:
        # p0 is between p1 and p2
        if dx1 * dx2 < 0 or dy1 * dy2 < 0:
            return -1
        # p2 is between p0 and p1, as the length is compared
        # square roots are avoided to increase performance
        elif dx1 * dx1 + dy1 * dy1 >= dx2 * dx2 + dy2 * dy2:
            return 0
        # p1 is between p0 and p2
        else:
            return 1

####################################################################################################

def same_side(p1, p2, a, b):

    """Return True if the points p1 and p2 lie on the same side of the edge [a, b]."""

    v = b - a
    cross1 = v.cross(p1 - a)
    cross2 = v.cross(p2 - a)

    # return cross1.dot(cross2) >= 0
    return cross1*cross2 >= 0

####################################################################################################

class Triangle2D(Primitive2DMixin, ClosedPrimitiveMixin, PathMixin, PolygonMixin, Primitive3P):

    """Class to implements 2D Triangle."""

    ##############################################

    def __init__(self, p0, p1, p2):

        if (p1 - p0).is_parallel((p2 - p0)):
            raise ValueError('Flat triangle')

        Primitive3P.__init__(self, p0, p1, p2)

        # self._p10 = None
        # self._p21 = None
        # self._p02 = None

    ##############################################

    @property
    def is_closed(self):
        return True

    ##############################################

    @property
    def edges(self):

        # Fixme: circular import, Segment import triangle_orientation
        from .Segment import Segment2D

        p0 = self._p0
        p1 = self._p1
        p2 = self._p2

        return (
            Segment2D(p0, p1),
            Segment2D(p1, p2),
            Segment2D(p2, p0),
        )

    ##############################################

    @property
    def bisector_vector0(self):
        return (self._p1 - self._p0) + (self._p2 - self._p0)

    @property
    def bisector_vector1(self):
        return (self._p0 - self._p1) + (self._p2 - self._p1)

    @property
    def bisector_vector2(self):
        return (self._p1 - self._p2) + (self._p0 - self._p2)

    ##############################################

    @property
    def bisector_line0(self):
        return Line2D(self._p0, self.bisector_vector0)

    @property
    def bisector_line1(self):
        return Line2D(self._p1, self.bisector_vector1)

    @property
    def bisector_line2(self):
        return Line2D(self._p2, self.bisector_vector2)

    ##############################################

    def _cache_length(self):

        if not hasattr(self._p10):
            self._p10 = (self._p1 - self._p0).magnitude
            self._p21 = (self._p2 - self._p1).magnitude
            self._p02 = (self._p0 - self._p2).magnitude

    ##############################################

    def _cache_angle(self):

        if not hasattr(self._a10):
            self._a10 = (self._p1 - self._p0).orientation
            self._a21 = (self._p2 - self._p1).orientation
            self._a02 = (self._p0 - self._p2).orientation

    ##############################################

    @property
    def perimeter(self):

        self._cache_length()
        return self._p10 + self._p21 + self._p02

    ##############################################

    @property
    def area(self):

        # using height
        #   = base * height / 2
        # using edge length
        #   = \frac{1}{4} \sqrt{(a+b+c)(-a+b+c)(a-b+c)(a+b-c)} = \sqrt{p(p-a)(p-b)(p-c)}
        # using sinus law
        #  = \frac{1}{2} a b \sin\gamma
        # using coordinate
        # = \frac{1}{2} \left\|{ \overrightarrow{AB} \wedge \overrightarrow{AC}}
        # = \dfrac{1}{2} \big| x_A y_C - x_A y_B + x_B y_A - x_B y_C + x_C y_B - x_C y_A \big|

        return .5 * math.fabs((self._p1 - self._p0).cross(self._p2 - self._p0))

    ##############################################

    @property
    def is_equilateral(self):

        self._cache_length()
        # all sides have the same length and angle = 60
        return (self._p10 == self._p21 and
                self._p21 == self._p02)

    ##############################################

    @property
    def is_scalene(self):

        self._cache_length()
        # all sides have different lengths
        return (self._p10 != self._p21 and
                self._p21 != self._p02 and
                self._p02 != self._p10)

    ##############################################

    @property
    def is_isosceles(self):
        self._cache_length()
        # two sides of equal length
        return not(self.is_equilateral) and not(self.is_scalene)

    ##############################################

    @property
    def is_right(self):
        self._cache_angle()
        # one angle = 90
        raise NotImplementedError

    ##############################################

    @property
    def is_obtuse(self):
        self._cache_angle()
        # one angle > 90
        return max(self._a10, self._a21, self._a02) > 90

    ##############################################

    @property
    def is_acute(self):
        self._cache_angle()
        # all angle < 90
        return max(self._a10, self._a21, self._a02) < 90

    ##############################################

    @property
    def is_oblique(self):
        return not self.is_equilateral

    ##############################################

    @property
    def orthocenter(self):
        # intersection of the altitudes
        raise NotImplementedError

    ##############################################

    @property
    def centroid(self):
        # intersection of the medians
        raise NotImplementedError

    ##############################################

    @property
    def circumcenter(self):
        # intersection of the perpendiculars at middle
        raise NotImplementedError

    ##############################################

    @property
    def in_circle(self):
        # intersection of the bisectors
        raise NotImplementedError # return circle

    ##############################################

    def is_point_inside(self, point):

        # Reference:
        #   http://mathworld.wolfram.com/TriangleInterior.html

        return (
            same_side(point, self._p0, self._p1, self._p2) and
            same_side(point, self._p1, self._p0, self._p2) and
            same_side(point, self._p2, self._p0, self._p1)
        )
