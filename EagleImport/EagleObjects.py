"""
Created on 31.01.2018

@author: christian
"""

import math

class EagleDrill(object):
    """
    Contains drill information (drill size and position).
    Inside of EagleDevice objects the drill position is relative to the device position.
    """

    def __init__(self, size, position):
        """
        Constructor

        :param float size: drill size in mm
        :param position: (x, y) coordinates
        :type position: tuple(float, float)
        """
        self.position = position[:]
        self.drillsize = size
        
    
    def __str__(self):
        """
        :returns: drill description
        :rtype: str
        """
        return "diameter {} at ({},{})".format(self.drillsize, *self.position)
        
        
        
class EagleLineMilling():
    """
    Contains line milling information (start and end position, curve)
    """
    
    def __init__(self, start, end, curve=0):
        """
        Constructor

        :param start: (x, y) start coordinates of the milling path
        :type start: tuple(float, float)
        :param end: (x, y) end coordinates of the milling path
        :type end: tuple(float, float)
        :param float curve: curvature of the line (opening angle of the arc in deg, positive for ccw)
        """
        self.start = start[:]
        self.end = end[:]
        self.curve = curve
        
    
    def __str__(self):
        """
        :returns: line milling description
        :rtype: str
        """
        return "({},{}) to ({},{}) C{}".format(*self.start, *self.end, self.curve)
    
    
    
class EagleCircleMilling(object):
    """
    Contains circle milling information (center and radius)
    """
    
    def __init__(self, radius, center):
        """
        Constructor

        :param float radius: Radius in mm
        :param center: (x, y) coordinates
        :type center: tuple(float, float)
        """
        self.radius = radius
        self.center = center[:]
        
        
    def __str__(self):
        """
        :returns: circle description
        :rtype: str
        """
        return "radius {} at ({},{})".format(self.radius, *self.center)
                 
                       

class EagleDeviceLibrary(object):
    """
    Contains dictionary of devices (packages)
    """
    
    def __init__(self, name):
        """
        Constructor

        :param str name: Library name
        """
        self.name = name
        self.devices = {}
        
    
    def __len__(self):
        """
        :returns: number of devices in the library
        :rtype: int
        """
        return len(self.devices)
        
        
    def addDevice(self, eagledev):
        """
        Add Eagle device to library

        :param EagleDevice eagldev: Object to append
        """
        self.devices[eagledev.name] = eagledev
        
        
    def append(self, eagledevlib):
        """
        Add Eagle device library entries to library

        :param EagleDeviceLibrary eagledevlib: Object to append
        """
        for name, dev in eagledevlib.devices.items():
            if name in self.devices.keys():
                # TODO: warn user
                pass
            self.devices[name] = dev
        
        
        
class EagleDevice(object):
    """
    Contains package information, especially EagleDrill objects.
    EagleDevice is meant as an abstract device entry for EagleDeviceLibraries,
    occurrences of the device are given by EagleDevicePosition objects.
    """
    
    def __init__(self, name):
        """
        Constructor

        :param str name:  Name of the device (package)
        """
        self.name = name
        self.drills = []
        
        
    def addDrill(self, size, position):
        """
        Add drill to Eagle device

        :param float size: (float) Drill size in mm
        :param position: (x, y) coordinates
        :type position: tuple(float, float)
        """
        eagledrill = EagleDrill(size, position)
        self.drills.append(eagledrill)
        
    
        
class EagleDevicePosition(object):
    """
    Links EagleDevice entries in an EagleLibrary to occurrences of the package
    on the board by specifying library and device name and position.
    """
    
    def __init__(self, library, device, position, rotation=0, mirrored=False):
        """
        Constructor

        :param str library: Name of the library containing the device (package)
        :param str device: containing the name of the device (package)
        :param position: (x, y) coordinates
        :type position: tuple(float, float)
        :param float rotation: rotation angle of the device in rad
        :param bool mirrored: device is mirrored
        """
        self.libraryName = library
        self.deviceName = device
        self.position = position[:]
        self.rotation = rotation
        self.mirrored = mirrored
        
        
    def __str__(self):
        """
        :returns: device description
        :rtype: str
        """
        return "{}:{} at ({},{})R{}".format(self.libraryName, self.deviceName, 
                                            *self.position, self.rotation * 180/math.pi)