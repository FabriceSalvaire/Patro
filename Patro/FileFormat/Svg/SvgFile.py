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

from lxml import etree

from Patro.Common.Xml.XmlFile import XmlFileMixin
from . import SvgFormat

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class RenderState:

    ##############################################

    def __init__(self):

        self._transformations = []

    ##############################################

    def push_transformation(self, transformation):
        self._transformations.append(transformation)

    def pop_transformation(self):
        self._transformations.pop()

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

        self._state = RenderState()

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

    SVG_DOCTYPE = '<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">'
    SVG_xmlns = 'http://www.w3.org/2000/svg'
    SVG_xmlns_xlink = 'http://www.w3.org/1999/xlink'
    SVG_version = '1.1'

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

    @classmethod
    def new_root(cls, paper):

        nsmap = {
            None: cls.SVG_xmlns,
            'xlink': cls.SVG_xmlns_xlink,
        }
        root = etree.Element('svg', nsmap=nsmap)
        attrib = root.attrib
        attrib['version'] = cls.SVG_version
        # Set document dimension and user space unit to mm
        # see https://mpetroff.net/2013/08/analysis-of-svg-units
        attrib['width'] = '{:.3f}mm'.format(paper.width)
        attrib['height'] = '{:.3f}mm'.format(paper.height)
        attrib['viewBox'] = '0 0 {:.3f} {:.3f}'.format(paper.width, paper.height)

        # Fixme: from conf
        root.append(etree.Comment('Pattern created with Patro (https://github.com/FabriceSalvaire/Patro)'))

        return root

    ##############################################

    def write(self, paper, root_tree, transformation=None, path=None):

        root = self.new_root(paper)

        # Fixme: implement tree, look at lxml
        if transformation:
            # transform text as well !!!
            group = SvgFormat.Group(transform=transformation).to_xml()
            root.append(group)
        else:
            group = root

        for element in root_tree:
            group.append(element.to_xml())

        if path is None:
            path = self.path

        tree = etree.ElementTree(root)
        tree.write(str(path),
                   pretty_print=True,
                   xml_declaration=True,
                   encoding='utf-8',
                   standalone=False,
                   doctype=self.SVG_DOCTYPE,
        )
