####################################################################################################

from Patro.Common.Logging import Logging
Logging.setup_logging()

from Patro.GeometryEngine.Path import (
    Path2D,
    LinearSegment, QuadraticBezierSegment, CubicBezierSegment
)
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
                self._make_path1(),
                self._make_path2(),
                self._make_path3(),
                self._make_path4(),
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

    def _make_path1(self):

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

    def _make_path2(self):

        start_point = Vector2D(20, 0)
        path = Path2D(start_point)
        path.horizontal_to(10)
        path.vertical_to(10)
        path.north_east_to(10)
        path.north_west_to(10)
        path.south_west_to(10)
        path.south_east_to(5)

        return path

    ##############################################

    def _make_path3(self):

        start_point = Vector2D(40, 0)
        path = Path2D(start_point)
        path.line_to(Vector2D(10, 0))
        path.line_to(Vector2D(0, 10), radius=5)
        path.line_to(Vector2D(10, 0), radius=5)
        path.line_to(Vector2D(0, 20), radius=5)
        path.line_to(Vector2D(-10, 0), radius=5)
        path.line_to(Vector2D(0, -10), radius=5)
        path.close(radius=0) # Fixme:

        return path

    ##############################################

    def _make_path4(self):

        start_point = Vector2D(70, 0)
        path = Path2D(start_point)
        # path.line_to(Vector2D(10, 0))
        # path.line_to(Vector2D(0, 10), radius=5)
        # path.line_to(Vector2D(-10, 0), radius=5)
        path.east_to(10)
        path.north_to(10, radius=5)
        path.west_to(10, radius=5)

        return path

    ##############################################

    def _add_path(self, path):

        path_style = GraphicPathStyle(
            line_width=3.0,
            stroke_color=Colors.black,
            stroke_style=StrokeStyle.SolidLine,
        )

        for item in path:
            # print('Path part:', item)
            if isinstance(item, LinearSegment):
                # print('linear', item.start_point, item.stop_point, item.points)
                if item.radius is not None:
                    print('-'*10)
                    print(item.bissector)
                    print(item.bulge_angle, item.bulge_center, item.start_point, item.stop_point)
                    print(item.bulge_geometry)
                    arc = item.bulge_geometry
                    self._scene.circle(arc.center, arc.radius,
                                       path_style,
                                       start_angle=arc.domain.start,
                                       stop_angle=arc.domain.stop,
                                       user_data=item,
                    )
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
