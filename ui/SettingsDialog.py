"""
Created on 05.03.2018

@author: Christian Ott
"""

import logging
logger = logging.getLogger(__name__)

from PyQt5 import QtWidgets, QtCore
from Base.AppBase import AppBase

from ui.templates.Ui_SettingsDialog import Ui_SettingsDialog


class SettingsDialog(QtWidgets.QDialog, Ui_SettingsDialog):
    """
    Main settings dialog.
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.CustomizeWindowHint | QtCore.Qt.WindowTitleHint);
        
        self.settings = AppBase.getSettings().copySettings()
        self.paramsSoftwareSettings.addParameters(self.settings.child("General"))
        self.paramsSoftwareSettings.addParameters(self.settings.child("Optimizers"))
        
        self.paramsMachineBasic.setParameters(self.settings.child("MachineBase"), showTop=True)
        
        self.btnApplyMachineParams.clicked.connect(self.btnApplyMachineParams_clicked)
        self.btnReadMachineParams.clicked.connect(self.btnReadMachineParams_clicked)
        
        self.settings.sigTreeStateChanged.connect(self.params_changed)
        
        machine = AppBase.getMachine()
        self.machineName = ""
        if machine is not None:
            self.machineName = machine.getName()
        
        self.comboMachine.addItems(AppBase.getSettings().machines.keys())
        self.comboMachine.setCurrentText(self.machineName)
        self.comboMachine.currentTextChanged.connect(self.comboMachine_textChanged)
        
        self.machineChanged = False
        self.settingsChanged = []
        
        self.updateMachineParams()
        
    
    def updateMachineParams(self):
        if self.machineName != "" and self.machineName != "None":
            logger.debug("Updating machine params for machine %s", self.machineName)
            AppBase.getMachineType(self.machineName).updateComParameters(self.settings.child("MachineCom", self.machineName))
            self.paramsMachineCom.setParameters(self.settings.child("MachineCom", self.machineName), showTop=False)
            self.paramsMachineAdvanced.setParameters(self.settings.child("MachineParams", self.machineName), showTop=False)
        else:
            self.paramsMachineCom.clear()
            self.paramsMachineAdvanced.clear()
             
    
    def checkMachineChanged(self):
        machine = AppBase.getMachine()
        machineName = ""
        if machine is not None:
            machineName = machine.getName()
        if machineName != self.machineName or 'MachineCom' in self.settingsChanged:
            self.machineChanged = True
        else:
            self.machineChanged = False
        
    @QtCore.pyqtSlot(str)
    def comboMachine_textChanged(self, machineName):
        self.machineName = machineName
        self.checkMachineChanged()
        self.updateMachineParams()
        
        
    @QtCore.pyqtSlot()
    def btnApplyMachineParams_clicked(self):
        apply = True
        if not AppBase.getMachine().isInitialized():
            result = QtWidgets.QMessageBox.question( self, "Connect to machine",
                     "The machine is not initialized.\nIntialize now?")
            if result == QtWidgets.QMessageBox.Yes:
                AppBase.changeMachine(self.machineName, init=True, setup=False, signal=True)
            else:
                apply = False
        if apply:
            AppBase.setupMachine()
        
    
    @QtCore.pyqtSlot()
    def btnReadMachineParams_clicked(self):
        params = AppBase.getMachine().retrieveParameters()
        self.settings.child('MachineParams').restoreState(params.saveState())
        
    
    @QtCore.pyqtSlot(object, object)
    def params_changed(self, param, changes):
        for param, change, data in changes:
            path = self.settings.childPath(param)
            if path is not None:
                if not path[0] in self.settingsChanged:
                    self.settingsChanged.append(path[0])