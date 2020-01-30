"""
Created on 06.03.2018

@author: Christian Ott
"""

#import logging
#logger = logging.getLogger(__name__)

from PyQt5 import QtWidgets, QtCore


class FocusLineEdit(QtWidgets.QLineEdit):
    """
    QLineEdit that has a clicked signal.

    ======================  ==========================================================================
    **Signals**
    ======================  ==========================================================================
    sigClicked              Emitted when the LineEdit is clicked (on mouseRelease)
    ======================  ==========================================================================
    """
    
    sigFocus = QtCore.pyqtSignal() 

    def __init__(self, parent=None):
        """
        Constructor
        """
        super().__init__(parent)
        
    
    def focusInEvent(self, event):
        super().focusInEvent(event)
        # Only works right when emitted by a timer or it will collide with other events
        QtCore.QTimer.singleShot(0, lambda: self.sigFocus.emit())