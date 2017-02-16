####################################################################################################
#
# -
# Copyright (C) 2015 Fabrice Salvaire
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

import math

import numpy as np

####################################################################################################

from Valentina.Math.Functions import sign, trignometric_clamp #, is_in_trignometric_range

####################################################################################################

class Vector2DBase(object):

    __data_type__ = None

    #######################################

    def __init__(self, *args):

        """
        Example of usage::

          Vector(1, 3)
          Vector((1, 3))
          Vector([1, 3])
          Vector(iterable)
          Vector(vector)

        """

        array = self._check_arguments(args)

        # Fixme: self._v
        # call __getitem__ once
        self.v = np.array(array[:2], dtype=self.__data_type__)

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

    #######################################

    @property
    def x(self):
        return self.__data_type__(self.v[0])

    @property
    def y(self):
        return self.__data_type__(self.v[1])

    @x.setter
    def set_x(self, x):
        self.v[0] = x

    @y.setter
    def set_y(self, y):
        self.v[1] = y

    #######################################

    def copy(self):

        """ Return a copy of self """

        return self.__class__(self.v)

    #######################################

    def __repr__(self):

        # return str(self.__class__) + ' ' + str(self.v)
        return 'Vector ' + str(self.v)

    #######################################

    def __nonzero__(self):

        return bool(self.v.any())

    #######################################

    def __len__(self):

        return 2

    #######################################

    def __iter__(self):

        return iter(self.v)

    #######################################

    def __getitem__(self, a_slice):

        return self.v[a_slice]

    #######################################

    def __setitem__(self, index, value):

        self.v[index] = value

    #######################################

    def __eq__(v1, v2):

        """ self == other """

        # return v1.v == v2.v
        return v1.x == v2.x and v1.y == v2.y

    #######################################

    def __add__(self, other):

        """ Return a new vector equal to the addition of self and other """

        return self.__class__(self.v + other.v)

    #######################################

    def __iadd__(self, other):

        """ Add other to self """

        self.v += other.v

        return self

    #######################################

    def __sub__(self, other):

        """ Return a new vector """

        return self.__class__(self.v - other.v)

    #######################################

    def __isub__(self, other):

        """ Return a new vector equal to the subtraction of self and other """

        self.v -= other.v

        return self

    ##############################################

    def to_int_list(self):

        return [int(x) for x in self.v]

####################################################################################################

class Vector2DInt(Vector2DBase):

    __data_type__ = np.int

####################################################################################################

class Vector2DFloatBase(Vector2DBase):

    __data_type__ = np.float

    #######################################

    def almost_equal(v1, v2, n=7):

        """ self ~= other """

        espilon = 10**(-n)

        return v1.x - v1.x < espilon and v2.y - v2.y < espilon

    #######################################

    def magnitude_square(self):

        """ Return the square of the magnitude of the vector """

        return np.dot(self.v, self.v)

    #######################################

    def magnitude(self):

        """ Return the magnitude of the vector """

        return math.sqrt(self.magnitude_square())

    #######################################

    def orientation(self):

        """ Return the orientation in degree """

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
            orientation = math.degrees(math.atan(self.tan()))
            if self.x < 0:
                if self.y > 0:
                    orientation += 180
                else:
                    orientation -= 180
            return orientation

    #######################################

    def rotate_counter_clockwise(self, angle):

        """ Return a new vector equal to self rotated of angle degree in the counter clockwise
        direction
        """

        radians = math.radians(angle)
        c = math.cos(radians)
        s = math.sin(radians)

        # Fixme: np matrice
        xp = c * self.v[0] -s * self.v[1]
        yp = s * self.v[0] +c * self.v[1]

        return self.__class__((xp, yp))

    #######################################

    def rotate_counter_clockwise_90(self):

        """ Return a new vector equal to self rotated of 90 degree in the counter clockwise
        direction
        """

        xp = -self.v[1]
        yp =  self.v[0]

        return self.__class__((xp, yp))

    #######################################

    def rotate_clockwise_90(self):

        """ Return a new vector equal to self rotated of 90 degree in the clockwise direction
        """

        xp =  self.v[1]
        yp = -self.v[0]

        return self.__class__((xp, yp))

    #######################################

    def rotate_180(self):

        """ Return a new vector equal to self rotated of 180 degree
        """

        # parity
        xp = -self.v[0]
        yp = -self.v[1]

        return self.__class__((xp, yp))

    #######################################

    def tan(self):

        """ Return the tangent """

        # RuntimeWarning: divide by zero encountered in double_scalars
        return self.y / self.x

    #######################################

    def inverse_tan(self):

        """ Return the inverse tangent """

        return self.x / self.y

    #######################################

    def dot(self, other):

        """ Return the dot product of self with other """

        return float(np.dot(self.v, other.v))

    #######################################

    def cross(self, other):

        """ Return the cross product of self with other """

        return float(np.cross(self.v, other.v))

    #######################################

    def is_parallel(self, other):

        """ Self is parallel with other """

        return round(self.cross(other), 7) == 0

    #######################################

    def is_orthogonal(self, other):

        """ Self is orthogonal with other """

        return round(self.dot(other), 7) == 0

    #######################################

    def cos_with(self, direction):

        """ Return the cosinus of self with direction """

        cos = direction.dot(self) / (direction.magnitude() * self.magnitude())

        return trignometric_clamp(cos)

    #######################################

    def projection_on(self, direction):

        """ Return the projection of self on direction """

        return direction.dot(self) / direction.magnitude()

    #######################################

    def sin_with(self, direction):

        """ Return the sinus of self with other """

        # turn from direction to self
        sin = direction.cross(self) / (direction.magnitude() * self.magnitude())

        return trignometric_clamp(sin)

    #######################################

    def deviation_with(self, direction):

        """ Return the deviation of self with other """

        return direction.cross(self) / direction.magnitude()

    #######################################

    def orientation_with(self, direction):

        # Fixme: check all cases
        # -> angle_with

        """ Return the angle of self on direction """

        angle = math.acos(self.cos_with(direction))
        angle_sign = sign(self.sin_with(direction))

        return angle_sign * math.degrees(angle)

####################################################################################################

class Vector2D(Vector2DFloatBase):

    """ 2D Vector """

    #######################################

    @staticmethod
    def from_angle(angle):

        """ Create the unitary vector (cos(angle), sin(angle)).  The *angle* is in degree. """

        rad = math.radians(angle)

        return Vector2D((math.cos(rad), math.sin(rad)))

    #######################################

    @staticmethod
    def middle(p0, p1):

        """ Return the middle point. """

        return Vector2D(p0 + p1) * .5

    #######################################

    def __mul__(self, scale):

        """ Return a new vector equal to the self scaled by scale """

        return self.__class__(scale * self.v)

    #######################################

    def __imul__(self, scale):

        """ Scale self by scale """

        self.v *= scale

        return self

    #######################################

    def __truediv__(self, scale):

        """ Return a new vector equal to the self dvivided by scale """

        return self.__class__(self.v / scale)

    #######################################

    def __itruediv__(self, scale):

        """ Scale self by 1/scale """

        self.v /= scale

        return self

    #######################################

    def normalise(self):

        """ Normalise the vector """

        self.v /= self.magnitude()

    #######################################

    def to_normalised(self):

        """ Return a normalised vector """

        return NormalisedVector2D(self.v / self.magnitude())

    #######################################

    def rint(self):

        return Vector2DInt(np.rint(self.v))

####################################################################################################

class NormalisedVector2D(Vector2DFloatBase):

    """ 2D Normalised Vector """

    #######################################

    def __init__(self, *args):

        super(NormalisedVector2D, self).__init__(*args)

        #! if self.magnitude() != 1.:
        #!     raise ValueError("Magnitude != 1")

        # if not (is_in_trignometric_range(self.x) and
        #         is_in_trignometric_range(self.y)):
        #     raise ValueError("Values must be in trignometric range")

    #######################################

    def __mul__(self, scale):

        """ Return a new vector equal to the self scaled by scale """

        return Vector2D(scale * self.v)
