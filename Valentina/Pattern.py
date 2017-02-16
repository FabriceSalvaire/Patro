####################################################################################################
#
# X - x
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

from lxml import etree

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

# Point
#   trueDarts {'type': 'trueDarts', 'name1': 'A34', 'dartP2': '139', 'dartP1': '141', 'my2': '-3.87275', 'point2': '146', 'dartP3': '140', 'id': '144', 'mx2': '0.794387', 'my1': '-2.44561', 'name2': 'A35', 'point1': '145', 'baseLineP2': '63', 'mx1': '-3.64071', 'baseLineP1': '68'}
#
# Line
#   {'typeLine': 'hair', 'lineColor': 'black', 'firstPoint': '74', 'secondPoint': '72', 'id': '76'}
#
# Spline
#    {'type': 'simpleInteractive',
#       'length2': '8.65783', 'angle2': '85.3921',
#        'point4': '31',
#        'color': 'black',
#        'length1': '8.85757', 'angle1': '251.913',
#        'point1': '20',
#        'id': '97'
#     }

####################################################################################################

class Operation:

    ##############################################

    def __init__(self, id_):

        self._id = id_

    ##############################################

    @staticmethod
    def from_xml(element):

        if element.tag == 'point':
            return Point.from_xml(element)
        else:
            return None

    ##############################################

    @staticmethod
    def xml_attributes(element, attributes, keys):

        attrib = element.attrib
        return {key:attrib.get(attribute, None) for key, attribute in zip(keys, attributes)}

####################################################################################################

class Pattern:

    ##############################################

    def __init__(self):

        self._operations = []

    ##############################################

    def add(self, operation):

        self._operations.append(operation)

    ##############################################

    def dump(self):

        for operation in self._operations:
            print(operation)

####################################################################################################

class LineProperties:

    ##############################################

    def __init__(self, line_type=None, line_color=None):

        self._line_type = line_type
        self._line_color = line_color

####################################################################################################

class Point(Operation):

    ##############################################

    def __init__(self, id_, name, mx=0, my=0):

        # super(Point, self).__init__(id_)
        Operation.__init__(self, id_)
        self._name = name
        self._mx = mx
        self._my = my

    ##############################################

    @staticmethod
    def from_xml(element):

        if element.tag != 'point':
            raise ValueError
        type_ = element.attrib['type']
        if type_ == 'single':
            return SinglePoint.from_xml(element)
        elif type_ == 'alongLine':
            return AlongLinePoint.from_xml(element)
        elif type_ == 'endLine':
            return EndLinePoint.from_xml(element)
        elif type_ == 'lineIntersect':
            return LineIntersectPoint.from_xml(element)
        elif type_ == 'normal':
            return NormalPoint.from_xml(element)
        elif type_ == 'pointOfIntersection':
            return PointOfIntersectionPoint.from_xml(element)
        else:
            return None

####################################################################################################

class SinglePoint(Point):

    ##############################################

    def __init__(self, id_, name, x, y, mx=0, my=0):

        # super(SinglePoint, self).__init__(id_, name, mx, my, line_type, line_color)
        Point.__init__(self, id_, name, mx, my)
        self._x = x
        self._y = y

    ##############################################

    @staticmethod
    def from_xml(element):

        # {'y': '1.05833', 'mx': '0.132292', 'type': 'single', 'my': '0.264583', 'id': '1', 'name': 'A0', 'x': '0.79375'}

        kwargs = Operation.xml_attributes(element,
                                          ('id', 'name', 'x', 'y', 'mx', 'my'),
                                          ('id_', 'name', 'x', 'y', 'mx', 'my'))
        return SinglePoint(**kwargs)

    ##############################################

    def __repr__(self):

        return self.__class__.__name__ + ' {0._name} = ({0._x}, {0._y})'.format(self)

####################################################################################################

class AlongLinePoint(Point, LineProperties):

    ##############################################

    def __init__(self, id_, name, first_point, second_point, length, mx=0, my=0, line_type=None, line_color=None):

        # super(AlongLinePoint, self).__init__(id_, name, mx, my, line_type, line_color)
        Point.__init__(self, id_, name, mx, my)
        LineProperties.__init__(self, line_type, line_color)
        self._first_point = first_point
        self._second_point = second_point
        self._length = length

    ##############################################

    @staticmethod
    def from_xml(element):

        # {'lineColor': 'black', 'firstPoint': '138', 'id': '141', 'mx': '-4.2484', 'typeLine': 'none',
        #  'my': '1.01162', 'name': 'A33', 'length': 'Line_A30_A32', 'type': 'alongLine', 'secondPoint': '68'}

        kwargs = Operation.xml_attributes(element,
                                          ('id', 'name', 'firstPoint', 'secondPoint', 'length', 'mx', 'my', 'lineType', 'lineType'),
                                          ('id_', 'name', 'first_point', 'second_point', 'length', 'mx', 'my', 'line_type', 'line_type'))
        return AlongLinePoint(**kwargs)

####################################################################################################

class EndLinePoint(Point, LineProperties):

    ##############################################

    def __init__(self, id_, name, base_point, angle, length, mx=0, my=0, line_type=None, line_color=None):

        # super(EndLinePoint, self).__init__(id_, name, mx, my, line_type, line_color)
        Point.__init__(self, id_, name, mx, my)
        LineProperties.__init__(self, line_type, line_color)
        self._base_point = base_point
        self._angle = angle
        self._length = length

    ##############################################

    @staticmethod
    def from_xml(element):

        # {'basePoint': '1', 'name': 'A1', 'id': '2', 'angle': '0', 'length': 'waist_circ/2+10',
        #  'typeLine': 'dashDotLine', 'my': '0.264583', 'type': 'endLine', 'mx': '0.132292', 'lineColor': 'black'}

        kwargs = Operation.xml_attributes(element,
                                          ('id', 'name', 'basePoint', 'angle', 'length', 'mx', 'my', 'lineType', 'lineType'),
                                          ('id_', 'name', 'base_point', 'angle', 'length', 'mx', 'my', 'line_type', 'line_type'))
        return EndLinePoint(**kwargs)

    ##############################################

    def __repr__(self):

        return self.__class__.__name__ + ' {0._name} = ({0._base_point}, {0._angle}, {0._length})'.format(self)

####################################################################################################

class LineIntersectPoint(Point, LineProperties):

    ##############################################

    def __init__(self, id_, name, point1_line1, point2_line1, point1_line2, point2_line2, mx=0, my=0, line_type=None, line_color=None):

        # super(LineIntersectPoint, self).__init__(id_, name, mx, my, line_type, line_color)
        Point.__init__(self, id_, name, mx, my)
        LineProperties.__init__(self, line_type, line_color)
        self._point1_line1 = point1_line1
        self._point2_line1 = point2_line1
        self._point1_line2 = point1_line2
        self._point2_line2 = point2_line2

    ##############################################

    @staticmethod
    def from_xml(element):

        # {'type': 'lineIntersect', 'p2Line1': '32', 'mx': '0.132292', 'p1Line2': '10',
        #  'p2Line2': '11', 'p1Line1': '27', 'id': '39', 'my': '0.264583', 'name': 'Cp'}

        kwargs = Operation.xml_attributes(element,
                                          ('id', 'name', 'p1Line1', 'p2line1', 'p1Line2', 'p2Line2', 'mx', 'my', 'lineType', 'lineType'),
                                          ('id_', 'name', 'point1_line1', 'point2_line1', 'point1_line2', 'mx', 'my', 'point2_line2', 'line_type', 'line_type'))
        return LineIntersectPoint(**kwargs)

####################################################################################################

class NormalPoint(Point, LineProperties):

    ##############################################

    def __init__(self, id_, name, first_point, second_point, angle, length, mx=0, my=0, line_type=None, line_color=None):

        # super(NormalPoint, self).__init__(id_, name, mx, my, line_type, line_color)
        Point.__init__(self, id_, name, mx, my)
        LineProperties.__init__(self, line_type, line_color)
        self._first_point = first_point
        self._second_point = second_point
        self._angle = angle
        self._length = length

    ##############################################

    @staticmethod
    def from_xml(element):

        # {'my': '-4.18524', 'secondPoint': '63', 'name': 'A36', 'angle': '0', 'length': '0.5',
        #  'firstPoint': '138', 'typeLine': 'hair', 'type': 'normal', 'mx': '-1.57131', 'id': '147', 'lineColor': 'black'}

        kwargs = Operation.xml_attributes(element,
                                          ('id', 'name', 'firstPoint', 'secondPoint', 'angle', 'length', 'lineType', 'lineType'),
                                          ('id_', 'name', 'first_point', 'second_point', 'angle', 'length', 'line_type', 'line_type'))
        return NormalPoint(**kwargs)

####################################################################################################

class PointOfIntersectionPoint(Point):

    ##############################################

    def __init__(self, id_, name, first_point, second_point, point_of_intersection, mx=0, my=0):

        # super(PointOfIntersectionPoint, self).__init__(id_, name, mx, my)
        Point.__init__(self, id_, name, mx, my)
        self._first_point = first_point
        self._second_point = second_point
        self._point_of_intersection = point_of_intersection

    ##############################################

    @staticmethod
    def from_xml(element):

        # {'id': '71', 'secondPoint': '56', 'type': 'pointOfIntersection', 'firstPoint': '59', 'name': 'Nc', 'mx': '0.132292', 'my': '0.264583'}

        kwargs = Operation.xml_attributes(element,
                                          ('id', 'name', 'firstPoint', 'secondPoint', 'pointOfIntersection', 'mx', 'my'),
                                          ('id_', 'name', 'first_point', 'second_point', 'point_of_intersection', 'mx', 'my'))
        return PointOfIntersectionPoint(**kwargs)

####################################################################################################

class ValParser:

    ##############################################

    def parse(self, val_path):

        with open(val_path, 'rb') as f:
            source = f.read()

        tree = etree.fromstring(source)

        pattern = Pattern()

        elements = self._get_xpath_element(tree, 'draw/calculation')
        for element in elements:
            operation = Operation.from_xml(element)
            pattern.add(operation)

        return pattern

    ##############################################

    def _get_xpath_element(self, root, path):

        return root.xpath(path)[0]
