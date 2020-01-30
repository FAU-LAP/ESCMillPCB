"""
Created on 14.02.2018

@author: Christian Ott
"""

import numpy as np

from Base import MachiningObjects as mo
from Base import BaseOptimizers as bo


class Workpiece(object):
    """
    Central class managing the workpiece.
    Contains machining objects and handles coordinate corrections system.
    """
 
    def __init__(self, size=(0, 0)):
        """
        Constructor

        :param size: (width, height) size of the board
        :type size: tuple(float, float)
        """
        self.holeList = mo.HoleList()
        self.holeList.appendOptimizer(bo.HoleOrderOptimizer())
        self.millingList = mo.MillingList()
        self.millingList.appendOptimizer(bo.MillingCombinationOptimizer())
        self.millingList.appendOptimizer(bo.BreakoutOptimizer())
        self.millingList.appendOptimizer(bo.MillingOrderOptimizer())
        self.position = np.array([0, 0])
        self.size = np.array(size)
        
    
    def getPosition(self):
        """
        :returns: coordinates of the lower left corner of the board outlines
        :rtype: tuple(float, float)
        """
        return self.position[:]
    
    def getSize(self):
        """
        :returns: (width, height) size of the board outlines
        :rtype: tuple(float, float)
        """
        return self.size[:]
    
    def setSize(self, size):
        """
        :param size: (width, height) size of the board outlines
        :type size: tuple(float, float)
        """
        self.size = size[:]
        
        
    def appendHole(self, hole):
        """
        Add hole to the workpiece's hole list

        :param Base.MachiningObjects.Hole hole: Hole object to append
        """
        self.holeList.append(hole)
        
        
    def appendMilling(self, milling):
        """
        Add milling to the workpiece's hole list

        :param Base.MachiningObjects.Milling milling: Milling object to append
        """
        self.millingList.append(milling)
        
        
    def optimize(self):
        """
        Runs all optimizers.
        """
        self.holeList.optimize()
        self.millingList.optimize()
        
        
    def planMachining(self, machine):
        """
        Plan machining.

        :param Base.MachineBase.MachineBase machine: Active machine
        """
        machine.preparePlanner()
        self.holeList.planMotion(machine)
        self.millingList.planMotion(machine)
        machine.finalizePlanner()
        
        
    def updateOptimizers(self, params):
        """
        Update parameters of all optimizers.

        :param pyqtgraph.GroupParameter params: GroupParameter containing the optimizer parameters
        """
        self.holeList.updateOptimizers(params)
        self.millingList.updateOptimizers(params)
        
        
    def translate(self, offset):
        """
        Translates all machining objects by a given offset.

        :param offset: (x, y) offset for translation
        :type offset: tuple(float, float)
        """
        self.holeList.translate(offset)
        self.millingList.translate(offset)
        self.position = self.position + offset
        
        
    def transform(self, matrix):
        """
        Transforms all machining objects with a transformation matrix.

        :param matrix: (2x2) transformation matrix
        :rtype: np.ndarray(float)
        """
        self.holeList.transform(matrix)
        self.millingList.transform(matrix)
        
        
    def mirror(self):
        """
        Mirrors all machining objects around the y-axis.
        """
        self.holeList.mirror()
        self.millingList.mirror()
        self.holeList.translate((self.getSize()[0], 0))
        self.millingList.translate((self.getSize()[0], 0))