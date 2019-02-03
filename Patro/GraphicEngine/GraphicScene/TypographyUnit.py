####################################################################################################
#
# Patro - A Python library to make patterns for fashion design
# Copyright (C) 2018 Fabrice Salvaire
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

"""Module to implement common typography units.

"""

# See https://en.wikipedia.org/wiki/Point_(typography)

####################################################################################################

__all__ = [
 'InchUnit',
 'MmUnit',
 'PointUnit',
]

####################################################################################################

class TypographyUnit:

    INCH_2_MM        = 25.4  # 1 inch = 25.4 mm
    POINT_2_INCH     = 72    # 1 inch = 72 point   PostScript, CSS pt and TeX bp
    TEX_POINT_2_INCH = 72.27 # TeX pt
    PICA_2_POINT     = 12    # 1 pica = 12 point

    POINT_2_MM    = INCH_2_MM / POINT_2_INCH

    MM_2_INCH     = 1 / INCH_2_MM
    INCH_2_POINT  = 1 / POINT_2_INCH
    MM_2_POINT    = 1 / POINT_2_MM

    ##############################################

    def __init__(self, value):
        self._value = value

    ##############################################

    def __float__(self):
        return self._value

####################################################################################################

class MmUnit(TypographyUnit):

    def to_mm(self):
        return self

    def to_inch(self):
        return InchUnit(self._value * self.MM_2_Point)

    def to_point(self):
        return PointUnit(self._value * self.MM_2_POINT)

####################################################################################################

class InchUnit(TypographyUnit):

    def to_inch(self):
        return self

    def to_mm(self):
        return MmUnit(self._value * self.INCH_2_MM)

    def to_point(self):
        return PointUnit(self._value * self.INCH_2_POINT)

####################################################################################################

class PointUnit(TypographyUnit):

    def to_point(self):
        return self

    def to_mm(self):
        return MmUnit(self._value * self.POINT_2_MM)

    def to_inch(self):
        return InchUnit(self._value * self.POINT_2_INCH)
