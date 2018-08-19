####################################################################################################
#
# Patro - A Python library to make patterns for fashion design
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

"""This modules implements the SVG file format.

Import Algorithm:

* text is informative, connect text to path
* short lines or polygon are sewing markers
* line with a small polygon at extremities is a grainline
* expect pieces are delimited by a path
* check for paths sharing vertexes and stroke style
"""

####################################################################################################

import logging
from pathlib import Path

from lxml import etree

from Patro.Common.Xml.XmlFile import XmlFileMixin
from . import SvgFormat

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class SvgDispatcher:

    """Class to dispatch XML to Python class."""

    __TAGS__ = {}
    for cls_name in SvgFormat.__all__:
        cls = getattr(SvgFormat, cls_name)
        __TAGS__[cls.__tag__] = cls

    __TAGS_TO_READ__ = [
        # 'svg', # implicit
        # 'anchor',
        # 'altGlyph',
        # 'altGlyphDef',
        # 'altGlyphItem',
        # 'animate',
        # 'animateMotion',
        # 'animateTransform',
        'circle',
        #? 'clipPath',
        # 'colorProfile',
        # 'cursor',
        # 'defs',
        # 'desc',
        'ellipse',
        # 'feBlend',
        # 'group', # implicit
        # 'image',
        'line',
        # 'linearGradient',
        # 'marker',
        # 'mask',
        'path',
        # 'pattern',
        'polyline',
        'polygon',
        # 'radialGradient',
        'rect',
        # 'stop',
        #! 'text',
        # 'textRef',
        #! 'textSpan',
        # 'use',
    ]

    ##############################################

    def __init__(self, root):

        self.on_root(root)

    ##############################################

    def element_tag(self, element):

        tag = element.tag
        if '{' in tag:
            tag = tag[tag.find('}')+1:]
        return tag

    ##############################################

    def from_xml(self, element):

        tag = self.element_tag(element)
        tag_class = self.__TAGS__[tag]
        if tag_class is not None:
            print(element, tag_class)
            return tag_class(element)
        else:
            raise NotImplementedError

    ##############################################

    def on_root(self, root):

        for element in root:
            tag = self.element_tag(element)
            if tag == 'g':
                self.on_group(element)
            elif tag in self.__TAGS_TO_READ__:
                self.on_graphic_item(element)

    ##############################################

    def on_group(self, group):

        self.on_root(group)

    ##############################################

    def on_graphic_item(self, element):

        item = self.from_xml(element)
        print(item)

####################################################################################################

class SvgFile(XmlFileMixin):

    """Class to read/write SVG file."""

    _logger = _module_logger.getChild('SvgFile')

    ##############################################

    def __init__(self, path=None):

        # Fixme: path
        if path is None:
            path = ''
        XmlFileMixin.__init__(self, path)
        # Fixme:
        # if path is not None:
        if path != '':
            self._read()

    ##############################################

    def _read(self):

        # <?xml version="1.0" encoding="UTF-8" standalone="no"?>
        # <!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
        # <svg xmlns="http://www.w3.org/2000/svg"
        #      xmlns:xlink="http://www.w3.org/1999/xlink"
        #      version="1.1"
        #      width="1000.0pt" height="1000.0" viewBox="0 0 1000.0 1000.0"
        # ></svg>

        tree = self._parse()
        dispatch = SvgDispatcher(tree)
        # Fixme: ...

    ##############################################

    def write(self, path=None):

        root = etree.Element('pattern')
        root.append(etree.Comment('Pattern created with Patro (https://github.com/FabriceSalvaire/Patro)'))

        # Fixme: ...

        if path is None:
            path = self.path
        with open(str(path), 'wb') as f:
            # ElementTree.write() ?
            f.write(etree.tostring(root, pretty_print=True))

