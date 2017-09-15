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

"""
A calculation must be build from the corresponding method of the Pattern class.
"""

####################################################################################################

import logging

from .Calculator import Expression
from Valentina.Geometry.Bezier import CubicBezier2D
from Valentina.Geometry.Line import Line2D
from Valentina.Geometry.Segment import Segment2D
from Valentina.Geometry.Vector import Vector2D

pyid = id

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

def quote(x):
    return "'{}'".format(x)

####################################################################################################

class CalculationMetaClass:

    _logger = _module_logger.getChild('CalculationMetaClass')

    ##############################################

    def __init__(cls, class_name, super_classes, class_attribute_dict):

        # cls._logger.info(str((cls, class_name, super_classes, class_attribute_dict)))
        type.__init__(cls, class_name, super_classes, class_attribute_dict)

####################################################################################################

# metaclass = CalculationMetaClass
class Calculation():

    _logger = _module_logger.getChild('Calculation')

    ##############################################

    def __init__(self, pattern, id=None):

        self._pattern = pattern

        if id is None:
            self._id = pattern.get_calculation_id()
        else:
            if pattern.has_calculation_id(id):
                raise NameError("calculation id {} is already attributed".format(id))
            else:
                self._id = id

        self._dag_node = self._dag.add_node(pyid(self), data=self)
        self._dependencies = set()

    ##############################################

    @property
    def id(self):
        return self._id

    @property
    def pattern(self):
        return self._pattern

    @property
    def _dag(self):
        return self._pattern.calculator.dag

    @property
    def dependencies(self):
        return self._dependencies

    ##############################################

    def __repr__(self):

        return self.__class__.__name__ + ' {0._id}'.format(self)

    ##############################################

    def __int__(self):

        return self._id

    ##############################################

    def _get_calculation(self, calculation):

        if isinstance(calculation, Calculation):
            return calculation
        # elif isinstance(calculation, (int, str)):
        else:
            return self._pattern.get_calculation(calculation)

    ##############################################

    def eval(self):

        self._logger.info('Eval {}'.format(self))
        self.eval_internal()

    ##############################################

    def eval_internal(self):

        pass

    ##############################################

    def to_python(self):

        args = self._init_args()
        values = []
        for arg in args:
            value = getattr(self, arg)
            # if arg == 'pattern':
            #     value_str = 'pattern'
            # if isinstance(value, Pattern):
            #     value_str = 'pattern'
            if value is  None:
                value_str = 'None'
            elif isinstance(value, (int, float)):
                value_str = str(value)
            elif isinstance(value, str):
                value_str = quote(value)
            # elif isinstance(value, Calculation):
            #     value_str = str(value.id)
            elif isinstance(value, Point):
                value_str = quote(value.name)
            elif isinstance(value, Expression):
                if value.is_float():
                    value_str = str(value)
                else:
                    value_str = quote(value)
            elif isinstance(value, Vector2D):
                value_str = 'Vector2D({0.x}, {0.y})'.format(value)
            else:
                value_str = ''
            values.append(value_str)
        kwargs = ', '.join(['pattern'] + [key + '=' + value for key, value in zip(args, values)])
        return self.__class__.__name__ + '(' + kwargs + ')'

    ##############################################

    def _init_args(self):

        args = self.__init__.__code__.co_varnames
        args = args[2:-1] # remove self, pattern, id
        return args

    ##############################################

    def _connect_ancestor(self, *points):

        dag = self._dag
        for point in points:
            self._dependencies.add(point)
            self._dag_node.connect_ancestor(dag[pyid(point)])

    ##############################################

    # def _connect_ancestor_for_expressions(self, *expressions):

    #     for expression in expressions:
    #         self._connect_ancestor(*expression.dependencies)

    def _iter_on_expressions(self):

        for attribute in self.__dict__.values():
            if isinstance(attribute, Expression):
                yield attribute

    def connect_ancestor_for_expressions(self):

        # Expression's dependencies are only known after compilation

        for expression in self._iter_on_expressions():
            self._connect_ancestor(*expression.dependencies)

    ##############################################

    # @property
    def geometry(self):
        raise NotImplementedError('Geometry is not implemented for {}'.format(self))

####################################################################################################

class LinePropertiesMixin:

    ##############################################

    def __init__(self, line_style, line_color):

        self._line_color = line_color
        self._line_style = line_style

    ##############################################

    @property
    def line_color(self):
        return self._line_color

    @line_color.setter
    def line_color(self, value):
        self._line_color = value

    @property
    def line_style(self):
        return self._line_style

    @line_style.setter
    def line_style(self, value):
        self._line_style = value

####################################################################################################

class FirstSecondPointMixin:

    ##############################################

    def __init__(self, first_point, second_point):

        self._first_point = self._get_calculation(first_point)
        self._second_point = self._get_calculation(second_point)
        self._connect_ancestor(self._first_point, self._second_point)

    ##############################################

    @property
    def first_point(self):
        return self._first_point

    @property
    def second_point(self):
        return self._second_point

####################################################################################################

class BasePointMixin:

    ##############################################

    def __init__(self, base_point):

        self._base_point = self._get_calculation(base_point)
        self._connect_ancestor(self._base_point)

    ##############################################

    @property
    def base_point(self):
        return self._base_point

####################################################################################################

class LengthMixin:

    ##############################################

    def __init__(self, length):

        self._length = Expression(length, self._pattern.calculator)
        # self._connect_ancestor_for_expressions(self._length)

    ##############################################

    @property
    def length(self):
        return self._length

####################################################################################################

class AngleMixin:

    ##############################################

    def __init__(self, angle):

        self._angle = Expression(angle, self._pattern.calculator)
        # self._connect_ancestor_for_expressions(self._angle)

    ##############################################

    @property
    def angle(self):
        return self._angle

####################################################################################################

class LengthAngleMixin(LengthMixin, AngleMixin):

    ##############################################

    def __init__(self, length, angle):

        LengthMixin.__init__(self, length)
        AngleMixin.__init__(self, angle)

####################################################################################################

class Point(Calculation):

    ##############################################

    def __init__(self, pattern, name, label_offset, id=None):

        Calculation.__init__(self, pattern, id)
        self._name = name
        self._label_offset = label_offset

        self._vector = None

    ##############################################

    @property
    def name(self):
        return self._name

    @property
    def label_offset(self):
        return self._label_offset

    @property
    def vector(self):
        return self._vector

    ##############################################

    def _post_eval_internal(self):

        self._logger.info('{0._name} {0._vector}'.format(self))

    ##############################################

    def geometry(self):

        return self._vector.clone()

####################################################################################################

class SinglePoint(Point):

    ##############################################

    def __init__(self, pattern, name,
                 x, y,
                 label_offset,
                 id=None
    ):

        Point.__init__(self, pattern, name, label_offset, id)
        self._x = Expression(x, pattern.calculator)
        self._y = Expression(y, pattern.calculator)
        # self._connect_ancestor_for_expressions(self._x, self._y)

    ##############################################

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    ##############################################

    def __repr__(self):

        return self.__class__.__name__ + ' {0._name} = ({0._x}, {0._y})'.format(self)

    ##############################################

    def eval_internal(self):

        self._vector = Vector2D(self._x.value, self._y.value)
        self._post_eval_internal()

####################################################################################################

class AlongLinePoint(Point, LinePropertiesMixin, FirstSecondPointMixin, LengthMixin):

    ##############################################

    def __init__(self, pattern, name,
                 first_point, second_point, length,
                 label_offset,
                 line_style=None, line_color=None,
                 id=None,
                 ):

        Point.__init__(self, pattern, name, label_offset, id)
        LinePropertiesMixin.__init__(self, line_style, line_color)
        FirstSecondPointMixin.__init__(self, first_point, second_point)
        LengthMixin.__init__(self, length)

    ##############################################

    def __repr__(self):

        return self.__class__.__name__ + ' {0._name} = ({0._first_point.name}, {0._second_point.name}, {0._length})'.format(self)

    ##############################################

    def eval_internal(self):

        vector = self._second_point.vector - self._first_point.vector
        self._pattern.calculator.set_current_segment(vector)
        self._vector = self._first_point.vector + vector.to_normalised()*self._length.value
        self._pattern.calculator.unset_current_segment()
        self._post_eval_internal()

####################################################################################################

class EndLinePoint(Point, LinePropertiesMixin, BasePointMixin, LengthAngleMixin):

    ##############################################

    def __init__(self, pattern, name,
                 base_point, angle, length,
                 label_offset,
                 line_style=None, line_color=None,
                 id=None,
    ):

        Point.__init__(self, pattern, name, label_offset, id)
        LinePropertiesMixin.__init__(self, line_style, line_color)
        BasePointMixin.__init__(self, base_point)
        LengthAngleMixin.__init__(self, length, angle)

    ##############################################

    def __repr__(self):

        return self.__class__.__name__ + ' {0._name} = ({0._base_point.name}, {0._angle}, {0._length})'.format(self)

    ##############################################

    def eval_internal(self):

        self._vector = self._base_point._vector + Vector2D.from_angle(self._angle.value)*self._length.value
        self._post_eval_internal()

####################################################################################################

class LineIntersectPoint(Point):

    ##############################################

    def __init__(self, pattern, name,
                 point1_line1, point2_line1, point1_line2, point2_line2,
                 label_offset,
                 id=None,
    ):

        Point.__init__(self, pattern, name, label_offset, id)
        self._point1_line1 = self._get_calculation(point1_line1)
        self._point2_line1 = self._get_calculation(point2_line1)
        self._point1_line2 = self._get_calculation(point1_line2)
        self._point2_line2 = self._get_calculation(point2_line2)
        self._connect_ancestor(self._point1_line1, self._point2_line1,
                               self._point1_line2, self._point2_line2)

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

    def __repr__(self):

        return self.__class__.__name__ + ' {0._name} = ({0._point1_line1.name}, {0._point2_line1.name}, {0._point1_line2.name}, {0._point2_line2.name})'.format(self)

    ##############################################

    def eval_internal(self):

        line1 = Line2D.from_two_points(self._point1_line1.vector, self._point2_line1.vector)
        line2 = Line2D.from_two_points(self._point1_line2.vector, self._point2_line2.vector)
        self._vector = line1.intersection(line2)
        self._post_eval_internal()

####################################################################################################

class NormalPoint(Point, LinePropertiesMixin, FirstSecondPointMixin, LengthAngleMixin):

    ##############################################

    def __init__(self, pattern, name,
                 first_point, second_point, angle, length,
                 label_offset,
                 line_style=None, line_color=None,
                 id=None,
    ):

        Point.__init__(self, pattern, name, label_offset, id)
        LinePropertiesMixin.__init__(self, line_style, line_color)
        FirstSecondPointMixin.__init__(self, first_point, second_point)
        LengthAngleMixin.__init__(self, length, angle)

    ##############################################

    def __repr__(self):

        return self.__class__.__name__ + ' {0._name} = ({0._first_point.name}, {0._second_point.name}, {0._angle}, {0._length})'.format(self)

    ##############################################

    def eval_internal(self):

        vector = self._second_point.vector - self._first_point.vector
        self._pattern.calculator.set_current_segment(vector)
        direction = vector.to_normalised()
        direction = direction.normal()
        angle = self._angle.value
        if angle:
            direction = direction.rotate(angle)
        self._vector = self._first_point.vector + direction*self._length.value
        self._pattern.calculator.unset_current_segment()
        self._post_eval_internal()

####################################################################################################

class PointOfIntersection(Point, FirstSecondPointMixin):

    ##############################################

    def __init__(self, pattern, name,
                 first_point, second_point,
                 label_offset,
                 id=None,
    ):

        Point.__init__(self, pattern, name, label_offset, id)
        FirstSecondPointMixin.__init__(self, first_point, second_point)

    ##############################################

    def __repr__(self):

        return self.__class__.__name__ + ' {0._name} = ({0._first_point.name}, {0._second_point.name})'.format(self)

    ##############################################

    def eval_internal(self):

        self._vector = Vector2D(self._first_point.vector.x, self._second_point.vector.y)
        self._post_eval_internal()

####################################################################################################

class Line(Calculation, LinePropertiesMixin, FirstSecondPointMixin):

    ##############################################

    def __init__(self, pattern,
                 first_point, second_point,
                 line_style='solid', line_color='black',
                 id=None,
    ):

        Calculation.__init__(self, pattern, id)
        LinePropertiesMixin.__init__(self, line_style, line_color)
        FirstSecondPointMixin.__init__(self, first_point, second_point)

    ##############################################

    def __repr__(self):

        return self.__class__.__name__ + ' ({0._first_point.name}, {0._second_point.name})'.format(self)

    ##############################################

    def eval_internal(self):

        pass

    ##############################################

    def geometry(self):
        return Segment2D(self._first_point.vector, self._second_point.vector)

####################################################################################################

class SimpleInteractiveSpline(Calculation, LinePropertiesMixin, FirstSecondPointMixin):

    ##############################################

    def __init__(self, pattern,
                 first_point, second_point,
                 angle1, length1,
                 angle2, length2,
                 line_style='solid', line_color='black',
                 id=None,
    ):

        Calculation.__init__(self, pattern, id)
        LinePropertiesMixin.__init__(self, line_style, line_color)
        FirstSecondPointMixin.__init__(self, first_point, second_point)
        self._angle1 = Expression(angle1, pattern.calculator)
        self._length1 = Expression(length1, pattern.calculator)
        self._angle2 = Expression(angle2, pattern.calculator)
        self._length2 = Expression(length2, pattern.calculator)
        # self._connect_ancestor_for_expressions(self._angle1, self._length1, self._angle2, self._length2)

        self._control_point1 = None # Fixme: not yet computed
        self._control_point2 = None

    ##############################################

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

    @property
    def control_point1(self):
        return self._control_point1

    @property
    def control_point2(self):
        return self._control_point2

    ##############################################

    def __repr__(self):

        return self.__class__.__name__ + ' ({0._first_point.name}, {0._second_point.name}, {0._angle1}, {0._length1}, {0._angle2}, {0._length2})'.format(self)

    ##############################################

    def eval_internal(self):

        control_point1_offset = Vector2D.from_angle(self._angle1.value)*self._length1.value
        control_point2_offset = Vector2D.from_angle(self._angle2.value)*self._length2.value
        self._control_point1 = self.first_point.vector + control_point1_offset
        self._control_point2 = self.second_point.vector + control_point2_offset
        # self._logger.info("Control points : {} {}".format(self._control_point1, self._control_point2))

    ##############################################

    def geometry(self):

        if self._control_point1 is None:
            raise NameError("eval before to get geometry")
        return CubicBezier2D(self._first_point.vector, self._control_point1,
                             self._control_point2, self._second_point.vector)
