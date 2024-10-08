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

from Patro.Common.Logging import Logging
Logging.setup_logging()

from Patro.FileFormat.Valentina.Measurement import VitFile
from PatroExample import find_data_path

####################################################################################################

# Read measurements file
vit_path = find_data_path('measurements', 'measurements.vit')
print(f'Open {vit_path}')
vit_file = VitFile(vit_path)
measurements = vit_file.measurements

print(measurements.dump())
print('-'*100)

# Accessors
print(measurements['waist_circ'])
print(measurements.waist_circ)
