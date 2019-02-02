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

from Patro.GeometryEngine.Conic import Circle2D
from Patro.GeometryEngine.Path import Path2D
from Patro.GraphicEngine.GraphicScene.GraphicStyle import GraphicPathStyle, GraphicBezierStyle
from Patro.GraphicEngine.Painter.QtPainter import QtScene
from Patro.GraphicStyle import Colors, StrokeStyle, CapStyle

####################################################################################################

class SceneBuilder:

    ##############################################

    def __init__(self):

        self._scene = QtScene()

        self._bounding_box = None
        self._line_width = 5.
        for path in self._make_figure1():
            self._add_item(path)
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

    def _make_figure1(self):

        width = 30
        space = 2
        seam_length = width / 4
        long_arm_length = width / 2
        short_arm_length = long_arm_length * .6
        height = 4
        radius = 2

        vertical_seam_position = short_arm_length * 2 / 3
        vertical_seam_length = height * 1.5

        right_side_length = width / 4
        y_right_side = height * 1.5
        right_side_circle_radius = 1

        path1 = Path2D((short_arm_length + space/2, -height/2))
        path1.west_to(short_arm_length)
        path1.north_to(height, radius=radius)
        path1.east_to(long_arm_length, radius=radius)

        path2 = path1.x_mirror(clone=True)

        path3 = Path2D((-seam_length/2, 0))
        path3.east_to(seam_length)

        path4 = Path2D((vertical_seam_position, -vertical_seam_length/2))
        path4.north_to(vertical_seam_length)

        path5 = path4.x_mirror(clone=True)

        path6 = Path2D((-right_side_length/2, y_right_side))
        path6.east_to(right_side_length)

        circle = Circle2D((0, y_right_side), right_side_circle_radius)

        return [path1, path2, path3, path4, path5, path6, circle]

    ##############################################

    def _add_item(self, item):

        if isinstance(item, Path2D):
            self._add_path(item)
        elif isinstance(item, Circle2D):
            self._add_circle(item)

    ##############################################

    def _add_path(self, path):

        path_style = GraphicPathStyle(
            line_width=self._line_width,
            stroke_color=Colors.black,
            stroke_style=StrokeStyle.SolidLine,
            cap_style=CapStyle.RoundCap,
        )

        self._scene.add_path(path, path_style)
        # Fixme: why here ???
        self._update_bounding_box(path)

    ##############################################

    def _add_circle(self, circle):

        path_style = GraphicPathStyle(
            line_width=self._line_width,
            stroke_color=Colors.black,
            stroke_style=StrokeStyle.SolidLine,
        )

        self._scene.add_geometry(circle, path_style)
        self._update_bounding_box(circle)

####################################################################################################

scene = QtScene()

scene_builder = SceneBuilder()
application.qml_application.scene = scene_builder.scene

# from Patro.GraphicEngine.Painter.QtPainter import QtPainter
# painter = QtPainter(scene_builder.scene)
# painter.to_svg('out.svg')
