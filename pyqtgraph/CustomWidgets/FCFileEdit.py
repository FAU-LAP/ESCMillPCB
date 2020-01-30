"""
Created on 28.05.2019

@author: Christian Ott
"""

import logging
logger = logging.getLogger(__name__)

from ..Qt import QtGui, QtCore
from ..flowchart.FlowchartCtrlLibrary import FlowchartCtrlLibrary


class FCFileEdit(QtGui.QWidget):
    """
    Line edit with file dialog button for CtrlNodes.

    Possible options:
    * value: initial value (default: '')
    * mode: browse mode (default: 'ExistingFile')
    * dir: initial directory (default: '')
    """
    
    browseModes = {
        'AnyFile': QtGui.QFileDialog.AnyFile,
        'ExistingFile': QtGui.QFileDialog.ExistingFile,
        'Directory': QtGui.QFileDialog.Directory,
        'ExistingFiles':QtGui.QFileDialog.ExistingFiles
    }
    
    
    def __init__(self, parent=None, **kargs):
        """
        Constructor
        """
        super().__init__(parent)
        # initialize UI
        self.formLayout = QtGui.QHBoxLayout(self)
        self.pathEdit = QtGui.QLineEdit(self)
        self.browseButton = QtGui.QPushButton(self)
        self.browseButton.setMaximumSize(25, 20)
        self.browseButton.setText('...')
        self.browseButton.clicked.connect(self.browseButton_clicked)
        self.formLayout.addWidget(self.pathEdit)
        self.formLayout.addWidget(self.browseButton)
        self.setLayout(self.formLayout)
        # initialize class data
        self.browseMode = QtGui.QFileDialog.ExistingFile
        self.initialDir = ''
        
        if 'value' in kargs:
            self.setValue(kargs['value'])
        if 'mode' in kargs:
            self.setBrowseMode(kargs['mode'])
        if 'dir' in kargs:
            self.setInitalDirectory(kargs['dir'])
    
    
    def setBrowseMode(self, browseMode):
        """
        Sets the browse mode.

        :param str browseMode: Possible values: AnyFile, ExistingFile, Directory, ExistingFiles
        """
        self.browseMode = self.browseModes[browseMode]
        
        
    def setInitialDirectory(self, directory):
        """
        Sets the initial directory of the file dialog.

        :param str directory: path to the initial directory
        """
        self.initialDir = directory
               
               
    def setValue(self, value):
        """
        :param str value: new value (path) of the FCFileEdit
        """
        self.pathEdit.setText(value)
        
        
    def value(self):
        """
        :returns: value of the FCFileEdit
        :rtype: str
        """
        return self.pathEdit.text()


    def widgetGroupInterface(self):
        return (self.pathEdit.textChanged, self.value, self.setValue)
    
    
    @QtCore.Slot()
    def browseButton_clicked(self):
        dlg = QtGui.QFileDialog()
        dlg.setFileMode(self.browseMode)
        dlg.setDirectory(self.initialDir)
        value = ''
        if dlg.exec() == dlg.Accepted:
            value = ';'.join(dlg.selectedFiles())
            self.setValue(value)
        
        
        
FlowchartCtrlLibrary.registerCtrlType('file', FCFileEdit)