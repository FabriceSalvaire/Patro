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

__all__ = [
    'QmlApplication',
]

####################################################################################################

import argparse
import logging
import sys
from pathlib import Path

from PyQt5.QtCore import (
    pyqtProperty, pyqtSignal, QObject,
    Qt, QTimer, QUrl,
)
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import qmlRegisterType, qmlRegisterUncreatableType, QQmlApplicationEngine
from PyQt5.QtQuick import QQuickPaintedItem, QQuickView

from Patro.GraphicEngine.Painter.QtPainter import QtScene, QtQuickPaintedSceneItem

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class QmlApplication(QObject):

    _logger = _module_logger.getChild('QmlApplication')

    ##############################################

    def __init__(self, application):

        super().__init__()

        self._application = application
        self._scene = None

    ##############################################

    sceneChanged = pyqtSignal()

    @pyqtProperty(QtScene, notify=sceneChanged)
    def scene(self):
        return self._scene

    @scene.setter
    def scene(self, scene):
        if self._scene is not scene:
            print('QmlApplication set scene', scene)
            self._logger.info('set scene') # Fixme: don't print ???
            self._scene = scene
            self.sceneChanged.emit()

####################################################################################################

class PathAction(argparse.Action):

    ##############################################

    def __call__(self, parser, namespace, values, option_string=None):

        if values is not None:
            if isinstance(values, list):
                path = [Path(x) for x in values]
            else:
                path = Path(values)
        else:
            path = None
        setattr(namespace, self.dest, path)

####################################################################################################

class Application(QObject):

    instance = None

    _logger = _module_logger.getChild('Application')

    ##############################################

    # Fixme: Singleton

    @classmethod
    def create(cls, *args, **kwargs):

        if cls.instance is not None:
            raise NameError('Instance exists')

        cls.instance = cls(*args, **kwargs)
        return cls.instance

    ##############################################

    def __init__(self):

        super().__init__()

        self._parse_arguments()

        self._appplication = QGuiApplication(sys.argv)
        self._engine = QQmlApplicationEngine()
        self._qml_application = QmlApplication(self)

        self._scene = None

        # self._load_translation()
        self._register_qml_types()
        self._set_context_properties()
        self._load_qml_main()

        # self._run_before_event_loop()

        QTimer.singleShot(0, self._post_init)

        # self._view = QQuickView()
        # self._view.setResizeMode(QQuickView.SizeRootObjectToView)
        # self._view.setSource(qml_url)

    ##############################################

    @property
    def args(self):
        return self._args

    @property
    def qml_application(self):
        return self._qml_application

    ##############################################

    @classmethod
    def setup_gui_application(cls):

        # QGuiApplication.setApplicationName(APPLICATION_NAME)
        # QGuiApplication.setOrganizationName(ORGANISATION_NAME)
        QGuiApplication.setAttribute(Qt.AA_EnableHighDpiScaling)

    ##############################################

    def _parse_arguments(self):

        parser = argparse.ArgumentParser(
            description='Patro',
        )

        # parser.add_argument(
        #     '--version',
        #     action='store_true', default=False,
        #     help="show version and exit",
        # )

        parser.add_argument(
            '--user-script',
            action=PathAction,
            default=None,
            help='user script to execute',
        )

        parser.add_argument(
            '--user-script-args',
            default='',
            help="user script args (don't forget to quote)",
        )

        self._args = parser.parse_args()

    ##############################################

    # def _load_translationt(self):

    #     locale = QLocale()

    #     if m_translator.load(locale, '...', '.', ':/translations', '.qm'):
    #         m_application.installTranslator(m_translator)
    #     else:
    #         raise "No translator for locale" locale.name()

    ##############################################

    def _register_qml_types(self):

        qmlRegisterUncreatableType(QmlApplication, 'Patro', 1, 0, 'QmlApplication', 'Cannot create QmlApplication')
        qmlRegisterUncreatableType(QtScene, 'Patro', 1, 0, 'QtScene', 'Cannot create QtScene')

        qmlRegisterType(QtQuickPaintedSceneItem, 'Patro', 1, 0, 'PaintedSceneItem')

    ##############################################

    def _set_context_properties(self):

        context = self._engine.rootContext()
        context.setContextProperty('application', self._qml_application)

    ##############################################

    def _load_qml_main(self):

        # self._engine.addImportPath('qrc:///qml')

        qml_path = Path(__file__).parent.joinpath('qml', 'main.qml')
        qml_url = QUrl.fromLocalFile(str(qml_path))
        # QUrl('qrc:/qml/main.qml')
        self._engine.load(qml_url)

    ##############################################

    def exec_(self):

        # self._view.show()
        sys.exit(self._appplication.exec_())

    ##############################################

    def _post_init(self):

        # Fixme: ui refresh ???

        self._logger.info('post init')

        if self._args.user_script is not None:
            self.execute_user_script(self._args.user_script)

    ##############################################

    def execute_user_script(self, script_path):

        """Execute an user script provided by file *script_path* in a context where is defined a variable
        *application* that is a reference to the application instance.

        """

        script_path = Path(script_path).absolute()
        self._logger.info('Execute user script: {}'.format(script_path))
        try:
            source = open(script_path).read()
        except FileNotFoundError:
            self._logger.info('File {} not found'.format(script_path))
            sys.exit(1)
        bytecode = compile(source, script_path, 'exec')
        exec(bytecode, {'application':self})
        self._logger.info('User script done')

