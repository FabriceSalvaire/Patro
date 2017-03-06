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

"""This subpackage implements the core engine for pattern.

"""

####################################################################################################

import inspect

from . import Calculation
from .Pattern import Pattern

####################################################################################################

def _get_calculations(module):
    return [item
            for item  in module.__dict__.values()
            if inspect.isclass(item) and issubclass(item, Calculation.Calculation)]

####################################################################################################

_calculations = _get_calculations(Calculation)

for calculation_class in _calculations:

    def _make_function(calculation_class):
        def function(self, *args, **kwargs):
            calculation = calculation_class(self, *args, **kwargs)
            self._add_calculation(calculation)
            return calculation
        return function

    function_name = calculation_class.__name__

    setattr(Pattern, function_name, _make_function(calculation_class))
