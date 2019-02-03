####################################################################################################
#
# Patro - A Python library to make patterns for fashion design
# Copyright (C) 2017 Fabrice Salvaire
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

import unittest

####################################################################################################

from Patro.GraphicEngine.Painter.Paper import PaperSize
from Patro.GraphicEngine.Painter.TexPainter import TexPainter

####################################################################################################

class TestTexPainter(unittest.TestCase):

    ##############################################

    def test(self):

        paper = PaperSize('a4', 'portrait', 10)
        tex_painter = TexPainter('out.tex', None, paper)
        print(tex_painter._document)

####################################################################################################

if __name__ == '__main__':

    unittest.main()
