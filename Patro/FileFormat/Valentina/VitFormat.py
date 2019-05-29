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

"""This module implements the val XML file format and is designed so as to decouple the XML format
and the calculation API.

The purpose of each XmlObjectAdaptator sub-classes is to serve as a bidirectional adaptor between
the XML format and the API.

Valentina File Format Concept

* all entities which are referenced later in the file are identified by a unique positive integer
  over the file, usually incremented from 1.

* a file contains one or several "pieces"

  * pieces correspond to independent scopes, one cannot access calculations of another piece
  * pieces share the same referential, usually the root point of a piece is placed next
    to the previous piece

* a piece has "calculations" and "details"

  * a calculations corresponds to a point, a segment, or a Bézier curve ...
  * a detail corresponds to a garment piece defined by segments and curves
  * one can define several details within a piece

"""

####################################################################################################

__all__ = [
    'Point',
    'Line',
    'Spline',
    'ModelingPoint',
    'ModelingSpline',
    'Detail',
    'DetailData',
    'DetailPatternInfo',
    'DetailGrainline',
    'DetailNode',
]

####################################################################################################

import Patro.Pattern.SketchOperation as SketchOperation
from Patro.Common.Xml.Objectivity import (
    Attribute,
    BoolAttribute,
    IntAttribute, FloatAttribute,
    StringAttribute,
    XmlObjectAdaptator
)
from Patro.GeometryEngine.Vector import Vector2D
from Patro.GraphicStyle import Colors, StrokeStyle

####################################################################################################

class ColorAttribute(Attribute):

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

    ##############################################

    @classmethod
    def from_xml(cls, value):
        return Colors.ensure_color(value)

####################################################################################################

class StrokeStyleAttribute(Attribute):

    __STROKE_STYLE__ = {
        'dashDotDotLine': StrokeStyle.DashDotDotLine,
        'dashDotLine': StrokeStyle.DashDotLine,
        'dashLine': StrokeStyle.DashLine,
        'dotLine': StrokeStyle.DotLine,
        'hair': StrokeStyle.SolidLine, # should be solid
        'none': StrokeStyle.NoPen,
    }

    # Fixme: from_xml to_xml ???
    __TO_STROKE_STYLE__ = {value:name for name, value in __STROKE_STYLE__.items()}
    __STROKE_STYLE__.update(__TO_STROKE_STYLE__)

    ##############################################

    @classmethod
    def from_xml(cls, value):
        return cls.__STROKE_STYLE__[value]

    ##############################################

    # @classmethod
    # def to_xml(cls, value):
    #     return cls.__TO_STROKE_STYLE__[value]

####################################################################################################

class ValentinaBuiltInVariables:

    # defined in libs/ifc/ifcdef.cpp

    current_length = 'CurrentLength'
    current_seam_allowance = 'CurrentSeamAllowance'

    angle_line  = 'AngleLine_'
    increment   = 'Increment_'
    line        = 'Line_'
    measurement = 'M_'
    seg         = 'Seg_'

    arc         = 'ARC_'
    elarc       = 'ELARC_'
    spl         = 'SPL_'

    angle1      = 'Angle1'
    angle2      = 'Angle2'
    c1_length   = 'C1Length'
    c2_length   = 'C2Length'
    radius      = 'Radius'
    rotation    = 'Rotation'

    spl_path    = 'SplPath'

    angle1_arc         = angle1 + arc
    angle1_elarc       = angle1 + elarc
    angle1_spl_path    = angle1 + spl_path
    angle1_spl         = angle1 + spl
    angle2_arc         = angle2 + arc
    angle2_elarc       = angle2 + elarc
    angle2_spl_path    = angle2 + spl_path
    angle2_spl         = angle2 + spl
    c1_length_spl_path = c1_length + spl_path
    c1_length_spl      = c1_length + spl
    c2_length_spl_path = c2_length + spl_path
    c2_length_spl      = c2_length + spl
    radius1_elarc      = radius + '1' + elarc
    radius2_elarc      = radius + '2' + elarc
    radius_arc         = radius + arc
    rotation_elarc     = rotation + elarc

####################################################################################################

VALENTINA_ATTRIBUTES = (
    'aScale',
    'angle',
    'angle1',
    'angle2',
    'arc',
    'axisP1',
    'axisP2',
    'axisType',
    'baseLineP1',
    'baseLineP2',
    'basePoint',
    'c1Center',
    'c1Radius',
    'c2Center',
    'c2Radius',
    'cCenter',
    'cRadius',
    'center',
    'closed',
    'color',
    'crossPoint',
    'curve',
    'curve1',
    'curve2',
    'cut',
    'dartP1',
    'dartP2',
    'dartP3',
    'duplicate',
    'firstArc',
    'firstPoint',
    'firstToCountour',
    'forbidFlipping',
    'forceFlipping',
    'hCrossPoint',
    'height',
    'idObject',
    'inLayout',
    'kAsm1',
    'kAsm2',
    'kCurve',
    'lastToCountour',
    'length',
    'length1',
    'length2',
    'lineColor',
    'mx',
    'mx1',
    'mx2',
    'my',
    'my1',
    'my2',
    'name',
    'name1',
    'name2',
    'p1Line',
    'p1Line1',
    'p1Line2',
    'p2Line',
    'p2Line1',
    'p2Line2',
    'pShoulder',
    'pSpline',
    'pathPoint',
    'penStyle',
    'placeLabelType',
    'point1',
    'point2',
    'point3',
    'point4',
    'radius',
    'radius1',
    'radius2',
    'rotationAngle',
    'secondArc',
    'secondPoint',
    'showLabel',
    'showLabel1',
    'showLabel2',
    'suffix',
    'tangent',
    'thirdPoint',
    'type',
    'typeLine',
    'vCrossPoint',
    'version',
    'width',
    'x',
    'y',
)

####################################################################################################

class MxMyMixin:

    __attributes__ = (
        FloatAttribute('mx'),
        FloatAttribute('my'),
    )

####################################################################################################

class CalculationMixin:

    __attributes__ = (
        IntAttribute('id'),
    )

    __operation__ = None # operation's class

    ##############################################

    def call_operation_function(self, sketch, kwargs):
        # Fixme: map valentina name -> ...
        method = getattr(sketch, self.__operation__.__name__)
        return method(**kwargs)

    ##############################################

    def to_operation(self, sketch):
        raise NotImplementedError

    ##############################################

    @classmethod
    def from_operation(operation):
        raise NotImplementedError

####################################################################################################

class CalculationTypeMixin(CalculationMixin):

    ##############################################

    def to_xml(self):
        return XmlObjectAdaptator.to_xml(self, type=self.__type__)

####################################################################################################

class LinePropertiesMixin:

    __attributes__ = (
        ColorAttribute('line_color', 'lineColor'),
        StrokeStyleAttribute('line_style', 'typeLine'),
    )

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

class FirstSecondThirdPointMixin(FirstSecondPointMixin):
    __attributes__ = (
        IntAttribute('third_point', 'thirdPoint'),
    )

class BasePointMixin:
    __attributes__ = (
        IntAttribute('base_point', 'basePoint'),
    )

class Line1Mixin:
    __attributes__ = (
        IntAttribute('point1_line1', 'p1Line1'),
        IntAttribute('point2_line1', 'p2Line1'),
    )

class Line2Mixin:
    __attributes__ = (
        IntAttribute('point1_line2', 'p1Line2'),
        IntAttribute('point2_line2', 'p2Line2'),
    )

class Line12Mixin(Line1Mixin, Line2Mixin):
    pass

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

class CenterRadiusMixin:
    __attributes__ = (
        IntAttribute('center'), # center point
        StringAttribute('radius'),
    )

####################################################################################################

class PointMixin(CalculationTypeMixin, MxMyMixin):

    __tag__ = 'point'
    __attributes__ = (
        StringAttribute('name'),
    )

    ##############################################

    def to_operation(self, sketch):

        kwargs = self.to_dict(exclude=('mx', 'my')) # id'
        kwargs['label_offset'] = Vector2D(self.mx, self.my)
        return self.call_operation_function(sketch, kwargs)

    ##############################################

    @classmethod
    def from_operation(cls, operation):

        kwargs = cls.get_dict(operation, exclude=('mx', 'my'))
        label_offset = operation.label_offset
        kwargs['mx'] = label_offset.x
        kwargs['my'] = label_offset.y
        return cls(**kwargs)

####################################################################################################

class PointLinePropertiesMixin(PointMixin, LinePropertiesMixin):
    pass

####################################################################################################

class AlongLinePoint(PointLinePropertiesMixin, FirstSecondPointMixin, LengthMixin, XmlObjectAdaptator):

    # <point id="27" firstPoint="25" typeLine="none" mx="0.1" secondPoint="26"
    # length="-Line_Bt_Ct" name="Dt" lineColor="black" type="alongLine" my="0.2"/>

    __type__ = 'alongLine'
    __operation__ = SketchOperation.AlongLinePoint

####################################################################################################

class BissectorPoint(PointLinePropertiesMixin, FirstSecondThirdPointMixin, LengthMixin, XmlObjectAdaptator):

    # <point id="13" firstPoint="2" thirdPoint="5" typeLine="hair" mx="0.1" secondPoint="1"
    # length="Line_A_X" name="B" lineColor="deepskyblue" type="bisector" my="0.2"/>

    __type__ = 'bisector'
    # __operation__ = SketchOperation.BissectorPoint

####################################################################################################

# __type__ = 'curveIntersectAxis'
# <point id="68" basePoint="64" typeLine="hair" mx="0.5" name="Cax1" lineColor="blue"
# type="curveIntersectAxis" angle="10" curve="59" my="-3.1"/>

# __type__ = 'cutArc'
# <point id="73" mx="-3.7" length="30" arc="72" name="Cl3" type="cutArc" my="1.4"/>

# __type__ = 'cutSpline'
# <point id="54" spline="53" mx="0.1" length="10" name="Cl1" type="cutSpline" my="0.2"/>

# __type__ = 'cutSplinePath'
# <point id="60" mx="0.1" splinePath="59" length="20" name="CI2" type="cutSplinePath" my="0.2"/>

####################################################################################################

class EndLinePoint(PointLinePropertiesMixin, BasePointMixin, LengthAngleMixin, XmlObjectAdaptator):

    # <point id="2" basePoint="1" typeLine="hair" mx="0.1" length="10" name="X"
    # lineColor="blue" type="endLine" angle="360" my="0.25"/>

    __type__ = 'endLine'
    __operation__ = SketchOperation.EndLinePoint

####################################################################################################

class HeightPoint(PointLinePropertiesMixin, BasePointMixin, Line1Mixin, XmlObjectAdaptator):

    # <point id="18" basePoint="7" typeLine="hair" mx="0.1" p2Line="14" name="P" p1Line="2"
    # lineColor="mediumseagreen" type="height" my="0.2"/>

    __type__ = 'height'
    # __operation__ = SketchOperation.HeightPoint

####################################################################################################

class LineIntersectPoint(PointMixin, Line12Mixin, XmlObjectAdaptator):

    # <point id="17" mx="0.1" p1Line2="2" p1Line1="1" name="I" type="lineIntersect" my="0.2"
    # p2Line1="12" p2Line2="14"/>

    __type__ = 'lineIntersect'
    __operation__ = SketchOperation.LineIntersectPoint

####################################################################################################

class LineIntersectAxisPoint(PointLinePropertiesMixin, BasePointMixin, Line1Mixin, AngleMixin, XmlObjectAdaptator):

    # <point id="20" basePoint="14" typeLine="hair" mx="0.4" p2Line="1" name="AxAn" p1Line="5"
    # lineColor="goldenrod" type="lineIntersectAxis" angle="150" my="-1.8"/>

    __type__ = 'lineIntersectAxis'
    # __operation__ = SketchOperation.LineIntersectAxisPoint

####################################################################################################

class NormalPoint(PointLinePropertiesMixin, FirstSecondPointMixin, LengthAngleMixin, XmlObjectAdaptator):

    # <point id="26" firstPoint="25" typeLine="hair" mx="0.1" secondPoint="24" length="5"
    # name="Ct" lineColor="blue" type="normal" angle="0" my="0.1"/>

    __type__ = 'normal'
    __operation__ = SketchOperation.NormalPoint

####################################################################################################

# __type__ = 'pointFromArcAndTangent'
# <point id="84" tangent="83" mx="-1.3" crossPoint="1" arc="77" name="Ctan" type="pointFromArcAndTangent" my="1.7"/>

# __type__ = 'pointFromCircleAndTangent'
# <point id="81" tangent="80" mx="-2.9" cRadius="3" cCenter="71" crossPoint="1" name="Cp1" type="pointFromCircleAndTangent" my="-2.7"/>

####################################################################################################

class PointOfContact(PointMixin, FirstSecondPointMixin, CenterRadiusMixin, XmlObjectAdaptator):

    # <point id="19" radius="Line_A_M*3/2" center="4" firstPoint="1" mx="0.1" secondPoint="5" name="R" type="pointOfContact" my="0.2"/>

    # Fixme: name
    __type__ = 'pointOfContact'
    __operation__ = SketchOperation.PointOfContact

####################################################################################################

class PointOfIntersection(PointMixin, FirstSecondPointMixin, XmlObjectAdaptator):

    # <point id="14" firstPoint="2" mx="0.1" secondPoint="5" name="XY" type="pointOfIntersection" my="0.2"/>

    __type__ = 'pointOfIntersection'
    __operation__ = SketchOperation.PointOfIntersection

####################################################################################################

# __type__ = 'pointOfIntersectionArcs'
# <point id="78" firstArc="72" mx="-1.3" secondArc="77" crossPoint="1" name="Ci2" type="pointOfIntersectionArcs" my="2."/>

# __type__ = 'pointOfIntersectionCircles'
# <point id="79" c1Center="71" mx="0.1" crossPoint="1" c1Radius="15" name="Ci3" c2Radius="18"
# type="pointOfIntersectionCircles" my="0.2" c2Center="76"/>

# __type__ = 'pointOfIntersectionCurves'
# <point id="67" mx="0.9" curve1="59" vCrossPoint="1" curve2="66" hCrossPoint="1" name="Ci1"
# type="pointOfIntersectionCurves" my="-3.8"/>

####################################################################################################

class ShoulderPoint(PointLinePropertiesMixin, Line1Mixin, LengthMixin, XmlObjectAdaptator):

    # <point id="21" typeLine="hair" mx="0.7" p2Line="14" length="Line_X_XY*2" pShoulder="20" name="Sh"
    # p1Line="5" lineColor="lightsalmon" type="shoulder" my="-1.3"/>

    __type__ = 'shoulder'
    # __operation__ = SketchOperation.ShoulderPoint
    __attributes__ = (
        IntAttribute('shoulder_point', 'pShoulder'),
    )

####################################################################################################

class SinglePoint(PointMixin, XyMixin, XmlObjectAdaptator):

    # <point id="1" mx="0.1" x="0.79375" y="1.05833" name="A" type="single" my="0.2"/>

    __type__ = 'single'
    __operation__ = SketchOperation.SinglePoint

####################################################################################################

# __type__ = 'triangle'
# <point id="28" axisP2="25" axisP1="24" firstPoint="27" mx="0.8" secondPoint="26" name="T1"
# type="triangle" my="1.4"/>

# __type__ = 'trueDarts'
# <point id="44" mx2="-3.9" baseLineP2="39" baseLineP1="38" mx1="0.2" dartP3="42" name1="Td1"
# dartP2="41" point2="46" point1="45" name2="Td2" my2="-0.1" type="trueDarts" my1="-2.5"
# dartP1="43"/>

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
        'pointOfContact': PointOfContact,
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

class Line(CalculationMixin, LinePropertiesMixin, FirstSecondPointMixin, XmlObjectAdaptator):

    # <line id="47" firstPoint="38" typeLine="hair" secondPoint="45" lineColor="blue"/>

    __tag__ = 'line'
    __operation__ = SketchOperation.Line

    ##############################################

    def to_operation(self, sketch):
        return self.call_operation_function(sketch, self.to_dict()) # exclude=('id')

    ##############################################

    @classmethod
    def from_operation(cls, operation):
        kwargs = cls.get_dict(operation)
        return cls(**kwargs)

####################################################################################################

class SplineMixin(CalculationTypeMixin):
    __tag__ = 'spline'

####################################################################################################

class SimpleInteractiveSpline(SplineMixin, XmlObjectAdaptator):

    # <spline id="53" angle2="138.403" length2="14.0301" angle1="329.987" length1="18.2062"
    # point4="52" type="simpleInteractive" point1="51" color="blue"/>

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
    __operation__ = SketchOperation.SimpleInteractiveSpline

    ##############################################

    def to_operation(self, sketch):
        return self.call_operation_function(sketch, self.to_dict()) # exclude=('id')

    ##############################################

    @classmethod
    def from_operation(cls, operation):
        kwargs = cls.get_dict(operation)
        return cls(**kwargs)

####################################################################################################

# <spline id="57" duplicate="1" point4="52" point2="55" point3="56" type="cubicBezier" point1="51" color="goldenrod"/>

# <spline id="66" type="cubicBezierPath" color="deepskyblue">
#     <pathPoint pSpline="51"/>
#     <pathPoint pSpline="52"/>
#     <pathPoint pSpline="58"/>
#     <pathPoint pSpline="61"/>
#     <pathPoint pSpline="63"/>
#     <pathPoint pSpline="64"/>
#     <pathPoint pSpline="65"/>
# </spline>

# <spline id="59" type="pathInteractive" color="violet">
#     <pathPoint angle2="333.352" length2="25.9685" length1="0" angle1="153.352" pSpline="51"/>
#     <pathPoint angle2="82.712" length2="15.9887" length1="9.36267" angle1="262.712" pSpline="52"/>
#     <pathPoint angle2="254.923" length2="1.78344" length1="7.70133" angle1="74.9232" pSpline="58"/>
# </spline>

####################################################################################################

class Spline:

    # We cannot use a metaclass to auto-register due to XmlObjectAdaptator (right ?)
    __TYPES__ = {
        'cubicBezier': None,
        'cubicBezierPath': None,
        'pathInteractive': None,
        'simpleInteractive': SimpleInteractiveSpline,
    }

####################################################################################################

# <arc id="86" radius="10" center="83" angle1="45" length="30" type="arcWithLength" color="black"/>
# <arc id="72" radius="10" angle2="-30" center="71" angle1="30" type="simple" color="black"/>
# __ARC_TYPE__ = (
#     'arcWithLength',
#     'simple',
#     )

# <elArc id="87" angle2="300" center="83" radius2="15" rotationAngle="60" radius1="10" angle1="30" type="simple" color="lime"/>
# __ELLIPSE_TYPE__ = (
#     'simple',
#     )

# <operation id="110" center="89" suffix="mir2" axisType="1" type="flippingByAxis">
#     <source>
#         <item idObject="88"/>
#     </source>
#     <destination>
#         <item idObject="111" mx="0.132292" my="0.264583"/>
#     </destination>
# </operation>

# <operation id="108" suffix="mir" p2Line="89" p1Line="88" type="flippingByLine">
#     <source>
#         <item idObject="90"/>
#     </source>
#     <destination>
#         <item idObject="109" mx="0.132292" my="0.264583"/>
#     </destination>
# </operation>

# <operation id="113" suffix="mov" length="15" type="moving" angle="160">
#     <source>
#         <item idObject="88"/>
#     </source>
#     <destination>
#         <item idObject="114" mx="-1.4973" my="1.56825"/>
#     </destination>
# </operation>

# <operation id="101" center="94" suffix="rot" type="rotation" angle="30">
#     <source>
#         <item idObject="88"/>
#     </source>
#     <destination>
#         <item idObject="102" mx="-0.193626" my="0.738642"/>
#     </destination>
# </operation>

# __OPERATION_TYPE__ = (
#     'flippingByAxis',
#     'flippingByLine',
#     'moving',
#     'rotation',
# )

####################################################################################################

class ModelingItemMixin:

    __attributes__ = (
        IntAttribute('id'),
        IntAttribute('object_id', 'idObject'),
        StringAttribute('type'),
        BoolAttribute('in_use', 'inUse'),
    )

###################################################################################################

class ModelingPoint(ModelingItemMixin, MxMyMixin, XmlObjectAdaptator):

    # <point id="108" idObject="66" inUse="true" mx="0.132292" type="modeling" my="0.264583"/>

    pass

####################################################################################################

class ModelingSpline(ModelingItemMixin, XmlObjectAdaptator):

    # <spline id="111" idObject="107" inUse="true" type="modelingSpline"/>

    pass

####################################################################################################

class Detail(MxMyMixin, XmlObjectAdaptator):

    # <detail id="118" version="2" forbidFlipping="false" width="1" united="false" mx="0"
    #  name="Devant" inLayout="true" seamAllowance="true" my="0">

    __attributes__ = (
        IntAttribute('id'),
        IntAttribute('version'),
        BoolAttribute('forbidFlipping'),
        IntAttribute('width'),
        BoolAttribute('united'),
        StringAttribute('name'),
        BoolAttribute('inLayout'),
        BoolAttribute('seamAllowance'),
    )

    ##############################################

    def __init__(self, modeling, *args, **kwargs):

        XmlObjectAdaptator.__init__(self, *args, **kwargs)
        self._modeling = modeling
        self._nodes = []

    ##############################################

    def append_node(self, node):
        self._nodes.append(node)

    ##############################################

    def iter_on_nodes(self):
        for node in self._nodes:
            yield node, self._modeling[node.object_id]

####################################################################################################

class VisibleRotationMixin:

    __attributes__ = (
        BoolAttribute('visible'),
        IntAttribute('rotation'),
    )

####################################################################################################

class HeightWidthMixin:

    __attributes__ = (
        IntAttribute('height'),
        IntAttribute('width'),
    )

####################################################################################################

class FontSizeMixin:

    __attributes__ = (
        IntAttribute('fontSize'),
    )

####################################################################################################

class DetailData(HeightWidthMixin, MxMyMixin, FontSizeMixin, VisibleRotationMixin, XmlObjectAdaptator):

    # <data letter="" width="0" mx="0" height="0" fontSize="0" visible="false" rotation="0" my="0"/>

    __attributes__ = (
        StringAttribute('letter'),
    )

####################################################################################################

class DetailPatternInfo(HeightWidthMixin, MxMyMixin, FontSizeMixin, VisibleRotationMixin, XmlObjectAdaptator):

    # <patternInfo width="0" mx="0" height="0" fontSize="0" visible="false" rotation="0" my="0"/>

    pass

####################################################################################################

class DetailGrainline(MxMyMixin, VisibleRotationMixin, XmlObjectAdaptator):

    # <grainline arrows="0" mx="0" length="0" visible="false" rotation="90" my="0"/>

    __attributes__ = (
        IntAttribute('arrows'),
        IntAttribute('length'),
    )

####################################################################################################

class DetailNode(XmlObjectAdaptator):

    # <node idObject="108" type="NodePoint"/>
    # <node idObject="120" reverse="1" type="NodeSpline"/>

    __attributes__ = (
        IntAttribute('object_id', 'idObject'),
        StringAttribute('type'),
        BoolAttribute('reverse'),
    )
