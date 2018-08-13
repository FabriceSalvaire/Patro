####################################################################################################

from Patro.Logging import Basic

####################################################################################################

from pathlib import Path

from Patro.FileFormat.Measurements import VitFile

####################################################################################################

vit_file = VitFile(Path('patterns', 'measurements.vit'))
vit_file.measurements.dump()
