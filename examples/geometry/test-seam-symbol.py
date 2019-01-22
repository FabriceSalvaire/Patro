####################################################################################################

from Patro.Common.Logging import Logging
Logging.setup_logging()

from Patro.GeometryEngine.Path import (
    Path2D,
    LinearSegment, QuadraticBezierSegment, CubicBezierSegment
)
from Patro.GeometryEngine.Transformation import Transformation2D
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

        start_point = Vector2D(short_arm_length + space/2, -height/2)
        path1 = Path2D(start_point)
        path1.west_to(short_arm_length)
        path1.north_to(height, radius=radius)
        path1.east_to(long_arm_length, radius=radius)

        path2 = path1.clone()
        # Fixme: path.x_mirror() ???
        path2.transform(Transformation2D.XReflection())

        start_point = Vector2D(-seam_length/2, 0)
        path3 = Path2D(start_point)
        path3.east_to(seam_length)

        vertival_seam_position = short_arm_length * 2 / 3
        vertival_seam_length = height * 1.5
        start_point = Vector2D(vertival_seam_position, -vertival_seam_length/2)
        path4 = Path2D(start_point)
        path4.north_to(vertival_seam_length)

        path5 = path4.clone()
        path5.transform(Transformation2D.XReflection())

        return [path1, path2, path3, path4, path5]

    ##############################################

    def _add_item(self, item):

        if isinstance(item, Path2D):
            self._add_path(item)

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
