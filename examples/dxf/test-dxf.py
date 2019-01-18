####################################################################################################

from pathlib import Path

from Patro.Common.Logging import Logging
Logging.setup_logging()

from Patro.FileFormat.Dxf.Importer import DxfImporter
from Patro.GeometryEngine.Bezier import CubicSpline2D, QuadraticSpline2D
from Patro.GeometryEngine.Conic import Circle2D, Conic2D
from Patro.GeometryEngine.Segment import Segment2D
from Patro.GraphicEngine.GraphicScene.GraphicItem import GraphicPathStyle, GraphicBezierStyle
from Patro.GraphicEngine.Painter.QtPainter import QtScene
from Patro.GeometryEngine.Vector import Vector2D
from Patro.GraphicStyle import Colors, StrokeStyle

####################################################################################################

def spline_from_svg(scene_importer):

    # https://pages.mtu.edu/~shene/COURSES/cs3621/NOTES/spline/B-spline/single-insertion.html

    # m 74.999689,150.7821
    # c
    # 9,-10 14.500002,-5 18.916662,-0.83334 4.41667,4.16667 7.749999,7.5 11.083339,5.83334
    # 3.33333,-1.66667 6.66666,-8.33334 13.33333,-11.66667 6.66667,-3.33333 16.66667,-3.33333
    # 16.66667,-3.33333

    x0, y0 = 40, 50
    control_points = (
        (9, -10),
        (14.500002, -5),
        (18.916662, -0.83334),

        (4.41667, 4.16667),
        (7.749999, 7.5),
        (11.083339, 5.83334),

        (3.33333, -1.66667),
        (6.66666, -8.33334),
        (13.33333, -11.66667),

        (6.66667, -3.33333),
        (16.66667, -3.33333),
        (16.66667, -3.33333),
    )

    vertices = []
    point = Vector2D(x0, y0)
    vertices.append(point)
    for i, xy in enumerate(control_points):
        xi, yi = xy
        yi = -yi
        if (i+1) % 3:
            x = xi + x0
            y = yi + y0
        else:
            x0 += xi
            y0 += yi
            x, y = x0, y0
        point = Vector2D(x, y)
        vertices.append(point)

    path_style = GraphicBezierStyle(
        line_width=3.0,
        stroke_color=Colors.blue,
        stroke_style=StrokeStyle.SolidLine,
        show_control=True,
        control_color=Colors.red,
    )

    for vertex in vertices:
        print(vertex)
    scene_importer.scene.bezier_path(vertices, degree=3, path_style=path_style, user_data=None)

####################################################################################################

class SceneImporter:

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

        # Fixme:
        path_style = GraphicPathStyle(
            line_width=2.0,
            stroke_color=Colors.black,
            stroke_style=StrokeStyle.SolidLine,
        )

        if isinstance(item, Segment2D):
            self._scene.segment(item.p0, item.p1,
                                path_style,
                                user_data=item,
            )
        elif isinstance(item, Circle2D):
            self._scene.circle(item.center, item.radius,
                               path_style,
                               user_data=item,
            )
        elif isinstance(item, QuadraticSpline2D):
            self._scene.polyline(item.points,
                                 path_style,
                                 user_data=item,
            )
        elif isinstance(item, CubicSpline2D):
            path_style = GraphicPathStyle(
                line_width=3.,
                stroke_color=Colors.green,
            ) # Fixme
            self._scene.polyline(item.points,
                                 path_style,
                                 user_data=item,
            )
            path_style = GraphicBezierStyle(
                line_width=5.0,
                stroke_color=Colors.black,
                show_control=True,
                control_color=Colors.red,
            ) # Fixme
            for part in item.iter_on_parts():
                bezier = part.to_bezier()
                print(bezier)
                self._scene.cubic_bezier(*bezier.points,
                                         path_style,
                                         user_data=item,
                )
                # t0 = 0
                # for i in range(1, 10 +1):
                #     t1 = 1 / i
                #     p0 = part.point_at_t(t0)
                #     p1 = part.point_at_t(t1)
                #     self._scene.segment(p0, p1,
                #                         path_style,
                #                         user_data=item,
                #     )
                #     t0 = t1
        # elif isinstance(item, Conic2D):
        #     pass
        elif isinstance(item, list):
            for segment in item:
                self._add_item(segment)

        if not isinstance(item, Circle2D):
            self._update_bounding_box(item)

####################################################################################################

# filename = 'protection-rectangulaire-v2.dxf'
filename = 'test-dxf-r15.dxf'
try:
    dxf_path = Path(__file__).parent.joinpath(filename)
except:
    dxf_path = Path('examples', 'dxf', filename)

scene_importer = SceneImporter(dxf_path)

spline_from_svg(scene_importer)

application.qml_application.scene = scene_importer.scene
