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

"""This module implements the val XML file format.

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

class Dispatcher:

    """Baseclass to dispatch XML to Python class."""

    __TAGS__ = {}

    ##############################################

    def from_xml(self, element):

        tag_class = self.__TAGS__[element.tag]
        if tag_class is not None:
            return tag_class(element)
        else:
            raise NotImplementedError

####################################################################################################

class CalculationDispatcher:

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

    def _register_mapping(self, xml_class):

        calculation_class = xml_class.__calculation__
        if calculation_class:
            self._mapping[xml_class] = calculation_class
            self._mapping[calculation_class] = xml_class

    ##############################################

    def _init_mapper(self):

        for tag_class in self.__TAGS__.values():
            if tag_class is not None:
                if hasattr(tag_class, '__TYPES__'):
                    for xml_class in tag_class.__TYPES__.values():
                        if xml_class is not None:
                            self._register_mapping(xml_class)
                else:
                    self._register_mapping(tag_class)

    ##############################################

    def from_xml(self, element):

        tag_class = self.__TAGS__[element.tag]
        if hasattr(tag_class, '__TYPES__'):
            cls = tag_class.__TYPES__[element.attrib['type']]
        else:
            cls = tag_class
        if cls is not None:
            return cls(element)
        else:
            raise NotImplementedError

    ##############################################

    def from_calculation(self, calculation):
        return self._mapping[calculation.__class__].from_calculation(calculation)

####################################################################################################

class Modeling:

    ##############################################

    def __init__(self):
        self._items = []
        self._id_map = {}

    ##############################################

    def __getitem__(self, id):
        return self._id_map[id]

    ##############################################

    def append(self, item):
        self._items.append(item)
        self._id_map[item.id] = item

####################################################################################################

class ModelingDispatcher(Dispatcher):

    __TAGS__ = {
        'point': ModelingPoint,
        'spline': ModelingSpline,
        }

####################################################################################################

class DetailDispatcher(Dispatcher):

    __TAGS__ = {
        'grainline': DetailGrainline,
        'patternInfo': DetailPatternInfo,
        'data': DetailData,
        }

####################################################################################################

class ValFile(XmlFileMixin):

    """Class to read/write val file."""

    _logger = _module_logger.getChild('ValFile')

    _calculation_dispatcher = CalculationDispatcher()
    _modeling_dispatcher = ModelingDispatcher()
    _detail_dispatcher = DetailDispatcher()

    ##############################################

    def __init__(self, path=None):

        # Fixme: path
        if path is None:
            path = ''
        XmlFileMixin.__init__(self, path)
        self._vit_file = None
        self._pattern = None
        # Fixme:
        # if path is not None:
        if path != '':
            self._read()

    ##############################################

    def Write(self, path, vit_file, pattern):

        # Fixme: write
        self._vit_file = vit_file
        self._pattern = pattern
        self.write(path)

    ##############################################

    @property
    def measurements(self):
        return self._vit_file.measurements

    @property
    def pattern(self):
        return self._pattern

    ##############################################

    def _read(self):

        # <?xml version='1.0' encoding='UTF-8'?>
        # <pattern>
        #     <!--Pattern created with Valentina (http://www.valentina-project.org/).-->
        #     <version>0.4.0</version>
        #     <unit>cm</unit>
        #     <author/>
        #     <description/>
        #     <notes/>
        #     <measurements/>
        #     <increments/>
        #     <draw name="Pattern piece 1">
        #         <calculation/>
        #         <modeling/>
        #         <details/>
        #         <groups/>
        #     </draw>
        # </pattern>

        tree = self._parse()

        measurements_path = self._get_xpath_element(tree, 'measurements').text
        if measurements_path is not None:
            measurements_path = Path(measurements_path)
            if not measurements_path.exists():
                measurements_path = self._path.parent.joinpath(measurements_path)
            if not measurements_path.exists():
                raise NameError("Cannot find {}".format(measurements_path))
            self._vit_file = VitFile(measurements_path)
            measurements = self._vit_file.measurements
        else:
            self._vit_file = None
            measurements = None

        unit = self._get_xpath_element(tree, 'unit').text

        pattern = Pattern(measurements, unit)
        self._pattern = pattern

        for element in self._get_xpath_element(tree, 'draw/calculation'):
            try:
                xml_calculation = self._calculation_dispatcher.from_xml(element)
                xml_calculation.to_calculation(pattern)
            except NotImplementedError:
                self._logger.warning('Not implemented calculation\n' +  str(etree.tostring(element)))

        pattern.eval()

        modeling = Modeling()
        for element in self._get_xpath_element(tree, 'draw/modeling'):
            xml_modeling_item = self._modeling_dispatcher.from_xml(element)
            modeling.append(xml_modeling_item)
            # print(xml_modeling_item)

        details = []
        for detail_element in self._get_xpath_element(tree, 'draw/details'):
            xml_detail = Detail(modeling, detail_element)
            details.append(xml_detail)
            # print(xml_detail)
            for element in detail_element:
                if element.tag == 'nodes':
                    for node in element:
                        xml_node = DetailNode(node)
                        # print(xml_node)
                        xml_detail.append_node(xml_node)
                else:
                    xml_modeling_item = self._detail_dispatcher.from_xml(element)
                    # Fixme: xml_detail. = xml_modeling_item
                    # print(xml_modeling_item)
            # for node, modeling_item in xml_detail.iter_on_nodes():
            #     # print(node.object_id, '->', modeling_item, '->', modeling_item.object_id)
            #     print(node, '->\n', modeling_item, '->\n', pattern.get_calculation(modeling_item.object_id))

    ##############################################

    def write(self, path=None):

        root = etree.Element('pattern')
        root.append(etree.Comment('Pattern created with Patro (https://github.com/FabriceSalvaire/Patro)'))

        etree.SubElement(root, 'version').text = '0.4.0'
        etree.SubElement(root, 'unit').text = self._pattern.unit
        etree.SubElement(root, 'author')
        etree.SubElement(root, 'description')
        etree.SubElement(root, 'notes')
        etree.SubElement(root, 'measurements').text = str(self._vit_file.path)
        etree.SubElement(root, 'increments')

        draw_element = etree.SubElement(root, 'draw') # Fixme:
        draw_element.attrib['name'] = 'Pattern piece 1' # Fixme:

        calculation_element = etree.SubElement(draw_element, 'calculation')
        modeling_element = etree.SubElement(draw_element, 'modeling')
        details_element = etree.SubElement(draw_element, 'details')
        # group_element = etree.SubElement(draw_element, 'groups')

        for calculation in self._pattern.calculations:
            xml_calculation = self._calculation_dispatcher.from_calculation(calculation)
            # print(xml_calculation)
            # print(xml_calculation.to_xml_string())
            calculation_element.append(xml_calculation.to_xml())

        if path is None:
            path = self.path
        with open(str(path), 'wb') as f:
            # ElementTree.write() ?
            f.write(etree.tostring(root, pretty_print=True))
