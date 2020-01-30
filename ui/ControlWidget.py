"""
Created on 03.03.2018

@author: Christian Ott
"""

import logging
logger = logging.getLogger(__name__)

import numpy as np
from PyQt5 import QtWidgets, QtCore, QtGui
from Base.AppBase import AppBase
from ui.templates.Ui_ControlWidget import Ui_ControlWidget

class ControlWidget(QtWidgets.QWidget, Ui_ControlWidget):
    """
    Machine control widget for the main window.

    ========================  =============================================================================
    **Signals**
    ========================  =============================================================================
    sigLaserCrosshairChanged  Emitted when the laser crosshair checkbox is changed.
                              Carries a bool indicating the checkbox state.
    ========================  =============================================================================
    """
    
    sigLaserCrosshairChanged = QtCore.pyqtSignal(bool)

    def __init__(self, parent=None):
        """
        Constructor
        """
        super().__init__(parent)
        self.setupUi(self)
        self.__initialized = False
        
        # Button Icons
        self.btnJogUp.setIcon(QtGui.QIcon(":/root/images/Arrow_Up.png"))
        self.btnJogRightUp.setIcon(QtGui.QIcon(":/root/images/Arrow_Right_Up.png"))
        self.btnJogRight.setIcon(QtGui.QIcon(":/root/images/Arrow_Right.png"))
        self.btnJogRightDown.setIcon(QtGui.QIcon(":/root/images/Arrow_Right_Down.png"))
        self.btnJogDown.setIcon(QtGui.QIcon(":/root/images/Arrow_Down.png"))
        self.btnJogLeftDown.setIcon(QtGui.QIcon(":/root/images/Arrow_Left_Down.png"))
        self.btnJogLeft.setIcon(QtGui.QIcon(":/root/images/Arrow_Left.png"))
        self.btnJogLeftUp.setIcon(QtGui.QIcon(":/root/images/Arrow_Left_Up.png"))
        self.btnJogZUp.setIcon(QtGui.QIcon(":/root/images/Arrow_Z_Up.png"))
        self.btnJogZDown.setIcon(QtGui.QIcon(":/root/images/Arrow_Z_Down.png"))
        self.btnStop.setIcon(QtGui.QIcon(":/root/images/Stop.png"))
        
        # set validators for coordinate inputs
        validator = QtGui.QDoubleValidator()
        self.txtGotoX.setValidator(validator)
        self.txtGotoY.setValidator(validator)
        self.txtGotoZ.setValidator(validator)
        
        # Jog buttons
        self.btnJogUp.pressed.connect(self.btnJogUp_pressed)
        self.btnJogRightUp.pressed.connect(self.btnJogRightUp_pressed)
        self.btnJogRight.pressed.connect(self.btnJogRight_pressed)
        self.btnJogRightDown.pressed.connect(self.btnJogRightDown_pressed)
        self.btnJogDown.pressed.connect(self.btnJogDown_pressed)
        self.btnJogLeftDown.pressed.connect(self.btnJogLeftDown_pressed)
        self.btnJogLeft.pressed.connect(self.btnJogLeft_pressed)
        self.btnJogLeftUp.pressed.connect(self.btnJogLeftUp_pressed)
        self.btnJogZUp.pressed.connect(self.btnJogZUp_pressed)
        self.btnJogZDown.pressed.connect(self.btnJogZDown_pressed)
        
        self.btnJogUp.released.connect(self.btnJogXXX_released)
        self.btnJogRightUp.released.connect(self.btnJogXXX_released)
        self.btnJogRight.released.connect(self.btnJogXXX_released)
        self.btnJogRightDown.released.connect(self.btnJogXXX_released)
        self.btnJogDown.released.connect(self.btnJogXXX_released)
        self.btnJogLeftDown.released.connect(self.btnJogXXX_released)
        self.btnJogLeft.released.connect(self.btnJogXXX_released)
        self.btnJogLeftUp.released.connect(self.btnJogXXX_released)
        self.btnJogZUp.released.connect(self.btnJogXXX_released)
        self.btnJogZDown.released.connect(self.btnJogXXX_released)
        
        # Stop button
        self.btnStop.clicked.connect(self.btnStop_clicked)
        
        # Goto controls
        self.txtGotoX.sigFocus.connect(self.txtGotoX.selectAll)
        self.txtGotoY.sigFocus.connect(self.txtGotoY.selectAll)
        self.txtGotoZ.sigFocus.connect(self.txtGotoZ.selectAll)
        self.btnGoto.clicked.connect(self.btnGoto_clicked)
        self.btnGotoBoardOrigin.clicked.connect(self.btnGotoBoardOrigin_clicked)
        self.btnGotoParkPos.clicked.connect(self.btnGotoParkPos_clicked)
        
        self.chkSpindle.clicked.connect(self.chkSpindle_clicked)
        
        # calibration controls
        self.btnHomingCycle.clicked.connect(self.btnHomingCycle_clicked)
        self.chkLaserCrosshair.clicked.connect(self.chkLaserCrosshair_clicked)
        
        AppBase.getSettings().sigMachineChanged.connect(self.settings_sigMachineChanged)
        self.settings_sigMachineChanged()
    
    
    def jog(self, directions):
        stepsize = None
        if self.radio1mm.isChecked():
            stepsize = 1
        elif self.radio01mm.isChecked():
            stepsize = 0.1
        elif self.radio005mm.isChecked():
            stepsize = 0.05
        AppBase.getMachine().jog(directions, stepsize)
        
        
    def goto(self, position, absolute):
        AppBase.getMachine().goTo(position, absolute)
        
        
    def updateCorrectionStatus(self, origin, rotation):
        self.chkOriginCorrected.setChecked(origin)
        self.chkRotationCorrected.setChecked(rotation)
        #if origin:
        #    self.txtCurrentBoardX.setEnabled(True)
        #    self.txtCurrentBoardY.setEnabled(True)
        #    self.txtCurrentBoardZ.setEnabled(True)
        #    self.radioGotoBoard.setEnabled(True)
        #    self.btnGotoBoardOrigin.setEnabled(True)
        #    self.chkOriginCorrected.setChecked(True)
        #else:
        #    self.txtCurrentBoardX.setEnabled(False)
        #    self.txtCurrentBoardY.setEnabled(False)
        #    self.txtCurrentBoardZ.setEnabled(False)
        #    self.radioGotoBoard.setEnabled(False)
        #    self.btnGotoBoardOrigin.setEnabled(False)
    
    
    def showEvent(self, event):
        super().showEvent(event)
        if not self.__initialized:
            # MainWindow signals
            AppBase.getMainwindow().sigNewWorkpiece.connect(self.mainwindow_sigNewWorkpiece)
            AppBase.getMainwindow().sigCorrectionChanged.connect(self.mainwindow_sigCorrectionChanged)
            self.__initialized = True
            
            
    def enableLaserCrosshair(self, value):
        """
        Enables/disables the laser crosshair.

        :param value: (bool) enable crosshair
        """
        AppBase.getMachine().setLaserCrosshair(value)
        self.chkLaserCrosshair.setChecked(value)
        self.sigLaserCrosshairChanged.emit(value)
    
    
    @QtCore.pyqtSlot()
    def settings_sigMachineChanged(self):
        machine = AppBase.getMachine()
        self.setEnabled(machine is not None and machine.isInitialized())
        machine.sigNewCoordinates.connect(self.machine_sigNewCoordinates)
    
    @QtCore.pyqtSlot()
    def mainwindow_sigNewWorkpiece(self):
        self.updateCorrectionStatus(False, False)
             
    @QtCore.pyqtSlot(dict)
    def mainwindow_sigCorrectionChanged(self, status):
        self.updateCorrectionStatus(status['origin_corrected'], status['rotation_corrected'])
        
    
    @QtCore.pyqtSlot(dict)
    def machine_sigNewCoordinates(self, coords):
        self.txtCurrentAbsoluteX.setText("{:.3f}".format(coords['absolute'][0]))
        self.txtCurrentAbsoluteY.setText("{:.3f}".format(coords['absolute'][1]))
        self.txtCurrentAbsoluteZ.setText("{:.3f}".format(coords['absolute'][2]))
        self.txtCurrentBoardX.setText("{:.3f}".format(coords['workpiece'][0]))
        self.txtCurrentBoardY.setText("{:.3f}".format(coords['workpiece'][1]))
        self.txtCurrentBoardZ.setText("{:.3f}".format(coords['workpiece'][2]))
            
    
    @QtCore.pyqtSlot()
    def btnJogUp_pressed(self):
        self.jog([0, 1, 0])
    @QtCore.pyqtSlot()
    def btnJogRightUp_pressed(self):
        self.jog([1, 1, 0])
    @QtCore.pyqtSlot()
    def btnJogRight_pressed(self):
        self.jog([1, 0, 0])
    @QtCore.pyqtSlot()
    def btnJogRightDown_pressed(self):
        self.jog([1, -1, 0])
    @QtCore.pyqtSlot()
    def btnJogDown_pressed(self):
        self.jog([0, -1, 0])
    @QtCore.pyqtSlot()
    def btnJogLeftDown_pressed(self):
        self.jog([-1, -1, 0])
    @QtCore.pyqtSlot()
    def btnJogLeft_pressed(self):
        self.jog([-1, 0, 0])
    @QtCore.pyqtSlot()
    def btnJogLeftUp_pressed(self):
        self.jog([-1, 1, 0])
    @QtCore.pyqtSlot()
    def btnJogZUp_pressed(self):
        self.jog([0, 0, 1])
    @QtCore.pyqtSlot()
    def btnJogZDown_pressed(self):
        self.jog([0, 0, -1])
    @QtCore.pyqtSlot()
    def btnJogXXX_released(self):
        if self.radioContinuous.isChecked():
            AppBase.getMachine().stop()
    
    @QtCore.pyqtSlot()
    def btnStop_clicked(self):
        AppBase.getMachine().stop()
    
    @QtCore.pyqtSlot()
    def btnGoto_clicked(self):
        pos = [float(self.txtGotoX.text()),
               float(self.txtGotoY.text()),
               float(self.txtGotoZ.text())]
        if self.radioGotoAbsolute.isChecked():
            self.goto(pos, True)
        elif self.radioGotoBoard.isChecked():
            self.goto(pos, False)
        elif self.radioGotoRelative.isChecked():
            curpos = np.array(AppBase.getMachine().getPosition(True))
            self.goto(list(curpos + pos), True)
        
    @QtCore.pyqtSlot()
    def btnGotoBoardOrigin_clicked(self):
        AppBase.getMachine().goToDefaultOrigin()
        
    @QtCore.pyqtSlot()
    def btnGotoParkPos_clicked(self):
        AppBase.getMachine().goToParkPosition()
        
    
    @QtCore.pyqtSlot(bool)
    def chkSpindle_clicked(self, enable):
        AppBase.getMachine().setSpindle(enable)
    
    
    @QtCore.pyqtSlot()
    def btnHomingCycle_clicked(self):
        AppBase.getMachine().homingCycle()
    
    @QtCore.pyqtSlot(bool)
    def chkLaserCrosshair_clicked(self, checked):
        self.enableLaserCrosshair(checked)