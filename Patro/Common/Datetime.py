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

from datetime import datetime, date

####################################################################################################

def ensure_date(x):
    if isinstance(x, date):
        return x
    else:
        # "1970-01-01"
        return datetime.strptime(str(x), '%Y-%m-%d').date()

####################################################################################################

def ensure_datetime(x):
    if isinstance(x, datetime):
        return x
    else:
        # "1970-01-01T12:00:00.123Z"
        return datetime.strptime(str(x), '%Y-%m-%dT%H:%M:%S.%fZ')
