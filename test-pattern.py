####################################################################################################

import logging

# FORMAT = '%(asctime)s - %(name)s - %(module)s.%(levelname)s - %(message)s'
FORMAT = '\033[1;32m%(asctime)s\033[0m - \033[1;34m%(name)s.%(funcName)s\033[0m - \033[1;31m%(levelname)s\033[0m - %(message)s'
logging.basicConfig(format=FORMAT, level=logging.DEBUG)

####################################################################################################

from Valentina.Pattern import ValParser
from Valentina.Tex import Tex

####################################################################################################

val_parser = ValParser()
pattern = val_parser.parse('flat-city-trouser.val')
pattern.dump()

tex = Tex('pattern.tex')
tex.open()
tex.add_detail_figure(pattern)
tex.close()
