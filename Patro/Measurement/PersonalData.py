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

from enum import Enum, auto

from Patro.Common.Datetime import ensure_date, ensure_datetime

####################################################################################################

class Gender(Enum):
    UNKNOWN = auto() # information is not available
    FEMALE = auto()
    MALE = auto()
    # Gender can be mixed or modified, body malformation or injury
    PARTICULAR = auto() # Fixme: use case to be defined ...

####################################################################################################

class PersonalData:

    """Class to define personal data like name and gender."""

    ##############################################

    def __init__(self, **kwargs):

        self._first_name = None
        self._last_name = None
        self._birth_date = None # to get age
        self._measurement_date = None # when the measurement was done
        self._gender = None
        self._email = None # contact
        self._comment = None # any useful information to adapt garment to the person

        for key, default in (
                ('first_name', ''), # Fixme: str_or_none ?
                ('last_name', ''),
                ('birth_date', None),
                ('measurement_date', None),
                ('gender', Gender.UNKNOWN),
                ('email', ''),
                ('comment', ''),
        ):
            setattr(self, key, kwargs.get(key, default))

    ##############################################

    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, value):
        self._first_name = str(value)

    ##############################################

    @property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, value):
        self._last_name = str(value)

    ##############################################

    @property
    def birth_date(self):
        return self._birth_date

    @birth_date.setter
    def birth_date(self, value):
        if value is not None:
            self._birth_date = ensure_date(value)
        else:
            self._birth_date = None

    ##############################################

    @property
    def measurement_date(self):
        return self._measurement_date

    @measurement_date.setter
    def measurement_date(self, value):
        if value is not None:
            self._measurement_date = ensure_datetime(value)
        else:
            self._measurement_date = None

    ##############################################

    @property
    def gender(self):
        return self._gender

    @gender.setter
    def gender(self, value):

        if isinstance(value, str):
            gender = Gender[value.upper()]
        else:
            gender = Gender(value)
        self._gender = gender

    ##############################################

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        self._email = str(value)

    ##############################################

    @property
    def comment(self):
        return self._comment

    @comment.setter
    def comment(self, value):
        self._comment = str(value)
