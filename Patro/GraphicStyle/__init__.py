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

"""Module to define graphic styles like colours and stroke styles.

This module import :class:`Color.Colors`.

"""

####################################################################################################

__all__ = ['Colors', 'StrokeStyle', 'CapStyle', 'JoinStyle']

####################################################################################################

from enum import Enum, auto

#: Colour Database Singleton as an instance of :class:`ColorDataBase`
from .Color import Colors

####################################################################################################

class StrokeStyle(Enum):

     """Enum class to define stroke styles"""

     NoPen = auto() # Inivisble ?
     SolidLine = auto()
     DashLine =	auto()
     DotLine = auto()
     DashDotLine = auto()
     DashDotDotLine = auto()
     # Custom

####################################################################################################

class CapStyle(Enum):

     """Enum class to define cap styles"""

     #: a square line end that does not cover the end point of the line
     FlatCap = auto()
     #: a square line end that covers the end point and extends beyond it by half the line width
     SquareCap = auto()
     #: a rounded line end.
     RoundCap = auto()

####################################################################################################

class JoinStyle(Enum):

     """Enum class to define join styles"""

     #! The outer edges of the lines are extended to meet at an angle, and this area is filled.
     MiterJoin = auto()
     #: The triangular notch between the two lines is filled.
     BevelJoin = auto()
     #: A circular arc between the two lines is filled.
     RoundJoin = auto()
     #: A miter join corresponding to the definition of a miter join in the SVG 1.2 Tiny specification.
     SvgMiterJoin = auto()
