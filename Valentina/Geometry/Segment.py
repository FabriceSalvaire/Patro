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

from .Line import Line2D
from .Primitive import Primitive2D, ReversablePrimitiveMixin, bounding_box_from_points
from .Vector import Vector2D

####################################################################################################

def triangle_orientation(p0, p1, p2):

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

def interpolate_two_points(p0, p1, t):
    return p0 * (1 - t) + p1 * t

####################################################################################################

class Segment2D(Primitive2D, ReversablePrimitiveMixin):

    """ 2D Segment """

    #######################################

    def __init__(self, p0, p1):

        """ Construct a :class:`Segment2D` between two points. """

        self._p0 = Vector2D(p0)
        self._p1 = Vector2D(p1)

    ##############################################

    def clone(self):

        return self.__class__(self._p0, self._p1)

    ##############################################

    def bounding_box(self):

        return bounding_box_from_points((self._p0, self._p1))

    ##############################################

    def reverse(self):

        return self.__class__(self._p1, self._p0)

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
    def start_point(self):
        return self._p0

    @property
    def end_point(self):
        return self._p1

    ##############################################

    @property
    def vector(self):
        return self._p1 - self._p0

    @property
    def length(self):
        return self.vector.magnitude()

    @property
    def center(self):
        # midpoint, barycenter
        return (self._p0 * self._p1) / 2

    ##############################################

    def to_line(self):
        return Line2D.from_two_points(self._p1, self._p0)

    ##############################################

    def point_at_t(self, t):

        # return interpolate_two_points(self._p0, self._p1)
        return self._p0 * (1 - t) + self._p1 * t

    ##############################################

    def intersect(self, segment2):

        """Checks if the line segments intersect.
        return 1 if there is an intersection
        0 otherwise
        """

        segment1 = self

        # triangle_orientation returns 0 if two points are identical, except from the situation
        # when p0 and p1 are identical and different from p2
        ccw11 = triangle_orientation(segment1.p0, segment1.p1, segment2.p0)
        ccw12 = triangle_orientation(segment1.p0, segment1.p1, segment2.p1)
        ccw21 = triangle_orientation(segment2.p0, segment2.p1, segment1.p0)
        ccw22 = triangle_orientation(segment2.p0, segment2.p1, segment1.p1)

        return (((ccw11 * ccw12 < 0) and (ccw21 * ccw22 < 0))
                # one ccw value is zero to detect an intersection
                or (ccw11 * ccw12 * ccw21 * ccw22 == 0))
