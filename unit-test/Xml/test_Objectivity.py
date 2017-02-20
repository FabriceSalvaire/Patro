####################################################################################################
#
# PyValentina - A Python implementation of Valentina Pattern Drafting Software
# Copyright (C) 2017 Salvaire Fabrice
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

import unittest

####################################################################################################

import Valentina.Logging.Basic
from Valentina.Xml.Objectivity import *

####################################################################################################

class FakeXmlElement:

    ##############################################

    def __init__(self, **kwargs):

        self.attrib = kwargs

    ##############################################

    def __getattr__(self, name):
        return self.attrib[name]

####################################################################################################

class MyObject(XmlObjectAdaptator):

    __tag__ = 'myobject'
    __attributes__ = (
        IntAttribute('int_attribute', 'xint_attribute'),
        FloatAttribute('float_attribute', 'xfloat_attribute'),
        StringAttribute('string_attribute', 'xstring_attribute'),
    )

####################################################################################################

class MyObjectMixin1:

    __tag__ = 'myobject'
    __attributes__ = (
        IntAttribute('int_attribute'),
    )

####################################################################################################

class MyObjectMixin2:

    __attributes__ = (
        IntAttribute('int_attribute2'),
    )

####################################################################################################

class MyObjectMixin3(MyObjectMixin2):

    __attributes__ = (
        FloatAttribute('float_attribute'),
    )

####################################################################################################

class MyComposedObject(XmlObjectAdaptator, MyObjectMixin1, MyObjectMixin3):

    __attributes__ = (
        StringAttribute('string_attribute'),
    )

####################################################################################################

class TestObjectivity(unittest.TestCase):

    ##############################################

    def test(self):

        xml_element1 = FakeXmlElement(xint_attribute='1',
                                      xfloat_attribute='1.0',
                                      xstring_attribute='string1')
        object1 = MyObject(xml_element1)

        xml_element2 = FakeXmlElement(xint_attribute='2',
                                      xfloat_attribute='2.0',
                                      xstring_attribute='string2')
        object2 = MyObject(xml_element2)

        self.assertEqual(object1.int_attribute, int(xml_element1.xint_attribute))
        self.assertEqual(object1.float_attribute, float(xml_element1.xfloat_attribute))
        self.assertEqual(object1.string_attribute, xml_element1.xstring_attribute)

        self.assertEqual(object2.int_attribute, int(xml_element2.xint_attribute))
        self.assertEqual(object2.float_attribute, float(xml_element2.xfloat_attribute))
        self.assertEqual(object2.string_attribute, xml_element2.xstring_attribute)

        object1.int_attribute = int_attribute = 10
        self.assertEqual(object1.int_attribute, int_attribute)
        object2.int_attribute = int_attribute = 20
        self.assertEqual(object2.int_attribute, int_attribute)

        int_attribute = 3
        object3 = MyObject(int_attribute=int_attribute)
        self.assertEqual(object3.int_attribute, int_attribute)

        print(object1.to_xml_string())

        int_attribute = 1
        int_attribute2 = 2
        float_attribute = 1.0
        string_attribute = 'string'
        composed_object = MyComposedObject(int_attribute=int_attribute,
                                           int_attribute2=int_attribute2,
                                           float_attribute=float_attribute,
                                           string_attribute=string_attribute,
        )
        self.assertEqual(composed_object.int_attribute, int_attribute)
        self.assertEqual(composed_object.int_attribute2, int_attribute2)
        self.assertEqual(composed_object.float_attribute, float_attribute)
        self.assertEqual(composed_object.string_attribute, string_attribute)

####################################################################################################

if __name__ == '__main__':

    unittest.main()
