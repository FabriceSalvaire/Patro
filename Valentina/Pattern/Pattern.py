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

from IntervalArithmetic import Interval2D

from Valentina.Geometry.Vector import Vector2D
from Valentina.GraphicScene.GraphicItem import PathStyle
from Valentina.GraphicScene.Scene import GraphicScene
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

    def _add_calculation(self, calculation):

        # Work as a post init
        self._calculations.append(calculation)
        self._calculation_dict[calculation.id] = calculation
        if hasattr(calculation, 'name'):
            self._calculation_dict[calculation.name] = calculation

    ##############################################

    def get_calculation_id(self):

        return len(self._calculations) + 1 # id > 0

    ##############################################

    def has_calculation_id(self, id):

        return id in self._calculation_dict

    ##############################################

    def get_calculation(self, id):

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
            calculation.connect_ancestor_for_expressions()

    ##############################################

    def dump(self):

        print("\nDump calculations:")
        for calculation in self._calculations:
            if isinstance(calculation, Calculation.Point):
                print(calculation, calculation.vector)
            else:
                print(calculation)
            for dependency in calculation.dependencies:
                print('  ->', dependency)

    ##############################################

    def bounding_box(self):

        bounding_box = None
        for calculation in self._calculations:
            interval = calculation.geometry().bounding_box()
            if bounding_box is None:
                bounding_box = interval
            else:
                bounding_box |= interval

        return bounding_box

    ##############################################

    def _calculation_to_path_style(self, calculation, **kwargs):

        return PathStyle(stroke_style=calculation.line_style,
                         stroke_color=calculation.line_color,
                         **kwargs)

    ##############################################

    def detail_scene(self):

        """Generate a graphic scene for the detail mode"""

        scene = GraphicScene()
        # Fixme: scene bounding box
        scene.bounding_box = self.bounding_box()

        # Fixme: implement a transformer class to prevent if ... ?

        for calculation in self._calculations:

            if isinstance(calculation, Calculation.Point):
                scene.add_coordinate(calculation.name, calculation.vector)
                scene.add_circle(calculation.name, '1pt', PathStyle(fill_color='black'))
                label_offset = calculation.label_offset
                offset = Vector2D(label_offset.x, -label_offset.y) # Fixme: ???
                label_position = calculation.vector + offset
                if offset:
                    # arrow must point to the label center and be clipped
                    scene.add_segment(calculation.vector, label_position, PathStyle(line_width='.5pt'))
                scene.add_text(label_position, calculation.name)

                if isinstance(calculation, Calculation.LinePropertiesMixin):
                    path_style = self._calculation_to_path_style(calculation, line_width='2pt')
                    if isinstance(calculation, Calculation.AlongLinePoint):
                        scene.add_segment(calculation.first_point.name, calculation.name, path_style)
                    elif isinstance(calculation, Calculation.EndLinePoint):
                        scene.add_segment(calculation.base_point.name, calculation.name, path_style)
                    # elif isinstance(calculation, LineIntersectPoint):
                    #     scene.add_segment(calculation.point1_line1.name, calculation.name, path_style)
                    #     source += r'\draw[{0}] ({1.point1_line1.name}) -- ({1.name});'.format(style, calculation) + '\n'
                    elif isinstance(calculation, Calculation.NormalPoint):
                        scene.add_segment(calculation.first_point.name, calculation.name, path_style)

            elif isinstance(calculation, Calculation.Line):
                path_style = self._calculation_to_path_style(calculation, line_width='4pt')
                scene.add_segment(calculation.first_point.name, calculation.second_point.name, path_style)

            elif isinstance(calculation, Calculation.SimpleInteractiveSpline):
                path_style = self._calculation_to_path_style(calculation, line_width='4pt')
                scene.add_cubic_bezier(calculation.first_point.name,
                                       calculation.control_point1, calculation.control_point2,
                                       calculation.second_point.name,
                                       path_style)

        return scene

