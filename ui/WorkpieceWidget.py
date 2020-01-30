"""
Created on 15.02.2018

@author: Christian Ott
"""

import logging
logger = logging.getLogger(__name__)

from PyQt5 import QtCore
import pyqtgraph as pg
import numpy as np

from ui import MachiningROIs as mroi
from Base import MachiningObjects as mo
from Base.AppBase import AppBase

class WorkpieceWidget(pg.PlotWidget):
    """
    Plot widget to view machining objects.

    ======================  ==========================================================================
    **Signals**
    ======================  ==========================================================================
    sigGotoActionTriggered  Emitted when the "Go to position" context menu entry is clicked.
                            Carries a dictionary {"pos": (x, y) coordinates of the ROI}
    sigRef1ActionTriggered  Emitted when the "Set reference 1" context menu entry is clicked.
                            Carries a dictionary {"pos": (x, y) coordinates of the ROI, "type":"ref1"}
    sigRef2ActionTriggered  Emitted when the "Set reference 1" context menu entry is clicked.
                            Carries a dictionary {"pos": (x, y) coordinates of the ROI, "type":"ref2"}
    ======================  ==========================================================================
    """
    
    sigGotoActionTriggered = QtCore.pyqtSignal(dict)
    sigRef1ActionTriggered = QtCore.pyqtSignal(dict)
    sigRef2ActionTriggered = QtCore.pyqtSignal(dict)

    def __init__(self, parent=None, **kargs):
        """
        Constructor
        """
        super().__init__(parent, **kargs)
        self.workpiece = None
        self.machiningROIs = []
        self.setAspectLocked()
        if not "showgrid" in kargs.keys():
            kargs["showgrid"] = True
        if not "gridalpha" in kargs.keys():
            kargs["gridalpha"] = 0.2
        if kargs["showgrid"]:
            self.showGrid(x=True, y=True, alpha=kargs["gridalpha"])
        
        # remove Plot Options and Export from context menu
        self.plotItem.ctrlMenu = None
        self.scene().contextMenu = None
        self.laserActive = False
        self.laserOffset = (AppBase.getSettings().value("MachineBase", "laser_offset_x"),
                            AppBase.getSettings().value("MachineBase", "laser_offset_y"))
        self.machinePosROI = mroi.MachinePositionROI(pos=(0, 0))
        self.laserPosROI = mroi.MachinePositionROI(pos=(0, 0), brush=pg.mkBrush("A00"), pen=pg.mkPen(color="A00", width=1))
        self.boardOutlineROI = mroi.WorkpieceOutlineROI()
        self.outlineVisible = False
    
    
    def setWorkpiece(self, workpiece):
        """
        Sets a new workpiece.

        :param workpiece: (Base.Workpiece) New workpiece
        """
        self.workpiece = workpiece
        self.refresh()
        
    
    def setBoardOutlineVisible(self, value):
        """
        Sets if the workpiece (board) outlines are visible.

        :param value: (bool) outlines visible
        """
        self.outlineVisible = value
        self.refresh()
        
    
    def refresh(self):
        """
        Refreshes the workpiece widget, i.e. the machining ROIs are deleted and recreated.
        """
        self.clear()
        self.machiningROIs.clear()
        if self.workpiece is not None:
            self.boardOutlineROI.setPos(self.workpiece.getPosition())
            self.boardOutlineROI.setBoardsize(self.workpiece.getSize())
            self.addItem(self.boardOutlineROI)
            self._addHoles()
            self._addMillings()
            
        self.addItem(self.machinePosROI)
        if self.laserActive:
            self.addItem(self.laserPosROI)

    
    
    def _addHoles(self):
        """
        Adds hole ROIs to widget.
        """
        if not self.workpiece.holeList.active:
            return
        positions = np.empty(shape=(len(self.workpiece.holeList), 2))
        for i, hole in enumerate(self.workpiece.holeList):
            r = mroi.HoleROI(hole.diameter, pos=hole.center, strokewidth=10)
            r.sigGotoActionTriggered.connect(self.machiningROI_sigGotoActionTriggered)
            r.sigRef1ActionTriggered.connect(self.machiningROI_sigRef1ActionTriggered)
            r.sigRef2ActionTriggered.connect(self.machiningROI_sigRef2ActionTriggered)
            positions[i,] = hole.center
            self.addItem(r)
            self.machiningROIs.append(r)
        self.getPlotItem().plot(positions, pen=pg.mkPen("r"))
        
    
    def _addMillings(self):
        """
        Adds milling ROIs to widget.
        """
        if not self.workpiece.millingList.active:
            return
        positions = np.empty(shape=(len(self.workpiece.millingList), 4))
        for i, milling in enumerate(self.workpiece.millingList):
            infeed = True
            outfeed = False
            positions[i,] = [*milling.getStart(), *milling.getEnd()]
            for k, path in enumerate(milling):
                if k == len(milling)-1:
                    outfeed = True
                if isinstance(path, mo.StraightPath):
                    r = mroi.StraightMillingROI(path.start, path.end, infeed, outfeed, strokewidth=10)
                    self.addItem(r)
                elif isinstance(path, mo.ArcPath):
                    r = mroi.ArcMillingROI(path.start, path.end, path.center, path.angle, path.ccw, infeed, outfeed, strokewidth=10)
                    self.addItem(r)
                infeed = False
        for i in range(positions.shape[0]-1):
            link = np.array([positions[i, 2:4], positions[i+1, 0:2]])
            self.getPlotItem().plot(link, pen=pg.mkPen("b"))
    
          
    def showEvent(self, event):
        super().showEvent(event)
        # MainWindow signals
        #AppBase.getMainwindow().sigNewWorkpiece.connect(self.mainwindow_sigNewWorkpiece)
        AppBase.getMainwindow().sigCorrectionChanged.connect(self.mainwindow_sigCorrectionChanged)
        AppBase.getSettings().sigMachineChanged.connect(self.settings_sigMachineChanged)
        AppBase.getSettings().sigSettingsChanged.connect(self.settings_sigSettingsChanged)
        AppBase.getMainwindow().sigLaserCrosshairChanged.connect(self.mainwindow_sigLaserCrosshairChanged)
    
        
    @QtCore.pyqtSlot(dict)
    def machiningROI_sigGotoActionTriggered(self, data):
        self.sigGotoActionTriggered.emit(data)
        
    @QtCore.pyqtSlot(dict)
    def machiningROI_sigRef1ActionTriggered(self, data):
        self.sigRef1ActionTriggered.emit(data)
        
    @QtCore.pyqtSlot(dict)
    def machiningROI_sigRef2ActionTriggered(self, data):
        self.sigRef2ActionTriggered.emit(data)
        
    
    @QtCore.pyqtSlot(dict)
    def machine_sigNewCoordinates(self, coords):
        self.machinePosROI.setPos(coords['workpiece'])
        self.laserPosROI.setPos(coords['workpiece'][0]-self.laserOffset[0], coords['workpiece'][1]-self.laserOffset[1])
                 
    @QtCore.pyqtSlot(bool)
    def mainwindow_sigLaserCrosshairChanged(self, checked):
        self.laserActive = checked
        self.refresh()
        
        
    @QtCore.pyqtSlot()
    def mainwindow_sigCorrectionChanged(self):
        self.refresh()
        
    
    @QtCore.pyqtSlot()
    def settings_sigMachineChanged(self):
        machine = AppBase.getMachine()
        if machine is not None:
            machine.sigNewCoordinates.connect(self.machine_sigNewCoordinates)
            
            
    @QtCore.pyqtSlot(list)
    def settings_sigSettingsChanged(self, changed):
        if 'MachineBase' in changed:
            self.laserOffset = (AppBase.getSettings().value('MachineBase', 'laser_offset_x'),
                                AppBase.getSettings().value('MachineBase', 'laser_offset_y'))
        self.refresh()