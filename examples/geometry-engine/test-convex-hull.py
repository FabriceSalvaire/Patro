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
#
# run as
#
#    ./bin/patro --user-script examples/geometry-engine/test-convex-hull.py
#
####################################################################################################

####################################################################################################

from Patro.GeometryEngine.Polygon import Polygon2D
from Patro.GeometryEngine.Vector import Vector2D
from Patro.GraphicEngine.GraphicScene.GraphicStyle import GraphicPathStyle
from Patro.GraphicEngine.Painter.QtPainter import QtScene
from Patro.GraphicStyle import Colors, StrokeStyle

####################################################################################################

class SceneBuilder:

    ##############################################

    def __init__(self):

        self._scene = QtScene()

        self._bounding_box = None
        for item in (
                self._make_polygon(),
                ):
            self._add_item(item)
        self._scene.bounding_box = self._bounding_box # Fixme:

    ##############################################

    @property
    def scene(self):
        return self._scene

    ##############################################

    def _update_bounding_box(self, item):
        interval = item.bounding_box
        if self._bounding_box is None:
            self._bounding_box = interval
        else:
            self._bounding_box |= interval

    ##############################################

    def _make_polygon(self):

        points = Vector2D.from_coordinates(
            (0, 0),
            (-1, 2),
            (0, 3),
            (2, 4),
            (1, 5),
            (4, 6),
            (3, 3),
            (5, 3),
            (7, 3),
            (7, 2),
            (6, 1),
            (3, 2),
            (2, 1),
        )

        polygon = Polygon2D(*points)
        return polygon

    ##############################################

    def _add_item(self, item):

        path_style = GraphicPathStyle(
            line_width=3.0,
            stroke_color=Colors.black,
            stroke_style=StrokeStyle.SolidLine,
        )

        self._scene.add_geometry(item, path_style)

        # Fixme: why here ???
        self._update_bounding_box(item)

####################################################################################################

scene = QtScene()

scene_builder = SceneBuilder()
application.qml_application.scene = scene_builder.scene
