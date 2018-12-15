####################################################################################################
#
# Patro - A Python library to make patterns for fashion design
# Copyright (C) 2018 Fabrice Salvaire
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

class ObjectIdMixin:

    """Mixin for object with id"""

    ##############################################

    def __init__(self, id=None):

        if id is None:
            self._id = self.new_id()
        else:
            self.check_id(id)
            self._id = id

    ##############################################

    @property
    def id(self):
        return self._id

    ##############################################

    def __repr__(self):
        return self.__class__.__name__ + ' {0._id}'.format(self)

    ##############################################

    def __int__(self):
        return self._id

    ##############################################

    def new_id(self):
        raise NotImplementedError

    ##############################################

    def check_id(self, id):
        return True
