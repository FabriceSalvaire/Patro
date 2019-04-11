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

__all__ = ['StitchType', 'StitchDatabase']

####################################################################################################

from .Database import Database

####################################################################################################

class StitchType:

    """Class to define stitch type.

    Stitch types are described in reference documents

    * `ASTM D6193 <https://www.astm.org/Standards/D6193.htm>`_
    * `ISO 4915:1991 Textiles — Stitch types — Classification and terminology <https://www.iso.org/standard/10932.html>`_

    """

    ##############################################

    def __init__(self, number, name, number_of_needles, number_of_threads, number_of_loops):

        self._number = int(number) # cf. ISO 4915:1991
        self._name = str(name)

        self._number_of_needles = int(number_of_needles)
        self._number_of_threads = int(number_of_threads)
        self._number_of_loops = int(number_of_loops) # looper

        # a 3D model and SVG projection, with a color per thread

    ##############################################

    @property
    def number(self):
        return self._number

    @property
    def name(self):
        return self._name

    @property
    def number_of_needles(self):
        return self._number_of_needles

    @property
    def number_of_threads(self):
        return self._number_of_threads

    @property
    def number_of_loops(self):
        return self._number_of_loops

####################################################################################################

class StitchDatabase(Database):

    DEFAULT_DATA_FILENAME = 'stitch.yaml'

    ##############################################

    def load(self, yaml_path=None):

        data = super().load(yaml_path)

        self._introduction = data['introduction']
        classes =  data['classes']

        for classe_name, stitch_classe in classes.items():
            name = stitch_classe['name']
            description = stitch_classe['description']
            for stitch_number, stitch_data in stitch_classe['stitches'].items():
                if stitch_data is not None:
                    name = stitch_data['name']
                    number_of_needles = stitch_data.get('number_of_needles', None)
                    number_of_threads = stitch_data.get('number_of_threads', None)
                    number_of_loops = stitch_data.get('number_of_loops', None)
                    composition = stitch_data.get('composition', None)
                    astm = stitch_data.get('astm', None)
