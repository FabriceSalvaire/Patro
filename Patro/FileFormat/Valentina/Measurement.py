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

####################################################################################################

import logging

from Patro.Common.Xml.Objectivity import StringAttribute, XmlObjectAdaptator
from Patro.Common.Xml.XmlFile import XmlFileMixin
from Patro.Measurement.ValentinaMeasurement import ValentinaMeasurements
from Patro.Measurement.PersonalData import Gender

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

# <?xml version='1.0' encoding='UTF-8'?>
# <vit>
#     <!--Measurements created with Valentina (http://www.valentina-project.org/).-->
#     <version>0.3.3</version>
#     <read-only>false</read-only>
#     <notes/>
#     <unit>cm</unit>
#     <pm_system>998</pm_system>
#     <personal>
#         <family-name>..</family-name>
#         <given-name>...</given-name>
#         <birth-date>...</birth-date>
#         <gender>...</gender>
#         <email/>
#     </personal>
#     <body-measurements>
#         <m value="46" name="height_knee"/>
#     </body-measurements>
# </vit>

####################################################################################################

class XmlMeasurement(XmlObjectAdaptator):

    __tag__ = 'm'
    __attributes__ = (
        StringAttribute('name'),
        StringAttribute('value'),
        StringAttribute('full_name', default=''),
        StringAttribute('description', default=''),
    )

####################################################################################################

class VitFileInternal(XmlFileMixin):

    _logger = _module_logger.getChild('VitFile')

    ##############################################

    def __init__(self, path):

        super().__init__(path)
        self.measurements = ValentinaMeasurements()
        self.read()

    ##############################################

    def read(self):

        self._logger.info('Load measurements from ' + str(self._path))

        tree = self.parse()

        measurements = self.measurements

        version = self.get_xpath_element(tree, 'version').text
        # self.read_only = self.get_xpath_element(tree, 'read-only').text
        # self.notes = self.get_xpath_element(tree, 'notes').text
        self.unit = self.get_xpath_element(tree, 'unit').text
        self.pattern_making_system = self.get_xpath_element(tree, 'pm_system').text

        personal = measurements.personal
        personal_element = self.get_xpath_element(tree, 'personal')
        # replace last_name first_name
        personal.customer = self.get_xpath_element(personal_element, 'customer').text
        # personal.last_name = self.get_xpath_element(personal_element, 'family-name').text
        # personal.first_name = self.get_xpath_element(personal_element, 'given-name').text
        personal.birth_date = self.get_xpath_element(personal_element, 'birth-date').text
        personal.gender = Gender[self.get_xpath_element(personal_element, 'gender').text.upper()]
        personal.email = self.get_xpath_element(personal_element, 'email').text

        elements = self.get_xpath_element(tree, 'body-measurements')
        for element in elements:
             if element.tag == XmlMeasurement.__tag__:
                 xml_measurement = XmlMeasurement(element)
                 measurements.add(**xml_measurement.to_dict())
             else:
                 raise NotImplementedError

####################################################################################################

class VitFile:

    ##############################################

    def __init__(self, path):
        self._internal = VitFileInternal(path)

    ##############################################

    @property
    def path(self):
        return self._internal.path

    @property
    def measurements(self):
        return self._internal.measurements
