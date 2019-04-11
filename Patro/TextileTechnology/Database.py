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

__all__ = ['Database']

####################################################################################################

from pathlib import Path
import yaml

####################################################################################################

class Database:

    DEFAULT_DATA_DIRECTORY = Path(__file__).resolve().parent.joinpath('data')
    DEFAULT_DATA_FILENAME = None

    ##############################################

    def __init__(self):
        self._items = {}

    ##############################################

    def __len__(self):
        return len(self._items)

    def __iter__(self):
        return iter(self._items.values())

    def __getitem__(self, name):
        return self._items[name]

    ##############################################

    def add(self, obj):
        if obj.name not in self._items:
            self._items[obj.name] = obj

    ##############################################

    def load(self, yaml_path=None):
        if yaml_path is None:
            yaml_path = self.DEFAULT_DATA_DIRECTORY.joinpath(self.DEFAULT_DATA_FILENAME)
        return yaml.load(open(yaml_path, 'r'), Loader=yaml.SafeLoader)
