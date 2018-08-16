####################################################################################################

from Patro.Common.Logging import Logging
Logging.setup_logging()

####################################################################################################

from pathlib import Path

from Patro.FileFormat.Valentina.Measurements import VitFile

####################################################################################################

vit_file = VitFile(Path('patterns', 'measurements.vit'))
vit_file.measurements.dump()
