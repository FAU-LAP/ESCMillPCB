"""
Created on 04.02.2018

@author: Christian Ott
"""

import logging
logger = logging.getLogger(__name__)

import numpy as np
import copy

from Base import Utility
from Base import Errors


class MachiningObject(object):
    """
    Base class for machining objects.
    """

    def __init__(self):
        """
        Constructor
        """
        self.optimizers = []
    
    
    def planMotion(self, machine):
        """
        Plan machining.

        :param Base.MachineBase.MachineBase machine: Active machine
        """
        pass
    
    
    def translate(self, offset):
        """
        Translates the machining object by a given offset.

        :param offset: (x, y) offset for translation
        :type offset: tuple(float, float)
        """
        pass
    
    
    def transform(self, matrix):
        """
        Transforms the machining object with a transformation matrix.

        :param matrix: (2x2) transformation matrix
        :type matrix: np.array(float)
        """
        pass
    
    
    def mirror(self):
        """
        Mirrors all machining objects around the y-axis.
        """
        pass
        
    
    def optimize(self):
        """
        Run all optimizers.
        """
        for optimizer in self.optimizers:
            optimizer.optimize(self)
    
    
    def appendOptimizer(self, optimizer):
        """
        Append new optimizer.

        :param Base.BaseOptimizers.MachiningOptimizer optimizer: Optimizer to append
        """
        self.optimizers.append(optimizer)
        
    
    def updateOptimizers(self, params):
        """
        Update parameters of all optimizers.

        :param pyqtgraph.GroupParameter params: GroupParameter containing the optimizer parameters
        """
        for optimizer in self.optimizers:
            optimizer.updateParameters(params.child(optimizer.getName()))
    
    
    
class HoleList(MachiningObject):
    """
    Represents a set of holes
    """
    
    def __init__(self):
        """
        Constructor
        """
        super().__init__()
        self.holes = []
        self.active = True
        
        
    def __len__(self):
        """
        :returns: number of Holes in the HoleList
        :rtype: int
        """
        return len(self.holes)
    
    
    def __iter__(self):
        """
        :returns: iterator over the included Holes
        :rtype: iterator(Hole)
        """
        return iter(self.holes)
        
        
    def append(self, hole):
        """
        Add hole to the HoleList

        :param Hole hole: Hole object to append
        """
        self.holes.append(hole)
        
    
    def reorder(self, order):
        """
        Reorder HoleList

        :param order: List of indexes mapping old indices to new order
        :type order: list[int]
        """
        holesordered = [ self.holes[i] for i in order ]
        self.holes = holesordered
    
    
    def optimize(self):
        """
        See :meth:`MachiningObject.optimize`
        """
        for hole in self:
            hole.optimize()
        super().optimize()
        
    
    def updateOptimizers(self, params):
        """
        See :meth:`MachiningObject.updateOptimizers`
        """
        super().updateOptimizers(params)
        for hole in self:
            hole.updateOptimizers(params)
            
            
    def planMotion(self, machine):
        """
        See :meth:`MachiningObject.planMotion`
        """
        if self.active:
            for hole in self:
                hole.planMotion(machine)
            
            
    def translate(self, offset):
        """
        See :meth:`MachiningObject.translate`
        """
        for hole in self:
            hole.translate(offset)
            
            
    def transform(self, matrix):
        """
        See :meth:`MachiningObject.transform`
        """
        for hole in self:
            hole.transform(matrix)
            
    
    def mirror(self):
        """
        See :meth:`MachiningObject.mirror`
        """
        for hole in self:
            hole.mirror()      



class Hole(MachiningObject):
    """
    MachiningObject representing a drill hole
    """
    
    def __init__(self, diameter, center):
        """
        Constructor

        :param float diameter: diameter of the hole
        :param center: (x, y) coordinates of the center
        :type center: tuple(float, float)
        """
        super().__init__()
        self.diameter = diameter
        self.center = np.array(center)
        
        
    def planMotion(self, machine):
        """
        See :meth:`MachiningObject.planMotion`
        """
        if machine.getToolDiameter() >= self.diameter:
            # directly drill hole
            logger.debug('Directly drill at %s (original diameter %s)', self.center, self.diameter)
            machine.planJog(self.center)
            machine.planInfeed()
            machine.planOutfeed()
        else:
            # mill hole
            logger.debug('Mill hole with diameter %s at %s', self.diameter, self.center)
            # also account for tool diameter!
            start = self.center - np.array([(self.diameter-machine.getToolDiameter())/2, 0])
            machine.planJog(start)
            machine.planInfeed()
            machine.planMillArc(start, start, self.center)
            machine.planOutfeed()
            
            
    def translate(self, offset):
        """
        See :meth:`MachiningObject.translate`
        """
        self.center += offset
        
        
    def transform(self, matrix):
        """
        See :meth:`MachiningObject.transform`
        """
        self.center = matrix.dot(self.center)
        
        
    def mirror(self):
        """
        See :meth:`MachiningObject.mirror`
        """
        self.center[0] *= -1
    
    
    
class MillingList(MachiningObject):
    """
    MachiningObject representing a set of millings.
    """
    
    def __init__(self):
        """
        Constructor
        """
        super().__init__()
        self.millings = []
        self.active = True
            
        
    def __len__(self):
        """
        :returns: number of Millings in the MillingList
        :rtype: int
        """
        return len(self.millings)
    
    
    def __iter__(self):
        """
        :returns: iterator over the included Millings
        :rtype: iterator(Milling)
        """
        return iter(self.millings)
    
    
    def __getitem__(self, key):
        """
        :param int key: index of the Milling entry
        :returns: Milling at index key
        :rtype: Milling
        """
        return self.millings[key]
    
    
    def append(self, milling):
        """
        Add milling to the MillingList.

        :param Milling milling: Milling object to append
        """
        if not isinstance(milling, Milling):
            ValueError("MillingList.append: invalid object")
        self.millings.append(milling)
        
        
    def pop(self, index=0):
        """
        Remove and return milling from MillingList.

        :param int index: Milling at this index will be removed from list and returned
        """
        return self.millings.pop(index)
    
    
    def appendList(self, millinglist):
        """
        Appends any iterable list of millings to the MillingList.

        :param millinglist: Milling objects to append
        :type millinglist: list(Milling)
        """
        for milling in millinglist:
            self.append(milling)
    
    
    def reorder(self, order):
        """
        Reorder MillingList

        :param order: List of indexes mapping old indices to new order
        :type order: list(int)
        """
        millingsordered = [ self.millings[i] for i in order ]
        self.millings = millingsordered
        
            
    def optimize(self):
        """
        See :meth:`MachiningObject.optimize`
        """
        for milling in self:
            milling.optimize()
        super().optimize()
        
    
    def updateOptimizers(self, params):
        """
        See :meth:`MachiningObject.updateOptimizers`
        """
        super().updateOptimizers(params)
        for milling in self:
            milling.updateOptimizers(params)
            
    
    def planMotion(self, machine):
        """
        See :meth:`MachiningObject.planMotion`
        """
        if self.active:
            for milling in self:
                milling.planMotion(machine)
            
            
    def translate(self, offset):
        """
        See :meth:`MachiningObject.translate`
        """
        for milling in self:
            milling.translate(offset)
            
            
    def transform(self, matrix):
        """
        See :meth:`MachiningObject.transform`
        """
        for milling in self:
            milling.transform(matrix)
            
            
    def mirror(self):
        """
        See :meth:`MachiningObject.mirror`
        """
        for milling in self:
            milling.mirror()
    
    
    
class Milling(MachiningObject):
    """
    MachiningObject representing a milling.
    Contains a list of MachiningPaths which need to be adjacent and ordered.
    The starting point of the fist path is the infeed point, the end point of the last path the outfeed point.
    """
    
    def __init__(self):
        """
        Constructor
        """
        super().__init__()
        self.pathList = []
        
    
    def __len__(self):
        """
        :returns: number of paths in the Milling
        :rtype: int
        """
        return len(self.pathList)
    
    
    def __iter__(self):
        """
        :returns: iterator over the included paths
        :rtype: iterator(MachiningPath)
        """
        return iter(self.pathList)
        
        
    def append(self, path):
        """
        Append MachiningPath to the Milling.
        Paths need to be adjacent, i.e. path.start must be equal to self.getEnd()

        :param MachiningPath path: Object to append
        """
        if len(self) and np.any(path.start != self.pathList[-1].end):
            raise ValueError("Milling.append: invalid path, paths need to be adjacent")
        self.pathList.append(path)
                    
            
    def appendMilling(self, milling):
        """
        Append paths of a milling object to the Milling.
        Paths need to be adjacent, i.e. milling.getStart() must be equal to self.getEnd()

        :param Milling milling: Object to append
        """
        if len(self) and not np.all(self.getEnd() == milling.getStart()):
            raise ValueError("Milling.appendMilling: invalid milling, paths need to be adjacent")
        self.pathList.extend(copy.deepcopy(milling.pathList))
        
    
    def getStart(self):
        """
        :returns: starting point of the milling
        :rtype: tuple(float, float)
        """
        if not len(self):
            return None
        return self.pathList[0].start
    
    
    def getEnd(self):
        """
        :returns: end point of the milling
        :rtype: tuple(float, float)
        """
        if not len(self):
            return None
        return self.pathList[-1].end
    
    
    def pathLength(self):
        """
        :returns: length of the milling (in mm)
        :rtype: float
        """
        length = 0
        for path in self:
            length += path.pathLength()
        return length
    
    
    def splitMilling(self, start, distance):
        """
        Splits the milling into two millings.
        If the split distance would span

        :param float start: path length after which the milling is split
        :param float distance: path length (relative to split position) after which the new milling starts
        :returns: new milling containing the split off part
        :rtype: Milling
        """
        if start > self.pathLength():
            logger.debug("Trying to split %s long milling at %s (with %s distance)", self.pathLength(), start, distance)
            raise Errors.InvalidArgument("start", "Milling too short to split!")
        
        remainingPaths = []
        curDistance = distance
        lastIndex = None
        newPath = None
        
        # loop through all paths until the split is completed
        for i, path in enumerate(self.pathList):
            lastIndex = i
            pathLength = path.pathLength()
            # check if there is distance to crop left from last step
            if curDistance < distance:
                # check if there is something left of the path after the split
                if pathLength <= curDistance:
                    # if not, drop path and update curDistance
                    curDistance -= pathLength
                    continue
                else:
                    # otherwise, crop path and break (split completed)
                    path.splitPath(0, curDistance)
                    lastIndex -= 1
                    break
            
            # if the path before was exactly the split start length, crop this path
            if start == 0:
                path.splitPath(0, curDistance)
                lastIndex -= 1
                break
                
            # append path to remaining paths of the milling
            remainingPaths.append(path)
            # check if the path is too short for the split
            if pathLength <= start:
                start -= pathLength
                continue
            else:
                newPath = path.splitPath(start, distance)
            # check if the path has only been cropped -> distance to crop left for next path
            if newPath is None:
                curDistance = start + curDistance - pathLength
                # check if the path length has exactly matched -> completed
                if curDistance <= 0:
                    break
            else:
                # otherwise the split is completed
                break
        
        # create new milling from remaining paths
        newMilling = None
        newMillingPaths = []
        # insert rest of last path into new milling
        if newPath is not None:
            newMillingPaths.append(newPath)
        # insert excess paths into new milling
        if lastIndex + 1 < len(self):
            newMillingPaths.extend(self.pathList[lastIndex + 1:])
        # create new milling if paths are available
        if newMillingPaths:
            newMilling = Milling()
            for path in newMillingPaths:
                newMilling.append(path)
                
        # update path list
        self.pathList.clear()
        for path in remainingPaths:
            self.append(path)
            
        return newMilling
        
    
    def reverse(self):
        """
        Reverses the Milling's path list and all pathes
        """
        self.pathList.reverse()
        for path in self.pathList:
            path.reverse()
            
            
    def planMotion(self, machine):
        """
        See :meth:`MachiningObject.planMotion`
        """
        machine.planJog(self.getStart())
        machine.planInfeed()
        for path in self:
            path.planMotion(machine)
        machine.planOutfeed()
        
        
    def translate(self, offset):
        """
        See :meth:`MachiningObject.translate`
        """
        for path in self:
            path.translate(offset)
            
            
    def transform(self, matrix):
        """
        See :meth:`MachiningObject.transform`
        """
        for path in self:
            path.transform(matrix)
            
    
    def mirror(self):
        """
        See :meth:`MachiningObject.mirror`
        """
        for path in self:
            path.mirror()
        
        

class MachiningPath(object):
    """
    Represents a milling path segment
    """
    
    def __init__(self):
        """
        Constructor
        """
        pass
    
    
    def reverse(self):
        """
        Interchanges start and end point.
        """
        pass
    
    
    def pathLength(self):
        """
        :returns: length of the path (in mm)
        :rtype: int
        """
        return 0
    
    
    def splitPath(self, start, distance):
        """
        Splits the path into two paths.
        If start is zero, shrinks the path distance from the beginning and returns None.
        If start + distance > path length, shrinks the path from the end and returns None.
        Returns an error if start is zero and distance > path length.

        :param flaot start: path length after which the path is split
        :param float distance: path length (relative to split position) after which the new path starts
        :returns: new path containing the split off part if available, None if not
        :rtype: MachiningPath
        """
        if start > self.pathLength() or (start == 0 and distance > self.pathLength()):
            raise Errors.InvalidArgument("start", "Path too short to split.")
        return None
    
    
    def planMotion(self, machine):
        """
        See :meth:`MachiningObject.planMotion`
        """
        pass
    
    
    def translate(self, offset):
        """
        See :meth:`MachiningObject.translate`
        """
        pass
    
    
    def transform(self, matrix):
        """
        See :meth:`MachiningObject.transform`
        """
        pass
        
        
    
class StraightPath(MachiningPath):
    """
    Represents a straight milling path
    """
    
    def __init__(self, start, end):
        """
        Constructor

        :param start: Start point coordinates
        :type start: tuple(float, float)
        :param end: End point coordinates
        :type end: tuple(float, float)
        """
        super().__init__()
        self.start = np.array(start)
        self.end = np.array(end)
        
    
    def reverse(self):
        """
        See :meth:`MachiningPath.reverse`
        """
        self.start, self.end = self.end, self.start
        
    
    def pathLength(self):
        """
        See :meth:`MachiningPath.pathLength`
        """
        return np.linalg.norm(self.end - self.start)
    
    
    def splitPath(self, start, distance):
        """
        See :meth:`MachiningPath.splitPath`
        """
        super().splitPath(start, distance)
        pathLength = self.pathLength()
        pathEnd = self.end
        
        pathDir = (self.end - self.start)/pathLength
        splitStart = self.start + pathDir * start
        splitEnd = self.start + pathDir * (start + distance)
        # crop path from beginning if start is zero
        if start == 0:
            self.start = splitEnd
            return None
        # otherwise, splitStart is now the end of this path
        self.end = splitStart
        # there is no new path if start + distance >= path length
        if start + distance >= pathLength:
            return None
        # new (separated) path starts from splitEnd and goes to the old path end
        splitPath = StraightPath(splitEnd, pathEnd)
        return splitPath
        
        
    def planMotion(self, machine):
        """
        See :meth:`MachiningPath.planMotion`
        """
        machine.planMill(self.end)
        
        
    def translate(self, offset):
        """
        See :meth:`MachiningPath.translate`
        """
        self.start += offset
        self.end += offset
        
        
    def transform(self, matrix):
        """
        See :meth:`MachiningPath.transform`
        """
        self.start = matrix.dot(self.start)
        self.end = matrix.dot(self.end)
        
        
    def mirror(self):
        """
        See :meth:`MachiningPath.mirror`
        """
        self.start[0] = -self.start[0]
        self.end[0] = -self.end[0]
        
        
        
class ArcPath(MachiningPath):
    """
    Represents an arc milling path (circle or circle segment)
    """
    
    @classmethod
    def createCircle(cls, radius, center):
        """
        Factory method ArcPath.createCircle(radius, center),
        constructs ArcPath for a full circle.

        :param float radius: Radius of the circle
        :param center: Center coordinates of the circle
        :type center: tuple(float, float)
        :returns: created arc path
        :rtype: ArcPath
        """
        start = (center[0]-radius, center[1])
        end = start
        return cls(start, end, center, 2*np.pi)
    
    
    @classmethod
    def createArc(cls, start, end, angle, ccw=True):
        """
        Factory method ArcPath.createArc(start, end, angle, ccw),
        constructs ArcPath for a partial circle in Eagle parameterization
        (given start point, end point and opening angle).

        :param start: Starting point coordinates of the arc
        :type start: tuple(float, float)
        :param end: End point coordinates of the arc
        :type end: tuple(float, float)
        :param float angle: Opening angle of the circle segment in radiant
        :param bool ccw: States if the arc path is to be drawn counterclockwise (default: True)
        :returns: created arc path
        :rtype: ArcPath
        """
        if angle <= 0 or angle >= 2*np.pi:
            raise ValueError("Angle has to be larger than 0 and smaller than 2pi!")
        
        # nomenclature: S: start, E: end, C: center, M: center of the chord SE
        # p: point, v: vector from point to point, l: length of line segment
        # use 3D vectors with z=0 for calculation
        pS = np.array((*start, 0))
        pE = np.array((*end, 0))
        vSE = pE - pS
        lSE = np.linalg.norm(vSE)
        vez = np.array([0, 0, 1])
        # calculate theta (angle(SC, SE) = |pi/2 - angle/2|)
        theta = np.abs(np.pi/2 - angle/2)
        # calculate radius ( r = SE / (2*cos(theta) )
        radius = lSE / (2*np.cos(theta))
        # calculate length of line segment MC = radius * sin(theta)
        lMC = radius * np.sin(theta)
        
        # angle < 180 and ccw or angle > 180� and cw: C is "left" to SE
        if (angle <= np.pi and ccw) or (angle >= np.pi and not ccw):
            vMC = lMC/lSE * np.cross(vez, vSE)
        # if angle > 180 and ccw or angle < 180� and cw: C is "right" to SE
        else:
            vMC = lMC/lSE * np.cross(vSE, vez)
            
        # center point is at pS + vSM + vMC = pS + 0.5vSE + vMC
        pC = pS + 0.5*vSE + vMC
        
        logger.debug("Importing arc from Eagle format: %s to %s, curve %s� -> center %s, ccw %s",
                     start, end, Utility.radToDeg(angle), (pC[0], pC[1]), ccw)
        
        return cls(start, end, (pC[0], pC[1]), angle, ccw)
        
    
    @classmethod
    def createArc2(cls, center, start, angle, ccw=True):
        """
        Factory method ArcPath.createArc2(center, start, angle, ccw),
        constructs ArcPath for a partial circle given center point, start point and opening angle.

        :param center: Center point coordinates of the arc
        :type center: tuple(float, float)
        :param start: Starting point coordinates of the arc
        :type start: tuple(float, float)
        :param float angle: Opening angle of the circle segment in radiant
        :param bool ccw: States if the arc path is to be drawn counterclockwise (default: True)
        :returns: created arc path
        :rtype: ArcPath
        """
        if angle <= 0 or angle >= 2*np.pi:
            raise ValueError("Angle has to be larger than 0 and smaller than 2pi!")
        pS = np.array(start)
        pC = np.array(center)
        
        rotAngle = angle
        if not ccw:
            rotAngle *= -1
        vCS = pS - pC
        vCE = Utility.create2DRotation(rotAngle).dot(vCS)
        pE = pC + vCE
        return cls(pS, pE, pC, angle, ccw)
    
    
    def __init__(self, start, end, center, angle, ccw=True):
        """
        Constructor. Arcs are parameterized by start and end point of the arc
        and the center point of the of the respective circle (if the arc were closed).
        Use the factory methods to convert from other parametrizations.

        :param start: Starting point coordinates of the arc
        :type start: tuple(float, float)
        :param end: End point coordinates of the arc
        :type end: tuple(float, float)
        :param center: Center point of the arc
        :type center: tuple(float, float)
        :param float angle: Opening angle of the arc in rad (absolute value)
        :param bool ccw: States if the arc path is to be drawn counterclockwise (default: True)
        """
        super().__init__()
        self.start = np.array(start)
        self.end = np.array(end)
        self.center = np.array(center)
        self.angle = np.abs(angle)
        self.ccw = ccw;
    
    
    def reverse(self):
        """
        See :meth:`MachiningPath.reverse`
        """
        self.start, self.end = self.end, self.start
        self.ccw = not self.ccw
    
        
    def pathLength(self):
        """
        See :meth:`MachiningPath.pathLength`
        """
        return self.angle*np.linalg.norm(self.start-self.center)
    
    
    def splitPath(self, start, distance):
        """
        See :meth:`MachiningPath.splitPath`
        """
        super().splitPath(start, distance)
        radius = np.linalg.norm(self.start - self.center)
        pathEnd = self.end
        pathLength = self.pathLength()
        # if start is 0, crop path from the beginning
        if start == 0:
            angle = self.angle - distance/radius
            path = self.createArc2(self.center, self.end, angle, not self.ccw)
            path.reverse()
            self.start = path.start
            self.angle = path.angle
            return None
        # otherwise calculate new end point for this path
        angle1 = start/radius
        angle2 = self.angle - (start + distance)/radius
        # create new path for first part of the split path
        path1 = self.createArc2(self.center, self.start, angle1, self.ccw)
        # use parameters of first part for this path
        self.end = path1.end
        self.angle = path1.angle
        # if start + distance >= path length, there is no split off second path
        if start + distance >= pathLength:
            return None
        # otherwise create new path for second part of the split path
        path2 = self.createArc2(self.center, pathEnd, angle2, not self.ccw)
        path2.reverse()
        return path2
        
        
    def planMotion(self, machine):
        """
        See :meth:`MachiningPath.reverse`
        """
        machine.planMillArc(self.start, self.end, self.center, self.ccw)
        
        
    def translate(self, offset):
        """
        See :meth:`MachiningPath.translate`
        """
        self.start += offset
        self.end += offset
        self.center += offset
    
    
    def transform(self, matrix):
        """
        See :meth:`MachiningPath.transform`
        """
        self.start = matrix.dot(self.start)
        self.end = matrix.dot(self.end)
        self.center = matrix.dot(self.center)
    
    
    def mirror(self):
        """
        See :meth:`MachiningPath.mirror`
        """
        self.start[0] = -self.start[0]
        self.end[0] = -self.end[0]
        self.center[0] = -self.center[0]
        self.ccw = not self.ccw