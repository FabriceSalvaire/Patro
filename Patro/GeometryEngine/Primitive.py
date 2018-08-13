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

class Primitive:

    """Base class for geometric primitive"""

    __dimension__ = None # in [2, 3] for 2D / 3D primitive

    ##############################################

    def clone(self):
        raise NotImplementedError

    ##############################################

    def bounding_box(self):
        # Fixme: infinite primitive
        raise NotImplementedError

    ##############################################

    @property
    def is_reversable(self):
        return False

    ##############################################

    def reverse(self):
        return self

####################################################################################################

class Primitive2D:
    __dimension__ = 2

####################################################################################################

class ReversablePrimitiveMixin:

    ##############################################

    @property
    def is_reversable(self):
        return True

    ##############################################

    def reverse(self):
        raise NotImplementedError

    ##############################################

    @property
    def start_point(self):
        raise NotImplementedError

    @property
    def end_point(self):
        raise NotImplementedError

    ##############################################

    def iter_on_points(self):
        for point in self.start_point, self.start_point:
            yield point
