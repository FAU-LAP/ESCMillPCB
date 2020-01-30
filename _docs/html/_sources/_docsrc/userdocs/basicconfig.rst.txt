.. _software-settings:

Software Settings
===================

The following section describes the available settings of the settings dialog.
All software settings are stored Windows-user specific in *%localappdata%\\ESCMillPCB\\settings.json*.
A settings file with the current default settings is included in the executable directory called
*[DATE]_default_settings.json*.

.. _general-settings:

General
-------

General software configuration.

========================================= ===================================================================================
Parameter                                 Description
========================================= ===================================================================================
Connect to machine on startup             If activated, the configured machine is initalized on software startup   
Apply machine settings on startup         If activated and the configured machine is initialized, the machine settings
                                          are applied to the machine on software startup  
Logfile threshold level                   Minimal importance level of log entries which are written to the log file
Logfiles to keep                          A new logfile is generated every day the software is run. This number denotes the
                                          amount of old logfiles to keep.
Log window threshold level                Minimal importance level of log entries which are shown in the log window.
========================================= ===================================================================================


.. _optimizer-settings:

Optimizers
----------

Optimizers are applied to the board objects to optimize the machining in different manners.

Hole order optimization
^^^^^^^^^^^^^^^^^^^^^^^

This optimizer changes the order in which the holes are drilled such that the distance of the
overall path is minimized.

=========== ===================================================================================
Parameter   Description
=========== ===================================================================================
Active      (De-)activates the optimizer
Algorithm   Algorithm for path distance optimization. 2opt (default) gives better results, 
            the simple greedy algorithm is slightly faster.
Iterations  Number of 2opt steps (starting from random distribution of holes) of which the best
            result is used. This is not applicable to the greedy algorithm.
=========== ===================================================================================			

Combine adjecent millings
^^^^^^^^^^^^^^^^^^^^^^^^^

This optimizer concatenates milling paths if the end of the first path is at the same position
as the start of the next path.

=========== ===================================================================================
Parameter   Description
=========== ===================================================================================
Active      (De-)activates the optimizer
=========== ===================================================================================	

Add breakouts to millings
^^^^^^^^^^^^^^^^^^^^^^^^^

This optimizer adds breakout bars (small leftover board bridges) to cut-outs, i.e. closed milling
paths. The cut-out parts of the board can then be broken out of the board after the milling process.
Combining adjecent millings (see above) is mandatory for this step, as otherwise closed milling paths
are not detected correctly.

========================================= ===================================================================================
Parameter                                 Description
========================================= ===================================================================================
Active                                    (De-)activates the optimizer
Breakout distance (mm)                    Distance in mm between breakout bars
Breakout size (mm)                        Size of the breakout bars in mm (note that drill size is not accounted for!)
Minimal number of breakouts per cut-out   Minimal number of breakout bars per cut-out. If the cut-out path is too short,
                                          the breakout distance is adjusted such that the breakouts are evenly spread.
Minimal cut-out length for breakouts (mm) Minimal milling path length (in mm) such that breakouts are inserted
========================================= ===================================================================================

Milling order optimization
^^^^^^^^^^^^^^^^^^^^^^^^^^

This optimizer changes the order in which the millings are milled such that the distance of the
overall path is minimized.

=========== ===================================================================================
Parameter   Description
=========== ===================================================================================
Active      (De-)activates the optimizer
=========== ===================================================================================	


.. _machine-settings:

Machine Settings
================

.. _basic-machine-setup:

Basic machine settings
----------------------

Basic machine parameter configuration.

========================================= ===================================================================================
Parameter                                 Description
========================================= ===================================================================================
X&Y axis jogging speed (mm/min)           Maximal jogging speed for X and Y axis (in mm/min)
Milling speed (mm/min)                    Maximal movement speed during milling operations for X and Y axis (in mm/min)
Z axis infeed depth (mm)                  Infeed depth for milling/drilling in mm measured from the Z axis working position
                                          (see also :ref:`coordinate-setup`)
Z axis jogging speed (mm/min)             Maximal jogging speed for Z axis (in mm/min)
Z axis infeed speed (mm/min)              Maximal Z axis speed for infeed/outfeed (in mm/min)
Z axis outfeed speed (mm/min)             Maximal Z axis speed for outfeed (in mm/min)
Tool diameter (mm)                        Diameter of the drill/milling tool (in mm)
Laser sight x offset                      Offset of the X coordinate of the laser sight to the machine position (in mm)
Laser sight y offset                      Offset of the X coordinate of the laser sight to the machine position (in mm)
Coordinate update interval (ms)           Machine position poll interval (in ms)
========================================= ===================================================================================

.. warning::
   
   Currently the tool diameter is only used for drilling (milling holes larger than the tool).
   For millings the tool diameter is ignored and the tool is guided along the milling path.
   This is also the case for breakouts!


.. _advanced-machine-settings:

Advanced machine settings
-------------------------

Machine communication settings and machine specific settings.

Machine: Type of the connected machine

Communication settings and machine parameters are machine specific and documented in the machine documentation:

* :ref:`tinyg`