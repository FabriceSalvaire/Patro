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
import QtQuick.Layouts 1.11

import Patro 1.0

ApplicationWindow {
    id: application_window
    title: 'Patro'
    visible: true

    width: 1000
    height: 500

    property int zoom_step: 10

    Component.onCompleted: {
	console.info('ApplicationWindow.onCompleted')
	// application_window.showMaximized()
    }

    menuBar: MenuBar {
        Menu {
            title: qsTr('&File')
            Action { text: qsTr('&Open') }
            MenuSeparator { }
            Action {
		text: qsTr('&Quit')
		onTriggered: application_window.close()
	    }
        }
        Menu {
            title: qsTr('&Help')
            Action { text: qsTr('&About') }
        }
    }

    header: ToolBar {
        RowLayout {
            anchors.fill: parent
            ToolButton {
		icon.source: 'qrc:/icons/36x36/settings-overscan-black.png'
		onClicked: scene_view.fit_scene()
            }
            ToolButton {
		icon.source: 'qrc:/icons/36x36/zoom-in-black.png'
		onClicked: {
		    var zoom_factor = 1 + application_window.zoom_step/100
		    scene_view.zoom_at_center(scene_view.zoom*zoom_factor)
		}
            }
            ToolButton {
		icon.source: 'qrc:/icons/36x36/zoom-out-black.png'
		onClicked: {
		    var zoom_factor = 1 - application_window.zoom_step/100
		    scene_view.zoom_at_center(scene_view.zoom*zoom_factor)
		}
            }
	    Item {
		Layout.fillWidth: true
	    }
        }
    }

    footer: ToolBar {
        RowLayout {
            anchors.fill: parent
            Text {
		id: position_label
		text: ''
            }
        }
    }

    PaintedSceneItem {
	id: scene_view
	anchors.fill: parent
	scene: application.scene

	MouseArea {
	    id: scene_mouse_area
            anchors.fill: parent
	    hoverEnabled: true
	    acceptedButtons: Qt.LeftButton | Qt.MiddleButton | Qt.RightButton
	    // var point ???
	    property var mouse_start
	    Component.onCompleted: {
		mouse_start = null
	    }
	    // onClicked: {
	    // 	if (mouse.button == Qt.LeftButton) {
	    // 	    console.info('Mouse left', mouse.x, mouse.y)
	    // 	}
	    // }
	    onPressed: {
		if (mouse.button == Qt.LeftButton) {
		    // console.info('Mouse left', mouse.x, mouse.y)
		    var position = Qt.point(mouse.x, mouse.y)
                    scene_view.item_at(position)
                }
		else if (mouse.button == Qt.MiddleButton) {
		    // console.info('Mouse left', mouse.x, mouse.y)
		    mouse_start = Qt.point(mouse.x, mouse.y)
		}
	    }
	    onReleased: {
		mouse_start = null
	    }
	    onPositionChanged: {
		// console.info('onPositionChanged', mouse.button, mouse_start)
		if (mouse_start !== null) {
		    var dx = mouse.x - mouse_start.x
		    var dy = mouse.y - mouse_start.y
                    // - so as to have a natural pan
                    // pan at right using a mouse move at right
		    var dxy = Qt.point(dx, -dy)
		    console.info('pan', dxy)
		    // if (dx^2 + dy^2 > 100)
		    scene_view.pan(dxy)
		    mouse_start = Qt.point(mouse.x, mouse.y)
		} else {
		    position_label.text = scene_view.format_coordinate(Qt.point(mouse.x, mouse.y))
		}
	    }
    	    onWheel: {
    		var direction = wheel.angleDelta.y > 0
    		console.info('Mouse wheel', wheel.x, wheel.y, direction)
    		var zoom = scene_view.zoom
    		if (direction)
    	    	    zoom *= 2
    		else
    	    	    zoom /= 2
    		scene_view.zoom_at(Qt.point(wheel.x, wheel.y), zoom)
    	    }
	}
    }
}
