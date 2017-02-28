####################################################################################################
#
# PyValentina - A Python implementation of Valentina Pattern Drafting Software
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

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class Personal:

    ##############################################

    def __init__(self, first_name=None, last_name=None, birth_date=None, gender=None, email=None):

        self._first_name = first_name
        self._last_name = last_name
        self._birth_date = birth_date
        self._gender = gender
        self._email = email

    ##############################################

    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, value):
        self._first_name = value

    @property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, value):
        self._last_name = value

    @property
    def birth_date(self):
        return self._birth_date

    @birth_date.setter
    def birth_date(self, value):
        self._birth_date = value

    @property
    def gender(self):
        return self._gender

    @gender.setter
    def gender(self, value):
        self._gender = value

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        self._email = value

####################################################################################################

class Measurements:

    _logger = _module_logger.getChild('Measurements')

    ##############################################

    def __init__(self):

        self._unit = None
        self._pattern_making_system = None
        self._personal = Personal()

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

    @property
    def unit(self):
        return self._unit

    @unit.setter
    def unit(self, value):
        self._unit = value

    @property
    def pattern_makin_system(self):
        return self._pattern_makin_system

    @pattern_makin_system.setter
    def pattern_makin_system(self, value):
        self._pattern_makin_system = value

    ##############################################

    def __iter__(self):
        return iter(self._measures)

    ##############################################

    def __getitem__(self, name):
        return self._measure_dict[name]

    ##############################################

    def add(self, *args, **kgwars):

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

####################################################################################################

class Measurement(NamedExpression):

    ##############################################

    def __init__(self, measurements, name, value, full_name='', description=''):

        self._valentina_name = name

        if self.is_custom():
            name = '__custom__' + name[1:]

        NamedExpression.__init__(self, name, value, calculator=measurements.calculator)

        self._full_name = full_name
        self._description = description

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
