####################################################################################################

import logging

# FORMAT = '%(asctime)s - %(name)s - %(module)s.%(levelname)s - %(message)s'
FORMAT = '\033[1;32m%(asctime)s\033[0m - \033[1;34m%(name)s.%(funcName)s\033[0m - \033[1;31m%(levelname)s\033[0m - %(message)s'
logging.basicConfig(format=FORMAT, level=logging.DEBUG)

####################################################################################################

from Valentina.Pattern import ValParser

####################################################################################################

val_parser = ValParser()
pattern = val_parser.parse('flat-city-trouser.val')
pattern.dump()
