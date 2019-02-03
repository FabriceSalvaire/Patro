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

"""This module implements the Valentina val XML file format.

"""

####################################################################################################

import logging
from pathlib import Path

from lxml import etree

from Patro.Common.Xml.XmlFile import XmlFileMixin
from Patro.Pattern.Pattern import Pattern
from .Measurement import VitFile
from .VitFormat import (
    Point,
    Line,
    Spline,
    ModelingPoint,
    ModelingSpline,
    Detail,
    DetailData,
    DetailPatternInfo,
    DetailGrainline,
    DetailNode,
)

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

# Last valentina version supported
VAL_VERSION = '0.7.10'

####################################################################################################

class Modeling:

    """Class to implement a modeling mapper."""

    ##############################################

    def __init__(self):
        self._id_map = {}

    ##############################################

    def __getitem__(self, id):
        return self._id_map[id]

    ##############################################

    def add(self, item):
        self._id_map[item.id] = item

####################################################################################################

class Dispatcher:

    """Baseclass to dispatch XML to Python class."""

    __TAGS__ = {}

    ##############################################

    def from_xml(self, element):

        tag_cls = self.__TAGS__[element.tag]
        if tag_cls is not None:
            return tag_cls(element)
        else:
            raise NotImplementedError

####################################################################################################

class CalculationDispatcher(Dispatcher):

    """Class to implement a dispatcher for calculations."""

    _logger = _module_logger.getChild('CalculationDispatcher')

    __TAGS__ = {
        'arc': None,
        'ellipse': None,
        'line': Line,
        'operation': None,
        'point': Point,
        'spline': Spline,
        }

    ##############################################

    def __init__(self):

        # Fixme: could be done in class definition
        self._mapping = {} # used for Calculation -> XML
        self._init_mapper()

    ##############################################

    def _register_mapping(self, xml_cls):

        operation_cls = xml_cls.__operation__
        if operation_cls:
            self._mapping[xml_cls] = operation_cls
            self._mapping[operation_cls] = xml_cls

    ##############################################

    def _init_mapper(self):

        for tag_cls in self.__TAGS__.values():
            if tag_cls is not None:
                if hasattr(tag_cls, '__TYPES__'):
                    for xml_cls in tag_cls.__TYPES__.values():
                        if xml_cls is not None:
                            self._register_mapping(xml_cls)
                else:
                    self._register_mapping(tag_cls)

    ##############################################

    def from_xml(self, element):

        tag_cls = self.__TAGS__[element.tag]
        if hasattr(tag_cls, '__TYPES__'):
            cls = tag_cls.__TYPES__[element.attrib['type']]
        else:
            cls = tag_cls
        if cls is not None:
            return cls(element)
        else:
            raise NotImplementedError

    ##############################################

    def from_operation(self, operation):
        return self._mapping[operation.__class__].from_operation(operation)

####################################################################################################

class ModelingDispatcher(Dispatcher):

    """Class to implement a dispatcher for modeling."""

    __TAGS__ = {
        'point': ModelingPoint,
        'spline': ModelingSpline,
        }

####################################################################################################

class DetailDispatcher(Dispatcher):

    """Class to implement a dispatcher for detail."""

    __TAGS__ = {
        'grainline': DetailGrainline,
        'patternInfo': DetailPatternInfo,
        'data': DetailData,
        }

####################################################################################################

_calculation_dispatcher = CalculationDispatcher()
_modeling_dispatcher = ModelingDispatcher()
_detail_dispatcher = DetailDispatcher()

####################################################################################################

class ValFileReaderInternal(XmlFileMixin):

    """Class to read val file."""

    _logger = _module_logger.getChild('ValFileReader')

    ##############################################

    def __init__(self, path):

        XmlFileMixin.__init__(self, path)

        self.root = None
        self.attribute = {}
        self.vit_file = None
        self.pattern = None

        self.read()

    ##############################################

    @property
    def measurements(self):
        if self.vit_file is not None:
            return self.vit_file.measurements
        else:
            return None

    ##############################################

    def read(self):

        # <?xml version="1.0" encoding="UTF-8"?>
        # <pattern>
        #     <!--Pattern created with Valentina v0.6.0.912b (https://valentinaproject.bitbucket.io/).-->
        #     <version>0.7.10</version>
        #     <unit>cm</unit>
        #     <description/>
        #     <notes/>
        #     <patternName>pattern name</patternName>
        #     <patternNumber>pattern number</patternNumber>
        #     <company>company/Designer name</company>
        #     <patternLabel>
        #         <line alignment="0" bold="true" italic="false" sfIncrement="4" text="%author%"/>
        #     </patternLabel>
        #     <patternMaterials/>
        #     <measurements>measurements.vit</measurements>
        #     <increments/>
        #     <previewCalculations/>
        #     <draw name="...">
        #         <calculation/>
        #         <modeling/>
        #         <details/>
        #         <groups/>
        #     </draw>
        # </pattern>

        self._logger.info('Read Valentina file "{}"'.format(self.path))

        self.root = self.parse()
        self.read_attributes()
        self.read_measurements()
        # patternLabel
        # patternMaterials
        # increments
        # previewCalculations

        self.pattern = Pattern(self.measurements, self.attribute['unit'])

        for piece in self.get_xpath_elements(self.root, 'draw'):
            self.read_piece(piece)

    ##############################################

    def read_measurements(self):

        measurements_path = self.get_xpath_element(self.root, 'measurements').text
        if measurements_path is not None:
            measurements_path = Path(measurements_path)
            if not measurements_path.exists():
                measurements_path = self.path.parent.joinpath(measurements_path)
            if not measurements_path.exists():
                raise NameError("Cannot find {}".format(measurements_path))
            self.vit_file = VitFile(measurements_path)
        else:
            self.vit_file = None

    ##############################################

    def read_attributes(self):

        required_attributes = (
            'unit',
        )
        optional_attributes = (
            'description',
            'notes',
            'patternName',
            'patternNumber',
            'company',
        )
        attribute_names = list(required_attributes) + list(optional_attributes)
        self.attribute = {name:self.get_text_element(self.root, name) for name in attribute_names}
        for name in required_attributes:
            if self.attribute[name] is None:
                raise NameError('{} is undefined'.format(name))

    ##############################################

    def read_piece(self, piece):

        piece_name = piece.attrib['name']
        self._logger.info('Create scope "{}"'.format(piece_name))
        scope = self.pattern.add_scope(piece_name)

        sketch = scope.sketch
        for element in self.get_xpath_element(piece, 'calculation'):
            try:
                xml_calculation = _calculation_dispatcher.from_xml(element)
                operation = xml_calculation.to_operation(sketch)
                self._logger.info('Add operation {}'.format(operation))
            except NotImplementedError:
                self._logger.warning('Not implemented calculation\n' +  str(etree.tostring(element)))
        sketch.eval()

        modeling = Modeling()
        for element in self.get_xpath_element(piece, 'modeling'):
            xml_modeling_item = _modeling_dispatcher.from_xml(element)
            modeling.add(xml_modeling_item)
            self._logger.info('Modeling {}'.format(xml_modeling_item))

        # details = []
        for detail_element in self.get_xpath_element(piece, 'details'):
            self.read_detail(scope, modeling, detail_element)
            # details.append(xml_detail)

    ##############################################

    def read_detail(self, scope, modeling, detail_element):

        xml_detail = Detail(modeling, detail_element)
        self._logger.info('Detail {}'.format(xml_detail))
        for element in detail_element:
            if element.tag == 'nodes':
                for node in element:
                    xml_node = DetailNode(node)
                    xml_detail.append_node(xml_node)
            else:
                xml_modeling_item = _detail_dispatcher.from_xml(element)
                # Fixme: xml_detail. = xml_modeling_item
                print(xml_modeling_item)

        for node, modeling_item in xml_detail.iter_on_nodes():
            # print(node.object_id, '->', modeling_item, '->', modeling_item.object_id)
            print(node, '->\n', modeling_item, '->\n', scope.sketch.get_operation(modeling_item.object_id))

####################################################################################################

class ValFileReader:

    """Class to read val file."""

    ##############################################

    def __init__(self, path):
        self._internal = ValFileReaderInternal(path)

    ##############################################

    @property
    def vit_file(self):
        return self._internal.vit_file

    @property
    def measurements(self):
        return self._internal.measurements

    @property
    def pattern(self):
        return self._internal.pattern

####################################################################################################

class ValFileWriter:

    """Class to write val file."""

    _logger = _module_logger.getChild('ValFileWriter')

    ##############################################

    def __init__(self, path, vit_file, pattern):

        self._path = str(path)
        self._vit_file = vit_file
        self._pattern = pattern

        root = self._build_xml_tree()
        self._write(root)

    ##############################################

    def _build_xml_tree(self):

        root = etree.Element('pattern')
        root.append(etree.Comment('Pattern created with Patro (https://github.com/FabriceSalvaire/Patro)'))

        etree.SubElement(root, 'version').text = VAL_VERSION
        etree.SubElement(root, 'unit').text = self._pattern.unit
        etree.SubElement(root, 'author')
        etree.SubElement(root, 'description')
        etree.SubElement(root, 'notes')
        measurements = etree.SubElement(root, 'measurements')
        if self._vit_file is not None:
            measurements.text = str(self._vit_file.path)
        etree.SubElement(root, 'increments')

        for scope in self._pattern.scopes:
            draw_element = etree.SubElement(root, 'draw')
            draw_element.attrib['name'] = scope.name
            calculation_element = etree.SubElement(draw_element, 'calculation')
            modeling_element = etree.SubElement(draw_element, 'modeling')
            details_element = etree.SubElement(draw_element, 'details')
            # group_element = etree.SubElement(draw_element, 'groups')

            for operation in scope.sketch.operations:
                xml_calculation = _calculation_dispatcher.from_operation(operation)
                # print(xml_calculation)
                # print(xml_calculation.to_xml_string())
                calculation_element.append(xml_calculation.to_xml())

        return root

    ##############################################

    def _write(self, root):

        with open(self._path, 'wb') as fh:
            # ElementTree.write() ?
            fh.write(etree.tostring(root, pretty_print=True))
