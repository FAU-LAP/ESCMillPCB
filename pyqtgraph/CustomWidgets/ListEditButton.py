"""
Created on 06.05.2019

@author: Christian Ott
"""

import logging
logger = logging.getLogger(__name__)

from ..Qt import QtGui, QtCore
from ..flowchart.FlowchartCtrlLibrary import FlowchartCtrlLibrary
from .ListEditDialog import ListEditDialog


class ListEditButton(QtGui.QPushButton):
    """
    Button which stores a list/dict and allows editing of this list/dict
    via a ListEditDialog. This widget is prepared for use in
    pyqtgraph CtrlNodes.

    Additional options:
    * controltype: type of control (valid pyqtgraph parametertree type), mandatory
    * canAdd: allow adding of list/dict entries (default: False)
    * value: initial value of the list/dict (default: None)
    """
    
    sigValueChanged = QtCore.pyqtSignal(object)

    def __init__(self, controltype, canAdd=False, **opts):
        """
        Constructor
        """
        super().__init__()
        self.clicked.connect(self.self_clicked)
        self._value = None
        self.controlType = controltype
        self.controlOpts = opts
        self.canAdd = canAdd
        self.setText('Edit...')
        
        
    def value(self):
        """
        :returns: list/dict associated with this button
        """
        return self._value
    
    
    def setValue(self, value, signal=True):
        """
        :param value:  list/dict to edit
        """
        logger.debug("ListEditButton value set to %s (signaling=%s)", value, signal)
        self._value = value
        self.sigValueChanged.emit(self)
        
    
    def widgetGroupInterface(self):
        """
        Necessary for pyqtgraph.WidgetGroup
        """
        return (self.sigValueChanged, self.value, lambda w, value: w.setValue(value, False))
    
        
    @QtCore.Slot()
    def self_clicked(self):
        dlg = ListEditDialog()
        dlg.setData(self._value, self.controlType, self.canAdd, **self.controlOpts)
        if dlg.exec() == QtGui.QDialog.Accepted:
            self._value = dlg.data
            self.sigValueChanged.emit(self)
            

def createListEditButton(opts):
    """
    ListEditButton factory function.
    """
    if not 'opts' in opts:
        opts['opts'] = {}
    if not 'canAdd' in opts:
        opts['canAdd'] = False
    w = ListEditButton(opts['controltype'], opts['canAdd'], **opts['opts'])
    if 'value' in opts:
        w.setValue(opts['value'])
    return w
        
FlowchartCtrlLibrary.registerCtrlType('listedit', ListEditButton, createListEditButton)