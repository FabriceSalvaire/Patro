####################################################################################################

import Logging

####################################################################################################

from Valentina import ValParser
from Valentina.Modelling.Tex import Tex

####################################################################################################

val_parser = ValParser()
pattern = val_parser.parse('flat-city-trouser.val')
pattern.dump()

tex = Tex('pattern.tex')
tex.open()
# tex.add_detail_figure(pattern)
tex.add_tiled_detail_figure(pattern)
tex.close()
