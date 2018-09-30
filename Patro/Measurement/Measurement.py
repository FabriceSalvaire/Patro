####################################################################################################
#
# Patro - A Python library to make patterns for fashion design
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

import logging

import sympy

from .PersonalData import PersonalData

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class Measurement:

    """Class to define a measurement"""

    ##############################################

    def __init__(self, measurements, name, value, full_name='', description=''):

        name = str(name)
        for c in name:
            if not c.isalnum() and c != '_':
                raise ValueError('Invalid measurement name "{}"'.format(name))

        self._measurements = measurements
        self._name = name
        self._full_name = str(full_name) # for human
        self._description = str(description) # describe the purpose of the measurement
        self._expression = sympy.sympify(value)
        self._evaluated_expression = None
        self._value = None

    ##############################################

    @property
    def name(self):
        return self._name

    @property
    def full_name(self):
        return self._full_name

    @property
    def description(self):
        return self._description

    @property
    def expression(self):
        return self._expression

    ##############################################

    @property
    def evaluated_expression(self):
        if self._evaluated_expression is None:
            # variable order doesn't matter, sympy do the job
            self._evaluated_expression = self._expression.subs(self._measurements._expressions)
        return self._evaluated_expression

    @property
    def value(self):
        if self._value is None:
            self._value = float(self.evaluated_expression.evalf(3)) # ensure a float or raise
        return self._value

    def __float__(self):
        return self.value

####################################################################################################

class Measurements:

    """Class to store a set of measurements"""

    __measurement_cls__ = Measurement

    _logger = _module_logger.getChild('Measurements')

    ##############################################

    def __init__(self):

        self._unit = None
        self._pattern_making_system = None # Fixme: purpose ???
        self._personal = PersonalData()

        self._measures = [] # Measurement list
        self._measure_dict = {} # name -> Measurement
        self._expressions = {} # name -> expression  for sympy substitution

    ##############################################

    @property
    def calculator(self):
        return self._calculator

    @property
    def personal(self):
        return self._personal

    ##############################################

    @property
    def unit(self):
        return self._unit

    @unit.setter
    def unit(self, value):
        self._unit = value

    ##############################################

    @property
    def pattern_making_system(self):
        return self._pattern_making_system

    @pattern_making_system.setter
    def pattern_making_system(self, value):
        self._pattern_making_system = value

    ##############################################

    def __iter__(self):
        return iter(self._measures)

    ##############################################

    def __getitem__(self, name):
        return self._measure_dict[name]

    ##############################################

    def add(self, *args, **kgwars):

        # Fixme: name ?

        measurement = self.__measurement_cls__(self, *args, **kgwars)
        self._measures.append(measurement)
        self._measure_dict[measurement.name] = measurement
        self._expressions[measurement.name] = measurement.expression

        return measurement

    ##############################################

    def dump(self):

        print("\nDump measurements:")
        template = '''{0.name} = {0.expression}
  = {0.evaluated_expression}
  = {0.value}
'''

        for measure in self:
            print(template.format(measure))
