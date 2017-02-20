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

import logging

from ArithmeticInterval import Interval2D

from . import Calculation

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

def vector_to_interval2d(vector):
    x, y = vector.x, vector.y
    return Interval2D((x, x), (y, y))

####################################################################################################

class Pattern:

    _logger = _module_logger.getChild('Pattern')

    ##############################################

    def __init__(self, measurements, unit):

        self._measurements = measurements
        self._calculator = measurements.calculator
        self._calculations = []
        self._calculation_dict = {}
        self._unit = unit

    ##############################################

    @property
    def measurements(self):
        return self._measurements

    @property
    def calculator(self):
        return self._calculator

    @property
    def unit(self):
        return self._unit

    ##############################################

    @property
    def calculations(self):
        return self._calculations

    ##############################################

    def add(self, calculation):

        if calculation is not None:
            self._calculations.append(calculation)
            self._calculation_dict[calculation.id] = calculation
            # Fixme: isinstance ?
            # Fixme: cannot due to init order ...
            # if hasattr(calculation, 'name'):
            #     print(calculation.name)
            #     self._calculation_dict[calculation.name] = calculation

    ##############################################

    def get_calculation_id(self):

        return len(self._calculations) + 1 # id > 0

    ##############################################

    def get_calculation(self, id):

        # Fixme: lazy ...
        if id not in self._calculation_dict and isinstance(id, str):
            for calculation in self._calculations:
                if hasattr(calculation, 'name') and calculation.name == id:
                    self._calculation_dict[calculation.name] = calculation

        return self._calculation_dict[id]

    ##############################################

    def get_point(self, name):

        return self._points[name]

    ##############################################

    def eval(self):

        self._logger.info('Eval all calculations')
        for calculation in self._calculations:
            if isinstance(calculation, Calculation.Point):
                self._calculator.add_point(calculation)
                calculation.eval()
            elif isinstance(calculation, Calculation.SimpleInteractiveSpline):
                calculation.eval() # for control points
            else:
                pass

    ##############################################

    def dump(self):

        print("\nDump calculations:")
        for calculation in self._calculations:
            if isinstance(calculation, Calculation.Point):
                print(calculation, calculation.vector)
            else:
                print(calculation)

    ##############################################

    def bounding_box(self):

        interval = None
        for calculation in self._calculations:
            if isinstance(calculation, Calculation.Point):
                interval_point = vector_to_interval2d(calculation.vector)
                if interval is None:
                    interval = interval_point
                else:
                    interval |= interval_point
            elif isinstance(calculation, Calculation.SimpleInteractiveSpline):
                interval |= vector_to_interval2d(calculation.control_point1)
                interval |= vector_to_interval2d(calculation.control_point2)
        return interval
