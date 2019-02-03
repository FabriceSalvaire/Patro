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

####################################################################################################

import logging

from .Measurement import Measurement, Measurements
from .ValentinaStandardMeasurement import ValentinaStandardMeasurement

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

_valentina_standard_measurement = ValentinaStandardMeasurement()

####################################################################################################

class ValentinaMeasurement(Measurement):

    """Class to define a Valentina measurement"""

    # CUSTOM_PREFIX = '__custom__'
    CUSTOM_PREFIX = 'C_'

    ##############################################

    @classmethod
    def replace_custom_prefix(cls, string):
        # Fixme: how to only replace when there is no clash ?
        return string.replace('@', cls.CUSTOM_PREFIX)

    ##############################################

    def __init__(self, measurements, name, value, full_name='', description=''):

        # Valentina defines custom measurement with a @ prefix
        self._valentina_name = str(name)
        name = self.replace_custom_prefix(self._valentina_name)
        # if self.is_custom():
        #     name = name[1:]
        #     if name in _valentina_standard_measurement:
        #         name = self.CUSTOM_PREFIX + name

        value = self.replace_custom_prefix(value)

        super().__init__(measurements, name, value, full_name, description)

    ##############################################

    @property
    def valentina_name(self):
        return self._valentina_name

    ##############################################

    def is_custom(self):
        return self._valentina_name.startswith('@')

####################################################################################################

class ValentinaMeasurements(Measurements):

    """Class to store a set of Valentina measurements"""

    __measurement_cls__ = ValentinaMeasurement

    _logger = _module_logger.getChild('ValentinaMeasurements')

    ##############################################

    def add(self, *args, **kgwars):

        # Fixme: name ?

        measurement = super().add(*args, **kgwars)
        if measurement.is_custom():
            self._measurements[measurement.valentina_name] = measurement
