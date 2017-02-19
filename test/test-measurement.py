####################################################################################################

import Logging

from Valentina import VitParser

####################################################################################################

vit_parser = VitParser()
measurements = vit_parser.parse('measurements.vit')
measurements.dump()
