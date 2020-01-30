"""
Created on 04.02.2018

@author: Christian Ott
"""

import logging
logger = logging.getLogger(__name__)

import math

from Base.AppBase import AppBase
from Base import Utility
from Base import MachiningObjects as mo
from Base.Workpiece import Workpiece

from EagleImport.EagleBrd import EagleBrd

class ImportFactory(object):
    """
    Static class that imports boards into ESCMillPCB classes
    """

    def __init__(self):
        """
        Constructor
        """
        pass
    
    
    @classmethod
    def importFile(cls, filepath, filetype=""):
        """
        Imports a board file and returns the resulting workpiece.

        :param str filepath: Absolute path to the file
        :param str filetype: Containing the type of file to import (see table below)

        Valid filetypes:

        =============  ===================================================================
        **Value**      **Description**
        =============  ===================================================================
        "eagle"        Eagle \*.brd files
        =============  ===================================================================
        """
        if filetype == "eagle":
            logger.debug("Importing file %s as Eagle Board.", filepath)
            brd = EagleBrd()
            brd.importBrd(filepath)
            return cls._importEagleBrd(brd)
        else:
            raise ValueError("Invalid type.")
        
        
    @staticmethod
    def _importEagleBrd(brd):
        """
        Imports an EagleBrd class.

        :param EagleImport.EagleBrd.EagleBrd brd: Object to import from
        """
        workpiece = Workpiece()
        # import holes
        for eaglehole in brd.getDrillsAbsolute():
            hole = mo.Hole(eaglehole.drillsize, eaglehole.position[:])
            workpiece.appendHole(hole)
        # import millings
        for linemill in brd.lineMillings:
            milling = mo.Milling()
            path = None
            if linemill.curve == 0:
                path = mo.StraightPath(linemill.start, linemill.end)
            else:
                curve = Utility.degToRad(linemill.curve)
                path = mo.ArcPath.createArc(linemill.start, linemill.end, math.fabs(curve), curve > 0)
            milling.append(path)
            workpiece.appendMilling(milling)
        for circlemill in brd.circleMillings:
            milling = mo.Milling()
            path = mo.ArcPath.createCircle(circlemill.radius, circlemill.center)
            milling.append(path)
            workpiece.appendMilling(milling)
        return workpiece