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

__all__ = ['AtomicCounter']

####################################################################################################

import threading

####################################################################################################

class AtomicCounter:

    """A thread-safe incrementing counter.

    """

    ##############################################

    def __init__(self, initial=0):
        """Initialize a new atomic counter to given initial value (default 0)."""
        self._value = initial
        self._lock = threading.Lock()

    ##############################################

    def __int__(self):
        return self._value

    ##############################################

    def increment(self, value=1):
        """Atomically increment the counter by value (default 1) and return the
        new value.
        """
        with self._lock:
            self._value += value
        return self._value

    ##############################################

    def set(self, value):
        """Atomically set the counter to a value."""
        with self._lock:
            if value <= self._value:
                raise ValueError
            self._value = value
