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

"""Module to implement segment.

"""

####################################################################################################

__all__ = ['Segment2D']

####################################################################################################

# from .Interpolation import interpolate_two_points
from .Line import Line2D
from .Primitive import Primitive2P, Primitive2DMixin
from .Triangle import triangle_orientation
from .Vector import Vector2D

####################################################################################################

class Segment2D(Primitive2DMixin, Primitive2P):

    """Class to implement 2D Segment"""

    # Fixme: _p0 versus p0

    #######################################

    def __init__(self, p0, p1):

        """Construct a :class:`Segment2D` between two points.

        Parameters

        p0 : :class:`Vector2D`
           from point

        p1 : :class:`Vector2D`
            to point

        """

        Primitive2P.__init__(self, p0, p1)

    ##############################################

    @property
    def vector(self):
        return self._p1 - self._p0

    # Fixme:
    direction = vector

    @property
    def length(self):
        return self.vector.magnitude

    @property
    def center(self):
        # midpoint, barycenter
        return (self._p0 + self._p1) / 2

    ##############################################

    @property
    def cross_product(self):
        return self._p0.cross(self._p1)

    ##############################################

    def cross(self, other):
        return self.vector.cross(other.vector)

    ##############################################

    def to_line(self):
        # Fixme: cache
        return Line2D.from_two_points(self._p0, self._p1)

    ##############################################

    point_at_t = Primitive2P.interpolate

    ##############################################

    def intersect_with(self, segment2):

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

    ##############################################

    def intersection(self, segment2):

        # P = (1-t) * Pa0 + t * Pa1 = Pa0 + t * (Pa1 - Pa0)
        #   = (1-u) * Pb0 + u * Pb1 = Pb0 + u * (Pb1 - Pb0)

        line1 = self.to_line()
        line2 = segment2.to_line()

        s1, s2 = line1.intersection_abscissae(line2)
        if s1 is None:
            return None, None
        else:
            intersect = (0 <= s1 <= 1) and (0 <= s2 <= 1)
            return self.interpolate(s1), intersect

    ##############################################

    def share_vertex_with(self, segment2):

        # return (
        #     self._p0 == segment2._p0 or
        #     self._p0 == segment2._p1 or
        #     self._p1 == segment2._p0 or
        #     self._p1 == segment2._p1
        # )

        if (self._p0 == segment2._p0 or
            self._p0 == segment2._p1):
            return self._p0
        elif (self._p1 == segment2._p0 or
              self._p1 == segment2._p1):
            return self._p1
        else:
            return None

    ##############################################

    def side_of(self, point):

        """Tests if a point is left/on/right of a line.

        > 0 if point is left of the line
        = 0 if point is on the line
        < 0 if point is right of the line
        """

        v1 = self.vector
        v2 = point - self._p0
        return v1.cross(v2)

    ##############################################

    def left_of(self, point):
        """Tests if a point is left a line"""
        return self.side_of(point) > 0

    def right_of(self, point):
        """Tests if a point is right a line"""
        return self.side_of(point) < 0

    def is_collinear(self, point):
        """Tests if a point is on line"""
        return self.side_of(point) == 0

    ##############################################

    def distance_to_point(self, point):

        line = self.to_line()

        if line.v.magnitude_square == 0:
            return (self._p0 - point).magnitude

        d, s = line.distance_and_abscissa_to_line(point)
        if 0 <= s <= self.length:
            return abs(d)
        else:
            if s < 0:
                p = self._p0
            else:
                p = self._p1
            return (p - point).magnitude

    ##############################################

    def contain_point(self, point):

        # Fixme: purpose ???

        line = self.to_line()
        d, s = line.distance_and_abscissa_to_line(point)
        # Fixme: check d / is collinear
        # Fixme: p2 <- p1
        #! print('>'*10, line, point, d, s)
        return 0 <= s <= 1
