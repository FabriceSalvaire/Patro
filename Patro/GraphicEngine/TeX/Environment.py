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

from .Buffer import Buffer

####################################################################################################

class Environment(Buffer):

    ##############################################

    def __init__(self, name, options=''):

        super(Environment, self).__init__()

        self._name = name
        # self._options = options

        self._begin_buffer = Buffer()
        self._end_buffer = Buffer()

        if options:
            _options = '[' + options + ']'
        else:
            _options = ''
        self._begin_buffer.append(r'\begin{%s}%s' % (self._name, _options) + '\n')
        self._end_buffer.append(r'\end{%s}' % (self._name) + '\n')

    ##############################################

    def __str__(self):

        source = str(self._begin_buffer)
        source += super(Environment, self).__str__()
        source += str(self._end_buffer)
        return source

####################################################################################################

class Center(Environment):
    def __init__(self):
        Environment.__init__(self, 'center')
