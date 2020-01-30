"""
Created on 31.01.2018

@author: Christian Ott
"""

# setup logging
import logging
logger = logging.getLogger(__name__)

import math, copy
import xml.etree.ElementTree as et

from EagleImport import EagleObjects as eo


class EagleBrd(object):
    """
    Represents an Eagle board
    """

    def __init__(self):
        """
        Constructor
        """
        self.deviceLibraries = {}
        self.devicePositions = []
        self.holes = []
        self.vias = []
        self.lineMillings = []
        self.circleMillings = []
    
    
    def importBrd(self, filepath):
        """
        Import Eagle \*.brd XML file, the file contents will be added to the EagleBrd object

        :param str filepath: Absolute path to the brd file
        """
        logger.info("Parsing Eagle board file %s", filepath)
        xmltree = et.parse(filepath)
        if str.lower(xmltree.getroot().tag) != 'eagle':
            raise ValueError("EagleBrd.importBrd: Invalid file.")
        self._buildDeviceLibraries(xmltree.find(".//libraries"))
        self._readDevicePositions(xmltree.find(".//elements"))
        self._readHoles(xmltree.find(".//plain"))
        self._readVias(xmltree.find(".//signals"))
        self._readMillings(xmltree.find(".//plain"))
        logger.info("Found %s libraries with %s packages, %s devices, %s stand-alone holes, %s vias, %s millings",
                    len(self.deviceLibraries), sum([len(lib) for lib in self.deviceLibraries.values()]),
                    len(self.devicePositions), len(self.holes), len(self.vias), 
                    len(self.lineMillings) + len(self.circleMillings))
    
    
    def getDevice(self, library, device):
        """
        Returns an EagleDevice from the library

        :param str library: Name of the library
        :param str device: Name of the device
        :returns: device from library
        :rtype: EagleImport.EagleObjects.EagleDevice
        """
        try:
            return self.deviceLibraries[library].devices[device]
        except KeyError:
            raise KeyError("Device not found: {} ({})".format(device, library))
    
    
    def getDrillsAbsolute(self):
        """
        :returns list of EagleDrill objects with all drills on the board (devices, stand-alone drills and vias)
        with absolute positions
        :rtype: list(EagleImport.EagleObjects.EagleDrill)
        """
        drills = []
        # iterate through devices
        for devpos in self.devicePositions:
            dev = self.getDevice(devpos.libraryName, devpos.deviceName)
            # calculate absolute drill positions (including rotation)
            for drill in dev.drills:
                rot = devpos.rotation
                posx = drill.position[0]*math.cos(rot) - drill.position[1]*math.sin(rot)
                posy = drill.position[0]*math.sin(rot) + drill.position[1]*math.cos(rot)
                if devpos.mirrored:
                    posx = -posx
                newdrill = eo.EagleDrill(
                    drill.drillsize,
                    (devpos.position[0]+posx, devpos.position[1]+posy)
                )
                drills.append(newdrill)
        # iterate through stand-alone holes
        for hole in self.holes:
            drills.append(copy.deepcopy(hole))
        # iterate through vias
        for via in self.vias:
            drills.append(copy.deepcopy(via))
        return drills
    
    
    def _buildDeviceLibraries(self, librariestag):
        """
        Adds libraries and containing packages to the EagleBrd object

        :param librariestag: XML tag object pointing to the <libraries> tag
        """
        libs = librariestag.findall(".//library")
        # find all libraries
        for lib in libs:
            libname = lib.attrib["name"]
            logger.debug("Found library %s", libname)
            eagledevlib = eo.EagleDeviceLibrary(libname)
            devs = lib.findall(".//package")
            
            # find all packages
            for dev in devs:
                devname = dev.attrib["name"]
                eagledev = eo.EagleDevice(devname)
                pads = dev.findall(".//pad")
                # find all pads (drills)
                for pad in pads:
                    eagledev.addDrill(
                        float(pad.attrib["drill"]), 
                        (float(pad.attrib["x"]), float(pad.attrib["y"]))
                    )
                logger.debug("Found package %s containing %s pads", devname, len(pads))
                eagledevlib.addDevice(eagledev)
                
            # add to deviceLibraries
            if libname in self.deviceLibraries.keys():
                self.deviceLibraries[libname].append(eagledevlib)
            else:        
                self.deviceLibraries[libname] = eagledevlib
    
    
    def _readDevicePositions(self, elementstag):
        """
        Adds device positions to the EagleBrd object

        :param elementstag: XML tag object pointing to the <elements> tag
        """
        devs = elementstag.findall(".//element")
        for dev in devs:
            rotation = 0
            mirrored = False
            if "rot" in dev.attrib.keys():
                mirrored = (dev.attrib["rot"][0] == "M")
                rotation = float(dev.attrib["rot"].lstrip("MR")) * math.pi/180
            devpos = eo.EagleDevicePosition(
                dev.attrib["library"],
                dev.attrib["package"],
                (float(dev.attrib["x"]), float(dev.attrib["y"])),
                rotation,
                mirrored
            )
            logger.debug("Found device %s", devpos)
            self.devicePositions.append(devpos)
    
    
    def _readHoles(self, plaintag):
        """
        Adds stand-alone holes to the EagleBrd object

        :param plaintag: XML tag object pointing to the <plain> tag
        """
        holes = plaintag.findall(".//hole")
        for hole in holes:
            drill = eo.EagleDrill(
                float(hole.attrib["drill"]),
                (float(hole.attrib["x"]), float(hole.attrib["y"]))
            )
            logger.debug("Found stand-alone hole %s", drill)
            self.holes.append(drill)
        
        
    def _readVias(self, signalstag):
        """
        Adds via drills to the EagleBrd object

        :param signalstag: XML tag object pointing to the <signals> tag
        """
        vias = signalstag.findall(".//via")
        for via in vias:
            drill = eo.EagleDrill(
                float(via.attrib["drill"]),
                (float(via.attrib["x"]), float(via.attrib["y"]))
            )
            logger.debug("Found via %s", drill)
            self.vias.append(drill)
            
            
            
    def _readMillings(self, plaintag):
        """
        Adds millings to the EagleBrd object.
        Millings are wires in the milling layer (46)

        :param plaintag: XML tag object pointing to the <plain> tag
        """
        # find line millings
        wires = plaintag.findall('.//wire[@layer="46"]')
        for wire in wires:
            curve = 0
            if "curve" in wire.attrib.keys():
                curve = float(wire.attrib["curve"])
            milling = eo.EagleLineMilling(
                (float(wire.attrib["x1"]), float(wire.attrib["y1"])),
                (float(wire.attrib["x2"]), float(wire.attrib["y2"])),
                curve
            )
            logger.debug("Found line milling %s", milling)
            self.lineMillings.append(milling)
        # find circle millings
        circles = plaintag.findall('.//circle[@layer="46"]')
        for circle in circles:
            milling = eo.EagleCircleMilling(
                float(circle.attrib["radius"]),
                (float(circle.attrib["x"]), float(circle.attrib["y"]))
            )
            logger.debug("Found circle milling %s", milling)
            self.circleMillings.append(milling)