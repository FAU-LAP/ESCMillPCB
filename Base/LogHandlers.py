"""
Created on 06.04.2018

@author: Christian Ott
"""

import logging
from PyQt5 import QtGui, QtWidgets


class QListWidgetLogger(logging.Handler):
    """
    Logging handler which prints logs into a QListWidget.
    """
    
    entrybrushes = {
        'DEBUG':QtGui.QBrush(QtGui.QColor(140, 140, 140)),
        'INFO':QtGui.QBrush(QtGui.QColor(0, 0, 0)),
        'WARNING':QtGui.QBrush(QtGui.QColor(230, 114, 0)),
        'ERROR':QtGui.QBrush(QtGui.QColor(150, 0, 0)),
        'CRITICAL':QtGui.QBrush(QtGui.QColor(255, 0, 0))
    }
    
    def __init__(self, widget):
        """
        Constructor

        :param QListWidget widget: ListWidget used to display errors
        """
        super().__init__()
        self.widget = widget
        formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s', '%H:%M:%S')
        self.setFormatter(formatter)
    
    
    def emit(self, record):
        entry = QtWidgets.QListWidgetItem(self.format(record))
        entry.setForeground(self.entrybrushes[record.levelname])
        self.widget.insertItem(0, entry)
        QtWidgets.qApp.processEvents()


#     def write(self, m):
#         pass
    

class TracebackFormatter(logging.Formatter):
    """
    Formatter including an optional traceback for exception logging.
    """
    
    def format(self, record):
        if hasattr(record, "traceback"):
            record.traceback = "\n" + record.traceback
        else:
            record.traceback = ""
        return super().format(record)