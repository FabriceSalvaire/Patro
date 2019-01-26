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

r"""Module to implement transformations like scale, rotation and translation.

Transformation matrices
-----------------------

To transform a vector, we multiply the vector with a transformation matrix

.. math::
     \begin{pmatrix} x' \\ y' \end{pmatrix} = \mathbf{T} \begin{pmatrix} x \\ y \end{pmatrix}

Usual transformation matrices in 2D are

.. math::
    \begin{align}
    \mathbf{Id} &= \begin{bmatrix}
      1 & 0 \\
      0 & 1
    \end{bmatrix} \\[1em]
    \mathbf{Scale}(s_x, s_y) &= \begin{bmatrix}
       s_x & 0 \\
       0   & s_y
    \end{bmatrix} \\[1em]
    \mathbf{Rotation}(\theta) &= \begin{bmatrix}
       \cos\theta & \sin\theta \\
      -\sin\theta & \cos\theta
    \end{bmatrix} \\[1em]
    \end{align}

For translation and affine transformation, we must introduce the concept of homogeneous coordinate
which add a virtual third dimension:

.. math::
    \mathbf{V} = \begin{bmatrix}
       x \\
       y \\
       1
    \end{bmatrix}

Then the translation and affine transformation matrix are expressed as:

.. math::
    \begin{align}
    \mathbf{Translation}(t_x, t_y) &= \begin{bmatrix}
       1 & 0 & t_x \\
       0 & 1 & t_y \\
       0 & 0 & 1
    \end{bmatrix} \\[1em]
    \mathbf{Generic} &= \begin{bmatrix}
       r_{11} & r_{12} & t_x \\
       r_{12} & r_{22} & t_y \\
       0 & 0 & 1
    \end{bmatrix}
    \end{align}

To compose transformations, we must multiply the transformations in this order:

.. math::
     \mathbf{T} = \mathbf{T_n} \ldots \mathbf{T_2} \mathbf{T_1}

Note the matrix multiplication is not commutative.

"""

####################################################################################################

__all__ = [
    'TransformationType',
    'Transformation',
    'Transformation2D',
    'AffineTransformation',
    'AffineTransformation2D',
]

####################################################################################################

from enum import Enum, auto
from math import sin, cos, radians, degrees

import numpy as np

from .Vector import Vector2D, HomogeneousVector2D

####################################################################################################

class TransformationType(Enum):

    Identity = auto()

    Scale = auto() # same scale factor across axes
    Shear = auto() # different scale factor

    Parity = auto()
    XParity = auto()
    YParity = auto()

    Rotation = auto()

    Translation = auto()

    Generic = auto()

####################################################################################################

class IncompatibleArrayDimension(ValueError):
    pass

####################################################################################################

class Transformation:

    __dimension__ = None
    __size__ = None

    ##############################################

    @classmethod
    def Identity(cls):
        return cls(np.identity(cls.__size__), TransformationType.Identity)

    ##############################################

    def __init__(self, obj, transformation_type=TransformationType.Generic):

        if isinstance(obj, Transformation):
            if self.same_dimension(obj):
                array = obj.array # *._m
            else:
                raise IncompatibleArrayDimension
        elif isinstance(obj, np.ndarray):
            if obj.shape == (self.__size__, self.__size__):
                array = obj
            else:
                raise IncompatibleArrayDimension
        elif isinstance(obj, (list, tuple)):
            if len(obj) == self.__size__ **2:
                array = np.array(obj)
                array.shape = (self.__size__, self.__size__)
            else:
                raise IncompatibleArrayDimension
        else:
            array = np.array((self.__size__, self.__size__))
            array[...] = obj

        self._m = np.array(array)
        self._type = transformation_type

    ##############################################

    @property
    def dimension(self):
        return self.__dimension__

    @property
    def size(self):
        return self._size

    @property
    def array(self):
        return self._m

    @property
    def type(self):
        return self._type

    @property
    def is_identity(self):
        return self._type == TransformationType.Identity

    ##############################################

    def __repr__(self):
        return self.__class__.__name__ + str(self._m)

    ##############################################

    def to_list(self):
        return list(self._m.flat)

    ##############################################

    def same_dimension(self, other):
        return self.__size__ == other.dimension

    ##############################################

    def _mul_type(self, obj):

        # Fixme: check matrix value ???
        #   usage identity/rotation, scale/parity test
        #   metric test ?
        # if t in (parity, xparity, yparity) t*t = Id
        # if t in (rotation, scale) t*t = t

        if self._type == obj._type:
            if self._type in (
                    TransformationType.Parity,
                    TransformationType.XParity,
                    TransformationType.YParity
            ):
                return TransformationType.Identity
            elif self._type not in (TransformationType.Rotation, TransformationType.Scale):
                return TransformationType.Generic
        else: # shear, generic
            return TransformationType.Generic

    #######################################

    def __mul__(self, obj):

        if isinstance(obj, Transformation):
            # T = T1 * T2
            array = np.matmul(self._m, obj.array)
            return self.__class__(array, self._mul_type(obj))
        elif isinstance(obj, Vector2D):
            array = np.matmul(self._m, np.transpose(obj.v))
            return Vector2D(array)
        elif isinstance(obj, (int, float)):
            # Scalar can only be scaled if the frame is not sheared
            if self._type in (TransformationType.Identity, TransformationType.Rotation):
                return obj
            elif self._type not in (TransformationType.Shear, TransformationType.Generic):
                return abs(self._m[0,0]) * obj
            else:
                raise ValueError('Transformation is sheared')
        else:
            raise ValueError

    #######################################

    def __imul__(self, obj):

        if isinstance(obj, Transformation):
            if obj.type != TransformationType.Identity:
                # (T = T1) *= T2
                # T = T2 * T1
                # order is inverted !
                self._m = np.matmul(obj.array, self._m)
                self._type = self._mul_type(obj)
        else:
            raise ValueError

        return self

####################################################################################################

class Transformation2D(Transformation):

    __dimension__ = 2
    __size__ = 2

    ##############################################

    @classmethod
    def Rotation(cls, angle):

        angle = radians(angle)
        c = cos(angle)
        s = sin(angle)

        return cls(np.array(((c, -s), (s,  c))), TransformationType.Rotation)

    ##############################################

    @classmethod
    def type_for_scale(cls, x_scale, y_scale):

        if x_scale == y_scale:
            if x_scale == 1:
                transformation_type = TransformationType.Identity
            elif x_scale == -1:
                transformation_type = TransformationType.Parity
            else:
                transformation_type = TransformationType.Scale
        else:
            if x_scale == -1 and y_scale == 1:
                transformation_type = TransformationType.XParity
            elif x_scale == 1 and y_scale == -1:
                transformation_type = TransformationType.YParity
            else:
                transformation_type = TransformationType.Shear

        return transformation_type

    ##############################################

    @classmethod
    def Scale(cls, x_scale, y_scale=None):
        if y_scale is None:
            y_scale = x_scale
        transformation_type = cls.type_for_scale(x_scale, y_scale)
        return cls(np.array(((x_scale, 0), (0,  y_scale))), transformation_type)

    ##############################################

    @classmethod
    def Parity(cls):
        return cls.Scale(-1, -1)

    ##############################################

    @classmethod
    def XReflection(cls):
        return cls.Scale(-1, 1)

    ##############################################

    @classmethod
    def YReflection(cls):
        return cls.Scale(1, -1)

####################################################################################################

class AffineTransformation(Transformation):

    ##############################################

    @classmethod
    def Translation(cls, vector):

        transformation = cls.Identity()
        transformation.translation_part[...] = vector.v[...]
        transformation._type = TransformationType.Translation
        return transformation

    ##############################################

    @classmethod
    def RotationAt(cls, center, angle):

        # return cls.Translation(center) * cls.Rotation(angle) * cls.Translation(-center)

        transformation = cls.Translation(-center)
        transformation *= cls.Rotation(angle)
        transformation *= cls.Translation(center)
        return transformation

    ##############################################

    @property
    def matrix_part(self):
        return self._m[:self.__dimension__,:self.__dimension__]

    @property
    def translation_part(self):
        return self._m[:self.__dimension__,-1]

####################################################################################################

class AffineTransformation2D(AffineTransformation):

    __dimension__ = 2
    __size__ = 3

    ##############################################

    @classmethod
    def Rotation(cls, angle):

        transformation = cls.Identity()
        transformation.matrix_part[...] = Transformation2D.Rotation(angle).array
        transformation._type = TransformationType.Rotation
        return transformation

    ##############################################

    @classmethod
    def Scale(cls, x_scale, y_scale):

        # Fixme: others, use *= ? (comment means ???)

        transformation = cls.Identity()
        transformation.matrix_part[...] = Transformation2D.Scale(x_scale, y_scale).array
        transformation._type = cls.type_for_scale(x_scale, y_scale)
        return transformation

    #######################################

    def __mul__(self, obj):

        if isinstance(obj, HomogeneousVector2D):
            array = np.matmul(self._m, obj.v)
            return obj.__class__(array)
        elif isinstance(obj, Vector2D):
            array = np.matmul(self._m, HomogeneousVector2D(obj).v)
            # return HomogeneousVector2D(array).to_vector()
            return Vector2D(array[:2])
        else:
            return super(AffineTransformation, self).__mul__(obj)

####################################################################################################

# The matrix to rotate an angle θ about the axis defined by unit vector (l, m, n) is
# l*l*(1-c) + c   , m*l*(1-c) - n*s , n*l*(1-c) + m*s
# l*m*(1-c) + n*s , m*m*(1-c) + c   , n*m*(1-c) - l*s
# l*n*(1-c) - m*s , m*n*(1-c) + l*s , n*n*(1-c) + c
