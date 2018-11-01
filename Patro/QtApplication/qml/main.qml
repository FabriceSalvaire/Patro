/***************************************************************************************************
 *
 *  Patro - A Python library to make patterns for fashion design
 *  Copyright (C) 2017 Fabrice Salvaire
 *
 *  This program is free software: you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation, either version 3 of the License, or
 *  (at your option) any later version.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License
 *  along with this program.  If not, see <http://www.gnu.org/licenses/>.
 *
 ***************************************************************************************************/

import QtQuick 2.11
import QtQuick.Controls 2.4

import Patro 1.0

ApplicationWindow {
    id: application_window
    title: 'Patro'
    visible: true

    width: 1000
    height: 500

    Component.onCompleted: {
	console.info('ApplicationWindow.onCompleted')
	// application_window.showMaximized()
    }

    PaintedSceneItem {
	id: scene_view
	anchors.fill: parent
	scene: application.scene

	MouseArea {
            anchors.fill: parent
	    acceptedButtons: Qt.LeftButton | Qt.RightButton
	    onClicked: {
		if (mouse.button == Qt.LeftButton)
		    console.info('Mouse left', mouse.x, mouse.y)
	    }
	    onWheel: {
		var direction = wheel.angleDelta.y > 0
		console.info('Mouse wheel', wheel.x, wheel.y, direction)
		if (direction)
		    scene_view.zoom *= 2
		else
		    scene_view.zoom /= 2
	    }
	}
    }
}
