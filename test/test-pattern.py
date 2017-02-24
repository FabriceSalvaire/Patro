####################################################################################################

from Valentina.Logging import Basic

####################################################################################################

from pathlib import Path

from Valentina.FileFormat.Pattern import ValFile
from Valentina.Pattern.Tex import Tex

####################################################################################################

val_file = ValFile(Path('patterns', 'flat-city-trouser.val'))
pattern = val_file.pattern

pattern.dump()

output = Path('output')
output.mkdir(exist_ok=True)

tex = Tex(output.joinpath('pattern.tex'), paper='a4paper', margin=10)
tex.open()
# tex.add_detail_figure(pattern)
tex.add_tiled_detail_figure(pattern)
tex.close()

# val_file.write(output.joinpath('write-test.val'))

# for calculation in pattern.calculations:
#     print(calculation.to_python())
