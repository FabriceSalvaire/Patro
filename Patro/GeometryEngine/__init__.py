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

"""This module implements a 2D geometry engine suitable for a low number of graphic entities. It
implements standard primitives like line, segment and Bezier curve.

"""

####################################################################################################

from .Primitive import Primitive2DMixin
from .Vector import Vector2D

####################################################################################################

# Fixme: to fix cyclic import issue
Primitive2DMixin.__vector_cls__ = Vector2D
