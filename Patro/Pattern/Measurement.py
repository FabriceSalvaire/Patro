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

from .Calculator import Calculator, NamedExpression
from .PersonalData import PersonalData

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class Measurement(NamedExpression):

    """Class to define a measurement"""

    ##############################################

    def __init__(self, measurements, name, value, full_name='', description=''):

        # Valentina defines custom measurement with a @ prefix
        name = str(name)
        self._valentina_name = name
        if self.is_custom():
            name = '__custom__' + name[1:]
        for c in name:
            if not c.isalnum() and c != '_':
                raise ValueError('Invalid measurement name "{}"'.format(self._valentina_name))

        NamedExpression.__init__(self, name, value, calculator=measurements.calculator)

        self._full_name = str(full_name) # for human
        self._description = str(description) # describe the purpose of the measurement

    ##############################################

    @property
    def valentina_name(self):
        return self._valentina_name

    @property
    def full_name(self):
        return self._full_name

    @property
    def description(self):
        return self._description

    ##############################################

    def is_custom(self):
        return self._valentina_name.startswith('@')

    ##############################################

    def eval(self):
        super(Measurement, self).eval()
        self._calculator._update_cache(self)

####################################################################################################

class Measurements:

    """Class to store a set of measurements"""

    _logger = _module_logger.getChild('Measurements')

    ##############################################

    def __init__(self):

        self._unit = None
        self._pattern_making_system = None
        self._personal = PersonalData()

        self._measures = []
        self._measure_dict = {}
        self._calculator = Calculator(self)

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

        measurement = Measurement(self, *args, **kgwars)
        self._measures.append(measurement)
        self._measure_dict[measurement.name] = measurement
        if measurement.is_custom():
            self._measure_dict[measurement.valentina_name] = measurement

    ##############################################

    def eval(self):

        # Fixme: eval / compute a graph from the ast to evaluate
        self._logger.info('Eval all measurements')
        for measure in self:
            measure.eval()

    ##############################################

    def dump(self):

        print("\nDump measurements:")
        for measure in self:
            print(measure.name, '=', measure.expression)
            print('  =', measure.value)
