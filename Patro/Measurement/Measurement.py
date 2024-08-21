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

__all__ = ['MeasurementSet', 'Measurement']

####################################################################################################

import logging
from pathlib import Path
from typing import Optional, Iterator

import sympy
import yaml

from .PersonalData import PersonalData

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class Measurement:

    """Class to define a measurement"""

    ##############################################

    def __init__(self,
                 measurements: 'MeasurementSet',
                 name: str,
                 value: int | float | str,
                 full_name: str = '',
                 description: str = '',
                 ) -> None:
        self._name = self._validate_name(name)
        self._measurements = measurements
        self._full_name = str(full_name)   # for human
        self._description = str(description)   # describe the purpose of the measurement
        if isinstance(value, (int, float)):
            self._expression = value
            self._evaluated_expression = value
            self._value = float(value)
        else:
            # https://docs.sympy.org/latest/modules/core.html#id1
            self._expression = sympy.sympify(str(value))
            self._evaluated_expression = None
            self._value = None

    ##############################################

    @staticmethod
    def _validate_name(name: str) -> str:
        name = str(name)
        name = name.replace(' ', '_')
        for c in name:
            # Valide characters are a-zA-Z0-9 _
            if not c.isalnum() and c != '_':
                raise ValueError(f'Invalid measurement name "{name}"')
        return name

    ##############################################

    def __repr__(self) -> str:
        return f'''
{self._name} = {self._expression}
  = {self.evaluated_expression}
  = {self.value}
'''

    ##############################################

    @property
    def name(self) -> str:
        return self._name

    @property
    def full_name(self) -> str:
        return self._full_name

    @property
    def description(self) -> str:
        return self._description

    @property
    def expression(self) -> sympy.core.expr.Expr:
        return self._expression

    ##############################################

    @property
    def evaluated_expression(self) -> sympy.core.expr.Expr:
        if self._evaluated_expression is None:
            # https://docs.sympy.org/latest/modules/core.html?highlight=subs#sympy.core.basic.Basic.subs
            # variable order doesn't matter, sympy do the job
            # self._evaluated_expression = self._expression.subs(self._measurements._expressions)
            self._evaluated_expression = self._measurements.subs(self)
        return self._evaluated_expression

    @property
    def value(self) -> float:
        if self._value is None:
            self._value = float(self.evaluated_expression.evalf(3))   # ensure a float or raise
        return self._value

    def __float__(self) -> float:
        return self.value

####################################################################################################

class MeasurementSet:

    """Class to store a set of measurements"""

    __measurement_cls__ = Measurement

    _logger = _module_logger.getChild('Measurements')

    ##############################################

    def __init__(self,
                 unit: Optional[str] = None,
                 pattern_making_system: Optional[str] = None,
                 personal_data: Optional[PersonalData] = None,
                 ) -> None:
        self._unit = unit
        self._pattern_making_system = pattern_making_system   # Fixme: purpose ???
        self._personal = PersonalData() if personal_data is None else personal_data
        self._measurements = {}   # name -> Measurement
        self._expressions = {}   # name -> expression  for sympy substitution

    ##############################################

    @property
    def personal(self) -> PersonalData:
        return self._personal

    ##############################################

    @property
    def unit(self) -> str:
        return self._unit

    @unit.setter
    def unit(self, value: str) -> None:
        self._unit = value

    ##############################################

    @property
    def pattern_making_system(self) -> str:
        return self._pattern_making_system

    @pattern_making_system.setter
    def pattern_making_system(self, value: str) -> None:
        self._pattern_making_system = value

    ##############################################

    def __iter__(self) -> Iterator[Measurement]:
        return iter(self._measurements.values())

    ##############################################

    def sorted_iter(self) -> Measurement:
        for name in sorted(self._measurements.keys()):
            yield self._measurements[name]

    ##############################################

    def __getitem__(self, name: str) -> Measurement:
        return self._measurements[name]

    def __getattr__(self, name: str) -> Measurement:
        return self._measurements[name]

    # Note: __setattr__ is called for by setattr

    ##############################################

    def add(self, *args: list, **kwargs: dict) -> Measurement:
        # Fixme: name ?
        measurement = self.__measurement_cls__(self, *args, **kwargs)
        if measurement.name in self._measurements:
            raise NameError(f"Measurement {measurement.name} is already registered")
        self._measurements[measurement.name] = measurement
        self._expressions[measurement.name] = measurement.expression
        return measurement

    ##############################################

    def subs(self, measurement: Measurement) -> sympy.core.expr.Expr:
        return measurement.expression.subs(self._expressions)

    ##############################################

    def dump(self) -> str:
        buffer = ''
        for measurement in self.sorted_iter():
            buffer += repr(measurement)
        return buffer

    ##############################################

    def save_as_yaml(self, yaml_path: str | Path) -> None:
        measurements = {}
        # for measurement in self:
        for measurement in self.sorted_iter():
            expression = measurement.expression
            if isinstance(expression, sympy.Integer):
                expression = int(expression)
            elif isinstance(expression, sympy.Float):
                expression = float(expression)
            else:
                expression = str(expression)
            data = [expression]
            if measurement.full_name or measurement.description:
                data += [measurement.full_name, measurement.description]
            measurements[measurement.name] = data
        with open(yaml_path, 'w', encoding='uft8') as fh:
            yaml_string = yaml.dump(measurements, default_flow_style=False, width=160)
            fh.write(yaml_string)

    ##############################################

    def load_yaml(self, yaml_path: str | Path) -> None:
        with open(yaml_path, 'r', encoding='uft8') as fh:
            measurements = yaml.load(fh.read(), Loader=yaml.SafeLoader)
            for name, data in measurements.items():
                if len(data) > 1:
                    value, full_name, description = data
                else:
                    value = data[0]
                    full_name = description = ''
                self.add(name, value, full_name, description)
