####################################################################################################
#
# PyValentina - A Python implementation of Valentina Pattern Drafting Software
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

def bounding_box_from_points(points):

    bounding_box = points[0].bounding_box()
    for point in points[1:]:
        bounding_box |= point.bounding_box()
    return bounding_box

####################################################################################################

class Primitive:

    __dimension__ = None

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

    def iter_on_points(self):
        for point in self.start_point, self.start_point:
            yield point
