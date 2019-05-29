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

from pathlib import Path

import yaml

from .StandardMeasurement import Measurement, StandardMeasurement

####################################################################################################

class ValentinaMeasurement(Measurement):

    ##############################################

    def __init__(self, code, name, full_name, description, default_value):

        super().__init__(name, full_name, description, default_value)

        self._code = code

    ##############################################

    @property
    def code(self):
        return self._code

    @code.setter
    def code(self, value):
        self._code = value

####################################################################################################

class ValentinaStandardMeasurement(StandardMeasurement):

    ##############################################

    def __init__(self):

        super().__init__()

        yaml_path = Path(__file__).parent.joinpath('data', 'valentina-standard-measurements.yaml')
        with open(yaml_path, 'r') as fh:
            data = yaml.load(fh.read(), Loader=yaml.SafeLoader)
            for topic in data.values():
                for code, measurement_data in topic['measurements'].items():
                    measurement = ValentinaMeasurement(code, *measurement_data)
                    self.add(measurement)
