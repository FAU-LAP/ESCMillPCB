"""
Created on 04.02.2018

@author: Christian Ott
"""

#initialize logging
import logging
logger = logging.getLogger(__name__)

import math
import numpy as np
import pyqtgraph.parametertree.parameterTypes as ptypes
from Algorithms import TSPOptimizer as tsp
from Algorithms import NXUtilities as nxutil


class MachiningOptimizer(object):
    """
    Base class for optimizers, not meant to be used directly.
    Optimizers are used to adjust machining objects, e.g. reorder, adjust sizes, etc.
    """

    def __init__(self, **kargs):
        """
        Constructor
        """
        pass
    
    
    def optimize(self, machiningObject):
        """
        :param Base.MachiningObjects.MachiningObject machiningObject: MachiningObject to optimize
        """
        pass
    
    
    def getName(self):
        """
        :returns: Optimizer's name
        :rtype: str
        """
        return type(self).__name__
    
    
    def updateParameters(self, params):
        """
        Called when the optimizer's parameters have changed. Updates the optimizers internal state.

        :param pyqtgraph.GroupParameter params: GroupParameter containing the settings
        """
        pass

    
    @staticmethod
    def getParameters():
        """
        Static method returning the optimizer's available parameters as a pyqtgraph ParameterGroup.
        :returns: Optimizer parameters or None if there are no available parameters
        :rtype: pyqtgraph.GroupParameter
        """
        return None



class HoleOrderOptimizer(MachiningOptimizer):
    """
    Optimizer for HoleLists, minimizes the hole path.

    +----------------+-----------------------------------------------------------------------------------------+
    | **Options**    |                                                                                         |
    +================+=========================================================================================+
    | **algorithm**  | (string) Default: 2opt                                                                  |
    |                +--------+--------------------------------------------------------------------------------+
    |                | 2opt   | 2opt algorithm starting from random start configurations                       |
    |                |        | Relatively fast with good results.                                             |
    |                |        | Number of iterations defines the number of optimized start configurations,     |
    |                |        | best result is chosen. More iterations is slower but                           |
    |                |        | statistically yields better results                                            |
    |                +--------+--------------------------------------------------------------------------------+
    |                | greedy | Greedy next neighbor algorithm. Fast but moderate results.                     |
    +----------------+--------+--------------------------------------------------------------------------------+
    | **iterations** | (int) Number of iterations depending on the algorithm. Default: 5                       |
    |                +--------+--------------------------------------------------------------------------------+
    |                | 2opt   | Number of random start configurations.                                         |
    |                +--------+--------------------------------------------------------------------------------+
    |                | greedy | Not used.                                                                      |
    +----------------+--------+--------------------------------------------------------------------------------+
    """
    
    def __init__(self, **kargs):
        super().__init__(**kargs)
        self.options = {'active':True, 'algorithm':'2opt', 'iterations':5}
        for key, val in kargs.items():
            self.options[key] = val
    
    
    def optimize(self, holelist):
        """
        :param Base.MachiningObjects.HoleList holelist: HoleList to optimize
        """
        if not self.options['active'] or len(holelist) <= 1:
            return
        logger.info("Running hole order optimization (algorithm %s, %s iterations)...", 
                    self.options['algorithm'], self.options['iterations'])
        # fetch all center positions of all holes
        nodes = np.array([hole.center for hole in holelist])
        # optimize graph
        optimized = None
        if self.options['algorithm'] == '2opt':
            optimized = tsp.twoOpt3(nodes, self.options['iterations'])
        elif self.options['algorithm'] == 'greedy':
            optimized = tsp.greedy(nodes)
        # reorder holes in list
        holelist.reorder(optimized)
        logger.info("Final optimized path length: %.3f", nxutil.pathDistanceFromNodes(nodes, optimized))
        
    
    def updateParameters(self, params):
        """
        See :meth:`MachiningOptimizer.updateParameters`
        """
        self.options['active'] = params.child('Active').value()
        self.options['algorithm'] = params.child('Algorithm').value()
        self.options['iterations'] = params.child('Iterations').value()
    
    
    @staticmethod
    def getParameters():
        """
        See :meth:`MachiningOptimizer.getParameters`
        """
        params = {
            'name':'HoleOrderOptimizer', 'title':'Hole order optimization', 'type':'group', 'children':[
                {'name':'Active', 'type':'bool', 'default':True, 'value':True},
                {'name':'Algorithm', 'type':'list', 'values':['2opt', 'greedy'], 'default':'2opt', 'value':'2opt'},
                {'name':'Iterations', 'type':'int', 'min':1, 'default':20, 'value':20}
            ]
        }
        return ptypes.GroupParameter(**params)
    
    

class MillingCombinationOptimizer(MachiningOptimizer):
    """
    Combines adjacent millings to a single milling path.
    """
    
    def __init__(self, **kargs):
        super().__init__(**kargs)
        self.options = {'active':True}
        for key, val in kargs.items():
            self.options[key] = val
    
    
    def optimize(self, millinglist):
        """
        Path combination: Start at first milling, go to end, search point in milling list which is equal
        to the end point and then add the path to the milling, repeat until there is no follow up point.
        Then start a new milling and repeat the procedure.

        :param Base.MachiningObjects.MillingList millinglist: MillingList to optimize
        """
        if not self.options['active']:
            return
        if not len(millinglist):
            logger.info("No millings to combine.")
            return
        logger.info("Combining adjacent milling paths from %s millings...", len(millinglist))
        currentmill = millinglist.pop()
        newmillings = [currentmill,]
        # repeat until all millings are transfered to the new list
        while len(millinglist):
            logger.debug("Millings to process: %s", len(millinglist))
            found = False
            # go through all remaining millings to find adjacent millings
            for i, mill in enumerate(millinglist):
                logger.debug("Step %s", i)
                if np.all(currentmill.getEnd() == mill.getEnd()):
                    # reverse adjacent milling if necessary
                    logger.debug("Reversing milling.")
                    mill.reverse()
                if np.all(currentmill.getEnd() == mill.getStart()):
                    logger.debug("Found adjacent milling.")
                    # append paths to currently processed milling
                    currentmill.appendMilling(mill)
                    # remove milling from old milling list
                    millinglist.pop(i)
                    found = True
                    break
            # if no adjacent milling has been found and still millings remaining, start new milling
            if not found and len(millinglist):
                logger.debug("Found no adjacent milling, continuing with new milling.")
                currentmill = millinglist.pop()
                newmillings.append(currentmill)
        millinglist.appendList(newmillings)
        logger.info("Remaining separate millings: %s", len(millinglist))
    
    
    def updateParameters(self, params):
        """
        See :meth:`MachiningOptimizer.updateParameters`
        """
        self.options['active'] = params.child('Active').value()
        
        
    @staticmethod
    def getParameters():
        """
        See :meth:`MachiningOptimizer.getParameters`
        """
        params = {
            'name':'MillingCombinationOptimizer', 
            'title':'Combine adjacent millings', 
            'type':'group', 
            'children':[
                {'name':'Active', 'type':'bool', 'default':True, 'value':True}
            ]
        }
        return ptypes.GroupParameter(**params)
    
    
class BreakoutOptimizer(MachiningOptimizer):
    """
    Adds breakouts to millings.
    """
    
    def __init__(self, **kargs):
        super().__init__(**kargs)
        self.options = {'Active':True, 'Distance':100.0, 'Size':2.0, 'Min_number':2, 'Min_cut_length':40.0}
        for key, val in kargs.items():
            self.options[key] = val
    
    
    def optimize(self, millinglist):
        """
        Insert breakout bars into closed milling paths according to the following algorithm:
        First, find closed milling paths (cut-outs) that are longer than Min_cut_length.
        Then check if the path is longer than Min_number * (Distance + Size),
        otherwise divide the cut equally. If it is longer, set a breakout bar after every
        (Distance + Size) distance. Ignore the last possible breakout bar.

        :param Base.MachiningObjects.MillingList millinglist: MillingList to optimize
        """
        if not self.options['Active'] or not len(millinglist):
            return
        logger.info("Inserting breakout bars into cut-outs...")
        logger.debug("Breakout parameters: %s", self.options)
        
        # find cut-outs
        cutouts = []
        for i in reversed(range(0, len(millinglist))):
            milling = millinglist[i]
            if not np.all(milling.getStart() == milling.getEnd()):
                continue 
            if not milling.pathLength() >= self.options['Min_cut_length']:
                continue
            logger.debug("Found cut-out (length: %s).", milling.pathLength())
            millinglist.pop(i)
            cutouts.append(milling)
            
        # process cut-outs
        newMillings = []
        for cutout in cutouts:
            curlen = self.options['Distance']
            ba_size = self.options['Size']
            num_bas = math.floor(cutout.pathLength()/(curlen + ba_size))
            if num_bas < self.options['Min_number']:
                num_bas = self.options['Min_number']
                curlen = cutout.pathLength() / num_bas - ba_size
            logger.debug("Split milling of length %s into %s parts with length %s.", cutout.pathLength(), num_bas, curlen)
            for i in range(num_bas):
                splitMilling = cutout.splitMilling(curlen, ba_size)
                newMillings.append(cutout)
                cutout = splitMilling
            if cutout is not None:
                newMillings.append(cutout)
            
        # update milling list
        millinglist.appendList(newMillings)
        logger.info("Added breakout bars to %s cut-outs.", len(cutouts))
            
            
            
    def updateParameters(self, params):
        """
        See :meth:`MachiningOptimizer.updateParameters`
        """
        for param in params.children():
            self.options[param.name()] = param.value()
                        
    
    @staticmethod
    def getParameters():
        """
        See :meth:`MachiningOptimizer.getParameters`
        """
        params = {
            'name':'BreakoutOptimizer', 
            'title':'Add breakouts to millings',
            'type':'group', 
            'children':[
                {'name':'Active', 'type':'bool', 'default':True, 'value':True},
                {
                    'name':'Distance', 
                    'title':'Breakout distance (mm)', 
                    'type':'float', 
                    'default':100.0, 
                    'value':100.0, 
                    'min':0
                },
                {
                    'name':'Size', 
                    'title':'Breakout size (mm)', 
                    'type':'float', 
                    'default':2.0, 
                    'value':2.0, 
                    'min':0
                },
                {
                    'name':'Min_number', 
                    'title':'Minimal number of breakouts per cut-out', 
                    'type':'int', 
                    'value':2,
                    'min':0
                },
                {
                    'name':'Min_cut_length', 
                    'title':'Minimal cut-out length for breakouts (mm)', 
                    'type':'float', 
                    'value':40.0,
                    'min':0
                }
            ]
        }
        return ptypes.GroupParameter(**params)
    

class MillingOrderOptimizer(MachiningOptimizer):
    """
    Minimizes the jog path between the millings.
    """
    
    def __init__(self, **kargs):
        super().__init__(**kargs)
        self.active = True
        
        
    def optimize(self, millinglist):
        """
        Optimizes the milling order to achieve a minimal jog path length.
        This optimizer uses a simple nearest neighbor approach.

        :param Base.MachiningObjects.MillingList: MillingList to optimize
        """
        if not self.active or len(millinglist) <= 1:
            return
        logger.info("Running milling order optimization...")
        # fetch all start and end positions of all millings
        nodes = (np.array([milling.getStart() for milling in millinglist]), 
                 np.array([milling.getEnd() for milling in millinglist]))
        # optimize graph
        optimized = tsp.greedyTwoPointNodes(nodes)
        # reorder holes in list
        millinglist.reorder(optimized)
        logger.info("Optimized path length: %.3f", nxutil.pathDistanceFromTwoPointNodes(nodes, optimized))
    
    
    def updateParameters(self, params):
        """
        See :meth:`MachiningOptimizer.updateParameters`
        """
        self.active = params['Active']
    
    
    @staticmethod
    def getParameters():
        """
        See :meth:`MachiningOptimizer.getParameters`
        """
        params = {
            'name':'MillingOrderOptimizer',
            'title':'Milling order optimization',
            'type':'group',
            'children':[
                {'name':'Active', 'type':'bool', 'value':True, 'default':True}
            ]
        }
        return ptypes.GroupParameter(**params)
        