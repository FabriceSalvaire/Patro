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

        """Construct a :class:`Segment2D` between two points."""

        Primitive2P.__init__(self, p0, p1)

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

    @property
    def cross_product(self):

        return self._p0.cross(self._p1)

    ##############################################

    def to_line(self):
        return Line2D.from_two_points(self._p1, self._p0)

    ##############################################

    point_at_t = Primitive2P.interpolate

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
