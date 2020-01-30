User Guide
==========


Overview
--------


Main menu
---------

+--------------------+-----------------------------+--------------------------------------------------------------------------------------+
| **Menu**           | **Menu entry**              | **Description**                                                                      |
+====================+=============================+======================================================================================+
| **File**           | Open eagle board...         | Import an EAGLE board file, see :ref:`import-eagle-board`                            |
|                    +-----------------------------+--------------------------------------------------------------------------------------+
|                    | Quit                        | Closes the program                                                                   |
+--------------------+-----------------------------+--------------------------------------------------------------------------------------+
| **Tools**          | (Re-)Initialize machine     | Closes and reopens the connection to the machine, see also :ref:`connecting-machine` |
|                    +-----------------------------+--------------------------------------------------------------------------------------+
|                    | (Re-)Apply machine settings | Applies the machine configuration to the machine, see also :ref:`connecting-machine` |
|                    +-----------------------------+--------------------------------------------------------------------------------------+
|                    | Run homing cycle            | Initializes a machine homing cycle                                                   |
|                    +-----------------------------+--------------------------------------------------------------------------------------+
|                    | Close machine connection    | Closes the connection to the machine                                                 |
|                    +-----------------------------+--------------------------------------------------------------------------------------+
|                    | Settings...                 | Opens the settings dialog                                                            |
+--------------------+-----------------------------+--------------------------------------------------------------------------------------+
| **Help**           | Documentation               | Opens the index of this documentation                                                |
|                    +-----------------------------+--------------------------------------------------------------------------------------+
|                    | About...                    | Information about the software including software version                            |
|                    +-----------------------------+--------------------------------------------------------------------------------------+
|                    | About Qt...                 | Shows licence and version iformation about the used Qt UI lbrary                     |
+--------------------+-----------------------------+--------------------------------------------------------------------------------------+

Additionally, machines can add machine specific menus, see the machine's documentation.


.. _connecting-machine:

Connecting to the machine
-------------------------

If activated in the settings (see :ref:`general-settings`), the connection the the machine is established on program start
and machine settings are applied. Otherwise, machine initialization/appliying the settings can be done via the
corresponding menu item (Tools menu). After initialization, it may be necessary to first apply the machine settings.
Also a homing cycle has to be performed in order to adjust the machine's coordinate system. Machine cycles can only
be started if the machine is homed.

Connecting to the machine requires that the machine communication is set up correctly (see :ref:`advanced-machine-settings`)


.. _import-eagle-board:

Importing EAGLE board files
---------------------------

EAGLE \*.brd files can be imported via the File menu and is compatible with at least EAGLE version 7.7.0 (other versions are not tested).
The following objects are imported from the EAGLE file:

* Holes/drills (including holes from packages, manually placed holes, vias)
* Lines and curves in the **Milling** layer (layer 46)

.. note::

   Holes larger then the tool diameter (see :ref:`basic-machine-setup`) are milled to the specified size. 
   In contrast, the milling paths are milled on the defined lines/curves without accounting for the tool diameter.
   The width of the lines has no influence on milling.
   
After the board is loaded, the board layout may be adjusted in the following way:

* If active (see :ref:`coordinate-setup`), the whole board is mirrored to account for the side on which the machine operates.
* Active optimizers are applied to the board (see :ref:`optimizer-settings`).

The board is then displayed in the workpiece widget.


.. workpiece-widget:

The workpiece widget
--------------------

The workpiece widget is placed in the central part of the main window. It shows a preview of the machine cycle
by displaying all holes and millings and the jog path in between.

* Holes are displayed as a crosshair, the circle has the same diameter as the hole.

* The jogging paths between the holes are displayed as red lines.

* Millings are displayed as solid black lines. The infeed point is displayed as a triangle pointing down,
  the outfeed point as a triangle pointing upwards. Jogging paths between the millings are displayed as blue lines.

Additionally, the workpiece widget can be used to drive the machine to a specific hole by right-clicking the
hole and selecting "Move to position" from the context menu. For this to work, the machine coordinate system
has to be adjusted to the workpiece first, see :ref:`coordinate-setup`. If the laser crosshair is active,
the laser crosshair is moved to the position instead of the tool.

.. warning::

   Due to the machine axis limits, the laser crosshair can only be centered to holes in the **lower** half
   of the board! If you try to "Move to position" to a hole in the upper half of the board while the
   laser crosshair is active, you will most likely hit the soft limit (or even the hard limit switch)
   of the y axis.

Navigation controls:

* Use the mouse wheel to zoom (alternatively press the right mouse button and move the mouse up/down for fast
  zooming and left/right for slow zooming)
  
* Press the left mouse button (or the third mouse button) and move the mouse to move the view.

* Click on the small A in the lower left corner to autoscale.

* Autoscale and adjustment of the axes can also be performed from the context menu.


.. _machine-control:

Controlling the machine
-----------------------

The machine control widget is located in the Control tab in the right part of the main window.
This widget offers several control groups:

* **Current Position**: Shows the current x,y,z position in absolute coordinates (relative to the homing switches)
  and board coordinates (relative to the board origin) respectively. Note that the latter is valid only after
  setting up the coordinate system.
  
* **Jog**: Manually move the machine with the cursor buttons. The step size is defined with the radio buttons below
  the cursor buttons. If "Continuous" is set, movement is continuous as long as the cursor button is pressed.
  The spindle checkbox (de-)activates the spindle.
  
* **Go to**: Move the machine to a specific position. The position can be given in board coodinates, absolute coordinates
  or relative to the current position, depending on the checked radio button. Additionally, the machine can be moved
  to the pre-defined (see :ref:`setup-widget`) default board origin or park position.
  
* **Calibration**: A homing cycle can be invoked from here. Also, the laser crosshair can be (de-)activated with the
  corresponding checkbox. "Board origin corrected" and "Board rotation corrected" checkboxes show, if the board origin
  and the reference coordinates are set (see :ref:`coordinate-setup`).


.. _coordinate-setup:

Setting up the coordinate system
--------------------------------

To adjust the workpiece coordinate system, a one or two step alignment process can be used:

#. Move the tool or the laser crosshair (if active) to a hole. It is recommended to use a hole near
   the center of the board. Make sure it is centered over the hole as precise as possible.
   In the workpiece widget, right click the corresponding hole and select
   "Set as origin" from the context menu. This will correct the coordinate offset.
   
#. (optional) Right-click on a hole e.g. near the lower right or left corner and select "Move to position".
   Check if the tool/the laser crosshair is correctly centered on this hole. If not, center the tool/laser crosshair
   over the hole. Then right-click the hole and select "Set as reference" from the context menu.
   This will perform an angle correction.
   
#. Use another hole (right-click, "Move to position") to check the offset and angle corrections.

.. note::

   If the laser crosshair is active, the laser position has to be used for setting up the coordinate system.
   The offset of the laser crosshair to the tool is automatically taken into account (if set up correctly,
   see :ref:`basic-machine-setup`).


.. _setup-widget:

The setup widget
----------------

The setup widget is located in the Setup tab in the right part of the main window.
This widget offers several control groups:

* **Tasks**: Enable/disable drilling and milling.

* **Board Settings**: The board can be mirrored with the checkbox "Mirrored". Board outlines are indicated in the workpiece 
  widget if "Show Outlines" is checked. The board size is specified with the text boxes below.
  
* **Park Position**: Sets the park position of the machine. The park position should be chosen such that the board can
  easily be removed/inserted. It is given in absolute coordinates. The button "Go" moves the machine to the park position.
  To change the park position, insert new coordinates in the right text boxes (or use "Set to current" to insert the current
  position) and press "Apply" to confirm the new coordinates.
  
* **Default Board Origin**: Set the default board origin of the machine. The board origin should be near the center of the
  board. The Z-position plays a special role: it defines the working distance during the machine cycle. It should therefore
  be set to a safe but near distance to the board surface. It is changed in the same way as the park position.