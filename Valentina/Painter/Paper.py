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

from math import sqrt

####################################################################################################

class PaperSize:

    ##############################################

    def __init__(self, size_name, orientation, margin):

        self._size_name = size_name

        if orientation not in ('portrait', 'landscape'):
            raise ValueError
        self._orientation = orientation

        self._margin = margin

        # ISO 216 / ISO 269
        # A0 841 × 1189 -> 594 × 841
        # B0 1000 × 1414 -> 707 × 1000
        # C0 917 × 1297 -> 648 × 917

        letter_to_dimension = {
            'a': 1189,
            'b': 1414,
            'c': 1297
            }

        size_name = size_name.lower()
        letter = size_name[0]
        level = int(size_name[1:])
        if letter in ('a', 'b', 'c'):
            if level < 0 or level > 10:
                raise ValueError
            scale = sqrt(2)**level
            height = letter_to_dimension[letter] / scale
            width = height / sqrt(2)
        if orientation == 'landscape':
            height, width = width, height
        self._height = height
        self._width = width

    ##############################################

    @property
    def size_name(self):
        return self._size_name

    @property
    def orientation(self):
        return self._orientation

    @property
    def height(self):
        return self._height

    @property
    def width(self):
        return self._width

    @property
    def margin(self):
        return self._margin
