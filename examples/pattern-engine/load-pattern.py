####################################################################################################
#
# Patro - A Python library to make patterns for fashion design
# Copyright (C) 2019 Fabrice Salvaire
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
####################################################################################################

####################################################################################################
#
# run as
#
#    ./bin/patro --user-script examples/...
#
####################################################################################################

####################################################################################################

# from Patro.Common.Logging import Logging
# Logging.setup_logging()

from Patro.FileFormat.Valentina.Pattern import ValFileReader
from Patro.GraphicEngine.Painter.Paper import PaperSize
from Patro.GraphicEngine.Painter.QtPainter import QtScene
from PatroExample import find_data_path

####################################################################################################

val_file = 'flat-city-trouser.val'
# val_file = 'path-bezier.val'
val_path = find_data_path('patterns-valentina', val_file)

val_file = ValFileReader(val_path)
pattern = val_file.pattern

kwargs = dict(scene_cls=QtScene)
first_scope = pattern.scope(0)
scene = first_scope.sketch.detail_scene(**kwargs)

application.qml_application.scene = scene
