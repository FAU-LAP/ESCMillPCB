.. _known_bugs:

Known Bugs
==========

General
-------

* Laser crosshair is sometimes activated again after each jogging step. This is most probably
  due to a sync error of the interface and the laser crosshair state.


TinyG
-----

* Sometimes TinyG crashes on intialization (usually scrambled "{err:'c}" ) message. 
  The reason for this behavior is not clear, may be some race condition or some problem
  with not cleared io buffers. Maybe a firmware update of the TinyG board could help, if
  it is not a software error in ESCMillPCB.

* Sometimes scrambled "{err:'c}" error messages appear during operation.
  Similar to the bug above, the reason for this behavior is not clear.

* Problems with the laser crosshair: Laser crosshair should be on, but turns off after
  every movement step. Can lead to communication error (timeout).


Fixed
-----

Please add fixed bugs together with version information here.

1.3 Build 021
^^^^^^^^^^^^^

* Fixed TinyGCycleControl dialog not showing correctly/closing again directly.

1.3 Build 016
^^^^^^^^^^^^^

* Fixed bug in path optimization for holes.

* Fixed bug in fetching TinyG machine parameters.
