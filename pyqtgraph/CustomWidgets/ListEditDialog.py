"""
Created on 28.05.2019

@author: Christian Ott
"""

import logging
logger = logging.getLogger(__name__)

from ..Qt import QtGui, QtCore
from ..parametertree.ParameterTree import ParameterTree
from ..parametertree.Parameter import Parameter


class ListEditDialog(QtGui.QDialog):
    """
    Dialog for editing a list or dict of values. Used by the ListEditButton.
    """

    def __init__(self, parent=None):
        """
        Constructor
        """
        super().__init__(parent)
        #self.ui = uic.loadUi("resources/ui/list_edit_dialog.ui", self)

        self.setObjectName("ListEditDialog")
        self.resize(415, 495)
        self.verticalLayout = QtGui.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.parameterTree = ParameterTree(self)
        self.parameterTree.setObjectName("parameterTree")
        self.verticalLayout.addWidget(self.parameterTree)
        self.buttonBox = QtGui.QDialogButtonBox(self)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel | QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)
        self.buttonBox.accepted.connect(self.buttonBox_accepted)
        self.buttonBox.rejected.connect(self.reject)
        
        self.data = None
        self.canAdd = False
        self.controlType = None
        self.controlOpts = {}
        self.dictmode = False
        
        
    def setData(self, data, controltype, canAdd=False, **opts):
        """
        Sets the list/dict to be edited. Additional parameters are passed to the
        parameter constructor.

        :param data: initial data
        :type data: list or dict
        :param str controltype: type of the used pyqtgraph.parametertree.Parameter
        :param bool canAdd: allow the user to add/remove elements
        """
        self.canAdd = canAdd
        self.controlType = controltype
        self.controlOpts = opts
        self.dictmode = hasattr(data, "items")
        
        self.parameterTree.clear()
        params = []
        if 'value' in opts:
            del opts['value']
        if self.dictmode:
            for key, val in data.items():
                params.append({'type':controltype, 'name':str(key), 'value':val,
                               'renamable':canAdd, 'removable':canAdd, **opts})
        else:
            for i, val in enumerate(data):
                params.append({'type':controltype, 'name':str(i), 'value':val, 'removable':canAdd, **opts})
        self.paramroot = Parameter.create(type='group', name='root', children=params)
        self.paramroot.sigChildRemoved.connect(self.paramroot_sigChildRemoved)
        if canAdd:
            addBtn = Parameter.create(type='action', name='Add new')
            self.paramroot.addChild(addBtn)
            addBtn.sigActivated.connect(self.addNewBtn_sigActivated)
        self.parameterTree.addParameters(self.paramroot, showTop=False)
        
        
    @QtCore.Slot(object)
    def paramroot_sigChildRemoved(self, child):
        if not self.dictmode:
            for i, child in enumerate(self.paramroot.children()):
                if not child.isType("action"):
                    child.setName(str(i))
    
    
    @QtCore.Slot()
    def addNewBtn_sigActivated(self):
        newparam = None
        if self.dictmode:
            newparam = Parameter.create(type=self.controlType, name='new',
                                        renamable=self.canAdd, removable=self.canAdd, 
                                        **self.controlOpts)
        else:
            new = 0
            for child in reversed(self.paramroot.children()):
                if not child.isType("action"):
                    new = int(child.name()) + 1
                    break
            newparam = Parameter.create(type=self.controlType, name=str(new),
                                        renamable=(self.canAdd and self.dictmode), 
                                        removable=self.canAdd, **self.controlOpts)
        self.paramroot.insertChild(len(self.paramroot.children())-1, newparam, True)
        
        
    @QtCore.Slot()
    def buttonBox_accepted(self):
        if self.dictmode:
            self.data = {}
            for child in self.paramroot.children():
                if not child.isType("action"):
                    self.data[child.name()] = child.value()
        else:
            self.data = []
            for child in self.paramroot.children():
                if not child.isType("action"):
                    self.data.append(child.value())
        self.accept()