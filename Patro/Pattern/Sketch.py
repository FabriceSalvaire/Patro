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

"""
"""

####################################################################################################

import logging

from Patro.GeometryEngine.Vector import Vector2D
from Patro.GraphicEngine.GraphicScene.GraphicStyle import GraphicPathStyle
from Patro.GraphicEngine.GraphicScene.Scene import GraphicScene
from . import SketchOperation
from .Calculator import Calculator
from .SketchStyle import DetailSketchStyle

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class Sketch:

    # Fixme:
    #   do we want to have several sketches
    #   apply a transformation
    #   share points

    _logger = _module_logger.getChild('Sketch')

    ##############################################

    def __init__(self, pattern):

        self._pattern = pattern

        self._calculator = Calculator(self.measurements)

        self._operations = []
        self._operation_dict = {}

    ##############################################

    @property
    def pattern(self):
        return self._pattern

    @property
    def measurements(self):
        return self._pattern.measurements

    @property
    def calculator(self):
        return self._calculator

    @property
    def unit(self):
        return self._pattern.unit

    ##############################################

    @property
    def operations(self):
        return self._operations

    ##############################################

    def _add_operation(self, operation):

        # Works as a post init
        self._operations.append(operation)
        # Fixme: operation id, only for valentina ?
        self._operation_dict[operation.id] = operation
        if hasattr(operation, 'name'):
            self._operation_dict[operation.name] = operation

    ##############################################

    def has_operation_id(self, id):
        return id in self._operation_dict

    ##############################################

    def get_operation(self, id):
        return self._operation_dict[id]

    ##############################################

    def eval(self):

        self._logger.info('Eval all operations')
        for operation in self._operations:
            if isinstance(operation, SketchOperation.Point):
                self._calculator.add_point(operation)
                operation.eval()
            elif isinstance(operation, SketchOperation.SimpleInteractiveSpline):
                operation.eval() # for control points
            else:
                pass
            operation.connect_ancestor_for_expressions()

    ##############################################

    def dump(self):

        print("\nDump operations:")
        for operation in self._operations:
            if isinstance(operation, SketchOperation.Point):
                print(operation, operation.vector)
            else:
                print(operation)
            for dependency in operation.dependencies:
                print('  ->', dependency)

    ##############################################

    @property
    def bounding_box(self):

        """Compute the bounding box of the pattern."""

        # Fixme: to function
        #        cache ???
        bounding_box = None
        for operation in self._operations:
            interval = operation.geometry().bounding_box
            if bounding_box is None:
                bounding_box = interval
            else:
                bounding_box |= interval

        return bounding_box

    ##############################################

    def _operation_to_path_style(self, operation, **kwargs):

        """Generate a :class:`GraphicPathStyle` instance for a operation"""

        return GraphicPathStyle(
            stroke_style=operation.line_style,
            stroke_color=operation.line_color,
            **kwargs
        )

    ##############################################

    def detail_scene(self, scene_cls=GraphicScene, style=None):

        """Generate a graphic scene for the detail mode

        Scene class can be customised using the *scene_cls* parameter.
        """

        scene = scene_cls()
        # Fixme: scene bounding box
        scene.bounding_box = self.bounding_box

        if style is None:
            style = DetailSketchStyle()

        # Fixme: implement a transformer class to prevent if ... ?

        for operation in self._operations:

            if isinstance(operation, SketchOperation.Point):
                # Register coordinate
                scene.add_coordinate(operation.name, operation.vector)
                # Draw point and label
                scene.circle(operation.name, style.point_size,
                             style.point_style,
                             user_data=operation,
                )
                label_offset = operation.label_offset
                offset = Vector2D(label_offset.x, -label_offset.y) # Fixme: ???
                label_position = operation.vector + offset
                if offset:
                    # arrow must point to the label center and be clipped
                    scene.segment(operation.vector, label_position,
                                  style.label_line_style,
                                  user_data=operation,
                    )
                    scene.text(label_position, operation.name, style.font, user_data=operation)

                if isinstance(operation, SketchOperation.LinePropertiesMixin):
                    path_style = self._operation_to_path_style(
                        operation,
                        line_width=style.construction_line_width,
                    )
                    if isinstance(operation, SketchOperation.AlongLinePoint):
                        scene.segment(operation.first_point.name, operation.name,
                                      path_style,
                                      user_data=operation,
                        )
                    elif isinstance(operation, SketchOperation.EndLinePoint):
                        scene.segment(operation.base_point.name, operation.name,
                                      path_style,
                                      user_data=operation,
                        )
                    # elif isinstance(operation, LineIntersectPoint):
                    #     scene.segment(operation.point1_line1.name, operation.name, path_style)
                    #     source += r'\draw[{0}] ({1.point1_line1.name}) -- ({1.name});'.format(style, operation) + '\n'
                    elif isinstance(operation, SketchOperation.NormalPoint):
                        scene.segment(operation.first_point.name, operation.name,
                                      path_style,
                                      user_data=operation,
                        )

            # Draw path item like segments and Bézier curves

            elif isinstance(operation, SketchOperation.Line):
                path_style = self._operation_to_path_style(operation, line_width=style.line_width)
                scene.segment(operation.first_point.name, operation.second_point.name,
                              path_style,
                              user_data=operation,
                )

            elif isinstance(operation, SketchOperation.SimpleInteractiveSpline):
                path_style = self._operation_to_path_style(operation, line_width=style.line_width)
                scene.cubic_bezier(operation.first_point.name,
                                   operation.control_point1, operation.control_point2,
                                   operation.second_point.name,
                                   path_style,
                                   user_data=operation,
                )

        return scene
