"""
Created on 06.02.2018

@author: Christian Ott
"""

#initialize logging
import logging
logger = logging.getLogger(__name__)

import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets
from pyqtgraph import ROI, Point, mkPen, mkBrush
from Base import Utility


class MachiningROI(ROI):
    """
    Base class for MachiningROIs, handles drawing and general behavior.

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
    
    def __init__(self, pos, highlightpen=None, strokewidth=1, contextmenu=True, brush=None, **kargs):
        """
        Constructor

        :param pos: (float, float) Position of the ROI's origin
        :param highlightpen: (QtPen) Used for highlighting on hover.
                             Default is mkPen(255, 0, 0, width=1.5)
        :param strokewidth: (float) Thickness of the stroke used for mouse hover detection.
        :param contextmenu: (bool) Determines if the ROI has a context menu
        :param \*\*kargs: Arguments passed to ROI.__init__()
        """
        if not "pen" in kargs.keys():
            kargs["pen"] = mkPen(color="k", width=1.5)
        if not "movable" in kargs.keys():
            kargs["movable"] = False
        self._outline = None
        self._shape = None
        super().__init__(pos, **kargs)
        if highlightpen == None:
            highlightpen = mkPen(255, 0, 0, width=1.5)
        self.highlightpen = highlightpen
        self.strokewidth = strokewidth
        self.currentBrush = brush
        self.contextmenu = contextmenu
        self.menuActive = False
        if contextmenu:
            self.setAcceptedMouseButtons(QtCore.Qt.RightButton)
        self.sigRegionChanged.connect(self.invalidate)
        self.menu = None
        self.ref1Action = None
        self.ref2Action = None
        self.gotoAction = None
        

    def _makePen(self):
        """
        Generate the pen color for this ROI based on its current state (e.g. hover).
        """
        if self.mouseHovering or self.menuActive:
            return self.highlightpen
        else:
            return self.pen
    
            
    def boundingRect(self):
        """
        (override) Calculates the bounding rectangle for drawing.
        """
        return self.shape().boundingRect()
    
    
    def invalidate(self):
        """
        (override) Causes a redraw of the ROI.
        """
        self._shape = None
        self._outline = None
        self.prepareGeometryChange()
        
        
    def outline(self):
        """
        Returns a QPainterPath marking the outline of the ROI.
        Is overridden by subclasses to define their geometry.
        """
        p = QtGui.QPainterPath()
        return p
    
    
    def shape(self):
        """
        (override) Uses self.outline() to define the shape of the ROI (e.g. for mouse hover detection).
        """
        if self._outline is None:
            self._outline = self.outline()
        p = self._outline
        p = self.mapToDevice(p)
        stroker = QtGui.QPainterPathStroker()
        stroker.setWidth(self.strokewidth)
        outline = stroker.createStroke(p)
        self._shape = self.mapFromDevice(outline)     
        return self._shape
    
    
    def paint(self, p, *args):
        """
        (override) Draws the ROI.

        :param p: (QPainter) Painter used for drawing.
        :param \*args: Unused (TODO ??)
        """
        if self._outline is None:
            self._outline = self.outline()
        p.setRenderHint(QtGui.QPainter.Antialiasing)
        p.setPen(self.currentPen)
        if self.currentBrush is not None:
            p.setBrush(self.currentBrush)
        p.drawPath(self._outline)
        
        
    def contextMenuEnabled(self):
        """
        (override) Determines if the ROI has a context menu.
        """
        return self.contextmenu
    
    
    def getMenu(self):
        """
        (override) Returns the ROIs context menu.
        """
        if self.menu is None:
            self.menu = QtWidgets.QMenu()
            self.gotoAction = QtWidgets.QAction("Move to position", self.menu)
            self.gotoAction.triggered.connect(self.gotoAction_triggered)
            self.ref1Action = QtWidgets.QAction("Set as origin", self.menu)
            self.ref1Action.triggered.connect(self.ref1Action_triggered)
            self.ref2Action = QtWidgets.QAction("Set as reference", self.menu)
            self.ref2Action.triggered.connect(self.ref2Action_triggered)
            self.menu.addAction(self.gotoAction)
            self.menu.addSeparator()
            self.menu.addAction(self.ref1Action)
            self.menu.addAction(self.ref2Action)
            self.menu.aboutToShow.connect(self.menu_aboutToShow)
            self.menu.aboutToHide.connect(self.menu_aboutToHide)
        return self.menu
    
    
    def enableMenuItems(self, goto=None, ref1=None, ref2=None):
        """
        Enables/disables context menu items. "None" arguments are ignored.

        :param goto: (bool) Enable "Go to position" menu item
        :param ref1: (bool) Enable "Set as reference 1" menu item
        :param ref2: (bool) Enable "Set as reference 2" menu item
        """
        if goto is not None:
            self.gotoAction.setEnabled(goto)
        if ref1 is not None:
            self.ref1Action.setEnabled(ref1)
        if ref2 is not None:
            self.ref2Action.setEnabled(ref2)
    
    
    @QtCore.pyqtSlot()
    def menu_aboutToShow(self):
        self.menuActive = True
    
    @QtCore.pyqtSlot()
    def menu_aboutToHide(self):
        self.menuActive = False
        self.setMouseHover(True)
        self.setMouseHover(False)
        self.update()
        
    @QtCore.pyqtSlot()
    def gotoAction_triggered(self):
        self.sigGotoActionTriggered.emit({'pos':self.pos()})
        
    @QtCore.pyqtSlot()
    def ref1Action_triggered(self):
        self.sigRef1ActionTriggered.emit({'pos':self.pos(), 'type':'ref1'})
        
    @QtCore.pyqtSlot()
    def ref2Action_triggered(self):
        self.sigRef2ActionTriggered.emit({'pos':self.pos(), 'type':'ref2'})
        
        

class HoleROI(MachiningROI):
    """
    pyqtgraph ROI for holes
    """

    def __init__(self, diameter, pos, crsize=None, **kargs):
        """
        Constructor

        :param diameter: (float) Diameter of the hole.
        :param pos: (float, float) Position of the hole center.
        :param crsize: (float) Size of the crosshair arms. Default (None): crsize=diameter
        :param \*\*kargs: Arguments passed to MachiningROI.__init__()
        """
        if crsize == None:
            crsize = diameter
        kargs["size"] = [max(diameter, crsize), max(diameter, crsize)]
        self.diameter = diameter
        self.crsize = crsize
        super().__init__(pos, **kargs)
    
    
    def outline(self):
        """
        See MachiningROI.outline()
        """
        p = QtGui.QPainterPath()
        p.moveTo(Point(0, -self.crsize))
        p.lineTo(Point(0, self.crsize))
        p.moveTo(Point(-self.crsize, 0))
        p.lineTo(Point(self.crsize, 0))
        p.moveTo(Point(0, 0))
        p.addEllipse(QtCore.QRectF(-self.diameter/2, -self.diameter/2, self.diameter, self.diameter))
        return p
        
        
    
class StraightMillingROI(MachiningROI):
    """
    pyqtgraph ROI for straight milling paths.
    """
    
    def __init__(self, start, end, infeed=False, outfeed=False, **kargs):
        """
        Constructor

        :param start: (float, float) Coordinates of the start point.
        :param end: (float, float) Coordinates of the end point.
        :param infeed: (bool) Draw infeed marker.
        :param outfeed: (bool) Draw outfeed marker.
        """
        # origin is starting point
        pos = start
        if not "contextmenu" in kargs.keys():
            kargs['contextmenu'] = False
        super().__init__(pos, **kargs)
        
        self.start = np.array(start)
        self.end = np.array(end)
        self.infeed = infeed
        self.outfeed = outfeed
        self._endPoint = Point(*(self.end-self.start))
    
    
    def outline(self):
        """
        See MachiningROI.outline()
        """
        p = QtGui.QPainterPath()
        p.moveTo(Point(0, 0))
        p.lineTo(self._endPoint)
        if self.infeed:
            p.addPolygon(Utility.createSimpleTriangle((0,0), 1, 1, "down"))
        if self.outfeed:
            p.addPolygon(Utility.createSimpleTriangle(self._endPoint, 1, 1, "up"))
        return p

             
            
class ArcMillingROI(MachiningROI):
    """
    pyqtgraph ROI for arc milling paths.
    """
    
    def __init__(self, start, end, center, angle, ccw=True, infeed=False, outfeed=False, **kargs):
        """
        Constructor
        Full circles have start = end. Causes an error if end does not lie on the circle.

        :param start: (float, float) Coordinates of the start point
        :param end: (float, float) Coordinates of the end point
        :param center: (float, float) Coordinates of the arc's center
        :param angle: (float) absolute value of the arc's opening angle
        :param ccw: (bool) States if the arc path is to be drawn counterclockwise (default: True)
        :param infeed: (bool) Draw infeed marker (default: False)
        :param outfeed: (bool) Draw outfeed marker (default: False)
        """
        # origin is arc center
        pos = center
        if not "contextmenu" in kargs.keys():
            kargs['contextmenu'] = False
        super().__init__(pos, **kargs)
        
        self.start = np.array(start)
        self.end = np.array(end)
        self.center = np.array(center)
        self.angle = np.abs(angle)
        self.infeed = infeed
        self.outfeed = outfeed
        
        self._startrel = self.start-self.center
        self._endrel = self.end-self.center
        self._radius = np.linalg.norm(self._startrel)
        
        # NOTE:
        # Despite the Qt docs claiming otherwise, angles seem to be measured CLOCKWISE in Qt!
        # This means the starting angle as well as the angle length have to be negated as
        # the arctan2 function (and I) use the usual counterclockwise measurement.
        # I do not know why the behavior differs from the documented one, might also be hidden in pyqtgraph...
        # Note also, that Qt measures angles in deg (unusual, but documented).
        
        # calculate angle between x-axis and start leg
        self._startangle = np.arctan2(self._startrel[1], self._startrel[0]) # np.arccos(self._startrel.dot((1, 0))/self._radius)
        if self._startangle < 0:
            self._startangle += 2*np.pi
        self._startangleQt = -Utility.radToDeg(self._startangle)

        self._anglelengthQt = Utility.radToDeg(self.angle)
        # counterclockwise -> negative angle
        if ccw:
            self._anglelengthQt *= -1


    def outline(self):
        """
        See MachiningROI.outline()
        """
        logger.debug("Drawing arc from %s to %s (%s -(%s)-> %s)", self._startrel, self._endrel, self._startangleQt, 
                     self._anglelengthQt, self._startangleQt+self._anglelengthQt)
        p = QtGui.QPainterPath()
        p.moveTo(Point(*self._startrel))
        box = QtCore.QRectF(-self._radius, -self._radius, 2*self._radius, 2*self._radius)
        p.arcTo(box, self._startangleQt, self._anglelengthQt)
        if self.infeed:
            p.addPolygon(Utility.createSimpleTriangle(self._startrel, 1, 1, "down"))
        if self.outfeed:
            p.addPolygon(Utility.createSimpleTriangle(self._endrel, 1, 1, "up"))
        return p
    
    
    
class MachinePositionROI(MachiningROI):
    """
    pyqtgraph ROI indicating current machine position
    """
    
    def __init__(self, pos=(0, 0), theight=4, twidth=1, **kargs):
        if not "contextmenu" in kargs.keys():
            kargs["contextmenu"] = False
        if not "pen" in kargs.keys():
            kargs["pen"] = mkPen(color="466646", width=1)
        if not "brush" in kargs.keys():
            kargs["brush"] = mkBrush("466646")
        super().__init__(pos, **kargs)
        self.theight = theight
        self.twidth = twidth
        
        
    def outline(self):
        """
        See MachiningROI.outline()
        """
        p = QtGui.QPainterPath()
        p.addPolygon(Utility.createSimpleTriangle([0, self.theight/2], self.twidth, self.theight, orientation="down"))
        return p
    
    
class WorkpieceOutlineROI(MachiningROI):
    """
    pyqtgraph ROI indicating the workpiece (board) outlines.
    """
    
    def __init__(self, boardsize=(0,0), pos=(0, 0), **kargs):
        if not "contextmenu" in kargs.keys():
            kargs["contextmenu"] = False
        if not "pen" in kargs.keys():
            kargs["pen"] = mkPen(color="AAA", width=3)
        super().__init__(pos, **kargs)
        self.boardsize = boardsize[:]
        
    
    def setBoardsize(self, size):
        """
        :param size: (float, float) (width, height) of the workpiece (board)
        """
        self.boardsize = size[:]
        
        
    def outline(self):
        """
        See MachiningROI.outline()
        """
        p = QtGui.QPainterPath()
        p.addRect(0, 0, *self.boardsize)
        return p
    