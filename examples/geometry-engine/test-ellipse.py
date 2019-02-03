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

from Patro.GeometryEngine.Conic import Ellipse2D, AngularDomain
from Patro.GeometryEngine.Vector import Vector2D
from Patro.GraphicEngine.GraphicScene.GraphicStyle import GraphicPathStyle
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

        center = (0, 0)
        ellipse1 = Ellipse2D(center, 20, 10)
        ellipse2 = Ellipse2D(center, 20, 10, angle=30)
        ellipse3 = Ellipse2D(center, 20, 10, angle=60, domain=AngularDomain(30, 160))

        ellipse1_bezier = ellipse1.to_bezier()
        ellipse2_bezier = ellipse2.to_bezier()
        ellipse3_bezier = ellipse3.to_bezier()

        return [
            # ellipse1,
            *ellipse1_bezier,
            # ellipse2,
            *ellipse2_bezier,
            # ellipse3,
            *ellipse3_bezier,
        ]

    ##############################################

    def _add_item(self, item):

        path_style = GraphicPathStyle(
            line_width=self._line_width,
            stroke_color=Colors.black,
            stroke_style=StrokeStyle.SolidLine,
            cap_style=CapStyle.RoundCap,
        )

        self._scene.add_geometry(item, path_style)
        # Fixme: why here ???
        self._update_bounding_box(item)

####################################################################################################

scene = QtScene()

scene_builder = SceneBuilder()
application.qml_application.scene = scene_builder.scene
