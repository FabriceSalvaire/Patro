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

__all__ = [
    'FabricType',
    'Fabric',
    'WovenFabric',
]

####################################################################################################

from enum import Enum, auto

####################################################################################################

class FabricType(Enum):

    # Woven fabrics are produced by interlacement of two sets of yarn: warp yarn and weft yarn.
    WovenFabric = auto()

    # Knitted fabrics are produced by one sets of yarn by interlooping.
    KnittedFabric = auto()

    # Non-woven fabrics are produced by connecting yarn with gummy bonded materials. It can be done
    # in mechanical, chemical or thermal ways.
    NonWovenFabric = auto()

    # For Braided fabrics, at least three sets of yarn is required. Fabric is produced diagonal
    # interlacement/interwining/twisting.
    BraidedFabric = auto()

####################################################################################################

class WeaveType:

    # In plain weave cloth, the warp and weft threads cross at right angles, aligned so they form a
    # simple criss-cross pattern. Each weft thread crosses the warp threads by going over one, then
    # under the next, and so on. The next weft thread goes under the warp threads that its neighbour
    # went over, and vice versa.
    Plain = auto()

    # The satin weave is characterized by four or more fill or weft yarns floating over a warp yarn,
    # four warp yarns floating over a single weft yarn.
    Satin = auto()

    # Twill is a type of textile weave with a pattern of diagonal parallel ribs (in contrast with a
    # satin and plain weave). This is done by passing the weft thread over one or more warp threads
    # then under two or more warp threads and so on, with a "step," or offset, between rows to
    # create the characteristic diagonal pattern. Because of this structure, twill generally drapes
    # well.
    Twill = auto()

####################################################################################################

def FloatPair(x, y):
    return [float(x), float(y)]

####################################################################################################

class Fabric:

    """Class to define a fabric"""

    __fabric_type__ = None

    # 1 dyn = 1 g⋅cm/s^2 = 10 µN
    BENDING_UNIT = 'dyn⋅cm'
    # grain-force 1 grf = 635.4602 µN
    STRETCH_UNIT = 'dyn/cm' # 'grf/cm' ???
    SHEAR_UNIT = 'dyn/cm' # 'grf/cm' ???
    FRICTION_UNIT = None
    THICKNESS_UNIT = 'mm'
    WEIGTH_UNIT = 'g/m^2'
    SHRINKAGE_UNIT = '%'
    PRESSURE_UNIT = 'bar' # psi

    ##############################################

    def __init__(self, **kwargs):

        self._bending = FloatPair(*kwargs['bending'])
        self._stretch = FloatPair(*kwargs['stretch'])
        self._shear = float(kwargs['shear'])
        self._fiction = float(kwargs['friction'])
        self._weight = float(kwargs['weight'])
        self._shrinkage = FloatPair(kwargs.get('shrinkage', (0, 0)))
        self._pressure = float(kwargs['pressure'])

        # texture attributes
        # flip
        # angle
        # offset (x, y)

####################################################################################################

class WovenFabric(Fabric):

    """Class to define a woven fabric"""

    __fabric_type__ = FabricType.WovenFabric

    ##############################################

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        # self._warp_yarn
        # self._weft_yarn
