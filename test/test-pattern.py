####################################################################################################

from Valentina.Logging import Basic

####################################################################################################

from Valentina.FileFormat.Pattern import ValFile
from Valentina.Pattern.Tex import Tex

####################################################################################################

val_file = ValFile('flat-city-trouser.val')
pattern = val_file.pattern

pattern.dump()

tex = Tex('pattern.tex')
tex.open()
tex.add_detail_figure(pattern)
# tex.add_tiled_detail_figure(pattern)
tex.close()
