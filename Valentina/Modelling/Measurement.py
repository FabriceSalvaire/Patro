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

from .Evaluator import Evaluator, NamedExpression

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

class Measurements:

    _logger = _module_logger.getChild('Measurements')

    ##############################################

    def __init__(self):

        self._measures = []
        self._measure_dict = {}
        self._evaluator = Evaluator(self)

    ##############################################

    @property
    def evaluator(self):
        return self._evaluator

    ##############################################

    def __iter__(self):
        return iter(self._measures)

    ##############################################

    def __getitem__(self, name):
        return self._measure_dict[name]

    ##############################################

    def add(self, *args, **kgwars):

        measurement = Measurement(self, *args, **kgwars)
        self._measures.append(measurement)
        self._measure_dict[measurement.name] = measurement
        if measurement.is_custom():
            self._measure_dict[measurement.valentina_name] = measurement

    ##############################################

    def eval(self):

        # Fixme: compute a graph from the ast to evaluate
        self._logger.info('Eval all measurements')
        for measure in self:
            measure.eval()

    ##############################################

    def dump(self):

        print("\nDump measurements:")
        for measure in self:
            print(measure.name, '=', measure.expression)
            print('  =', measure.value)

####################################################################################################

class Measurement(NamedExpression):

    ##############################################

    def __init__(self, measurements, name, value, full_name='', description=''):

        self._valentina_name = name

        if self.is_custom():
            name = '__custom__' + name[1:]

        NamedExpression.__init__(self, name, value, evaluator=measurements.evaluator)

        self._full_name = full_name
        self._description = description

    ##############################################

    @property
    def valentina_name(self):
        return self._valentina_name

    @property
    def full_name(self):
        return self._full_name

    @property
    def description(self):
        return self._description

    ##############################################

    def is_custom(self):
        return self._valentina_name.startswith('@')

    ##############################################

    def eval(self):

        super(Measurement, self).eval()
        self._evaluator._update_cache(self)

####################################################################################################

class VitParser:

    _logger = _module_logger.getChild('VitParser')

    ##############################################

    def parse(self, val_path):

        self._logger.info('Load measurements from ' + val_path)

        with open(val_path, 'rb') as f:
            source = f.read()

        tree = etree.fromstring(source)

        measurements = Measurements()

        elements = self._get_xpath_element(tree, 'body-measurements')
        for element in elements:
             if element.tag == 'm':
                 attrs = element.attrib
                 measurements.add(attrs['name'], attrs['value'],
                                  attrs.get('full_name', ''),
                                  attrs.get('description', ''))
             else:
                 raise NotImplementedError

        measurements.eval()

        return measurements

    ##############################################

    def _get_xpath_element(self, root, path):

        return root.xpath(path)[0]
