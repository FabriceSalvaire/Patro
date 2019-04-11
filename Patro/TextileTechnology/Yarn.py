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

__all__ = ['Yarn']

####################################################################################################

from enum import Enum, auto

####################################################################################################

def tex2den(x):
    return x*9

def den2tex(x):
    return x*10/9

def tex2nm(x):
    return 1000/x

def nm2tex(x):
    return 1000*x

####################################################################################################

class TwistType(Enum):

    """When the yarn is held in a vertical position, the twist of yarn which is spirals in the line
    with the central portion of the letter S or Z is known as S-Twist or Z-Twist.

    """

    S = auto()
    Z = auto()

####################################################################################################

class Yarn:

    """Class to define yarn / thread"""

    ##############################################

    def __init__(self, fiber, color, tex, twist_type=None):

        # twist_per_m
        # retor

        self._fiber = str(fiber) # composition ?
        self._color = color # Fixme: multicolor ? data type ?
        self._tex = float(tex) # g/km
        self._twist_type = TwistType(twist_type)

    ##############################################

    @property
    def fiber(self):
        return self._fiber

    @property
    def color(self):
        return self._color

    ##############################################

    @property
    def tex(self):
        '''Return the weight of the thread in gram for a length of 1 km'''
        return self._tex

    @property
    def denier(self):
        '''Return the weight of the thread in gram for a length of 9 km'''
        return tex2den(self._tex)

    @property
    def nm(self):
        '''Return the metric number, number of meters per gram of thread'''
        return tex2nm(self._tex)

    ##############################################

    @property
    def twist_type(self):
        return self._twist_type
