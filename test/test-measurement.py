####################################################################################################

from Valentina.Logging import Basic

####################################################################################################

from pathlib import Path

from Valentina.FileFormat.Measurements import VitFile

####################################################################################################

vit_file = VitFile(Path('patterns', 'measurements.vit'))
vit_file.measurements.dump()
