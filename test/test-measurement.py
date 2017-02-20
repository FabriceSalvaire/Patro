####################################################################################################

from Valentina.Logging import Basic

from Valentina.FileFormat.Measurements import VitFile

####################################################################################################

vit_file = VitFile('measurements.vit')
vit_file.measurements.dump()
