####################################################################################################

from Patro.Common.Logging import Logging
Logging.setup_logging()

from Patro.GeometryEngine.Path import (
    Path2D,
    LinearSegment, QuadraticBezierSegment, CubicBezierSegment
)
from Patro.GeometryEngine.Vector import Vector2D
from Patro.GraphicEngine.GraphicScene.GraphicItem import GraphicPathStyle, GraphicBezierStyle
from Patro.GraphicEngine.Painter.QtPainter import QtScene
from Patro.GraphicStyle import Colors, StrokeStyle

####################################################################################################

class SceneBuilder:

    ##############################################

    def __init__(self):

        self._scene = QtScene()

        self._bounding_box = None
        path = self._make_path()
        self._add_items(path)
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

    def _make_path(self):

        start_point = Vector2D(0, 0)
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

    def _add_items(self, path):

        path_style = GraphicPathStyle(
            line_width=3.0,
            stroke_color=Colors.black,
            stroke_style=StrokeStyle.SolidLine,
        )

        for item in path:
            print('Path part:', item)
            if isinstance(item, LinearSegment):
                print('linear', item.start_point, item.stop_point, item.points)
                self._scene.segment(*item.points,
                                    path_style,
                                    user_data=item,
                )
            elif isinstance(item, QuadraticBezierSegment):
                self._scene.quadratic_bezier(*item.points,
                                             path_style,
                                             user_data=item,
                )
            elif isinstance(item, CubicBezierSegment):
                self._scene.cubic_bezier(*item.points,
                                         path_style,
                                         user_data=item,
                )
            # Fixme: why here ???
            self._update_bounding_box(item)

####################################################################################################

scene = QtScene()

scene_builder = SceneBuilder()

application.qml_application.scene = scene_builder.scene
