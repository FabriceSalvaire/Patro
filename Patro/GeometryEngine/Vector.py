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

"""Module to implement vector.

Example of usage::

  v = Vector2D(10, 20)
  v = Vector2D((10, 20))
  v = Vector2D([10, 20])
  v = Vector2D(iterable)
  v = Vector2D(v)

  v.x
  v.y

  # array interface
  v[0], v[1]
  iter(v)

  -v

  v + v
  v += v

  v - v
  v -= v

  v * 2
  2 * v
  v *= 2

  v / 2
  v /= 2

"""

####################################################################################################

__all__ = [
    'Vector2D',
    'NormalisedVector2D',
    'HomogeneousVector2D',
]

####################################################################################################

import math

import numpy as np

from IntervalArithmetic import Interval2D, IntervalInt2D

from Patro.Common.Math.Functions import sign, trignometric_clamp #, is_in_trignometric_range
from .Primitive import Primitive, Primitive2DMixin

####################################################################################################

class Vector2DBase(Primitive, Primitive2DMixin):

    __data_type__ = None

    ##############################################

    def __init__(self, *args):

        array = self._check_arguments(args)

        # call __getitem__ once
        self._v = np.array(array[:2], dtype=self.__data_type__) # Numpy implementation

    ##############################################

    def _check_arguments(self, args):

        size = len(args)
        if size == 1:
            array = args[0]
        elif size == 2:
            array = args
        else:
            raise ValueError("More than 2 arguments where given")

        if not (np.iterable(array) and len(array) == 2):
            raise ValueError("Argument must be iterable and of length 2")

        return array

    ##############################################

    def clone(self):
        return self.__class__(self)

    ##############################################

    @property
    def v(self):
        return self._v

    # @v.setter
    # def v(self, value):
    #     self._v = value

    @property
    def x(self):
        return self.__data_type__(self._v[0])

    @property
    def y(self):
        return self.__data_type__(self._v[1])

    @x.setter
    def x(self, x):
        self._v[0] = x

    @y.setter
    def y(self, y):
        self._v[1] = y

    ##############################################

    def clone(self):
        """ Return a copy of self """
        return self.__class__(self._v)

    ##############################################

    def __repr__(self):
        return self.__class__.__name__ + str(self.v)

    ##############################################

    def __nonzero__(self):
        return bool(self._v.any())

    ##############################################

    def __len__(self):
        return 2

    ##############################################

    def __iter__(self):
        return iter(self._v)

    ##############################################

    def __getitem__(self, a_slice):
        return self._v[a_slice]

    ##############################################

    def __setitem__(self, index, value):
        self._v[index] = value

    ##############################################

    def __eq__(v1, v2):
        """ self == other """
        return np.array_equal(v1.v, v2.v)

    ##############################################

    def __add__(self, other):
        """Return a new vector equal to the addition of self and other"""
        return self.__class__(self._v + other.v)

    ##############################################

    def __iadd__(self, other):
        """Add other to self"""
        self._v += other.v
        return self

    ##############################################

    def __sub__(self, other):
        """Return a new vector"""
        return self.__class__(self._v - other.v)

    ##############################################

    def __isub__(self, other):
        """Return a new vector equal to the subtraction of self and other"""
        self._v -= other.v
        return self

    ##############################################

    def __pos__(self):
        """ Return a new vector equal to self """
        return self.__class__(self._v)

    ##############################################

    def __neg__(self):
        """Return a new vector equal to the negation of self"""
        return self.__class__(-self._v)

    ##############################################

    def __abs__(self):
        """Return a new vector equal to abs of self"""
        return self.__class__(np.abs(self._v))

    ##############################################

    def to_int_list(self):
        return [int(x) for x in self._v]

####################################################################################################

class Vector2DInt(Vector2DBase):

    __data_type__ = np.int

    ##############################################

    @property
    def bounding_box(self):
        x, y = self.x, self.y
        return IntervalInt2D((x, x) , (y, y))

####################################################################################################

class Vector2DFloatBase(Vector2DBase):

    __data_type__ = np.float

    ##############################################

    @property
    def bounding_box(self):
        x, y = self.x, self.y
        return Interval2D((x, x) , (y, y))

    ##############################################

    def almost_equal(v1, v2, rtol=1e-05, atol=1e-08, equal_nan=False):
        """self ~= other"""
        return np.allclose(v1, v2, rtol, atol, equal_nan)

    ##############################################

    @property
    def magnitude_square(self):
        """Return the square of the magnitude of the vector"""
        return np.dot(self._v, self._v)

    ##############################################

    @property
    def magnitude(self):
        """Return the magnitude of the vector"""
        # Note: To avoid float overflow use
        #   abs(x) * sqrt(1 + (y/x)**2)  if x > y
        return math.sqrt(self.magnitude_square)

    ##############################################

    @property
    def orientation(self):

        """Return the orientation in degree"""

        #
        # 2 | 1
        # - + -
        # 4 | 3
        #
        #       | 1    | 2         | 3    | 4         |
        # x     | +    | -         | +    | -         |
        # y     | +    | +         | -    | -         |
        # tan   | +    | -         | -    | +         |
        # atan  | +    | -         | -    | +         |
        # theta | atan | atan + pi | atan | atan - pi |
        #

        if not bool(self):
            raise NameError("Null Vector")
        if self.x == 0:
            return math.copysign(90, self.y)
        elif self.y == 0:
            return 0 if self.x >= 0 else 180
        else:
            orientation = math.degrees(math.atan(self.tan))
            if self.x < 0:
                if self.y > 0:
                    orientation += 180
                else:
                    orientation -= 180
            return orientation

    ##############################################

    def rotate(self, angle, counter_clockwise=True):

        """Return a new vector equal to self rotated of angle degree in the counter clockwise direction

        """

        radians = math.radians(angle)
        if not counter_clockwise:
            radians = -radians
        c = math.cos(radians)
        s = math.sin(radians)

        # Fixme: np matrice
        xp = c * self._v[0] - s * self._v[1]
        yp = s * self._v[0] + c * self._v[1]

        return self.__class__((xp, yp))

    ##############################################

    @property
    def normal(self):

        """Return a new vector equal to self rotated of 90 degree in the counter clockwise direction

        """

        xp = -self._v[1]
        yp =  self._v[0]

        return self.__class__((xp, yp))

    ##############################################

    @property
    def anti_normal(self):

        """Return a new vector equal to self rotated of 90 degree in the clockwise direction

        """

        xp =  self._v[1]
        yp = -self._v[0]

        return self.__class__((xp, yp))

    ##############################################

    @property
    def permute(self):

        """Return a new vector where x and y are permuted.

        """

        xp = self._v[1]
        yp = self._v[0]

        return self.__class__((xp, yp))

    ##############################################

    @property
    def parity(self):

        """Return a new vector equal to self rotated of 180 degree

        """

        # parity
        xp = -self._v[0]
        yp = -self._v[1]

        return self.__class__((xp, yp))

    ##############################################

    @property
    def tan(self):
        """Return the tangent"""
        # RuntimeWarning: divide by zero encountered in double_scalars
        return self.y / self.x

    ##############################################

    @property
    def inverse_tan(self):
        """Return the inverse tangent"""
        return self.x / self.y

    ##############################################

    def dot(self, other):
        """Return the dot product of self with other"""
        return float(np.dot(self._v, other.v))

    ##############################################

    def cross(self, other):
        """Return the cross product of self with other"""
        return float(np.cross(self._v, other.v))

    ##############################################

    # perp dot product
    #   perp = (-y1, x1)
    #   perp dot = -y1*x2 + x1*y2 = x1*y2 - x2*y1

    perp_dot = cross

    ##############################################

    def is_parallel(self, other, return_cross=False):
        """Self is parallel with other"""

        cross = self.cross(other)
        test = round(cross, 7) == 0
        if return_cross:
            return test, cross
        else:
            return test

    ##############################################

    def is_orthogonal(self, other):
        """Self is orthogonal with other"""
        return round(self.dot(other), 7) == 0

    ##############################################

    def cos_with(self, direction):
        """Return the cosinus of self with direction"""
        cos = direction.dot(self) / (direction.magnitude * self.magnitude)
        return trignometric_clamp(cos)

    ##############################################

    def projection_on(self, direction):
        """Return the projection of self on direction"""
        return direction.dot(self) / direction.magnitude

    ##############################################

    def sin_with(self, direction):

        """Return the sinus of self with other"""

        # turn from direction to self
        sin = direction.cross(self) / (direction.magnitude * self.magnitude)

        return trignometric_clamp(sin)

    ##############################################

    def deviation_with(self, direction):
        """Return the deviation of self with other"""
        return direction.cross(self) / direction.magnitude

    ##############################################

    def angle_with(self, direction):

        """Return the angle of self on direction"""

        angle = math.acos(self.cos_with(direction))
        angle_sign = sign(self.sin_with(direction))

        return angle_sign * math.degrees(angle)

    orientation_with = angle_with

####################################################################################################

class Vector2D(Vector2DFloatBase):

    """2D Vector"""

    ##############################################

    @classmethod
    def from_list(cls, coordinates):
        return [cls(*xy) for xy in coordinates]

    ##############################################

    @classmethod
    def from_coordinates(cls, *coordinates):
        return cls.from_list(coordinates)

    ##############################################

    @staticmethod
    def from_angle(angle):

        """Create the unitary vector (cos(angle), sin(angle)).  *angle* is in degree."""

        rad = math.radians(angle)

        return Vector2D((math.cos(rad), math.sin(rad))) # Fixme: classmethod

    ##############################################

    @staticmethod
    def from_polar(radius, angle):

        """Create the polar vector (radius*cos(angle), radius*sin(angle)).  *angle* is in degree."""

        return Vector2D.from_angle(angle) * radius # Fixme: classmethod

    ##############################################

    @staticmethod
    def from_ellipse(radius_x, radius_y, angle):

        """Create the vector (radius_x*cos(angle), radius_y*sin(angle)).  *angle* is in degree."""

        angle = math.radians(angle)
        x = radius_x * math.cos(angle)
        y = radius_y * math.sin(angle)

        return Vector2D(x, y) # Fixme: classmethod

    ##############################################

    @staticmethod
    def middle(p0, p1):
        """Return the middle point."""
        return Vector2D(p0 + p1) * .5 # Fixme: classmethod

    ##############################################

    def __mul__(self, scale):
        """Return a new vector equal to the self scaled by scale"""
        return self.__class__(scale * self._v) # Fixme: Vector2D ?

    ##############################################

    def __rmul__(self, scale):
        """Return a new vector equal to the self scaled by scale"""
        return self.__mul__(scale)

    ##############################################

    def __imul__(self, scale):
        """Scale self by scale"""
        self._v *= scale
        return self

    ##############################################

    def __truediv__(self, scale):
        """Return a new vector equal to the self dvivided by scale"""
        return self.__class__(self._v / scale)

    ##############################################

    def __itruediv__(self, scale):
        """Scale self by 1/scale"""
        self._v /= scale
        return self

    ##############################################

    def scale(self, scale_x, scale_y):
        """Scale self by scale"""
        obj = self.clone()
        obj._v *= np.array((scale_x, scale_y))
        return obj

    ##############################################

    def divide(self, scale_x, scale_y):
        """Scale self by 1/scale"""
        obj = self.clone()
        obj._v /= np.array((scale_x, scale_y))
        return obj

    ##############################################

    def normalise(self):
        """Normalise the vector"""
        self._v /= self.magnitude
        return self

    ##############################################

    def to_normalised(self):
        """Return a normalised vector"""
        return NormalisedVector2D(self._v / self.magnitude)

    ##############################################

    def rint(self):
        return Vector2DInt(np.rint(self._v))

####################################################################################################

class NormalisedVector2D(Vector2DFloatBase):

    """2D Normalised Vector"""

    ##############################################

    def __init__(self, *args):

        super(NormalisedVector2D, self).__init__(*args)

        #! if self.magnitude != 1.:
        #!     raise ValueError("Magnitude != 1")

        # if not (is_in_trignometric_range(self.x) and
        #         is_in_trignometric_range(self.y)):
        #     raise ValueError("Values must be in trignometric range")

    ##############################################

    def __mul__(self, scale):
        """ Return a new vector equal to the self scaled by scale """
        return self.__class__(scale * self._v) # Fixme: Vector2D ?

    ##############################################

    def __rmul__(self, scale):
        """ Return a new vector equal to the self scaled by scale """
        return self.__mul__(scale)

####################################################################################################

class HomogeneousVector2D(Vector2D):

    """2D Homogeneous Coordinate Vector"""

    ##############################################

    def __init__(self, vector):

        # self._v = np.ones((3), dtype=self.__data_type__)
        # self._v[:2] = vector.v[:2]

        self._v = np.array(vector[:2]) # to keep compatibility
        self._w = 1

    ##############################################

    @property
    def v(self):
        return np.array(((self.x), (self.y), (self._w)), dtype=self.__data_type__)

    # @v.setter
    # def v(self, value):
    #     self._v = value

    @property
    def w(self):
        return self._w

    @w.setter
    def w(self, value):
        self._w = value

    ##############################################

    def to_vector(self):
        return Vector2D(self._v)
