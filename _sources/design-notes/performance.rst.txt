.. include:: /abbreviation.txt

.. _design-note-performance-page:

==============
 Performances
==============

SVG Import
----------

For the complex dress pattern "Veravenus" of the file
:file:`veravenus-little-bias-dress.pattern-a0.svg` made of 270 SVG paths and 1051 segments, the
parsing and rendering time is of the order of one seconde ( cf. following log ).  In comparison,
Inkscape launched in parallel using a shell script, takes a little more times to start and open this
file.  Of course the comparison is not perfect since Inkscape is a heavier software to load, but it
shows a full Python implementation ( excepted the work done by Qt ) is competitive for a such file.

.. image:: /_static/patro-svg-import.png
   :alt: Patro SVG Import
   :width: 300px
   :height: 300px
   :align: center

.. code-block:: text

    > ./bin/patro --user-script examples/file-format/svg/test-svg-import.py

    ... :mm:ss,sss

    ... :11:26,528 - __main__.<module> - INFO - Started Patro
    ... :11:27,111 - Patro.QtApplication.QmlApplication.Application._message_handler - INFO - main.qml onCompleted
    ... :11:27,113 - Patro.QtApplication.QmlApplication.Application._post_init - INFO - post init

    ... :11:27,113 - Patro.QtApplication.QmlApplication.Application.execute_user_script - INFO - Execute user script:
    ...     patro/examples/file-format/svg/test-svg-import.py
    ... :11:27,361 - builtins.SceneImporter.__init__ - INFO - Number of SVG item: 270
    ... :11:27,361 - builtins.SceneImporter.__init__ - INFO - Number of scene item: 1051
    ... :11:27,361 - Patro.QtApplication.QmlApplication.QmlApplication.scene - INFO - set scene
    ... :11:27,362 - Patro.GraphicEngine.Painter.QtPainter.QtQuickPaintedSceneItem.scene - INFO - set scene
    ... :11:27,362 - Patro.QtApplication.QmlApplication.Application.execute_user_script - INFO - User script done

    ... :11:27,387 - Patro.GraphicEngine.Painter.QtPainter.QtQuickPaintedSceneItem.paint - INFO - Start painting
    ... :11:27,530 - Patro.GraphicEngine.Painter.QtPainter.QtQuickPaintedSceneItem.paint - INFO - Paint done
