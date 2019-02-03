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

__all__ = ['ObjectNameMixin', 'ObjectGlobalIdMixin']

####################################################################################################

from .AtomicCounter import AtomicCounter

####################################################################################################

class ObjectNameMixin:

    """Mixin for object with name"""

    ##############################################

    def __init__(self, name=None):
        self.name = name

    ##############################################

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if value is None:
            self._name = None
        else:
            self._name = str(value)

    ##############################################

    def __repr__(self):
        return self.__class__.__name__ + ' {0._name}'.format(self)

    ##############################################

    def __str__(self):
        return self._name

####################################################################################################

class ObjectGlobalIdMixin:

    """Mixin for object with a global id"""

    __object_counter__ = AtomicCounter(-1)

    ##############################################

    def __init__(self, id=None):

        # Note: sub-classes share the same counter !
        if id is not None:
            ObjectGlobalIdMixin.__object_counter__.set(id)
            self._id = id
        else:
            self._id = ObjectGlobalIdMixin.__object_counter__.increment()

    ##############################################

    @property
    def id(self):
        return self._id

    ##############################################

    def __int__(self):
        return self._id

    ##############################################

    def __repr__(self):
        return self.__class__.__name__ + ' {0._id}'.format(self)

####################################################################################################

class ObjectCkeckedIdMixin:

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
