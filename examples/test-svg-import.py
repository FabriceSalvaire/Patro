####################################################################################################

from pathlib import Path

from Patro.Common.Logging import Logging
Logging.setup_logging()

from Patro.FileFormat.Svg.SvgFile import SvgFile

####################################################################################################

svg_file = SvgFile(Path('patterns', 'veravenus-little-bias-dress.pattern-a0.svg'))
