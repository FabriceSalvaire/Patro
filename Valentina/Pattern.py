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

from .Evaluator import Expression
from .Geometry.Vector2D import Vector2D
from .Geometry.Line2D import Line2D
from .Measurement import VitParser

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

# Point
#   trueDarts {'type': 'trueDarts', 'name1': 'A34', 'dartP2': '139', 'dartP1': '141', 'my2': '-3.87275', 'point2': '146', 'dartP3': '140', 'id': '144', 'mx2': '0.794387', 'my1': '-2.44561', 'name2': 'A35', 'point1': '145', 'baseLineP2': '63', 'mx1': '-3.64071', 'baseLineP1': '68'}

####################################################################################################

class Operation:

    _logger = _module_logger.getChild('Operation')

    ##############################################

    @staticmethod
    def from_xml(element, pattern):

        if element.tag == 'point':
            return Point.from_xml(element, pattern)
        elif element.tag == 'line':
            return Line.from_xml(element, pattern)
        elif element.tag == 'spline':
            return Curve.from_xml(element, pattern)
        else:
            return Operation(pattern, element.attrib['id'])

    ##############################################

    @staticmethod
    def xml_attributes(element, pattern, attributes, keys):

        attrib = element.attrib
        kwargs = {key:attrib.get(attribute, None) for key, attribute in zip(keys, attributes)}
        kwargs['pattern'] = pattern
        return kwargs

    ##############################################

    def __init__(self, pattern, id_):

        self._pattern = pattern
        self._id = id_

    ##############################################

    @property
    def id(self):
        return self._id

    @property
    def pattern(self):
        return self._pattern

    ##############################################

    def __repr__(self):

        return self.__class__.__name__ + ' {0._id}'.format(self)

    ##############################################

    def eval(self):

        self._logger.info('Eval {}'.format(self))
        self.eval_internal()

    ##############################################

    def eval_internal(self):

        pass

####################################################################################################

class Pattern:

    _logger = _module_logger.getChild('Pattern')

    ##############################################

    def __init__(self, measurements):

        self._measurements = measurements
        self._evaluator = measurements.evaluator
        self._operations = []
        self._operation_dict = {}

    ##############################################

    @property
    def measurements(self):
        return self._measurements

    ##############################################

    @property
    def evaluator(self):
        return self._evaluator

    ##############################################

    def add(self, operation):

        if operation is not None:
            self._operations.append(operation)
            self._operation_dict[operation.id] = operation

    ##############################################

    def get_operation(self, id_):

        return self._operation_dict[id_]

    ##############################################

    def get_point(self, name):

        return self._points[name]

    ##############################################

    def eval(self):

        for operation in self._operations:
            if isinstance(operation, Point):
                self._evaluator.add_point(operation)
                operation.eval()
            else:
                pass

    ##############################################

    def dump(self):

        for operation in self._operations:
            if isinstance(operation, Point):
                print(operation, operation.vector)
            else:
                print(operation)

####################################################################################################

class LineProperties:

    ##############################################

    def __init__(self, line_type=None, line_color=None):

        self._line_type = line_type
        self._line_color = line_color

    ##############################################

    @property
    def line_color(self):
        return self._line_color

    @property
    def line_type(self):
        return self._line_type

####################################################################################################

class Point(Operation):

    ##############################################

    def __init__(self, pattern, id_, name,
                 mx=0, my=0,
                 ):

        # super(Point, self).__init__(id_)
        Operation.__init__(self, pattern, id_)
        self._name = name
        self._mx = mx
        self._my = my

        self._vector = None

    ##############################################

    @property
    def name(self):
        return self._name

    @property
    def mx(self):
        return self._mx

    @property
    def my(self):
        return self._my

    @property
    def vector(self):
        return self._vector

    ##############################################

    @staticmethod
    def from_xml(element, pattern):

        if element.tag != 'point':
            raise ValueError
        type_ = element.attrib['type']
        if type_ == 'single':
            return SinglePoint.from_xml(element, pattern)
        elif type_ == 'alongLine':
            return AlongLinePoint.from_xml(element, pattern)
        elif type_ == 'endLine':
            return EndLinePoint.from_xml(element, pattern)
        elif type_ == 'lineIntersect':
            return LineIntersectPoint.from_xml(element, pattern)
        elif type_ == 'normal':
            return NormalPoint.from_xml(element, pattern)
        elif type_ == 'pointOfIntersection':
            return PointOfIntersectionPoint.from_xml(element, pattern)
        else:
            return None

    ##############################################

    def _post_eval_internal(self):

        self._logger.info('{0._name} {0._vector}'.format(self))

####################################################################################################

class SinglePoint(Point):

    ##############################################

    def __init__(self, pattern, id_, name,
                 x, y,
                 mx=0, my=0,
                 ):

        # super(SinglePoint, self).__init__(id_, name, mx, my, line_type, line_color)
        Point.__init__(self, pattern, id_, name, mx, my)
        self._x = Expression(x, pattern.evaluator)
        self._y = Expression(y, pattern.evaluator)

    ##############################################

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    ##############################################

    @staticmethod
    def from_xml(element, pattern):

        # {'y': '1.05833', 'mx': '0.132292', 'type': 'single', 'my': '0.264583', 'id': '1', 'name': 'A0', 'x': '0.79375'}

        kwargs = Operation.xml_attributes(element, pattern,
                                          ('id', 'name', 'x', 'y', 'mx', 'my'),
                                          ('id_', 'name', 'x', 'y', 'mx', 'my'))
        return SinglePoint(**kwargs)

    ##############################################

    def __repr__(self):

        return self.__class__.__name__ + ' {0._name} = ({0._x}, {0._y})'.format(self)

    ##############################################

    def eval_internal(self):

        self._vector = Vector2D(self._x.value, self._y.value)
        self._post_eval_internal()

####################################################################################################

class AlongLinePoint(Point, LineProperties):

    ##############################################

    def __init__(self, pattern, id_, name,
                 first_point, second_point, length,
                 mx=0, my=0,
                 line_type=None, line_color=None,
                 ):

        # super(AlongLinePoint, self).__init__(id_, name, mx, my, line_type, line_color)
        Point.__init__(self, pattern, id_, name, mx, my)
        LineProperties.__init__(self, line_type, line_color)
        self._first_point = pattern.get_operation(first_point)
        self._second_point = pattern.get_operation(second_point)
        self._length = Expression(length, pattern.evaluator)

    ##############################################

    @property
    def first_point(self):
        return self._first_point

    @property
    def second_point(self):
        return self._second_point

    @property
    def length(self):
        return self._length

    ##############################################

    @staticmethod
    def from_xml(element, pattern):

        # {'lineColor': 'black', 'firstPoint': '138', 'id': '141', 'mx': '-4.2484', 'typeLine': 'none',
        #  'my': '1.01162', 'name': 'A33', 'length': 'Line_A30_A32', 'type': 'alongLine', 'secondPoint': '68'}

        kwargs = Operation.xml_attributes(element, pattern,
                                          ('id', 'name', 'firstPoint', 'secondPoint', 'length', 'mx', 'my', 'lineType', 'lineType'),
                                          ('id_', 'name', 'first_point', 'second_point', 'length', 'mx', 'my', 'line_type', 'line_type'))
        return AlongLinePoint(**kwargs)

    ##############################################

    def __repr__(self):

        return self.__class__.__name__ + ' {0._name} = ({0._first_point.name}, {0._second_point.name}, {0._length})'.format(self)

    ##############################################

    def eval_internal(self):

        vector = self._second_point.vector - self._first_point.vector
        self._pattern.evaluator.set_current_segment(vector)
        self._vector = vector.to_normalised()*self._length.value
        self._pattern.evaluator.unset_current_segment()
        self._post_eval_internal()

####################################################################################################

class EndLinePoint(Point, LineProperties):

    ##############################################

    def __init__(self, pattern, id_, name,
                 base_point, angle, length,
                 mx=0, my=0,
                 line_type=None, line_color=None,
                 ):

        # super(EndLinePoint, self).__init__(id_, name, mx, my, line_type, line_color)
        Point.__init__(self, pattern, id_, name, mx, my)
        LineProperties.__init__(self, line_type, line_color)
        self._base_point = pattern.get_operation(base_point)
        self._angle = Expression(angle, pattern.evaluator)
        self._length = Expression(length, pattern.evaluator)

    ##############################################

    @property
    def base_point(self):
        return self._base_point

    @property
    def length(self):
        return self._length

    @property
    def angle(self):
        return self._angle

    ##############################################

    @staticmethod
    def from_xml(element, pattern):

        # {'basePoint': '1', 'name': 'A1', 'id': '2', 'angle': '0', 'length': 'waist_circ/2+10',
        #  'typeLine': 'dashDotLine', 'my': '0.264583', 'type': 'endLine', 'mx': '0.132292', 'lineColor': 'black'}

        kwargs = Operation.xml_attributes(element, pattern,
                                          ('id', 'name', 'basePoint', 'angle', 'length', 'mx', 'my', 'lineType', 'lineType'),
                                          ('id_', 'name', 'base_point', 'angle', 'length', 'mx', 'my', 'line_type', 'line_type'))
        return EndLinePoint(**kwargs)

    ##############################################

    def __repr__(self):

        return self.__class__.__name__ + ' {0._name} = ({0._base_point.name}, {0._angle}, {0._length})'.format(self)

    ##############################################

    def eval_internal(self):

        self._vector = self._base_point._vector + Vector2D.from_angle(self._angle.value)*self._length.value
        self._post_eval_internal()

####################################################################################################

class LineIntersectPoint(Point, LineProperties):

    ##############################################

    def __init__(self, pattern, id_, name,
                 point1_line1, point2_line1, point1_line2, point2_line2,
                 mx=0, my=0,
                 line_type=None, line_color=None,
                 ):

        # super(LineIntersectPoint, self).__init__(id_, name, mx, my, line_type, line_color)
        Point.__init__(self, pattern, id_, name, mx, my)
        LineProperties.__init__(self, line_type, line_color)
        self._point1_line1 = pattern.get_operation(point1_line1)
        self._point2_line1 = pattern.get_operation(point2_line1)
        self._point1_line2 = pattern.get_operation(point1_line2)
        self._point2_line2 = pattern.get_operation(point2_line2)

    ##############################################

    @property
    def point1_line1(self):
        return self._point1_line1

    @property
    def point2_line1(self):
        return self._point2_line1

    @property
    def point1_line2(self):
        return self._point1_line2

    @property
    def point2_line2(self):
        return self._point2_line2

    ##############################################

    @staticmethod
    def from_xml(element, pattern):

        # {'type': 'lineIntersect', 'p2Line1': '32', 'mx': '0.132292', 'p1Line2': '10',
        #  'p2Line2': '11', 'p1Line1': '27', 'id': '39', 'my': '0.264583', 'name': 'Cp'}

        kwargs = Operation.xml_attributes(element, pattern,
                                          ('id', 'name', 'p1Line1', 'p2Line1', 'p1Line2', 'p2Line2', 'mx', 'my', 'lineType', 'lineType'),
                                          ('id_', 'name', 'point1_line1', 'point2_line1', 'point1_line2', 'point2_line2', 'mx', 'my', 'line_type', 'line_type'))
        return LineIntersectPoint(**kwargs)

    ##############################################

    def __repr__(self):

        return self.__class__.__name__ + ' {0._name} = ({0._point1_line1.name}, {0._point2_line1.name}, {0._point1_line2.name}, {0._point2_line2.name})'.format(self)

    ##############################################

    def eval_internal(self):

        line1 = Line2D(self._point1_line1.vector, self._point2_line1.vector)
        line2 = Line2D(self._point1_line2.vector, self._point2_line2.vector)
        print(self._point1_line1.vector, self._point2_line1.vector)
        print(self._point1_line2.vector, self._point2_line2.vector)
        self._vector = line1.intersection(line2)
        self._post_eval_internal()

####################################################################################################

class NormalPoint(Point, LineProperties):

    ##############################################

    def __init__(self, pattern, id_, name,
                 first_point, second_point, angle, length,
                 mx=0, my=0,
                 line_type=None, line_color=None,
                 ):

        # super(NormalPoint, self).__init__(id_, name, mx, my, line_type, line_color)
        Point.__init__(self, pattern, id_, name, mx, my)
        LineProperties.__init__(self, line_type, line_color)
        self._first_point = pattern.get_operation(first_point)
        self._second_point = pattern.get_operation(second_point)
        self._angle = Expression(angle, pattern.evaluator)
        self._length = Expression(length, pattern.evaluator)

    ##############################################

    @property
    def first_point(self):
        return self._first_point

    @property
    def second_point(self):
        return self._second_point

    @property
    def angle(self):
        return self._angle

    @property
    def length(self):
        return self._length

    ##############################################

    @staticmethod
    def from_xml(element, pattern):

        # {'my': '-4.18524', 'secondPoint': '63', 'name': 'A36', 'angle': '0', 'length': '0.5',
        #  'firstPoint': '138', 'typeLine': 'hair', 'type': 'normal', 'mx': '-1.57131', 'id': '147', 'lineColor': 'black'}

        kwargs = Operation.xml_attributes(element, pattern,
                                          ('id', 'name', 'firstPoint', 'secondPoint', 'angle', 'length', 'lineType', 'lineType'),
                                          ('id_', 'name', 'first_point', 'second_point', 'angle', 'length', 'line_type', 'line_type'))
        return NormalPoint(**kwargs)

    ##############################################

    def __repr__(self):

        return self.__class__.__name__ + ' {0._name} = ({0._first_point.name}, {0._second_point.name}, {0._angle}, {0._length})'.format(self)

    ##############################################

    def eval_internal(self):

        vector = self._second_point.vector - self._first_point.vector
        self._pattern.evaluator.set_current_segment(vector)
        direction = vector.to_normalised()
        direction = direction.rotate_counter_clockwise_90()
        angle = self._angle.value
        if angle:
            direction = direction.rotate_counter_clockwise(angle)
        self._vector = self._first_point.vector + direction*self._length.value
        self._pattern.evaluator.unset_current_segment()
        self._post_eval_internal()

####################################################################################################

class PointOfIntersectionPoint(Point):

    ##############################################

    def __init__(self, pattern, id_, name,
                 first_point, second_point,
                 mx=0, my=0,
                 ):

        # super(PointOfIntersectionPoint, self).__init__(id_, name, mx, my)
        Point.__init__(self, pattern, id_, name, mx, my)
        self._first_point = pattern.get_operation(first_point)
        self._second_point = pattern.get_operation(second_point)

    ##############################################

    @property
    def first_point(self):
        return self._first_point

    @property
    def second_point(self):
        return self._second_point

    ##############################################

    @staticmethod
    def from_xml(element, pattern):

        # {'id': '71', 'secondPoint': '56', 'type': 'pointOfIntersection', 'firstPoint': '59', 'name': 'Nc', 'mx': '0.132292', 'my': '0.264583'}

        kwargs = Operation.xml_attributes(element, pattern,
                                          ('id', 'name', 'firstPoint', 'secondPoint', 'mx', 'my'),
                                          ('id_', 'name', 'first_point', 'second_point', 'mx', 'my'))
        return PointOfIntersectionPoint(**kwargs)

    ##############################################

    def __repr__(self):

        return self.__class__.__name__ + ' {0._name} = ()'.format(self)


    ##############################################

    def eval_internal(self):

        self._vector = Vector2D(self._first_point.vector.x, self._second_point.vector.y)
        self._post_eval_internal()

####################################################################################################

class Line(Operation, LineProperties):

    ##############################################

    def __init__(self, pattern, id_,
                 first_point, second_point,
                 line_type=None, line_color=None,
                 ):

        Operation.__init__(self, pattern, id_)
        LineProperties.__init__(self, line_type, line_color)
        self._first_point = pattern.get_operation(first_point)
        self._second_point = pattern.get_operation(second_point)

    ##############################################

    @property
    def first_point(self):
        return self._first_point

    @property
    def second_point(self):
        return self._second_point

    ##############################################

    @staticmethod
    def from_xml(element, pattern):

        # {'typeLine': 'hair', 'lineColor': 'black', 'firstPoint': '74', 'secondPoint': '72', 'id': '76'}

        kwargs = Operation.xml_attributes(element, pattern,
                                          ('id', 'firstPoint', 'secondPoint', 'lineType', 'lineType'),
                                          ('id_', 'first_point', 'second_point', 'line_type', 'line_type'))
        return Line(**kwargs)

    ##############################################

    def __repr__(self):

        return self.__class__.__name__ + ' ({0._first_point.name}, {0._second_point.name})'.format(self)

    ##############################################

    def eval_internal(self):

        pass

####################################################################################################

class Curve(Operation, LineProperties):

    ##############################################

    def __init__(self, pattern, id_,
                 first_point, second_point,
                 angle1, length1,
                 angle2, length2,
                 line_type=None, line_color=None,
                 ):

        Operation.__init__(self, pattern, id_)
        LineProperties.__init__(self, line_type, line_color)
        self._first_point = pattern.get_operation(first_point)
        self._second_point = pattern.get_operation(second_point)
        self._angle1 = Expression(angle1, pattern.evaluator)
        self._length1 = Expression(length1, pattern.evaluator)
        self._angle2 = Expression(angle2, pattern.evaluator)
        self._length2 = Expression(length2, pattern.evaluator)

    ##############################################

    @property
    def first_point(self):
        return self._first_point

    @property
    def second_point(self):
        return self._second_point

    @property
    def angle1(self):
        return self._angle1

    @property
    def length1(self):
        return self._length1

    @property
    def angle2(self):
        return self._angle2

    @property
    def length2(self):
        return self._length2

    ##############################################

    @staticmethod
    def from_xml(element, pattern):

        # 'type': 'simpleInteractive',
        #   'length2': '8.65783', 'angle2': '85.3921',
        #    'point4': '31',
        #    'color': 'black',
        #    'length1': '8.85757', 'angle1': '251.913',
        #    'point1': '20',
        #    'id': '97'
        # }

        kwargs = Operation.xml_attributes(element, pattern,
                                          ('id', 'point1', 'point4', 'angle1', 'length1', 'angle2', 'length2', 'lineType', 'lineType'),
                                          ('id_', 'first_point', 'second_point', 'angle1', 'length1', 'angle2', 'length2', 'line_type', 'line_type'))
        return Curve(**kwargs)

    ##############################################

    def __repr__(self):

        return self.__class__.__name__ + ' ({0._first_point.name}, {0._second_point.name}, {0._angle1}, {0._length1}, {0._angle2}, {0._length2})'.format(self)

    ##############################################

    def eval_internal(self):

        pass

####################################################################################################

class ValParser:

    _logger = _module_logger.getChild('ValParser')

    ##############################################

    def parse(self, val_path):

        with open(val_path, 'rb') as f:
            source = f.read()

        tree = etree.fromstring(source)

        measurements_path = self._get_xpath_element(tree, 'measurements').text
        self._logger.info('Measurements loaded from ' + measurements_path)
        measurements = VitParser().parse(measurements_path)
        measurements.eval()

        pattern = Pattern(measurements)

        elements = self._get_xpath_element(tree, 'draw/calculation')
        for element in elements:
            operation = Operation.from_xml(element, pattern)
            pattern.add(operation)
            pattern.eval()

        return pattern

    ##############################################

    def _get_xpath_element(self, root, path):

        return root.xpath(path)[0]
