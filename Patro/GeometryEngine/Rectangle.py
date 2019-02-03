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

"""Module to implement rectangle.

"""

####################################################################################################

__all__ = ['Rectangle2D']

####################################################################################################

import math

from .Path import Path2D
from .Primitive import Primitive2P, ClosedPrimitiveMixin, PathMixin, PolygonMixin, Primitive2DMixin
from .Segment import Segment2D

####################################################################################################

class Rectangle2D(Primitive2DMixin, ClosedPrimitiveMixin, PathMixin, PolygonMixin, Primitive2P):

    """Class to implements 2D Rectangle."""

    ##############################################

    def __init__(self, p0, p1):

        # if p1 == p0:
        #     raise ValueError('Rectangle reduced to a point')

        Primitive2P.__init__(self, p0, p1)

    ##############################################

    @classmethod
    def from_point_and_offset(self, p0, v):
        return cls(p0, p0+v)

    @classmethod
    def from_point_and_radius(self, p0, v):
        return cls(p0-v, p0+v)

    ##############################################

    @property
    def is_closed(self):
        return True

    ##############################################

    @property
    def p01(self):
        return self.__vector_cls__(self._p0.x, self._p1.y)

    @property
    def p10(self):
        return self.__vector_cls__(self._p1.x, self._p0.y)

    @property
    def edges(self):

        p0 = self._p0
        p1 = self.p01
        p2 = self._p1
        p3 = self.p10

        return (
            Segment2D(p0, p1),
            Segment2D(p1, p2),
            Segment2D(p2, p3),
            Segment2D(p3, p0),
        )

    ##############################################

    @property
    def diagonal(self):
        return self._p1 - self._p0

    ##############################################

    @property
    def perimeter(self):
        d = self.diagonal
        return 2*(abs(d.x) + abs(d.y))

    ##############################################

    @property
    def area(self):
        d = self.diagonal
        return abs(d.x * d.y)

    ##############################################

    def is_point_inside(self, point):

        bounding_box = self.bounding_box
        return (point.x in bounding_box.x and
                point.y in bounding_box.y)

    ##############################################

    def distance_to_point(self, point):
        raise NotImplementedError
