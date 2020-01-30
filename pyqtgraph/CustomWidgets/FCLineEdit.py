"""
Created on 15.05.2019

@author: ot34uleh
"""

import logging
logger = logging.getLogger(__name__)

from ..Qt import QtGui
from ..flowchart.FlowchartCtrlLibrary import FlowchartCtrlLibrary


class FCLineEdit(QtGui.QLineEdit):
    """
    Due to some bug in the interplay between pyqtgraph's flowchart library and
    its WidgetGroup, QLineEdits have data synchronization problems when used
    in a flowchart node (values are lost when not entered by the user, as the
    editingChanged signal is not emitted on programmatic changes).
    This wrapper class accounts for this problem.

    Possible options:
    * value: initial value (default: '')
    """

    def __init__(self, parent=None, **kargs):
        """
        Constructor
        """
        super().__init__(parent)
        if 'value' in kargs:
            self.setText(kargs['value'])
            
        
    def widgetGroupInterface(self):
        return (self.textChanged, FCLineEdit.text, FCLineEdit.setText)
    
    
    
FlowchartCtrlLibrary.registerCtrlType('str', FCLineEdit)