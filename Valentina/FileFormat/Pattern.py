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

####################################################################################################

import logging

from lxml import etree

from Valentina.Geometry.Vector2D import Vector2D
from Valentina.Pattern.Measurement import Measurements, Measurement
from Valentina.Pattern.Pattern import Pattern
from Valentina.Xml.Objectivity import (IntAttribute, FloatAttribute, StringAttribute,
                                       XmlObjectAdaptator)
from Valentina.Xml.XmlFile import XmlFileMixin
from .Measurements import VitFile

import Valentina.Pattern.Calculation as Calculation

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class CalculationMixin:

    __attributes__ = (
        IntAttribute('id'),
    )

    ##############################################

    def to_calculation(self, pattern):

        raise NotImplementedError

####################################################################################################

class LinePropertiesMixin:

    __attributes__ = (
        StringAttribute('line_color', 'lineColor'),
        StringAttribute('line_style', 'typeLine'),
    )

    __COLORS__ = (
        'black',
        'blue',
        'cornflowerblue',
        'darkBlue',
        'darkGreen',
        'darkRed',
        'darkviolet',
        'deeppink',
        'deepskyblue',
        'goldenrod',
        'green',
        'lightsalmon',
        'lime',
        'mediumseagreen',
        'orange',
        'violet',
        'yellow',
    )

    __LINE_STYLE__ = (
        'dashDotDotLine',
        'dashDotLine',
        'dashLine',
        'dotLine',
        'hair', # should be solid
        'none',
    )

####################################################################################################

class XyMixin:
    __attributes__ = (
        StringAttribute('x'),
        StringAttribute('y'),
    )

class FirstSecondPointMixin:
    __attributes__ = (
        IntAttribute('first_point', 'firstPoint'),
        IntAttribute('second_point', 'secondPoint'),
    )

class BasePointMixin:
    __attributes__ = (
        IntAttribute('base_point', 'basePoint'),
    )

class FourPointMixin:
    __attributes__ = (
        IntAttribute('point1_line1', 'p1Line1'),
        IntAttribute('point2_line1', 'p2Line1'),
        IntAttribute('point1_line2', 'p1Line2'),
        IntAttribute('point2_line2', 'p2Line2'),
    )

class LengthMixin:
    __attributes__ = (
        StringAttribute('length'),
    )

class AngleMixin:
    __attributes__ = (
        StringAttribute('angle'),
    )

class LengthAngleMixin(LengthMixin, AngleMixin):
    pass

####################################################################################################

class PointMixin(CalculationMixin):

    __tag__ = 'point'
    __attributes__ = (
        StringAttribute('name'),
        FloatAttribute('mx'),
        FloatAttribute('my'),
    )

    __calculation__ = None

    ##############################################

    def to_calculation(self, pattern):

        kwargs = self.to_dict(exclude=('mx', 'my')) # id'
        kwargs['label_offset'] = Vector2D(self.mx, self.my)
        return self.__calculation__(pattern, **kwargs)

####################################################################################################

class PointLinePropertiesMixin(PointMixin, LinePropertiesMixin):
    pass

####################################################################################################

class AlongLinePoint(XmlObjectAdaptator, PointLinePropertiesMixin, FirstSecondPointMixin, LengthMixin):

    # {'lineColor': 'black', 'firstPoint': '138', 'id': '141', 'mx': '-4.2484', 'typeLine': 'none',
    #  'my': '1.01162', 'name': 'A33', 'length': 'Line_A30_A32', 'type': 'alongLine', 'secondPoint': '68'}

    __type__ = 'alongLine'
    __calculation__ = Calculation.AlongLinePoint

####################################################################################################

class EndLinePoint(XmlObjectAdaptator, PointLinePropertiesMixin, BasePointMixin, LengthAngleMixin):

    # {'basePoint': '1', 'name': 'A1', 'id': '2', 'angle': '0', 'length': 'waist_circ/2+10',
    #  'typeLine': 'dashDotLine', 'my': '0.264583', 'type': 'endLine', 'mx': '0.132292', 'lineColor': 'black'}

    __type__ = 'endLine'
    __calculation__ = Calculation.EndLinePoint

####################################################################################################

class LineIntersectPoint(XmlObjectAdaptator, PointMixin, FourPointMixin):

    # {'type': 'lineIntersect', 'p2Line1': '32', 'mx': '0.132292', 'p1Line2': '10',
    #  'p2Line2': '11', 'p1Line1': '27', 'id': '39', 'my': '0.264583', 'name': 'Cp'}

    __type__ = 'lineIntersect'
    __calculation__ = Calculation.LineIntersectPoint

####################################################################################################

class NormalPoint(XmlObjectAdaptator, PointLinePropertiesMixin, FirstSecondPointMixin, LengthAngleMixin):

    # {'my': '-4.18524', 'secondPoint': '63', 'name': 'A36', 'angle': '0', 'length': '0.5',
    #  'firstPoint': '138', 'typeLine': 'hair', 'type': 'normal', 'mx': '-1.57131', 'id': '147', 'lineColor': 'black'}

    __type__ = 'normal'
    __calculation__ = Calculation.NormalPoint

####################################################################################################

class PointOfIntersection(XmlObjectAdaptator, PointMixin, FirstSecondPointMixin):

    # {'id': '71', 'secondPoint': '56', 'type': 'pointOfIntersection', 'firstPoint': '59',
    #  'name': 'Nc', 'mx': '0.132292', 'my': '0.264583'}

    __type__ = 'pointOfIntersection'
    __calculation__ = Calculation.PointOfIntersection

####################################################################################################

class SinglePoint(XmlObjectAdaptator, PointMixin, XyMixin):

    # {'y': '1.0', 'mx': '0.1', 'type': 'single', 'my': '0.2', 'id': '1', 'name': 'A0', 'x': '0.7'}

    __type__ = 'single'
    __calculation__ = Calculation.SinglePoint

####################################################################################################

# {'type': 'trueDarts', 'name1': 'A34', 'dartP2': '139', 'dartP1': '141',
# 'my2': '-3.87275', 'point2': '146', 'dartP3': '140', 'id': '144', 'mx2': '0.794387',
# 'my1': '-2.44561', 'name2': 'A35', 'point1': '145', 'baseLineP2': '63', 'mx1': '-3.64071',
# 'baseLineP1': '68'}

####################################################################################################

class Point:

    # We cannot use a metaclass to auto-register due to XmlObjectAdaptator (right ?)
    __TYPES__ = {
        'alongLine': AlongLinePoint,
        'bisector': None,
        'curveIntersectAxis': None,
        'cutArc': None,
        'cutSpline': None,
        'cutSplinePath': None,
        'endLine': EndLinePoint,
        'height': None,
        'lineIntersect': LineIntersectPoint,
        'lineIntersectAxis': None,
        'normal': NormalPoint,
        'pointFromArcAndTangent': None,
        'pointFromCircleAndTangent': None,
        'pointOfContact': None,
        'pointOfIntersection': PointOfIntersection,
        'pointOfIntersectionArcs': None,
        'pointOfIntersectionCircles': None,
        'pointOfIntersectionCurves': None,
        'shoulder': None,
        'single': SinglePoint,
        'triangle': None,
        'trueDarts': None,
    }

####################################################################################################

class Line(XmlObjectAdaptator, CalculationMixin, LinePropertiesMixin, FirstSecondPointMixin):

    # {'typeLine': 'hair', 'lineColor': 'black', 'firstPoint': '74', 'secondPoint': '72', 'id': '76'}

    __tag__ = 'line'

    ##############################################

    def to_calculation(self, pattern):

        return Calculation.Line(pattern, **self.to_dict()) # exclude=('id')

####################################################################################################

class SplineMixin(CalculationMixin):
    __tag__ = 'spline'

####################################################################################################

class SimpleInteractiveSpline(XmlObjectAdaptator, SplineMixin):

    # 'type': 'simpleInteractive',
    #   'length2': '8.65783', 'angle2': '85.3921',
    #    'point4': '31',
    #    'color': 'black',
    #    'length1': '8.85757', 'angle1': '251.913',
    #    'point1': '20',
    #    'id': '97'
    # }

    __type__ = 'simpleInteractive'
    __attributes__ = (
        IntAttribute('first_point', 'point1'),
        IntAttribute('second_point', 'point4'),
        StringAttribute('length1'),
        StringAttribute('length2'),
        StringAttribute('angle1'),
        StringAttribute('angle2'),
        StringAttribute('line_color', 'color'),
    )

    ##############################################

    def to_calculation(self, pattern):

        return Calculation.SimpleInteractiveSpline(pattern, **self.to_dict()) # exclude=('id')

####################################################################################################

class Spline:

    # We cannot use a metaclass to auto-register due to XmlObjectAdaptator (right ?)
    __TYPES__ = {
        'simpleInteractive': SimpleInteractiveSpline,
    }

####################################################################################################

    # __ARC_TYPE__ = (
    #     'arcWithLength', # to be implemented
    #     'simple', # to be implemented
    #     )

    # __ELLIPSE_TYPE__ = (
    #     'simple', # to be implemented
    #     )

    # __OPERATION_TYPE__ = (
    #     'flippingByAxis', # to be implemented
    #     'flippingByLine', # to be implemented
    #     'moving', # to be implemented
    #     'rotation', # to be implemented
    # )

####################################################################################################

class CalculationDispatcher:

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

    @staticmethod
    def from_xml(element):

        tag_class = CalculationDispatcher.__TAGS__[element.tag]
        if hasattr(tag_class, '__TYPES__'):
            cls = tag_class.__TYPES__[element.attrib['type']]
        else:
            cls = tag_class
        if cls is not None:
            return cls(element)
        else:
            raise NotImplementedError

####################################################################################################

class ValFile(XmlFileMixin):

    _logger = _module_logger.getChild('ValFile')

    ##############################################

    def __init__(self, path):

        XmlFileMixin.__init__(self, path)
        self._vit_file = None
        self._pattern = None
        self._read()

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
        self._vit_file = VitFile(measurements_path)

        pattern = Pattern(self._vit_file.measurements)
        self._pattern = pattern

        elements = self._get_xpath_element(tree, 'draw/calculation')
        for element in elements:
            try:
                xml_calculation = CalculationDispatcher.from_xml(element)
                calculation = xml_calculation.to_calculation(pattern)
                pattern.add(calculation)
            except NotImplementedError:
                self._logger.warning('Not implemented calculation\n' +  str(etree.tostring(element)))

        pattern.eval()
