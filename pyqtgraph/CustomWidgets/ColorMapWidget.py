"""
Created on 01.05.2019

@author: ot34uleh
"""

import logging
logger = logging.getLogger(__name__)

from ..Qt import QtGui, QtCore
from .. import GradientWidget, ColorMap
from ..graphicsItems.GradientEditorItem import Gradients
from ..parametertree import Parameter, registerParameterType
from ..parametertree.parameterTypes import WidgetParameterItem
from ..flowchart.FlowchartCtrlLibrary import FlowchartCtrlLibrary

if not 'default' in Gradients.keys():
    Gradients['default'] = {'ticks':[(0.0, (196, 0, 255, 255)), (0.5, (0, 188, 129, 255)), (1.0, (255, 0, 0, 255))], 
                            'mode':'rgb'}
    

class ColorMapWidget(GradientWidget):
    """
    Custom implementation of pyqtgraph's GradientWidget.
    In contrast to the original GradientWidget, additional stops are
    inserted by the context menu and not by clicking on the gradient.

    This version is prepared to be used in a pyqtgraph WidgetGroup and as a
    control in pyqtgraph CtrlNodes. Can also be used in a pyqtgraph ParameterTree.

    Possible options:
    * value: intial value (default: default gradient)
    * alpha: set global alpha parameter (default: 0)
    """

    def __init__(self, parent=None, orientation='bottom', *args, **kargs):
        """
        Constructor

        All parameters are passed to pyqtgraph.GradientWidget.
        """
        if not 'allowAdd' in kargs.keys():
            kargs['allowAdd'] = False
        super().__init__(parent, orientation, *args, **kargs)
        self.item.loadPreset('default')
        # add additional "Add tick" menu entry to context menu
        self.newTickAction = QtGui.QAction("Add Tick")
        self.item.menu.addSeparator()
        self.item.menu.addAction(self.newTickAction)
        self.newTickAction.triggered.connect(self.newTickAction_triggered)
        
        if 'alpha' in kargs:
            self.setAlpha(kargs['alpha'])
        if 'value' in kargs:
            self.setValue(kargs['value'])
        
        
    def setAlpha(self, alpha):
        """
        Convinience function which sets the alpha value of all colors in the ramp.

        :param int alpha: overrides all alpha values
        """
        colors = self.colormap().getStops(ColorMap.BYTE)
        colors[1][:,3] = alpha
        self.setColormap(ColorMap(colors[0], colors[1]))
        
        
    def colormap(self):
        """
        :returns: current color map
        :rtype: pyqtgraph.ColorMap
        """
        return self.item.colorMap()
    
    
    def setColormap(self, colormap):
        """
        Sets the current color map.

        :param pyqtgraph.ColorMap colormap: new color map
        """
        self.item.setColorMap(colormap)
        
        
    def value(self):
        """
        :returns: color map in JSON serializable data type
        """
        stops = self.colormap().getStops(ColorMap.BYTE)
        return (stops[0].tolist(), stops[1].tolist())
    
    
    def setValue(self, colors):
        """
        Set the current color map from a JSON serializable data type

        :param colors: tuple(stops, list[colors])
        :type colors: tuble(list[float], list[np.ndarray])
        """
        self.setColormap(ColorMap(colors[0], colors[1]))
    
    
    def widgetGroupInterface(self):
        return (self.sigGradientChangeFinished, self.value, self.setValue)
    
    
    @QtCore.Slot()
    def newTickAction_triggered(self):
        self.item.addTick(0.5)
        
FlowchartCtrlLibrary.registerCtrlType('colormap', ColorMapWidget)
        
        
class ColorMapWidgetParameterItem(WidgetParameterItem):
    """
    UI for ColorMapWidgetParameter
    """
    def __init__(self, param, depth):
        super().__init__(param, depth)
    
    def makeWidget(self):
        widget = ColorMapWidget()
        widget.sigChanged = widget.sigGradientChangeFinished
        widget.sigChanging = widget.sigGradientChanged
        self.hideWidget = False
        return widget
        

class ColorMapWidgetParameter(Parameter):
    """
    Used for displaying a ColorMapWidget within a pyqtgraph ParameterTree.
    """
    itemClass = ColorMapWidgetParameterItem
    
    def __init__(self, **opts):
        if not 'default' in opts:
            opts['default'] = ColorMapWidget().value()
        super().__init__(**opts)
    
registerParameterType('colormapwidget', ColorMapWidgetParameter, override=True)