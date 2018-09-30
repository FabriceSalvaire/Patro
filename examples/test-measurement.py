####################################################################################################

from Patro.Common.Logging import Logging
Logging.setup_logging()

####################################################################################################

from pathlib import Path

from Patro.FileFormat.Valentina.Measurement import VitFile
from Patro.Measurement.Measurement import Measurements

####################################################################################################

vit_file = VitFile(Path('patterns', 'measurements.vit'))
# vit_file.measurements.dump()
yaml_path = Path('output', 'measurements.yaml')
vit_file.measurements.save_as_yaml(yaml_path)

measurements = Measurements()
measurements.load_yaml(yaml_path)
measurements.dump()
