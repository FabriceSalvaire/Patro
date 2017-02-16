####################################################################################################

from Valentina.Measurement import VitParser
from Valentina.Pattern import ValParser

####################################################################################################

vit_parser = VitParser()
measurements = vit_parser.parse('measurements.vit')
measurements.eval()

val_parser = ValParser()
pattern = val_parser.parse('flat-city-trouser.val')
pattern.dump()
