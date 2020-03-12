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

__all__ = []

####################################################################################################

from enum import Enum, auto

####################################################################################################

class BedType(Enum):
    FlatBed = auto()
    CylinderBed = auto()
    PostBed = auto()
    OffTheArm = auto()

class OffTheArmType(Enum):
    Parallel = auto() # to the machine
    Perpendicular = auto()

# long arm
# feed-off-the-arm
# cutter

####################################################################################################

class SewingMachine:

    """Class to define a sewing machine"""

    ##############################################

    def __init__(self, **kwargs):

        self._name = str(kwargs.get('name', None))
        self._description = str(kwargs.get('description', None))

        self._stitche_types = list(kwargs.get('sitche_types', None)) # StitchType
        self._number_of_needles = int(kwargs.get('number_of_needles', None))
        self._number_of_loopers = int(kwargs.get('number_of_loopers', None))

        self._max_sewing_speed = float(kwargs.get('max_sewing_speed', None)) # [stitch/min]

        self._stitch_length = kwargs.get('sitch_length', None) # Fixme: range [mm]
        self._stitch_width = kwargs.get('sitch_width', None) # Fixme: range [mm]

        self._feed_system = str(kwargs.get('feed_system', None))
        # Gathering 1:x , Stretching 1:y
        self._differential_feed_ratio = kwargs.get('differential_feed_ratio', None)

        self._needle_gauge = float(kwargs.get('needle_gauge', None)) # [mm]
        self._needle_system = str(kwargs.get('needle_system', None))

        self._overedging_width = float(kwargs.get('overedging_width', None)) # [mm]

    ##############################################

    @property
    def name(self):
        return self._name

    @property
    def description(self):
        return self._description

####################################################################################################

class NeedleType:

    """Class to define a needle type"""

    ##############################################

    def __init__(self, name, description, fabric_use):

        self._name = name
        self._description = description
        self._fabric_use = fabric_use

    ##############################################

    @property
    def name(self):
        return self._name

    @property
    def description(self):
        return self._description

    @property
    def fabric_use(self):
        return self._fabric_use

####################################################################################################

class Needle:

    """Class to define a needle"""

    ##############################################

    def __init__(self, system, needle_type, nm_size, multiplicity=1):

        self._system = system
        self._type = needle_type
        self._nm_size = nm_size
        self._multiplicity = multiplicity # twin, triple

        # quality grade e.g. chrome

    ##############################################

    @property
    def system(self):
        return self._system

    @property
    def type(self):
        return self._type

    @property
    def size(self):
        return self._size

    @property
    def multiplicity(self):
        return self._multiplicity
