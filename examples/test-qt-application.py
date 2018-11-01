####################################################################################################

from pathlib import Path

from Patro.Common.Logging import Logging
Logging.setup_logging()

from Patro.FileFormat.Valentina.Pattern import ValFile
from Patro.GraphicEngine.Painter.Paper import PaperSize
from Patro.GraphicEngine.Painter.QtPainter import QtScene

####################################################################################################

try:
    val_path = Path(__file__).parent.joinpath('patterns', 'flat-city-trouser.val')
except:
    val_path = Path('examples', 'patterns', 'flat-city-trouser.val')
val_file = ValFile(val_path)
pattern = val_file.pattern

kwargs = dict(scene_cls=QtScene)
scene = pattern.detail_scene(**kwargs)

application.qml_application.scene = scene
