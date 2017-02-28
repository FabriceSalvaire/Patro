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

import copy

####################################################################################################

class Buffer:

    ##############################################

    def __init__(self):

        self._content = []
        self.clear()

    ##############################################

    def __str__(self):

        source = ''
        for item in self._content:
            source += str(item)
        return source

    ##############################################

    def clear(self):

        self._content.clear()

    ##############################################

    def append(self, data, deepcopy=False):

        if isinstance(data, list):
            for item in data:
                self._append(item, deepcopy)
        else:
            self._append(data, deepcopy)

        return self

    ##############################################

    def _append(self, data, deepcopy=False):

        if deepcopy:
            data = copy.deepcopy(data)
        # if isinstance(data, str) or isinstance(data, Buffer):
        self._content.append(data)
