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

__all__ = ['Fiber', 'FiberDatabase']

####################################################################################################

from enum import Enum, auto

from .Database import Database

####################################################################################################

class FiberType(Enum):

    Animal = auto()
    Natural = auto()
    Plant = auto()
    Synthetic = auto()

####################################################################################################

class Fiber:

    """Class to define a textile fiber"""

    ##############################################

    def __init__(self, name, fiber_type, source_type, source):

        self._name = str(name)
        self._fiber_type = FiberType(fiber_type)
        self._source_type = str(source_type)
        self._source = str(source)

    ##############################################

    @property
    def name(self):
        return self._name

    @property
    def fiber_type(self):
        return self._fiber_type

    @property
    def source_type(self):
        return self._source_type

    @property
    def source(self):
        return self._source

####################################################################################################

class FiberDatabase(Database):

    DEFAULT_DATA_FILENAME = 'fiber.yaml'

    ##############################################

    def load(self, yaml_path=None):

        data = super().load(yaml_path)

        natural_fibers = data['Natural Fibers']
        for name, item in natural_fibers['Plant Fibers'].items():
            self.add(Fiber(name, FiberType.Natural, FiberType.Plant, item['source']))
        for name, item in natural_fibers['Animal Fibers'].items():
            self.add(Fiber(name, FiberType.Natural, FiberType.Animal, item['source']))

        synthetic_fibers = data['Synthetic Fibers']
        for name, item in synthetic_fibers.items():
            self.add(Fiber(name, FiberType.Synthetic, None, None))
