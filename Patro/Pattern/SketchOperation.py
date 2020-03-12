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

"""This module defines all the sketch operations supported by the pattern engine, e.g. the
intersection between two lines.

A sketch operation must be build from the corresponding method of the Pattern class.

"""

####################################################################################################

import logging

from Patro.Common.Object import ObjectGlobalIdMixin
from Patro.GeometryEngine.Bezier import CubicBezier2D
from Patro.GeometryEngine.Conic import Circle2D
from Patro.GeometryEngine.Line import Line2D
from Patro.GeometryEngine.Segment import Segment2D
from Patro.GeometryEngine.Vector import Vector2D
from Patro.GraphicStyle import StrokeStyle, Colors
from .Calculator import Expression

# Rename id buitin
pyid = id

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

def quote(x):
    return "'{}'".format(x)

####################################################################################################

### class SketchOperationMetaClass:
###
###     _logger = _module_logger.getChild('SketchOperationMetaClass')
###
###     ##############################################
###
###     def __init__(cls, class_name, super_classes, class_attribute_dict):
###         # cls._logger.debug(str((cls, class_name, super_classes, class_attribute_dict)))
###         type.__init__(cls, class_name, super_classes, class_attribute_dict)

####################################################################################################

# metaclass = SketchOperationMetaClass
class SketchOperation(ObjectGlobalIdMixin):

    """Baseclass for sketch operation"""

    _logger = _module_logger.getChild('SketchOperation')

    ##############################################

    def __init__(self, sketch, id=None):

        self._sketch = sketch

        # Valentina set an incremental integer id for each calculation (entity)
        # id is used to identify operation, see _get_operation
        # A calculation which generate a point has also a name
        try:
            super().__init__(id)
        except ValueError:
            raise NameError("id {} is already attributed".format(id))

        self._dag_node = self._dag.add_node(pyid(self), data=self)
        self._dependencies = set()

    ##############################################

    @property
    def sketch(self):
        return self._sketch

    @property
    def _dag(self):
        return self._sketch.calculator.dag

    @property
    def dependencies(self):
        return self._dependencies

    ##############################################

    def _get_operation(self, operation):

        """Return the corresponding :obj:`SketchOperation` object where *operation* can be
        :obj:`SketchOperation` instance, an id or a name.

        """

        if isinstance(operation, SketchOperation):
            return operation
        # elif isinstance(operation, (int, str)):
        else: # must be id or string
            return self._sketch.get_operation(operation)

    ##############################################

    def eval(self):
        self._logger.debug('Eval {}'.format(self))
        self.eval_internal()

    ##############################################

    def eval_internal(self):
        """Code to evaluate the operation in subclasses, i.e. to compute internal states like points."""
        pass

    ##############################################

    def _init_args(self):

        # cf. to_python

        args = self.__init__.__code__.co_varnames
        args = args[2:-1] # remove self, sketch, id
        return args

    ##############################################

    def to_python(self):

        """Return the Python code for the operation"""

        args = self._init_args()
        values = []
        for arg in args:
            value = getattr(self, arg)
            # if arg == 'sketch':
            #     value_str = 'sketch'
            # if isinstance(value, Sketch):
            #     value_str = 'sketch'
            if value is  None:
                value_str = 'None'
            elif isinstance(value, (int, float)):
                value_str = str(value)
            elif isinstance(value, str):
                value_str = quote(value)
            # elif isinstance(value, SketchOperation):
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
        kwargs = ', '.join(['sketch'] + [key + '=' + value for key, value in zip(args, values)])
        return self.__class__.__name__ + '(' + kwargs + ')'

    ##############################################

    def _connect_ancestor(self, *points):
        """Connect point dependencies in the DAG."""
        dag = self._dag
        for point in points:
            self._dependencies.add(point)
            self._dag_node.connect_ancestor(dag[pyid(point)])

    ##############################################

    # def _connect_ancestor_for_expressions(self, *expressions):

    #     for expression in expressions:
    #         self._connect_ancestor(*expression.dependencies)

    def _iter_on_expressions(self):
        """Lookup for :obj:`Expression` in the object and yield them."""
        for attribute in self.__dict__.values():
            if isinstance(attribute, Expression):
                yield attribute

    def connect_ancestor_for_expressions(self):
        """Connect dependencies from expressions in the DAG."""
        # Expression's dependencies are only known after compilation
        for expression in self._iter_on_expressions():
            self._connect_ancestor(*expression.dependencies)

    ##############################################

    # @property
    def geometry(self):
        """Return the geometric object"""
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
        self._first_point = self._get_operation(first_point)
        self._second_point = self._get_operation(second_point)
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
        self._base_point = self._get_operation(base_point)
        self._connect_ancestor(self._base_point)

    ##############################################

    @property
    def base_point(self):
        return self._base_point

####################################################################################################

class LengthMixin:

    ##############################################

    def __init__(self, length):
        self._length = Expression(length, self._sketch.calculator)
        # self._connect_ancestor_for_expressions(self._length)

    ##############################################

    @property
    def length(self):
        return self._length

####################################################################################################

class AngleMixin:

    ##############################################

    def __init__(self, angle):
        self._angle = Expression(angle, self._sketch.calculator)
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

class CenterMixin:

    ##############################################

    def __init__(self, center):
        self._center = self._get_operation(center)
        self._connect_ancestor(self._center)

    ##############################################

    @property
    def center(self):
        return self._center

####################################################################################################

class RadiusMixin:

    ##############################################

    def __init__(self, radius):
        self._radius = Expression(radius, self._sketch.calculator)
        # self._connect_ancestor_for_expressions(self._radius)

    ##############################################

    @property
    def radius(self):
        return self._radius

####################################################################################################

class CenterRadiusMixin(CenterMixin, RadiusMixin):

    ##############################################

    def __init__(self, center, radius):
        CenterMixin.__init__(self, center)
        RadiusMixin.__init__(self, radius)

####################################################################################################

class Point(SketchOperation):

    """Base class for point."""

    ##############################################

    def __init__(self, sketch, name, label_offset, id=None):

        SketchOperation.__init__(self, sketch, id)
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
        self._logger.debug('{0._name} {0._vector}'.format(self))

    ##############################################

    def geometry(self):
        return self._vector.clone()

####################################################################################################

class SinglePoint(Point):

    """Construct a point from coordinate"""

    ##############################################

    def __init__(self, sketch, name,
                 x, y,
                 label_offset,
                 id=None
    ):

        Point.__init__(self, sketch, name, label_offset, id)
        self._x = Expression(x, sketch.calculator)
        self._y = Expression(y, sketch.calculator)
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

    """Construct a point from two points defining a direction and a length"""

    ##############################################

    def __init__(self, sketch, name,
                 first_point, second_point, length,
                 label_offset,
                 line_style=None, line_color=None,
                 id=None,
                 ):

        Point.__init__(self, sketch, name, label_offset, id)
        LinePropertiesMixin.__init__(self, line_style, line_color)
        FirstSecondPointMixin.__init__(self, first_point, second_point)
        LengthMixin.__init__(self, length)

    ##############################################

    def __repr__(self):
        return self.__class__.__name__ + ' {0._name} = ({0._first_point.name}, {0._second_point.name}, {0._length})'.format(self)

    ##############################################

    def eval_internal(self):

        vector = self._second_point.vector - self._first_point.vector
        self._sketch.calculator.set_current_segment(vector)
        self._vector = self._first_point.vector + vector.to_normalised()*self._length.value
        self._sketch.calculator.unset_current_segment()
        self._post_eval_internal()

####################################################################################################

class EndLinePoint(Point, LinePropertiesMixin, BasePointMixin, LengthAngleMixin):

    """Construct a point from a base point and a vector defined by an angle and a length"""

    ##############################################

    def __init__(self, sketch, name,
                 base_point, angle, length,
                 label_offset,
                 line_style=None, line_color=None,
                 id=None,
    ):

        Point.__init__(self, sketch, name, label_offset, id)
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

    """Construct a point from the intersection of two segments defined by four points"""

    ##############################################

    def __init__(self, sketch, name,
                 point1_line1, point2_line1, point1_line2, point2_line2,
                 label_offset,
                 id=None,
    ):

        Point.__init__(self, sketch, name, label_offset, id)
        self._point1_line1 = self._get_operation(point1_line1)
        self._point2_line1 = self._get_operation(point2_line1)
        self._point1_line2 = self._get_operation(point1_line2)
        self._point2_line2 = self._get_operation(point2_line2)
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

    """Construct a point at a distance of the first point on the rotated normal of a line defined by two points"""

    ##############################################

    def __init__(self, sketch, name,
                 first_point, second_point, angle, length,
                 label_offset,
                 line_style=None, line_color=None,
                 id=None,
    ):

        Point.__init__(self, sketch, name, label_offset, id)
        LinePropertiesMixin.__init__(self, line_style, line_color)
        FirstSecondPointMixin.__init__(self, first_point, second_point)
        LengthAngleMixin.__init__(self, length, angle)

    ##############################################

    def __repr__(self):
        return self.__class__.__name__ + ' {0._name} = ({0._first_point.name}, {0._second_point.name}, {0._angle}, {0._length})'.format(self)

    ##############################################

    def eval_internal(self):

        vector = self._second_point.vector - self._first_point.vector
        self._sketch.calculator.set_current_segment(vector)
        direction = vector.to_normalised()
        direction = direction.normal
        angle = self._angle.value
        if angle:
            direction = direction.rotate(angle)
        self._vector = self._first_point.vector + direction*self._length.value
        self._sketch.calculator.unset_current_segment()
        self._post_eval_internal()

####################################################################################################

class PointOfContact(Point, FirstSecondPointMixin, CenterRadiusMixin):

    """Construct a point at the intersection of a circle and a line"""

    # Fixme: name

    _logger = _module_logger.getChild('PointOfContact')

    ##############################################

    def __init__(self, sketch, name,
                 first_point, second_point,
                 center, radius,
                 label_offset,
                 id=None,
    ):

        Point.__init__(self, sketch, name, label_offset, id)
        FirstSecondPointMixin.__init__(self, first_point, second_point)
        CenterRadiusMixin.__init__(self, center, radius)

    ##############################################

    def __repr__(self):
        return (self.__class__.__name__ +
                ' {0._name} = ({0._first_point.name}, {0._second_point.name})'
                ', {0._center}, {0._radius}'.format(self))

    ##############################################

    def eval_internal(self):
        print('>'*50)
        print(self)
        segment = Segment2D(self._first_point.vector, self._second_point.vector)
        circle = Circle2D(self._center.vector, self._radius.value)
        points = circle.intersect_segment(segment)
         # Fixme: multi-points ???
        if not points:
            self._logger.warning('line-circle intersection is null')
            self._vector = None
        elif len(points) == 1:
            self._vector = points[0]
        else:
            self._logger.warning('More than one points for line-circle intersection')
            # point must lie in the segment
            point0 = points[0]
            segment.contain_point(points[0])
            segment.contain_point(points[1])
            print('>'*50)
            if segment.contain_point(point0):
                self._vector = point0
            else:
                # Fixme: more than two points ???
                self._vector = points[1]
        self._post_eval_internal()

####################################################################################################

class PointOfIntersection(Point, FirstSecondPointMixin):

    """Construct a point from the x coordinate of a fist point and the y coordinate of a second point"""

    ##############################################

    def __init__(self, sketch, name,
                 first_point, second_point,
                 label_offset,
                 id=None,
    ):

        Point.__init__(self, sketch, name, label_offset, id)
        FirstSecondPointMixin.__init__(self, first_point, second_point)

    ##############################################

    def __repr__(self):
        return self.__class__.__name__ + ' {0._name} = ({0._first_point.name}, {0._second_point.name})'.format(self)

    ##############################################

    def eval_internal(self):
        self._vector = Vector2D(self._first_point.vector.x, self._second_point.vector.y)
        self._post_eval_internal()

####################################################################################################

class Line(SketchOperation, LinePropertiesMixin, FirstSecondPointMixin):

    """Construct a line defined by two points"""

    ##############################################

    def __init__(self, sketch,
                 first_point, second_point,
                 line_style=StrokeStyle.SolidLine, line_color=Colors.black,
                 id=None,
    ):

        SketchOperation.__init__(self, sketch, id)
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

class SimpleInteractiveSpline(SketchOperation, LinePropertiesMixin, FirstSecondPointMixin):

    """"Construct a quadratic Bezier curve from two extremity points and two control points"""

    ##############################################

    def __init__(self, sketch,
                 first_point, second_point,
                 angle1, length1,
                 angle2, length2,
                 line_style=StrokeStyle.SolidLine, line_color=Colors.black,
                 id=None,
    ):

        SketchOperation.__init__(self, sketch, id)
        LinePropertiesMixin.__init__(self, line_style, line_color)
        FirstSecondPointMixin.__init__(self, first_point, second_point)
        self._angle1 = Expression(angle1, sketch.calculator)
        self._length1 = Expression(length1, sketch.calculator)
        self._angle2 = Expression(angle2, sketch.calculator)
        self._length2 = Expression(length2, sketch.calculator)
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
        # self._logger.debug("Control points : {} {}".format(self._control_point1, self._control_point2))

    ##############################################

    def geometry(self):

        if self._control_point1 is None:
            raise NameError("eval before to get geometry")
        return CubicBezier2D(self._first_point.vector, self._control_point1,
                             self._control_point2, self._second_point.vector)
