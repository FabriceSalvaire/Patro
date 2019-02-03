####################################################################################################
#
# Patro - A Python library to make patterns for fashion design
# Copyright (C) 2018 Fabrice Salvaire
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
####################################################################################################

####################################################################################################

from pathlib import Path

from Patro.Common.Logging import Logging
Logging.setup_logging()

from Patro.FileFormat.Valentina.Pattern import ValFileReader, ValFileWriter
from Patro.GraphicEngine.GraphicScene.TypographyUnit import PointUnit
from Patro.GraphicEngine.Painter.Paper import PaperSize
from Patro.Pattern.SketchStyle import DetailSketchStyle
from PatroExample import find_data_path

from Patro.GraphicEngine.Painter.DxfPainter import DxfPainter
from Patro.GraphicEngine.Painter.MplPainter import MplPainter
from Patro.GraphicEngine.Painter.PdfPainter import PdfPainter
from Patro.GraphicEngine.Painter.SvgPainter import SvgPainter
from Patro.GraphicEngine.Painter.TexPainter import TexPainter

####################################################################################################

val_file = 'flat-city-trouser.val'
val_path = find_data_path('patterns-valentina', val_file)

val_file = ValFileReader(val_path)
pattern = val_file.pattern

scope_names = pattern.scope_names()
print(scope_names)
scope = pattern.scope(scope_names[0])
sketch = scope.sketch

sketch.dump()

for operation in sketch.operations:
    print(operation.to_python())

nodes = sketch.calculator.dag.topological_sort()
for node in nodes:
    print(node.data)

output = Path('output')
output.mkdir(exist_ok=True)

# Fixme: see VitFormat.py StrokeStyleAttribute !!!
# val_file.write(output.joinpath('write-test.val'))
val_file = ValFileWriter(output.joinpath('write-test-from-api.val'), val_file.vit_file, pattern)

scene = sketch.detail_scene()

# paper = PaperSize('a0', 'portrait', 10)
# mpl_painter = MplPainter(scene, paper)
# mpl_painter.show()

# paper = PaperSize('a0', 'portrait', 10)
# pdf_path = output.joinpath('pattern-a0-reportlab.pdf')
# pdf_painter = PdfPainter(pdf_path, scene, paper, driver='reportlab')

paper = PaperSize('a0', 'portrait', 10)
svg_path = output.joinpath('pattern-a0.svg')
svg_painter = SvgPainter(svg_path, scene, paper)

# paper = PaperSize('a0', 'portrait', 10)
# dxf_path = output.joinpath('pattern.dxf')
# dxf_painter = DxfPainter(dxf_path, scene, paper)


# style = DetailSketchStyle(
#     point_size=PointUnit(1),
#     line_style=PointUnit(.5),
# )
# scene = sketch.detail_scene(style=style)

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
