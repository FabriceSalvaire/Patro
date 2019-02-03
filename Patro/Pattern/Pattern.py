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

"""
"""

####################################################################################################

import logging

from Patro.Common.Object import ObjectNameMixin
from .Sketch import Sketch

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class Pattern:

    """Class to implement the root of a pattern"""

    _logger = _module_logger.getChild('Pattern')

    ##############################################

    def __init__(self, measurements, unit):

        self._measurements = measurements
        self._unit = unit

        self._scopes = [] # not a dict so as to don't manage renaming

    ##############################################

    @property
    def measurements(self):
        return self._measurements

    @property
    def unit(self):
        return self._unit

    ##############################################

    @property
    def scopes(self):
        return iter(self._scopes)

    ##############################################

    def scope_names(self):
        return [scope.name for scope in self._scopes]

    ##############################################

    def add_scope(self, name):
        scope = PatternScope(self, name)
        self._scopes.append(scope)
        return scope

    ##############################################

    def scope(self, id):

        # Fixem: try ? for slice
        if isinstance(id, int):
            return self._scopes[id]
        else:
            for scope in self._scopes:
                if scope.name == id:
                    return scope
            return None

    ##############################################

    def remove_scope(self, name):
        scope = self.scope(name)
        if scope is not None:
            self._scopes.remove(scope)

####################################################################################################

class PatternScope(ObjectNameMixin):

    """Class to implement a pattern scope"""

    _logger = _module_logger.getChild('Pattern')

    ##############################################

    def __init__(self, pattern, name):

        super().__init__(name)
        self._pattern = pattern

        self._sketch = Sketch(self)

    ##############################################

    @property
    def measurements(self):
        return self._pattern.measurements

    @property
    def unit(self):
        return self._pattern._unit

    @property
    def sketch(self):
        return self._sketch
