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

import os
import subprocess

####################################################################################################

from .Buffer import Buffer
from .Environment import Environment

####################################################################################################

LINE_BREAK = r'\\'

####################################################################################################

class Document:

    ##############################################

    def __init__(self, filename, class_name, class_options=''):

        # Fixme: Path, vs path

        if (len(filename) - filename.rfind('.tex')) == 4:
            filename = filename[:-4]

        self._filename = filename
        self._class_name = class_name
        self._class_options = class_options

        self._preambule = Buffer()
        self._content = Environment(name='document')

    ##############################################

    @property
    def tex_filename(self):
        return self._filename + '.tex'

    @property
    def output_directory(self):
        return os.path.dirname(self._tex_filename())

    @property
    def pdf_filename(self):
        return self._filename + '.pdf'

    @property
    def preambule(self):
        return self._preambule

    @property
    def content(self):
        return self._content

    ##############################################

    @staticmethod
    def _format(pattern, *args, **kwargs):

        pattern = pattern.replace('{', '{{')
        pattern = pattern.replace('}', '}}')
        pattern = pattern.replace('«', '{')
        pattern = pattern.replace('»', '}')
        return pattern.format(*args, **kwargs)

    ##############################################

    def __str__(self):

        source = self._format(r'\documentclass[«0._class_options»]{«0._class_name»}', self) + '\n'
        source += str(self._preambule)
        source += str(self._content)
        return source

    ##############################################

    def newpage(self):

        self._content.append(r'\newpage' + '\n')

    ##############################################

    def write(self):

        with open(self.tex_filename, 'w') as fd:
            fd.write(str(self))

    ##############################################

    def run_pdflatex(self):

        pass
        # command_template = 'pdflatex --interaction=batchmode --output-directory=%s %s'
        # command =  command_template % (self.output_directory(), self.tex_filename())
        # subprocess.call([command], shell=True)
