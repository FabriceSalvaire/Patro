####################################################################################################

from pathlib import Path

from Patro.Common.Logging import Logging
Logging.setup_logging()

from Patro.FileFormat.Valentina.Pattern import ValFile

####################################################################################################

parts = ('patterns', 'several-pieces.val')
try:
    val_path = Path(__file__).parent.joinpath(*parts)
except:
    val_path = Path('examples', *parts)
val_file = ValFile(val_path)
pattern = val_file.pattern

# pattern.dump()

# for calculation in pattern.calculations:
#     print(calculation.to_python())

# nodes = pattern.calculator.dag.topological_sort()
# for node in nodes:
#     print(node.data)

output = Path('output')
output.mkdir(exist_ok=True)

val_file.write(output.joinpath('write-test.val'))
