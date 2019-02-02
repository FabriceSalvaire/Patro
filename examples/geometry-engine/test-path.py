####################################################################################################
#
# Patro - A Python library to make patterns for fashion design
# Copyright (C) 2019 Fabrice Salvaire
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

from Patro.GeometryEngine.Path import Path2D
from Patro.GeometryEngine.Vector import Vector2D
from Patro.GraphicEngine.GraphicScene.GraphicStyle import GraphicPathStyle, GraphicBezierStyle
from Patro.GraphicEngine.Painter.QtPainter import QtScene
from Patro.GraphicStyle import Colors, StrokeStyle

####################################################################################################

class SceneBuilder:

    ##############################################

    def __init__(self):

        self._scene = QtScene()

        self._bounding_box = None
        for path in (
                self._make_directional_path((0, 0)),
                self._make_rounded_rectangle((20, 0), width=10, height=15, radius=5),
                self._make_closed_path((35, 0), radius=None),
                self._make_closed_path((55, 0), radius=3),
                self._make_absolute_cw_path((0, 40), radius=3),
                self._make_absolute_ccw_path((0, 45), radius=3),
                self._make_quadratic((25, 40)),
                self._make_absolute_quadratic((35, 40)),
                self._make_cubic((40, 40)),
                self._make_absolute_cubic((50, 40)),
                ):
            self._add_path(path)
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

    def _make_directional_path(self, start_point):

        path = Path2D(start_point)
        path.horizontal_to(10)
        path.vertical_to(10)
        path.north_east_to(10)
        path.north_west_to(10)
        path.south_west_to(10)
        path.south_east_to(5)
        path.south_to(5)
        path.west_to(10)
        path.north_to(5)
        path.east_to(5)

        return path

    ##############################################

    def _make_rounded_rectangle(self, start_point, width, height, radius):

        path = Path2D(start_point)
        path.horizontal_to(width)
        path.vertical_to(height, radius=radius)
        path.horizontal_to(-width, radius=radius)
        path.close(radius=radius, close_radius=radius)

        return path

    ##############################################

    def _make_closed_path(self, start_point, radius):

        path = Path2D(start_point)
        path.line_to(Vector2D(10, 0))
        path.line_to(Vector2D(0, 10), radius=radius)
        path.line_to(Vector2D(10, 0), radius=radius)
        path.line_to(Vector2D(0, 20), radius=radius)
        path.line_to(Vector2D(-10, 0), radius=radius)
        path.line_to(Vector2D(0, -10), radius=radius)
        path.close(radius=radius, close_radius=radius)

        return path

    ##############################################

    def _make_absolute_cw_path(self, start_point, radius):

        # radius = None
        path = Path2D(start_point)
        for i, vector in enumerate((
                (10, -5),
                (5, -15),
                (-5, -15),
                (-10, -5),
        )):
            path.line_to(path.p0 + Vector2D(vector), absolute=True, radius=(radius if i else None))
        path.close(radius=radius, close_radius=radius)

        return path

    ##############################################

    def _make_absolute_ccw_path(self, start_point, radius):

        path = Path2D(start_point)
        for i, vector in enumerate((
                (10, 0),
                (15, 10),
                (5, 15),
                (-5, 10),
        )):
            path.line_to(path.p0 + Vector2D(vector), absolute=True, radius=(radius if i else None))
        path.close(radius=radius, close_radius=radius)

        return path

    ##############################################

    def _make_quadratic(self, start_point):

        path = Path2D(start_point)
        path.quadratic_to(
            Vector2D(0, 10),
            Vector2D(10, 10),
        )

        return path

    ##############################################

    def _make_absolute_quadratic(self, start_point):

        path = Path2D(start_point)
        path.quadratic_to(
            path.p0 + Vector2D(0, 10),
            path.p0 + Vector2D(10, 10),
            absolute=True,
        )

        return path

    ##############################################

    def _make_cubic(self, start_point):

        path = Path2D(start_point)
        path.cubic_to(
            Vector2D(5, 10),
            Vector2D(10, 10),
            Vector2D(15, 0),
        )

        return path

    ##############################################

    def _make_absolute_cubic(self, start_point):

        path = Path2D(start_point)
        path.cubic_to(
            path.p0 + Vector2D(5, 10),
            path.p0 + Vector2D(10, 10),
            path.p0 + Vector2D(15, 0),
            absolute=True,
        )

        return path

    ##############################################

    def _add_path(self, path):

        path_style = GraphicPathStyle(
            line_width=3.0,
            stroke_color=Colors.black,
            stroke_style=StrokeStyle.SolidLine,
        )

        self._scene.add_path(path, path_style)

        # Fixme: why here ???
        self._update_bounding_box(path)

####################################################################################################

scene = QtScene()

scene_builder = SceneBuilder()
application.qml_application.scene = scene_builder.scene
