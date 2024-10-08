####################################################################################################
#
# Patro - A Python library to make patterns for fashion design
# Copyright (C) 2022 Fabrice Salvaire
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
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

# http://www.pyinvoke.org

####################################################################################################

from invoke import task, Collection
# import sys

####################################################################################################

# PYSPICE_SOURCE_PATH = Path(__file__).resolve().parent

####################################################################################################

from . import clean
from . import doc

ns = Collection()
ns.add_collection(Collection.from_module(clean))
ns.add_collection(Collection.from_module(doc))
