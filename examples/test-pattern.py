####################################################################################################

from pathlib import Path

from Patro.Common.Logging import Logging
Logging.setup_logging()

from Patro.FileFormat.Valentina.Pattern import ValFile
from Patro.GraphicEngine.Painter.Paper import PaperSize
from Patro.GraphicEngine.Painter.DxfPainter import DxfPainter
from Patro.GraphicEngine.Painter.MplPainter import MplPainter
from Patro.GraphicEngine.Painter.PdfPainter import PdfPainter
from Patro.GraphicEngine.Painter.SvgPainter import SvgPainter
from Patro.GraphicEngine.Painter.TexPainter import TexPainter
from Patro.GraphicEngine.Painter.QtPainter import QtScene

####################################################################################################

try:
    val_path = Path(__file__).parent.joinpath('patterns', 'flat-city-trouser.val')
except:
    val_path = Path('examples', 'patterns', 'flat-city-trouser.val')
val_file = ValFile(val_path)
pattern = val_file.pattern

pattern.dump()

for calculation in pattern.calculations:
    print(calculation.to_python())

nodes = pattern.calculator.dag.topological_sort()
for node in nodes:
    print(node.data)

output = Path('output')
output.mkdir(exist_ok=True)

val_file.write(output.joinpath('write-test.val'))

kwargs = dict(scene_cls=QtScene)
scene = pattern.detail_scene(**kwargs)

application.qml_application.scene = scene

# tex_path = output.joinpath('pattern-a0.tex')
# paper = PaperSize('a0', 'portrait', 10)
# tex_painter = TexPainter(str(tex_path), scene, paper)
# tex_painter.add_detail_figure()
# tex_painter._document.write()

# tex_path = output.joinpath('pattern-a4.tex')
# paper = PaperSize('a4', 'portrait', 10)
# tex_painter = TexPainter(str(tex_path), scene, paper)
# tex_painter.add_tiled_detail_figure()
# tex_painter._document.write()

# paper = PaperSize('a0', 'portrait', 10)
# mpl_painter = MplPainter(scene, paper)
# mpl_painter.show()

# paper = PaperSize('a0', 'portrait', 10)
# pdf_path = output.joinpath('pattern-a0-reportlab.pdf')
# pdf_painter = PdfPainter(pdf_path, scene, paper, driver='reportlab')

# paper = PaperSize('a0', 'portrait', 10)
# svg_path = output.joinpath('pattern-a0.svg')
# svg_painter = SvgPainter(svg_path, scene, paper)

# paper = PaperSize('a0', 'portrait', 10)
# dxf_path = output.joinpath('pattern.dxf')
# dxf_painter = DxfPainter(dxf_path, scene, paper)
