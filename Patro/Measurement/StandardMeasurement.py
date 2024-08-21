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

####################################################################################################

from typing import Iterator

####################################################################################################

class Measurement:

    """Class to define a measurement."""

    ##############################################

    def __init__(self, name: str, full_name: str, description: str, default_value: int | float=0) -> None:
        self._name = name
        self._full_name = full_name
        self._description = description
        self._default_value = default_value

    ##############################################

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value

    ##############################################

    @property
    def full_name(self) -> str:
        return self._full_name

    @full_name.setter
    def full_name(self, value: str) -> None:
        self._full_name = value

    ##############################################

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, value: str) -> None:
        self._description = value

    ##############################################

    @property
    def default_value(self) -> int | float:
        return self._default_value

    @default_value.setter
    def default_value(self, value: str) -> None:
        self._default_value = value

####################################################################################################

class StandardMeasurement:

    """Class to define a set of measurements."""

    ##############################################

    def __init__(self) -> None:
        self._names = {}

    ##############################################

    def __len__(self) -> int:
        return len(self._names)

    ##############################################

    def __iter__(self) -> Iterator[Measurement]:
        return iter(self._names.values())

    ##############################################

    def __getitem__(self, name: str) -> Measurement:
        return self._names[name]

    ##############################################

    def __contains__(self, name: str) -> bool:
        return name in self._names

    ##############################################

    def add(self, measurement: Measurement) -> None:
        if measurement.name not in self._names:
            self._names[measurement.name] = measurement
        else:
            raise NameError(f'{measurement.name} is already registered')

    ##############################################

    def dump(self) -> None:
        template = '''{0.name}
- {0.full_name}
- {0.description}
- {0.default_value}
'''
        for measurement in self:
            print(template.format(measurement))
