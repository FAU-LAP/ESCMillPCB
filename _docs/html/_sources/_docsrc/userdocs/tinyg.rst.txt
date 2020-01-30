.. _tinyg:

TinyG
=====


General
-------

This section describes the usage and configuration of the TinyG controller from Synthetos (see `here <https://github.com/synthetos/TinyG/wiki>`_),
which is currently the only supported machine.

The following features are supported:

* X, Y, Z axes are supported, where X & Y axes are used for the board plane and the Z axis for in- and outfeed of the milling tool. 
  Driving the A axis is **not** supported.
  
* Limit switches can be freely configured for all four axes (X, Y, Z, A), but only X, Y, Z axes can be used for homing of the machine. 
  The A axis limit switch can be used for an emergency stop switch.
  
* The coolant signal output is used for enabling/disabling the laser crosshair.


Communication settings
----------------------

Basic parameters communication with the machine.

============== ===================================================================================
Parameter      Description
============== ===================================================================================
Com Port       Port identifier of the TinyG's virtual COM port
Baudrate       Baudrate used for communication (default: 115200)
Flow Control   Used type of flow control (recommended: XON/XOFF)
Timeout (s)    Timeout in seconds for queries (recommended: 10s)
============== ===================================================================================


Machine settings
----------------

Motor settings
^^^^^^^^^^^^^^

In the following table, *n* = 1, 2, 3 refers to the motor index.

========================================= ===================================================================================
Parameter                                 Description
========================================= ===================================================================================
Motor *n* axis                            Axis driven by motor *n* (X, Y, Z)
Motor *n* step angle (deg)                Rotation angle per full motor step of motor *n* (in degrees)
Motor *n* travel per revolution (mm)      Linear movement of the motor's axis per revolution (in mm)
Motor *n* microsteps                      Microsteps per full step of motor *n* (1, 2, 4, 8)
Motor *n* polarity                        Direction of motor rotation for movement in positive axis direction
Motor *n* power management                Condition under which the motor is powered (including active breaking)
========================================= ===================================================================================


.. _tinyg-axis-settings:

Axis settings
^^^^^^^^^^^^^

In the following table, *N* = X, Y, Z refers to the axis index.

========================================= ====================================================================================
Parameter                                 Description
========================================= ====================================================================================
*N* axis feed rate upper limit (mm/min)   Maximal jog speed in *N* direction (in mm/min)
*N* axis travel minimum (mm)              Minimal *N* axis position (for soft limits, in mm)
*N* axis travel maximum (mm)              Maximal *N* axis position (for soft limits, in mm)
*N* axis maximum jerk (mm/min^3)          Maximal *N* axis jerk (jerk = (d/dt)^3 x, in mm/min^3, **see warning below**)
*N* axis junction deviation (mm)          Theoretical radius for cornering control.
                                          Larger values yield faster cornering, but more corner jerk.
                                          (in mm, see also the `junction deviation wiki entry`_)
Junction acceleration (mm/min^2)          Global parameter affecting the cornering speed (in mm/min^2, see junction deviation)
Enable soft limits                        If enabled, minimum and maximum travel parameters are used for soft limit checking
========================================= ====================================================================================

.. _junction deviation wiki entry: https://github.com/synthetos/TinyG/wiki/TinyG-Configuration-for-Firmware-Version-0.97#xjd---junction-deviation

.. warning::

   The controller interpretes jerk values less than 1E6 in units of 1E6, e.g. a jerk value of 100 is interpreted as 1E8 mm/min^3.
 
Homing settings
^^^^^^^^^^^^^^^

These settings configure the homing cycle and also the limit switch roles. *N* = X, Y, Z refers to the axis index.

========================================= ===========================================================================================
Parameter                                 Description
========================================= ===========================================================================================
Switch type                               Global setting for the switch type (normally open, normally closed).
                                          Note that it is **not** possible to configure the switching behavior individually.
*N* minimum switch                        Role of the *N* axis minimum switch (disabled, homing, limit, homing & limit)
*N* maximum switch                        Role of the *N* axis maximum switch (disabled, homing, limit, homing & limit)
*N* axis homing search velocity (mm/min)  Maximal speed when searching the *N* axis homing switch.
*N* axis homing latch velocity (mm/min)   Speed with which the latching point of the homing switch is searched after it has been hit.
*N* axis homing jerk (mm/min^3)           Maximal jerk during homing (see jerk settings and warning in :ref:`tinyg-axis-settings`).
*N* axis homing backup (mm)               Distance to the switch in which the axis origin is set.
A axis maximum switch                     Role of the A axis minimum switch (disabled, limit).
A axis minimum switch                     Role of the A axis maximum switch (disabled, limit).
========================================= ===========================================================================================

General settings
^^^^^^^^^^^^^^^^

Miscellaneous settings which do not fit in the other categories.

========================================= ====================================================================================
Parameter                                 Description
========================================= ====================================================================================
Status report interval (ms)               Interval in which the controller sends status reports to the program (in ms).
                                          Status reports contain current machine position, cycle status, buffer status, etc.
========================================= ====================================================================================


.. tinyg-menu:

Machine specific menus and dialogs
----------------------------------

Com Testpanel
^^^^^^^^^^^^^

The communication testpanel can be used to send or query commands and responses to and from the controller.
Commands have to be given in JSON format (e.g. *{"gc":"m3"}* to enable the spindle), the only exceptions are feedhold (*!*),
resume (*~*) and stop (*%* or *!%*).

Reset
^^^^^

Performs a hardware reset. Normally the machine settings are persistent, so it usually is not necessary to reapply the machine
settings. The homing, however, is lost, so a new homing cycle is mandatory.

Clear
^^^^^

Clears the machines error/alarm state. Note that only soft alarms can be cleared (e.g. violating the soft limits), hard alarms
(e.g. hitting a limit switch) cannot be cleared and require a hardware reset.

TinyG Cycle Control Window
^^^^^^^^^^^^^^^^^^^^^^^^^^

This window is opened during the machining cycle and shows the cycle progress. It is also possible to pause or abort the cycle.

* **Command buffer**: GCode program executed during the cycle
* **Linebuffer**: Commands buffered by the controller
* **Planner Queue**: State of the controller's planner queue (motion buffer)
* **Progress**: Ratio of the already send commands to the overall command buffer length
