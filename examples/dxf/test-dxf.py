####################################################################################################

from pathlib import Path

from Patro.Common.Logging import Logging
Logging.setup_logging()

from Patro.FileFormat.Dxf.Importer import DxfImporter
from Patro.GeometryEngine.Conic import Circle2D, Ellipse2D
from Patro.GeometryEngine.Segment import Segment2D
from Patro.GeometryEngine.Spline import BSpline2D
from Patro.GeometryEngine.Vector import Vector2D
from Patro.GraphicEngine.GraphicScene.GraphicStyle import GraphicPathStyle, GraphicBezierStyle
from Patro.GraphicEngine.Painter.QtPainter import QtScene
from Patro.GraphicStyle import Colors, StrokeStyle

####################################################################################################

def spline_from_svg(scene_importer):

    # m 74.999689,150.7821
    # c
    # 9,-10 14.500002,-5 18.916662,-0.83334 4.41667,4.16667 7.749999,7.5 11.083339,5.83334
    # 3.33333,-1.66667 6.66666,-8.33334 13.33333,-11.66667 6.66667,-3.33333 16.66667,-3.33333
    # 16.66667,-3.33333

    # Vector2D[40. 50.]
    # Vector2D[49. 60.]
    # Vector2D[54.500002 55.      ]
    # Vector2D[58.916662 50.83334 ]
    # Vector2D[63.333332 46.66667 ]
    # Vector2D[66.666661 43.33334 ]
    # Vector2D[70.000001 45.      ]
    # Vector2D[73.333331 46.66667 ]
    # Vector2D[76.666661 53.33334 ]
    # Vector2D[83.333331 56.66667 ]
    # Vector2D[90.000001 60.      ]
    # Vector2D[100.000001  60.      ]
    # Vector2D[100.000001  60.      ]

    # CubicBezier2D(Vector2D[40. 50.], Vector2D[49. 60.], Vector2D[54.5 55. ], Vector2D[58.91666667 50.83333333])
    # CubicBezier2D(Vector2D[58.91666667 50.83333333], Vector2D[63.33333333 46.66666667], Vector2D[66.66666667 43.33333333], Vector2D[70. 45.])
    # CubicBezier2D(Vector2D[70. 45.], Vector2D[73.33333333 46.66666667], Vector2D[76.66666667 53.33333333], Vector2D[83.33333333 56.66666667])
    # CubicBezier2D(Vector2D[83.33333333 56.66666667], Vector2D[90. 60.], Vector2D[100.  60.], Vector2D[100.  60.])

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
    # scene_importer.scene.bezier_path(vertices, degree=3, path_style=path_style, user_data=None)

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
            kwargs = dict(user_data=item)
            if item.domain:
                kwargs['start_angle'] = item.domain.start
                kwargs['stop_angle'] = item.domain.stop
            self._scene.circle(item.center, item.radius,
                               path_style,
                               **kwargs,
            )
        elif isinstance(item, BSpline2D):
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
            for bezier in item.to_bezier():
                self._scene.cubic_bezier(*bezier.points,
                                         path_style,
                                         user_data=item,
                )
        elif isinstance(item, Ellipse2D):
            self._scene.ellipse(item.center,
                                item.x_radius,
                                item.y_radius,
                                item.angle,
                                path_style,
                                user_data=item,
            )
        elif isinstance(item, list):
            for segment in item:
                self._add_item(segment)

        self._update_bounding_box(item)

####################################################################################################

# filename = 'protection-rectangulaire-v2.dxf'
filename = 'test-dxf-r15.dxf'
try:
    dxf_path = Path(__file__).parent.joinpath(filename)
except:
    dxf_path = Path('examples', 'dxf', filename)

scene_importer = SceneImporter(dxf_path)

# spline_from_svg(scene_importer)

application.qml_application.scene = scene_importer.scene
