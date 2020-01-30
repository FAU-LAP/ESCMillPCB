"""
Created on 24.02.2018

@author: Christian Ott
"""

import logging
logger = logging.getLogger(__name__)

import numpy as np
from PyQt5 import QtCore
import pyqtgraph.parametertree.parameterTypes as ptypes

import Base.Utility as util
import Base.Errors as errs


class MachineBase(QtCore.QObject):
    """
    **Machine control concept**

    MachineBase serves as an abstract base class for machine control. It implements some
    standard behavior while hardware near operations are to be implemented by the descendants
    of this class. All methods which are marked "(abstract)" in the class documentation
    are meant to be overridden.

    The milling cycle of the workpiece is executed via a planner system. This class defines a
    couple of planXXX methods which are used to plan the machine motion during the cycle.
    These methods should not start machining but interface to the concrete planner system
    defined by the concrete machine class. The planned motion is then executed by
    the executeCycle() method.

    MachineBase inherits from QtCore.QObject to support Qt Signals.

    ==========================  ===================================================================================
    **Signals**
    ==========================  ===================================================================================
    sigNewCoordinates           Emitted when new coordinates are present. Carries a dictionary
                                {"absolute":(x,y,z) absolute position of the machine,
                                "workpiece":(x,y,z) position of the machine on the board}
    sigStatusUpdate             Emitted when the machine status changed. Carries a string with the status message.
    sigCycleCompleted           Emitted when the machining cycle is finished.
    ==========================  ===================================================================================
    """
    
    sigNewCoordinates = QtCore.pyqtSignal(dict)
    sigStatusUpdate = QtCore.pyqtSignal(str)
    sigCycleCompleted = QtCore.pyqtSignal()
    

    def __init__(self):
        """
        Constructor
        """
        super().__init__(None)
        self.jogspeedXY = 0
        self.jogspeedZ = 0
        self.millspeedXY = 0
        self.infeedspeed = 0
        self.outfeedspeed = 0
        self.infeeddepth = 0
        self.tooldiameter = 0
        self.parkPosition = [0, 0, 0]
        self.defaultOrigin = [0, 0, 0]
        self.laseroffset = [0, 0]
        self.coordinateInterval = 500
        # initialize coordinate update timer
        self.coordinateTimer = QtCore.QTimer(self)
        self.coordinateTimer.setInterval(self.coordinateInterval)
        self.coordinateTimer.timeout.connect(self.coordinateTimer_timeout)
        
        
    def getName(self):
        """
        :returns: Machine's name
        :rtype: str
        """
        if type(self).__name__ == "MachineBase":
            return "None"
        else:
            return type(self).__name__
    
    
    def startCoordinateTimer(self):
        """
        Starts the coordinate update timer which is used by GUI elements displaying the current position.
        """
        self.coordinateTimer.start()
        
        
    def intialize(self, comparams):
        """
        (abstract)

        Initialize machine, i.e. communication and base settings.

        :param pyqtgraph.GroupParameter comparams: GroupParameter containing communication settings.
        """
        raise errs.ImplementationMissing("MachineBase.initialize")
    
    
    def finalize(self):
        """
        (abstract)

        Bring machine to save state and close communication.
        """
        raise errs.ImplementationMissing("MachineBase.finalize")
    
    
    def isInitialized(self):
        """
        (abstract)

        :returns: True if the machine is already initialized.
        :rtype: bool

        """
        return False;
    
    
    def getPosition(self, absolute=True):
        """
        (abstract)

        :param bool absolute: If true return absolute coordinates, otherwise return workpiece coordinates
        :returns: Current position
        :rtype: tuple(float, float, float)
        """
        raise errs.ImplementationMissing("MachineBase.getPosition")
        
    
    def feedhold(self):
        """
        (abstract)

        Feedhold, i.e. pause movement or cycle.
        """
        raise errs.ImplementationMissing("MachineBase.feedhold")
    
    
    def resume(self):
        """
        (abstract)

        Resume from feedhold.
        """
        raise errs.ImplementationMissing("MachineBase.resume")
    
    
    def stop(self):
        """
        (abstract)

        Feedhold and abort movement/cycle.
        """
        raise errs.ImplementationMissing("MachineBase.stop")
    
    
    def jog(self, directions, stepsize=None):
        """
        (abstract)

        Jog into given directions with optional stepsize.
        If no stepsize is given, jogging will be endless (until a stop command is invoked).

        :param directions: Tuple of directions (x, y, z), possible entries are
                           0: no jog in this direction, 1: jog in positive direction,
                           -1: jog in negative direction
        :type directions: tuple(int, int, int)
        :param float stepsize: Size of the jogging step in mm. If none, jogging is performed
                               until a stop command is invoked (or a limit switch is reached if present)
        """
        raise errs.ImplementationMissing("MachineBase.jog")
    
    
    def goTo(self, position, absolute=True):
        """
        (abstract)

        Move to given position.
        If a z coordinate is given, z movement should be carried out in a way that the tool does not crash.
        E.g.: If the tool moves towards the workpiece, xy movement should be carried out first, otherwise
        z movement should precede.

        :param position: Coordinates (x, y) / (x, y, z) to move to.
        :type position: tuple(float, float) or tuple(float, float, float)
        :param bool absolute: Use absolute (machine) coordinate system. If False uses workpiece coordinate system
        """
        raise errs.ImplementationMissing("MachineBase.goTo")
    
    
    def goToParkPosition(self):
        """
        Move to park position.
        """
        self.goTo(self.getParkPosition(), True)
    
    
    def goToDefaultOrigin(self):
        """
        Move to default board origin.
        """
        self.goTo(self.getDefaultOrigin(), True)
    
    
    def setSpindle(self, enable):
        """
        (abstract)

        Set spindle state.

        :param bool enable: Enable or disable spindle
        """
        raise errs.ImplementationMissing("MachineBase.setSpindle")
    
    
    def setLaserCrosshair(self, enable):
        """
        (abstract, optional)

        Enables the laser crosshair if available.

        :param bool enable: Enable or disable laser crosshair
        """
        pass
            
    
    def homingCycle(self):
        """
        (abstract)

        Perform a homing cycle.
        """
        raise errs.ImplementationMissing("MachineBase.homingCycle")
    
    
    def isHomed(self):
        """
        (abstract)

        Returns if the machine's coordinate system is homed.
        """
        return False;
    
    
    def preparePlanner(self):
        """
        (abstract)

        Initializes the motion planner.
        """
        raise errs.ImplementationMissing("MachineBase.preparePlanner")
    
    
    def finalizePlanner(self):
        """
        (abstract)

        Finalizes the motion planner.
        """
        raise errs.ImplementationMissing("MachineBase.finalizePlanner")
    
    
    def planJog(self, position):
        """
        (abstract)

        Plans jogging to the given position in the XY plane.

        :param position: Coordinates (x, y) to move to.
        :type position: tuple(float, float)
        """
        raise errs.ImplementationMissing("MachineBase.planJog")
    
    
    def planMill(self, position):
        """
        (abstract)

        Plans straight milling to the given position in the XY plane.

        :param position: Coordinates (x, y) to move to.
        :type position: tuple(float, float)
        """
        raise errs.ImplementationMissing("MachineBase.planMill")
    
    
    def planMillArc(self, startposition, endposition, center, ccw=True):
        """
        (abstract)

        Plans arc milling to the given end position in the XY plane.
        This does not include jogging to the start position.

        :param startposition: Coordinates (x, y) to arc from.
        :type startposition: tuple(float, float)
        :param endposition: Coordinates (x, y) to arc to.
        :type endposition: tuple(float, float)
        :param center: Coordinates (x, y) of the arc center.
        :type center: tuple(float, float)
        :param bool ccw: Arc diretion, default is counterclockwise
        """
        raise errs.ImplementationMissing("MachineBase.planMillArc")
    
    
    def planInfeed(self):
        """
        (abstract)

        Plans an infeed at the current position.
        """
        raise errs.ImplementationMissing("MachineBase.planInfeed")
    
    
    def planOutfeed(self):
        """
        (abstract)

        Plans an outfeed at the current position.
        """
        raise errs.ImplementationMissing("MachineBase.planOutfeed")
    
    
    def executeCycle(self):
        """
        (abstract)

        Execute the planned work cycle.
        """
        raise errs.ImplementationMissing("MachineBase.executeCycle")
    
    
    def setWorkpieceOrigin(self, offset=(0, 0)):
        """
        (abstract)

        Sets the current position as workpiece origin.

        :param offset: (x, y) offset of the new origin to the current position
        :type offset: tuple(float, float)
        """
        raise errs.ImplementationMissing("MachineBase.setWorkpieceOrigin")
        
        
    def performAngleCorrection(self, refcoords, offset=(0, 0)):
        """
        Calculates and applies angle correction. Returns a correction matrix used for transforming the
        workpiece element coordinates.

        The default implementation returns a rotation matrix to rotate the workpiece elements itself to
        cancle the rotation error. If the machine supports rotation correction it might be better to use
        this instead and just return a unity matrix.

        A coordinate offset to the current machine position can be given which is especially needed
        to account for the laser crosshair offset.

        :param refcoords: (x, y) coordinates of the workpiece reference point
        :type refcoords: tuple(float, float)
        :param offset: (x, y) coordinate offset to the current machine position
        :type offset: tuple(float, float)
        :returns: (2x2) rotation matrix and mismatch angle (in rad)
        :rtype: tuple(np.array(float), float)
        """
        reference = np.array(refcoords)
        current = np.array(self.getPosition(absolute=False)[:2])
        current[0] += offset[0]
        current[1] += offset[1]
        angle = util.calculateAngle(reference, current)
        return util.create2DRotation(angle), angle
    
    
    def applyComParameters(self, params):
        """
        (abstract)

        Apply set of communication parameters to the machine object.

        :param pyqtgraph.GroupParameter params: GroupParameter containing the parameter values
        """
        raise errs.ImplementationMissing("MachineBase.applyComParameters")
    
    
    def applyParameters(self, params, hiddenparams=None):
        """
        (abstract)

        Apply set of parameters to the machine.

        :param pyqtgraph.GroupParameter params: GroupParameter containing the parameter values
        :param pyqtgraph.GroupParameter hiddenparams: GroupParameter containing the hidden parameter values if available
        """
        raise errs.ImplementationMissing("MachineBase.applyParameters")
    
    
    def retrieveParameters(self):
        """
        (abstract)

        Read parameters from the machine.

        :returns: GroupParameter containing the parameter values
        :rtype: pyqtgraph.GroupParameter
        """
        return ptypes.GroupParameter()
    
    
    def applyBasicParameters(self, params, hiddenparams):
        """
        Apply set of basic (machine independent) parameters.

        :param pyqtgraph.GroupParameter params: GroupParameter containing the parameter values
        :param pyqtgraph.GroupParameter hiddenparams: GroupParameter containing the hidden parameter values
        """
        self.jogspeedXY = params.child('jog_speed_xy').value()
        self.jogspeedZ = params.child('jog_speed_z').value()
        self.millspeedXY = params.child('mill_speed_xy').value()
        self.infeedspeed = params.child('infeed_speed').value()
        self.outfeedspeed = params.child('outfeed_speed').value()
        self.infeeddepth = params.child('infeed_depth').value()
        self.tooldiameter = params.child('tool_diameter').value()
        self.laseroffset = [params.child('laser_offset_x').value(),
                            params.child('laser_offset_y').value()]
        self.parkPosition = [hiddenparams.child('parkpos_x').value(), 
                             hiddenparams.child('parkpos_y').value(),
                             hiddenparams.child('parkpos_z').value()]
        self.defaultOrigin = [hiddenparams.child('boardorigin_x').value(), 
                              hiddenparams.child('boardorigin_y').value(),
                              hiddenparams.child('boardorigin_z').value()]
        
    
    def getJogSpeed(self):
        """
        :returns: (jogspeedXY, jogspeedZ) in mm/min
        :rtype: tuple(float, float)
        """
        return self.jogspeedXY, self.jogspeedZ
    
    def getMillSpeed(self):
        """
        :returns: millspeedXY in mm/min
        :rtype: float
        """
        return self.millspeedXY
    
    def getInfeedSpeed(self):
        """
        :returns: infeedspeed in mm/min
        :rtype: float
        """
        return self.infeedspeed
    
    def getToolDiameter(self):
        """
        :returns: tooldiameter in mm/min
        :rtype: float
        """
        return self.tooldiameter
    
    def getLaserOffset(self):
        """
        :returns: (x,y) laser position offset in mm
        :rtype: tuple(float, float)
        """
        return self.laseroffset[:]
    
    
    def getParkPosition(self):
        """
        :returns: (x,y,z) park position in machine coordinates
        :rtype: tuple(float, float, float)
        """
        return self.parkPosition[:]
    
    def setParkPosition(self, position):
        """
        :param position: (x,y,z) park position in machine coordinates
        :type position: tuple(float, float, float)
        """
        if len(position) != 3:
            raise errs.InvalidArgument("position", "Invalid length.")
        self.parkPosition = position[:]
        
        
    def getDefaultOrigin(self):
        """
        :returns: (x,y,z) default workpiece origin in machine coordinates
        :rtype: tuple(float, float, float)
        """
        return self.defaultOrigin[:]
    
    def setDefaultOrigin(self, position):
        """
        :param position: (x,y,z) default workpiece origin in machine coordinates
        :type position: tuple(float, float, float)
        """
        if len(position) != 3:
            raise errs.InvalidArgument("position", "Invalid length.")
        self.defaultOrigin = position[:]
    
    
    def getMachineMenu(self):
        """
        (abstract)

        :returns: Machine specific menu for the main window menu bar (or None if not available)
        :rtype: QtWidgets.QMenu
        """
        return None
    
    
    @QtCore.pyqtSlot()
    def coordinateTimer_timeout(self):
        if self.isInitialized():
            self.sigNewCoordinates.emit({'absolute':self.getPosition(True), 'workpiece':self.getPosition(False)})
    
    
    @staticmethod
    def getParameters():
        """
        :returns: Machine parameters
        :rtype: pyqtgraph.GroupParameter
        """
        return ptypes.GroupParameter(name='MachineParams')        
    
    @staticmethod
    def getComParameters():
        """
        :returns: Communication parameters
        :rtype: pyqtgraph.GroupParameter
        """
        return ptypes.GroupParameter(name='ComParams')
    
    @staticmethod
    def updateComParameters(params):
        """
        Updates the com parameters (e.g. rescanns COM ports)

        :param params: Com parameters
        :rtype: pyqtgraph.GroupParameter
        """
        pass
        
    
    @staticmethod
    def getHiddenParameters():
        """
        :returns: Hidden machine parameters (not shown in settings dialog)
        :rtype: pyqtgraph.GroupParameter
        """
        return ptypes.GroupParameter(name='HiddenParams')

    
    @staticmethod
    def getBasicParameters():
        """
        This function is not meant to be overridden.

        :returns: Machine independent basic parameters
        :rtype: pyqtgraph.GroupParameter
        """
        params = {
            'name':'MachineSettings', 'type':'group', 'children':[
                {
                    'name':'jog_speed_xy',
                    'title':'X&Y axis jogging speed (mm/min)',
                    'type':'float',
                    'min':0,
                    'default':1000,
                    'value':1000
                },
                {
                    'name':'jog_speed_z',
                    'title':'Z axis jogging speed (mm/min)',
                    'type':'float',
                    'min':0,
                    'default':1000,
                    'value':1000
                },
                {
                    'name':'mill_speed_xy',
                    'title':'Milling speed (mm/min)',
                    'type':'float',
                    'min':0,
                    'default':60,
                    'value':60
                },
                {
                    'name':'infeed_speed',
                    'title':'Z axis infeed speed (mm/min)',
                    'type':'float',
                    'min':0,
                    'default':400,
                    'value':400
                },
                {
                    'name':'outfeed_speed',
                    'title':'Z axis outfeed speed (mm/min)',
                    'type':'float',
                    'min':0,
                    'default':1000,
                    'value':1000
                },
                {
                    'name':'infeed_depth',
                    'title':'Z axis infeed depth (mm)',
                    'type':'float',
                    'min':0,
                    'default':3,
                    'value':3
                },
                {
                    'name':'tool_diameter',
                    'title':'Tool diameter (mm)',
                    'type':'float',
                    'min':0,
                    'default':0.85,
                    'value':0.85
                },
                {
                    'name':'laser_offset_x',
                    'title':'Laser sight x offset',
                    'type':'float',
                    'default':0,
                    'value':0
                },
                {
                    'name':'laser_offset_y',
                    'title':'Laser sight y offset',
                    'type':'float',
                    'default':0,
                    'value':0
                },
                {
                    'name':'coordinate_interval',
                    'title':'Coordinate update interval (ms)',
                    'type':'int',
                    'default':200,
                    'value':200
                }
            ]
        }
        return ptypes.GroupParameter(**params)
    
    @staticmethod
    def getBasicHiddenParameters():
        """
        This function is not meant to be overridden.

        :returns: Machine independent basic hidden parameters (not shown in settings dialog)
        :rtype: pyqtgraph.GroupParameter
        """
        params = {
            'name':'MachineHiddenSettings', 'type':'group', 'children':[
                {
                    'name':'machine_name',
                    'type':'str',
                    'value':'None'
                },
                {
                    'name':'parkpos_x',
                    'type':'float',
                    'value':0
                },
                {
                    'name':'parkpos_y',
                    'type':'float',
                    'value':0
                },
                {
                    'name':'parkpos_z',
                    'type':'float',
                    'value':0
                },
                {
                    'name':'boardorigin_x',
                    'type':'float',
                    'value':0
                },
                {
                    'name':'boardorigin_y',
                    'type':'float',
                    'value':0
                },
                {
                    'name':'boardorigin_z',
                    'type':'float',
                    'value':0
                }
            ]
        }
        return ptypes.GroupParameter(**params)