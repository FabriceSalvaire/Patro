####################################################################################################
#
# Patro - A Python library to make patterns for fashion design
# Copyright (C) 2019 Fabrice Salvaire
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

"""Module to implement mixins.

"""

# Fixme: versus mixin Primitive.py

####################################################################################################

__all__ = [
    'AngularDomain',

    'AngularDomainMixin',
    'CenterMixin',
]

####################################################################################################

import math
from math import radians, pi # , degrees

####################################################################################################

class AngularDomain:

    """Class to define an angular domain"""

    ##############################################

    def __init__(self, start=0, stop=360, degrees=True):

        if not degrees:
            start = math.degrees(start)
            stop = math.degrees(stop)

        self.start = start
        self.stop = stop

    ##############################################

    def __clone__(self):
        return self.__class__(self._start, self._stop)

    ##############################################

    def __repr__(self):
        return '{0}({1._start}, {1._stop})'.format(self.__class__.__name__, self)

    ##############################################

    @property
    def start(self):
        return self._start

    @start.setter
    def start(self, value):
        self._start = float(value)

    @property
    def stop(self):
        return self._stop

    @stop.setter
    def stop(self, value):
        self._stop = float(value)

    @property
    def start_radians(self):
        return radians(self._start)

    @property
    def stop_radians(self):
        return radians(self._stop)

    ##############################################

    @property
    def span(self):
        return abs(self._stop - self._start)

    ##############################################

    @property
    def is_null(self):
        return self._stop == self._start

    @property
    def is_closed(self):
        return self.span >= 360

    @property
    def is_over_closed(self):
        return self.span > 360

    @property
    def is_counterclockwise(self):
        """Return True if start <= stop, e.g. 10 <= 300"""
        # Fixme: name ???
        return self.start <= self.stop

    @property
    def is_clockwise(self):
        """Return True if stop < start, e.g. 300 < 10"""
        return self.stop < self.start

    ##############################################

    @property
    def length(self):
        """Return the length for an unitary circle"""
        if self.is_closed:
            return 2*pi
        else:
            length = self.stop_radians - self.start_radians
            if self.is_counterclockwise:
                return length
            else:
                return 2*pi - length

    ##############################################

    def is_inside(self, angle):
        if self.is_counterclockwise:
            return self._start <= angle <= self._stop
        else:
            # Fixme: check !!!
            return not(self._stop < angle < self._start)

####################################################################################################

class AngularDomainMixin:

    ##############################################

    @property
    def domain(self):
        return self._domain

    @domain.setter
    def domain(self, value):
        if value is not None:
            self._domain = value # Fixme: AngularDomain() ??
        else:
            self._domain = None

    ##############################################

    @property
    def is_closed(self):
        return self._domain is None

    ##############################################

    def start_stop_point(self, start=True):

        if self._domain is not None:
            angle = self.domain.start if start else self.domain.stop
            return self.point_at_angle(angle)
        else:
            return None

    ##############################################

    @property
    def start_point(self):
        return self.start_stop_point(start=True)

    ##############################################

    @property
    def stop_point(self):
        return self.start_stop_point(start=False)

####################################################################################################

class CenterMixin:

    @property
    def center(self):
        return self._center

    @center.setter
    def center(self, value):
        self._center = self.__vector_cls__(value)

    @property
    def points(self):
        return (self._center,)
