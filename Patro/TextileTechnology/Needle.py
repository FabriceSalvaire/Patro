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

__all__ = ['NeedleSystem', 'NeedleType', 'Needle']

####################################################################################################

class NeedleSystem:

    """Class to define a needle system"""

    ##############################################

    def __init__(self, name, description):

        self._name = str(name)
        self._description = str(description)

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

        self._name = str(name)
        self._description = str(description)
        self._fabric_use = str(fabric_use) # Fixme: list ?

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

        self._system = system # NeedleSystem
        self._type = needle_type # NeedleType
        self._nm_size = int(nm_size)
        self._multiplicity = int(multiplicity) # twin, triple

        # quality grade e.g. chrome

    ##############################################

    @property
    def system(self):
        return self._system

    @property
    def type(self):
        return self._type

    @property
    def nm_size(self):
        return self._nm_size

    @property
    def multiplicity(self):
        return self._multiplicity
