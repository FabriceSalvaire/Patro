####################################################################################################
#
# PyValentina - A Python implementation of Valentina Pattern Drafting Software
# Copyright (C) 2017 Salvaire Fabrice
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
####################################################################################################

####################################################################################################

import unittest

####################################################################################################

from Valentina.Painter.Paper import PaperSize
from Valentina.Painter.TexPainter import TexPainter

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
