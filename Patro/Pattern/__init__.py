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

"""This subpackage implements the core engine for pattern.

"""

####################################################################################################

import inspect

from . import SketchOperation
from .Sketch import Sketch

####################################################################################################

def _get_sketch_operations(module):
    return [item
            for item  in module.__dict__.values()
            if inspect.isclass(item) and issubclass(item, SketchOperation.SketchOperation)]

####################################################################################################

_sketch_operations = _get_sketch_operations(SketchOperation)

for operation_cls in _sketch_operations:

    def _make_function(operation_cls):
        def function(self, *args, **kwargs):
            sketch_operation = operation_cls(self, *args, **kwargs)
            self._add_operation(sketch_operation)
            return sketch_operation
        return function

    function_name = operation_cls.__name__

    setattr(Sketch, function_name, _make_function(operation_cls))
