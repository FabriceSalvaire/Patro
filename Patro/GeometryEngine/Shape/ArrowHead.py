####################################################################################################
#
# Patro - A Python library to make patterns for fashion design
# Copyright (C) 2019 Fabrice Salvaire
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

"""Module to implement arrow head.

"""

####################################################################################################

__all__ = [
    'ArrowHead',
    'TriangularHead',
    'TriangularCurvyHead',
]

####################################################################################################

from ..Path import Path2D
from ..Polygon import Polygon2D
from ..Vector import Vector2D

####################################################################################################

class ArrowHead: # Primitive

    """Base class to implement arrow head.

    An arrow head (tip) is placed at an anchor point along a direction (support line).  It can be
    placed at a segment extremities or shifted from an extremity, for example for multiple tips.

    """

    ##############################################

    def __init__(self, point, direction):

        self._point = Vector2D(point)
        self._direction = Vector2D(direction).normalise()

    ##############################################

    def clone(self):
        raise NotImplementedError

    ##############################################

    @property
    def anchor_point(self):
        return self._point

    # @point.setter
    # def point(self, value):
    #     self._point = value

    @property
    def direction(self):
        return self._direction

    # @direction.setter
    # def direction(self, value):
    #     self._direction = value

####################################################################################################

class TriangularHeadMixin(ArrowHead):

    ##############################################

    def __init__(self, point, direction,
                 length, width,
                 axial_offset=0,
                 left_side=True,
                 right_side=True):

        ArrowHead.__init__(self, point, direction)

        self._length = float(length)
        self._width = float(width)
        self._axial_offset = float(axial_offset)
        self._left_side = bool(left_side)
        self._right_side = bool(right_side)

        # Fixme: check length width ???
        if not(self._left_side and self._right_side):
            return ValueError('Any side')

        self._back_tip_point = None

    ##############################################

    @property
    def length(self):
        return self._length

    @property
    def width(self):
        return self._width

    @property
    def axial_offset(self):
        return self._axial_offset

    @property
    def has_axial_offset(self):
        return self._axial_offset != 0

    @property
    def left_side(self):
        return self._left_side

    @property
    def right_side(self):
        return self._right_side

    @property
    def both_side(self):
        return self._right_side and self._left_side

    @property
    def only_left(self):
        return not self._right_side and self._left_side

    @property
    def only_right(self):
        return self._right_side and not self._left_side

    ##############################################

    @property
    def angle(self):
        return 2 * Vector2D(self._length, self._width).orientation

    # tip_point = anchor_point
    @property
    def tip_point(self):
        return self._point

    @property
    def back_tip_point(self):
        if self._back_tip_point is None:
            self._back_tip_point = self.tip_point - self._direction * self._length
        return self._back_tip_point

    @property
    def offseted_back_tip_point(self):
        return self.back_tip_point - self._direction * self._self._axial_offset

    @property
    def left_point(self):
        # Fixme: not cached
        if self._left_side:
            return self.back_tip_point + self._direction.normal * self._width
        else:
            return None

    @property
    def right_point(self):
        if self._right_side:
            return self.back_tip_point - self._direction.normal * self._width
        else:
            return None

####################################################################################################

class TriangularHead(TriangularHeadMixin, Polygon2D):

    ##############################################

    def __init__(self, point, direction,
                 length, width,
                 axial_offset=0,
                 left_side=True,
                 right_side=True):

        TriangularHeadMixin.__init__(self,
                                     point, direction,
                                     length, width, axial_offset,
                                     left_side, right_side,
        )

        points = self._make_points()
        Polygon2D.__init__(self, *points)

    ##############################################

    def _make_points(self):

        # tip_point = self._point
        # back_tip_point = tip_point - direction * self._width
        # if self._left_side:
        #     left_point = back_tip_point + direction.normal * self._width
        # if self._right_side:
        #     right_point = back_tip_point - direction.normal * self._width

        if self.has_axial_offset:
            if self.both_side:
                points = [self.left_point, self.offseted_back_tip_point, self.right_point]
            elif self.only_left:
                points = [self.left_point, self.offseted_back_tip_point]
            else: # only right
                points = [self.right_point, self.offseted_back_tip_point]
        else:
            if self.both_side:
                points = [self.left_point, self.right_point]
            elif self.only_left:
                points = [self.left_point, self.back_tip_point]
            else: # only right
                points = [self.right_point, self.back_tip_point]

        return [self.tip_point] + points

####################################################################################################

class TriangularCurvyHead(TriangularHeadMixin, Path2D):

    ##############################################

    def __init__(self, point, direction,
                 length, width,
                 curve_depth, # Fixme: name
                 axial_offset=0,
                 left_side=True,
                 right_side=True):

        TriangularHeadMixin.__init__(self,
                                     point, direction,
                                     length, width, axial_offset,
                                     left_side, right_side,
        )

        self._curve_depth = float(curve_depth)

        Path2D.__init__(self, self._point)
        self._make_path()

    ##############################################

    @property
    def curve_depth(self):
        return self._curve_depth

    ##############################################

    @property
    def left_curved_point(self):
        if self._left_side:
            direction = self.left_point - self.tip_point
            return (self.left_point + self.tip_point) / 2 - direction.normal * self._curve_depth
        else:
            return None

    @property
    def right_curved_point(self):
        if self._right_side:
            direction = self.right_point - self.tip_point
            return (self.right_point + self.tip_point) / 2 - direction.normal * self._curve_depth
        else:
            return None

    ##############################################

    def _make_path(self):

        # Fixme: factorise
        control2 = None
        if self.has_axial_offset:
            if self.both_side:
                controls1 = (self.left_curved_point, self.left_point)
                vertices = (self.offseted_back_tip_point, self.right_point)
                control2 = self.right_curved_point
            elif self.only_left:
                controls1 = (self.left_curved_point, self.left_point)
                vertices = (self.offseted_back_tip_point,)
            else: # only right
                controls1 = (self.right_curved_point, self.right_point)
                vertices = (self.offseted_back_tip_point,)
        else:
            if self.both_side:
                controls1 = (self.left_curved_point, self.left_point)
                vertices = (self.right_point,)
                control2 = self.right_curved_point
            elif self.only_left:
                controls1 = (self.left_curved_point, self.left_point)
                vertices = (self.back_tip_point,)
            else: # only right
                controls1 = (self.right_curved_point, self.right_point)
                vertices = (self.back_tip_point,)

        self.quadratic_to(*controls1, absolute=True)
        for vertex in vertices:
            self.line_to(vertex, absolute=True)
        if control2 is not None:
            self.quadratic_to(control2, self.tip_point, absolute=True)
        self.close() # Fixme: if control2, path has a zero segment !!!
