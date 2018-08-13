####################################################################################################

from Valentina.Logging import Basic

####################################################################################################

from pathlib import Path

from Valentina.FileFormat.Pattern import ValFile
from Valentina.Painter.Paper import PaperSize
from Valentina.Painter.TexPainter import TexPainter

####################################################################################################

val_file = ValFile(Path('patterns', 'flat-city-trouser.val'))
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

scene = pattern.detail_scene()

tex_path = output.joinpath('pattern-a0.tex')
paper = PaperSize('a0', 'portrait', 10)
tex_painter = TexPainter(str(tex_path), scene, paper)
tex_painter.add_detail_figure()
tex_painter._document.write()

tex_path = output.joinpath('pattern-a4.tex')
paper = PaperSize('a4', 'portrait', 10)
tex_painter = TexPainter(str(tex_path), scene, paper)
tex_painter.add_tiled_detail_figure()
tex_painter._document.write()
