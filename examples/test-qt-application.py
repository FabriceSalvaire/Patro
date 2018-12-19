####################################################################################################

from pathlib import Path

from Patro.Common.Logging import Logging
Logging.setup_logging()

from Patro.FileFormat.Valentina.Pattern import ValFile
from Patro.GraphicEngine.Painter.Paper import PaperSize
from Patro.GraphicEngine.Painter.QtPainter import QtScene

####################################################################################################

# val_file = 'flat-city-trouser.val'
val_file = 'path-bezier.val'

try:
    val_path = Path(__file__).parent.joinpath('patterns', val_file)
except:
    val_path = Path('examples', 'patterns', val_file)
val_file = ValFile(val_path)
pattern = val_file.pattern

kwargs = dict(scene_cls=QtScene)
first_scope = pattern.scope(0)
scene = first_scope.sketch.detail_scene(**kwargs)

application.qml_application.scene = scene
