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

####################################################################################################

from math import sqrt

####################################################################################################

class PaperSize:

    """Class to implements ISO 216 / ISO 269 paper size."""

    # A0  841 × 1189 -> 594 ×  841
    # B0 1000 × 1414 -> 707 × 1000
    # C0  917 × 1297 -> 648 ×  917
    LETTER_TO_DIMENSION = {
        'A': 1189,
        'B': 1414,
        'C': 1297
    }

    ##############################################

    def __init__(self, name, orientation, margin):

        name = name.upper()
        letter = name[0]
        level = int(name[1:])
        if letter not in ('A', 'B', 'C'):
            raise ValueError
        if level < 0 or level > 10:
            raise ValueError
        self._name = name

        if orientation not in ('portrait', 'landscape'):
            raise ValueError
        self._orientation = orientation

        self._margin = float(margin)

        SQRT_2 = sqrt(2)
        scale = SQRT_2**level
        height = self.LETTER_TO_DIMENSION[letter] / scale
        width = height / SQRT_2
        if orientation == 'landscape':
            height, width = width, height
        self._height = height
        self._width = width

    ##############################################

    @property
    def name(self):
        return self._name

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
    def height_in(self):
        return self._height / 25.4

    @property
    def width_in(self):
        return self._width / 25.4

    @property
    def margin(self):
        return self._margin
