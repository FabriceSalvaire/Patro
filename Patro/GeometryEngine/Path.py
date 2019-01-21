####################################################################################################
#
# Patro - A Python library to make patterns for fashion design
# Copyright (C) 2019 Fabrice Salvaire
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

__all__ = [
    'LinearSegment',
    'QuadraticBezierSegment',
    'CubicBezierSegment',
    'Path2D',
    ]

####################################################################################################

from .Primitive import Primitive1P, Primitive2DMixin
from .Bezier import QuadraticBezier2D, CubicBezier2D
from .Segment import Segment2D
from .Vector import Vector2D

####################################################################################################

class PathPart:

    ##############################################

    def __init__(self, path, position):

        self._path = path
        self._position = position

    ##############################################

    def __repr__(self):
        return self.__class__.__name__

    ##############################################

    @property
    def path(self):
        return self._path

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        self._position = int(value)

    ##############################################

    @property
    def prev_part(self):
        return self._path[self._position -1]

    @property
    def next_part(self):
        return self._path[self._position +1]

    ##############################################

    @property
    def start_point(self):
        prev_part = self.prev_part
        if prev_part is not None:
            return prev_part.stop_point
        else:
            return self._path.p0

    ##############################################

    @property
    def stop_point(self):
        raise NotImplementedError

    @property
    def geometry(self):
        raise NotImplementedError

    ##############################################

    @property
    def bounding_box(self):
        return self.geometry.bounding_box

####################################################################################################

class LinearSegment(PathPart):

    @property
    def points(self):
        return self.start_point, self.stop_point

####################################################################################################

class PathSegment(LinearSegment):

    ##############################################

    def __init__(self, path, position, point):
        PathPart.__init__(path, position)
        self.point = point

    ##############################################

    @property
    def point(self):
        return self._point

    @point.setter
    def point(self, value):
        self._point = Vector2D(value) # self._path.__vector_cls__

    ##############################################

    @property
    def stop_point(self):
        return self._point + self.start_point

    ##############################################

    @property
    def geometry(self):
        # Fixme: cache ???
        return Segment2D(*self.points)

####################################################################################################

class DirectionalSegment(LinearSegment):

    __angle__ = None

    ##############################################

    def __init__(self, path, position, length):
        PathPart.__init__(self, path, position)
        self.length = length

    ##############################################

    @property
    def length(self):
        return self._length

    @length.setter
    def length(self, value):
        self._length = float(value)

    ##############################################

    @property
    def stop_point(self):
        # Fixme: cache ???
        return self.start_point + Vector2D.from_polar(self._length, self.__angle__)

    ##############################################

    @property
    def geometry(self):
        # Fixme: cache ???
        return Segment2D(self.start_point, self.stop_point)

####################################################################################################

class HorizontalSegment(DirectionalSegment):
    __angle__ = 0

class VerticalSegment(DirectionalSegment):
    __angle__ = 90

class NorthSegment(DirectionalSegment):
    __angle__ = 90

class SouthSegment(DirectionalSegment):
    __angle__ = -90

class EastSegment(DirectionalSegment):
    __angle__ = 0

class WestSegment(DirectionalSegment):
    __angle__ = 180

class NorthEastSegment(DirectionalSegment):
    __angle__ = 45

class NorthWestSegment(DirectionalSegment):
    __angle__ = 180 - 45

class SouthEastSegment(DirectionalSegment):
    __angle__ = -45

class SouthWestSegment(DirectionalSegment):
    __angle__ = -180 + 45

####################################################################################################

class TwoPointsMixin:

    @property
    def point1(self):
        return self._point1

    @point1.setter
    def point1(self, value):
        self._point1 = Vector2D(value) # self._path.__vector_cls__

    @property
    def point2(self):
        return self._point2

    @point2.setter
    def point2(self, value):
        self._point2 = Vector2D(value)

####################################################################################################

class QuadraticBezierSegment(PathPart, TwoPointsMixin):

    # Fixme: abs / inc

    ##############################################

    def __init__(self, path, position, point1, point2):
        PathPart.__init__(self, path, position)
        self.point1 = point1
        self.point2 = point2

    ##############################################

    @property
    def stop_point(self):
        return self._point2

    @property
    def points(self):
        return (self.start_point, self._point1, self._point2)

    ##############################################

    @property
    def geometry(self):
        # Fixme: cache ???
        return QuadraticBezier2D(self.start_point, self._point1, self._point2)

####################################################################################################

class CubicBezierSegment(PathPart, TwoPointsMixin):

    ##############################################

    def __init__(self, path, position, point1, point2, point3):
        PathPart.__init__(self, path, position)
        self.point1 = point1
        self.point2 = point2
        self.point3 = point3

    ##############################################

    @property
    def point3(self):
        return self._point3

    @point3.setter
    def point3(self, value):
        self._point3 = Vector2D(value) # self._path.__vector_cls__

    ##############################################

    @property
    def stop_point(self):
        return self._point3

    @property
    def points(self):
        return (self.start_point, self._point1, self._point2, self._point3)

    ##############################################

    @property
    def geometry(self):
        # Fixme: cache ???
        return CubicBezier2D(self.start_point, self._point1, self._point2, self._point3)

####################################################################################################

class Path2D(Primitive2DMixin, Primitive1P):

    """Class to implements 2D Path."""

    ##############################################

    def __init__(self, start_point):

        Primitive1P.__init__(self, start_point)

        self._parts = []

    ##############################################

    def __len__(self):
        return len(self._parts)

    def __iter__(self):
        return iter(self._parts)

    def __getitem__(self, position):
        # try:
        #     return self._parts[slice_]
        # except IndexError:
        #     return None
        position = int(position)
        if 0 <= position < len(self._parts):
            return self._parts[position]
        else:
            return None

    ##############################################

    def _add_part(self, part_cls, *args):
        obj = part_cls(self, len(self._parts), *args)
        self._parts.append(obj)
        return obj

    ##############################################

    def move_to(self, point):
        self.p0 = point

    ##############################################

    def horizontal_to(self, distance):
        return self._add_part(HorizontalSegment, distance)

    def vertical_to(self, distance):
        return self._add_part(VerticalSegment, distance)

    def north_to(self, distance):
        return self._add_part(NorthSegment, distance)

    def south_to(self, distance):
        return self._add_part(SouthSegment, distance)

    def west_to(self, distance):
        return self._add_part(WestSegment, distance)

    def east_to(self, distance):
        return self._add_part(EastSegment, distance)

    def north_east_to(self, distance):
        return self._add_part(NorthEastSegment, distance)

    def south_east_to(self, distance):
        return self._add_part(SouthEastSegment, distance)

    def north_west_to(self, distance):
        return self._add_part(NorthWestSegment, distance)

    def south_west_to(self, distance):
        return self._add_part(SouthWestSegment, distance)

    ##############################################

    def line_to(self, point):
        return self._add_part(PathSegment, point)

    def close(self):
        return self._add_part(PathSegment, self._p0)

    ##############################################

    def quadratic_to(self, point1, point2):
        return self._add_part(QuadraticBezierSegment, point1, point2)

    ##############################################

    def cubic_to(self, point1, point2, point3):
        return self._add_part(CubicBezierSegment, point1, point2, point3)
