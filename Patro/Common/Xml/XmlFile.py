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

import logging
from pathlib import Path

from lxml import etree

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class XmlFileMixin:

    """Class mixin to parse a XML file using lxml module"""

    # _logger = _module_logger.getChild('XmlFile')

    ##############################################

    def __init__(self, path, data=None):

        if path is not None:
            self._path = Path(path)
        else:
            self._path = None
        self._data = data

    ##############################################

    @property
    def path(self):
        return self._path

    ##############################################

    def parse(self):
        """Parse a XML file and return the etree"""

        data = self._data
        if data is None:
            with open(str(self._path), 'rb') as f:
                source = f.read()
        else:
            if isinstance(data, bytes):
               source = data
            else:
                source = bytes(str(self._data).strip(), 'utf-8')

        return etree.fromstring(source)

    ##############################################

    @staticmethod
    def get_xpath_elements(root, path):
        """Utility function to get elements from a xpath and a root"""
        return root.xpath(path)

    ##############################################

    @staticmethod
    def get_xpath_element(root, path):
        """Utility function to get an element from a xpath and a root"""
        element = root.xpath(path)
        if element:
            return element[0]
        else:
            return None

    ##############################################

    @classmethod
    def get_text_element(cls, root, path):
        """Utility function to a text element from a xpath and a root"""
        element = cls.get_xpath_element(root, path)
        if hasattr(element, 'text'):
            return element.text
        else:
            return None
