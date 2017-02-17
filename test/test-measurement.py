####################################################################################################

from Valentina.Measurement import VitParser

####################################################################################################

vit_parser = VitParser()
measurements = vit_parser.parse('measurements.vit')
measurements.dump()
