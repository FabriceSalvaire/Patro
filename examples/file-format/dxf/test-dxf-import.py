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

####################################################################################################

import logging

from Patro.Common.Logging import Logging
Logging.setup_logging()

from Patro.FileFormat.Dxf.Importer import DxfImporter
from Patro.GeometryEngine.Spline import BSpline2D
from Patro.GraphicEngine.GraphicScene.GraphicStyle import GraphicPathStyle, GraphicBezierStyle
from Patro.GraphicEngine.Painter.QtPainter import QtScene
from Patro.GraphicStyle import Colors, StrokeStyle
from PatroExample import find_data_path

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class SceneImporter:

    _logger = _module_logger.getChild('SceneImporter')

    ##############################################

    def __init__(self, dxf_path):

        self._importer = DxfImporter(dxf_path)
        self._scene = QtScene()

        self._bounding_box = None
        for item in self._importer:
            self._add_item(item)
        self._scene.bounding_box = self._bounding_box # Fixme:

    ##############################################

    @property
    def scene(self):
        return self._scene

    ##############################################

    def _update_bounding_box(self, item):

        if hasattr(item, 'bounding_box'):
            interval = item.bounding_box
            if self._bounding_box is None:
                self._bounding_box = interval
            else:
                self._bounding_box |= interval

    ##############################################

    def _add_item(self, item):

        self._logger.info(item)

        line_width = 3.

        path_style = GraphicPathStyle(
            line_width=line_width,
            stroke_color=Colors.black,
            stroke_style=StrokeStyle.SolidLine,
        )

        if isinstance(item, list):
            for segment in item:
                self._add_item(segment)

        elif isinstance(item, BSpline2D):
            path_style = GraphicPathStyle(
                line_width=line_width,
                stroke_color=Colors.blue_blue,
            )
            self._scene.polyline(item.points,
                                 path_style,
                                 user_data=item,
            )
            path_style = GraphicBezierStyle(
                line_width=5.0,
                stroke_color=Colors.black,
                show_control=True,
                control_color=Colors.red,
            )
            self._scene.add_spline(item, path_style)

        else:
            self._scene.add_geometry(item, path_style)


        self._update_bounding_box(item)

####################################################################################################

dxf_path = find_data_path('dxf', 'test-dxf-r15.dxf')

scene_importer = SceneImporter(dxf_path)
application.qml_application.scene = scene_importer.scene
