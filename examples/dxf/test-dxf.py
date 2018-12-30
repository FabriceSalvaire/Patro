####################################################################################################

from pathlib import Path

from Patro.Common.Logging import Logging
Logging.setup_logging()

from Patro.FileFormat.Dxf.Importer import DxfImporter
from Patro.GeometryEngine.Bezier import CubicSpline2D
from Patro.GeometryEngine.Conic import Circle2D, Conic2D
from Patro.GeometryEngine.Segment import Segment2D
from Patro.GraphicEngine.GraphicScene.GraphicItem import GraphicStyle
from Patro.GraphicEngine.Painter.QtPainter import QtScene

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

        path_style = GraphicStyle(line_width='1pt')
        if isinstance(item, Segment2D):
            self._scene.segment(item.p0, item.p1,
                                path_style,
                                user_data=item,
            )
        elif isinstance(item, Circle2D):
            print(item.center, item.radius)
            self._scene.circle(item.center, item.radius,
                               path_style,
                               user_data=item,
            )
        elif isinstance(item, CubicSpline2D):
            for part in item.iter_on_parts():
                bezier = part.to_bezier()
                self._scene.cubic_bezier(bezier.p0,
                                         bezier.p1, bezier.p2,
                                         bezier.p3,
                                         path_style,
                                         user_data=item,
                )
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

application.qml_application.scene = scene_importer.scene
