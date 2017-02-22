####################################################################################################
#
# PyValentina - A Python implementation of Valentina Pattern Drafting Software
# Copyright (C) 2017 Fabrice Salvaire
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

import logging
from pathlib import Path

from lxml import etree

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class XmlFileMixin:

    # _logger = _module_logger.getChild('XmlFile')

    ##############################################

    def __init__(self, path):

        self._path = Path(path)

    ##############################################

    @property
    def path(self):
        return self._path

    ##############################################

    def _parse(self):

        with open(str(self._path), 'rb') as f:
            source = f.read()

        return etree.fromstring(source)

    ##############################################

    @staticmethod
    def _get_xpath_element(root, path):

        return root.xpath(path)[0]
