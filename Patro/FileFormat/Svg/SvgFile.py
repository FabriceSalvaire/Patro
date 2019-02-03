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

from IntervalArithmetic import Interval2D

from Patro.Common.Xml.XmlFile import XmlFileMixin
from Patro.GeometryEngine.Transformation import AffineTransformation2D
from . import SvgFormat

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class RenderState:

    # Fixme: convert type !!!

    STATES = [name for name in SvgFormat.PresentationAttributes.__dict__.keys()
              if not name.startswith('_')]

    ##############################################

    @classmethod
    def to_python(cls, value):

        # Fixme: move ???

        if isinstance(value, str):
            if value == 'none':
                return None
            else:
                try:
                    float_value = float(value)
                    if '.' in value:
                        return float_value
                    else:
                        return int(float_value)
                except ValueError:
                    pass

        return value

    ##############################################

    def __init__(self, item=None):

        # Init from item else use default value
        for state in self.STATES:
            if item is not None and hasattr(item, state):
                value = self.to_python(getattr(item, state))
            else:
                value = getattr(SvgFormat.PresentationAttributes, state)
            setattr(self, state, value)

    ##############################################

    def clone(self):
        return self.__class__(self)

    ##############################################

    def to_dict(self, all=False):

        if all:
            return {state:getattr(self, state) for state in self.STATES}
        else:
            d = {}
            for state in self.STATES:
                value = getattr(self, state)
                if value is not None:
                    d[state] = value
            return d

    ##############################################

    def merge(self, item):

        for state in self.STATES:
            if hasattr(item, state):
                value = getattr(item, state)
                if state == 'transform':
                    if value is not None:
                        # Transform matrix is composed from top to item
                        # thus left to right
                        self.transform = self.transform * value
                elif state == 'style':
                    pass
                else:
                    setattr(self, state, self.to_python(value))

        # Merge style
        style = getattr(item, 'style', None)
        if style is not None:
            for pair in style.split(';'):
                state, value = [x.strip() for x in pair.split(':')]
                state = state.replace('-', '_')
                if state == 'transform':
                    self.transform = self.transform * value
                else:
                    setattr(self, state, self.to_python(value))

        return self

    ##############################################

    def __str__(self):
        return str(self.to_dict())

####################################################################################################

class RenderStateStack:

    ##############################################

    def __init__(self):

        self._stack = [RenderState()]

    ##############################################

    @property
    def state(self):
        return self._stack[-1]

    ##############################################

    def push(self, kwargs):
        new_state = self.state.clone()
        new_state.merge(kwargs)
        self._stack.append(new_state)

    ##############################################

    def pop(self):
        self._stack.pop()

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

    _logger = _module_logger.getChild('SvgDispatcher')

    ##############################################

    def __init__(self, reader):

        self._reader =reader
        self.reset()
        # self.on_root(root)

    ##############################################

    def reset(self):
        self._state_stack = RenderStateStack()

    ##############################################

    @property
    def state(self):
        return self._state_stack.state

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
            # self._logger.info('\n{}  /  {}'.format(element, tag_class))
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

    def on_group(self, element):

        group = self.from_xml(element)
        # self._logger.info('Group: {}\n{}'.format(group.id, group))
        self._reader.on_group(group)

        self._state_stack.push(group)
        # self._logger.info('State:\n' + str(self.state))

        self.on_root(element)

    ##############################################

    def on_graphic_item(self, element):

        item = self.from_xml(element)
        # self._logger.info('Item: {}\n{}'.format(item.id, item))
        self._reader.on_graphic_item(item)

####################################################################################################

class SvgFileMixin:

    SVG_DOCTYPE = '<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">'
    SVG_xmlns = 'http://www.w3.org/2000/svg'
    SVG_xmlns_xlink = 'http://www.w3.org/1999/xlink'
    SVG_version = '1.1'

####################################################################################################

class SvgFileInternal(XmlFileMixin, SvgFileMixin):

    """Class to read/write SVG file."""

    _logger = _module_logger.getChild('SvgFile')

    __dispatcher_cls__ = SvgDispatcher

    ##############################################

    def __init__(self, path, data=None):

        super().__init__(path, data)

        # Fixme: API
        #  purpose of dispatcher, where must be state ???
        self._dispatcher = self.__dispatcher_cls__(self)
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

        tree = self.parse()

        svg_root = self._dispatcher.from_xml(tree)
        self.on_svg_root(svg_root)

        self._dispatcher.on_root(tree)

    ##############################################

    @property
    def view_box(self):
        return self._view_box

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    ##############################################

    def on_svg_root(self, svg_root):
        x_inf, y_inf, x_sup, y_sup = svg_root.view_box
        self._view_box = Interval2D((x_inf, x_sup), (y_inf, y_sup))
        self._width = svg_root.width
        self._height = svg_root.height

    ##############################################

    def on_group(self, group):
        self._logger.info('Group: {}\n{}'.format(group.id, group))

    ##############################################

    def on_graphic_item(self, item):

        self._logger.info('Item: {}\n{}'.format(item.id, item))
        state = self._dispatcher.state.clone().merge(item)
        self._logger.info('Item State:\n' + str(state))

####################################################################################################

class SvgFileWriter(SvgFileMixin):

    """Class to write a SVF file."""

    _logger = _module_logger.getChild('SvgFileWriter')

    COMMENT = 'Pattern created with Patro (https://github.com/FabriceSalvaire/Patro)'

    ##############################################

    def __init__(self, path, paper, root_tree, transformation=None):

        self._path = str(path)

        self._write(paper, root_tree, transformation)

    ##############################################

    @classmethod
    def _new_root(cls, paper):

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
        root.append(etree.Comment(cls.COMMENT))

        return root

    ##############################################

    def _write(self, paper, root_tree, transformation=None):

        root = self._new_root(paper)

        # Fixme: implement tree, look at lxml
        if transformation:
            # transform text as well !!!
            group = SvgFormat.Group(transform=transformation).to_xml()
            root.append(group)
        else:
            group = root

        for element in root_tree:
            group.append(element.to_xml())

        tree = etree.ElementTree(root)
        tree.write(self._path,
                   pretty_print=True,
                   xml_declaration=True,
                   encoding='utf-8',
                   standalone=False,
                   doctype=self.SVG_DOCTYPE,
        )

####################################################################################################

class SvgFile:

    ##############################################

    def __init__(self, path):
        self._interval = SvgFileInternal(path)
