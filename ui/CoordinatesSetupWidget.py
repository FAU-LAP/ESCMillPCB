"""
Created on 03.03.2018

@author: Christian Ott
"""

from PyQt5 import QtWidgets, QtGui, QtCore

from Base.AppBase import AppBase

from ui.templates.Ui_CoordinatesSetupWidget import Ui_CoordinatesSetupWidget


class CoordinatesSetupWidget(QtWidgets.QWidget, Ui_CoordinatesSetupWidget):
    """
    Basic setup widget for main window.

    =======================  ==========================================================================
    **Signals**
    =======================  ==========================================================================
    sigBoardMirroredChanged  Emitted when the "Board Mirrored" checkbox has changed
                             Carries a boolean with the checkbox state
    sigBoardOutlinesChanged  Emitted when the "Show Outlines" checkbox or the board size has changed
                             Carries a dictionary {"show":(bool), "size":(float, float)}
    =======================  ==========================================================================
    """
    
    sigBoardMirroredChanged = QtCore.pyqtSignal(bool)
    sigBoardOutlinesChanged = QtCore.pyqtSignal(dict)

    def __init__(self, parent=None):
        """
        Constructor
        """
        super().__init__(parent)
        self.setupUi(self)
        
        settings = AppBase.getSettings()
        
        self.chkHoles.setChecked(settings.value('UI', 'holes_active'))
        self.chkMillings.setChecked(settings.value('UI', 'millings_active'))
        self.chkBoardMirrored.setChecked(settings.value('UI', 'board_mirrored'))
        self.chkBoardOutlines.setChecked(settings.value('UI', 'board_outlines'))
        self.txtBoardSizeX.setText(str(settings.value('UI', 'board_size_x')))
        self.txtBoardSizeY.setText(str(settings.value('UI', 'board_size_y')))
        
        # validator for coordinate inputs
        validator = QtGui.QDoubleValidator()
        
        # task checkboxes
        self.chkHoles.clicked.connect(self.chkHoles_clicked)
        self.chkMillings.clicked.connect(self.chkMillings_clicked)
        
        # board settings
        self.txtBoardSizeX.setValidator(validator)
        self.txtBoardSizeY.setValidator(validator)
        self.chkBoardMirrored.clicked.connect(self.chkBoardMirrored_clicked)
        self.chkBoardOutlines.clicked.connect(self.chkBoardOutlines_clicked)
        self.btnApplyBoardSize.clicked.connect(self.btnApplyBoardSize_clicked)
        
        # park position controls
        self.txtNewParkX.setValidator(validator)
        self.txtNewParkY.setValidator(validator)
        self.txtNewParkZ.setValidator(validator)
        self.btnGotoParkPosition.clicked.connect(self.btnGotoParkPosition_clicked)
        self.btnNewParkPosSetCurrent.clicked.connect(self.btnNewParkPosSetCurrent_clicked)
        self.btnApplyParkPos.clicked.connect(self.btnApplyParkPos_clicked)
        
        # board origin controls
        self.txtNewBoardX.setValidator(validator)
        self.txtNewBoardY.setValidator(validator)
        self.txtNewBoardZ.setValidator(validator)
        self.btnGotoBoardOrigin.clicked.connect(self.btnGotoBoardOrigin_clicked)
        self.btnNewBoardSetCurrent.clicked.connect(self.btnNewBoardSetCurrent_clicked)
        self.btnApplyBoardOrigin.clicked.connect(self.btnApplyBoardOrigin_clicked)
        
        AppBase.getSettings().sigMachineChanged.connect(self.settings_sigMachineChanged)
        self.settings_sigMachineChanged()
        
    
    def updatePositions(self):
        machine = AppBase.getMachine()
        if machine is not None:
            parkpos = machine.getParkPosition()
            self.txtParkX.setText(str(parkpos[0]))
            self.txtParkY.setText(str(parkpos[1]))
            self.txtParkZ.setText(str(parkpos[2]))
            origin = machine.getDefaultOrigin()
            self.txtBoardX.setText(str(origin[0]))
            self.txtBoardY.setText(str(origin[1]))
            self.txtBoardZ.setText(str(origin[2]))
            
            
    @QtCore.pyqtSlot()
    def btnApplyBoardSize_clicked(self):
        AppBase.getSettings().setValue(float(self.txtBoardSizeX.text()), 'UI', 'board_size_x')
        AppBase.getSettings().setValue(float(self.txtBoardSizeY.text()), 'UI', 'board_size_y')
        self.sigBoardOutlinesChanged.emit({
            'show':self.chkBoardOutlines.isChecked(),
            'size':(float(self.txtBoardSizeX.text()), float(self.txtBoardSizeY.text()))
        })
    
    @QtCore.pyqtSlot()
    def chkBoardOutlines_clicked(self):
        AppBase.getSettings().setValue(self.chkBoardOutlines.isChecked(), 'UI', 'board_outlines')
        self.sigBoardOutlinesChanged.emit({
            'show':self.chkBoardOutlines.isChecked(),
            'size':(float(self.txtBoardSizeX.text()), float(self.txtBoardSizeY.text()))
        })
        
        
    @QtCore.pyqtSlot()
    def chkBoardMirrored_clicked(self):
        AppBase.getSettings().setValue(self.chkBoardMirrored.isChecked(), 'UI', 'board_mirrored')
        self.sigBoardMirroredChanged.emit(self.chkBoardMirrored.isChecked())
    
    
    @QtCore.pyqtSlot()
    def chkHoles_clicked(self):
        AppBase.getSettings().setValue(self.chkHoles.isChecked(), 'UI', 'holes_active')
        workpiece = AppBase.getWorkpiece()
        if workpiece is not None:
            workpiece.holeList.active = self.chkHoles.isChecked()
    
    @QtCore.pyqtSlot()
    def chkMillings_clicked(self):
        AppBase.getSettings().setValue(self.chkMillings.isChecked(), 'UI', 'millings_active')
        workpiece = AppBase.getWorkpiece()
        if workpiece is not None:
            workpiece.millingList.active = self.chkMillings.isChecked()
    
    
    @QtCore.pyqtSlot()
    def btnGotoParkPosition_clicked(self):
        AppBase.getMachine().goToParkPosition()
    
    @QtCore.pyqtSlot()
    def btnNewParkPosSetCurrent_clicked(self):
        current = AppBase.getMachine().getPosition(True)
        self.txtNewParkX.setText(str(current[0]))
        self.txtNewParkY.setText(str(current[1]))
        self.txtNewParkZ.setText(str(current[2]))
    
    @QtCore.pyqtSlot()
    def btnApplyParkPos_clicked(self):
        AppBase.setParkPosition([
            float(self.txtNewParkX.text()), 
            float(self.txtNewParkY.text()), 
            float(self.txtNewParkZ.text())
        ])
        self.updatePositions()
    
    
    @QtCore.pyqtSlot()
    def btnGotoBoardOrigin_clicked(self):
        AppBase.getMachine().goToDefaultOrigin()
    
    @QtCore.pyqtSlot()
    def btnNewBoardSetCurrent_clicked(self):
        current = AppBase.getMachine().getPosition(True)
        self.txtNewBoardX.setText(str(current[0]))
        self.txtNewBoardY.setText(str(current[1]))
        self.txtNewBoardZ.setText(str(current[2]))
    
    @QtCore.pyqtSlot()
    def btnApplyBoardOrigin_clicked(self):
        AppBase.setDefaultOrigin([
            float(self.txtNewBoardX.text()),
            float(self.txtNewBoardY.text()), 
            float(self.txtNewBoardZ.text())
        ])
        self.updatePositions()
        
        
    @QtCore.pyqtSlot()
    def settings_sigMachineChanged(self):
        machine = AppBase.getMachine()
        self.setEnabled(machine is not None and machine.isInitialized())
        self.updatePositions()