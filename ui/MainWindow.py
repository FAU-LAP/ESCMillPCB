"""
Created on 03.03.2018

@author: Christian Ott
"""

import logging
logger = logging.getLogger(__name__)

from PyQt5 import QtWidgets, QtCore
import numpy as np
import webbrowser

from Base.AppBase import AppBase
from Base.LogHandlers import QListWidgetLogger
from Base.ImportFactory import ImportFactory
import Base.Utility as utils
from ui.SettingsDialog import SettingsDialog

from ui.templates.Ui_MainWindow import Ui_MainWindow


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    """
    Main window of the program.

    ========================  ===============================================================================
    **Signals**
    ========================  ===============================================================================
    sigNewWorkpiece           Emitted when the workpiece changes
    sigCorrectionChanged      Emitted when workpiece coordinate system origin or rotation corretion status
                              has changed. Carries a dictionary
                              {"origin_corrected":(bool) workpiece coordinate system is origin corrected,
                              "rotation_corrected":(bool) workpiece coordinate system is rotation corrected}
    sigLaserCrosshairChanged  Emitted when the laser crosshair checkbox is changed.
                              Carries a bool indicating the checkbox state.
    ========================  ===============================================================================
    """
    
    sigMachineChanged = QtCore.pyqtSignal()
    sigNewWorkpiece = QtCore.pyqtSignal()
    sigCorrectionChanged = QtCore.pyqtSignal(dict)
    sigLaserCrosshairChanged = QtCore.pyqtSignal(bool)
    

    def __init__(self, parent=None):
        """
        Constructor
        """
        super().__init__(parent)
        self.setupUi(self)
        self.__initialized = False
        
        self.machineMenu = None
        settings = AppBase.getSettings()
        self.laserActive = False
        self.lastLaserActive = False
        self.laserOffset = np.array([
            settings.value("MachineBase", "laser_offset_x"),
            settings.value("MachineBase", "laser_offset_y")
        ])
        
        # initialize logging
        self.loghandler = QListWidgetLogger(self.lstLog)
        self.loghandler.setLevel(settings.value("General", "loglist_level"))
        logging.getLogger().addHandler(self.loghandler)
        
        # connect signals
        self.mnuOpenEagleBrd.triggered.connect(self.mnuOpenEagleBrd_triggered)
        self.mnuQuit.triggered.connect(QtWidgets.QApplication.quit)
        self.mnuSettings.triggered.connect(self.mnuSettings_triggered)
        self.mnuInitMachine.triggered.connect(self.mnuInitMachine_triggered)
        self.mnuCloseMachine.triggered.connect(self.mnuCloseMachine_triggered)
        self.mnuDocumentation.triggered.connect(self.mnuDocumentation_triggered)
        self.mnuAbout.triggered.connect(self.mnuAbout_triggered)
        self.mnuAboutQt.triggered.connect(QtWidgets.QApplication.aboutQt)

        self.workpieceViewer.sigGotoActionTriggered.connect(self.workpieceViewer_sigGotoActionTriggered)
        self.workpieceViewer.sigRef1ActionTriggered.connect(self.workpieceViewer_sigRef1ActionTriggered)
        self.workpieceViewer.sigRef2ActionTriggered.connect(self.workpieceViewer_sigRef2ActionTriggered)
        
        self.wdgControl.sigLaserCrosshairChanged.connect(self.wdgControl_sigLaserCrosshairChanged)
        
        self.wdgCoordinateSetup.sigBoardMirroredChanged.connect(self.wdgCoordinateSetup_sigBoardMirroredChanged)
        self.wdgCoordinateSetup.sigBoardOutlinesChanged.connect(self.wdgCoordinateSetup_sigBoardOutlinesChanged)
        
        self.btnStartCycle.clicked.connect(self.btnStartCycle_clicked)
        
        settings.sigSettingsChanged.connect(self.settings_sigSettingsChanged)
        settings.sigMachineChanged.connect(self.settings_sigMachineChanged)
        
        # restore settings 
        settings.restoreQtGeometry(self, "UI", "mainWindow_geometry")
        settings.restoreQtState(self.splitterRight, "UI", "splitterRight_state")
        settings.restoreQtState(self.splitterBottom, "UI", "splitterBottom_state")
        
        self.settings_sigMachineChanged()
    
    
    def setWorkpiece(self, workpiece):
        AppBase.setWorkpiece(workpiece)
        AppBase.setWorkpieceMirrored(AppBase.getSettings().value('UI', 'board_mirrored'))
        self.workpieceViewer.setWorkpiece(workpiece)
        self.workpieceViewer.setBoardOutlineVisible(AppBase.getSettings().value('UI', 'board_outlines'))
        self.sigNewWorkpiece.emit()
        
    
    def updateMachineMenu(self):
        # remove old menu
        if self.machineMenu is not None:
            self.menubar.removeAction(self.machineMenu.menuAction())
        # check if machine is valid and insert new menu
        if AppBase.getMachine is not None:
            self.machineMenu = AppBase.getMachine().getMachineMenu()
            if self.machineMenu is not None:
                beforeAction = self.menubar.actions()[-1]
                self.menubar.insertMenu(beforeAction, self.machineMenu)
    
    
    def showEvent(self, event):
        super().showEvent(event)
        if not self.__initialized:
            QtWidgets.qApp.setOverrideCursor(QtCore.Qt.WaitCursor)
            # notify base that application is loaded
            try:
                AppBase.applicationLoaded()
            finally:
                QtWidgets.qApp.restoreOverrideCursor()
            # perform homing cycle
            if AppBase.getMachine().isInitialized():
                homing = (QtWidgets.QMessageBox.question(self, "Homing Cycle?", "Perform homing cycle?",
                            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No) == QtWidgets.QMessageBox.Yes)
                if homing:
                    AppBase.getMachine().homingCycle()
            self.__initialized = True
        
    
    def closeEvent(self, event):
        AppBase.closeMachine()
        settings = AppBase.getSettings()
        settings.storeQtGeometry(self, "UI", "mainWindow_geometry")
        settings.storeQtState(self.splitterRight, "UI", "splitterRight_state")
        settings.storeQtState(self.splitterBottom, "UI", "splitterBottom_state")
        super().closeEvent(event)
    
    
    @QtCore.pyqtSlot()
    def mnuOpenEagleBrd_triggered(self):
        file = QtWidgets.QFileDialog.getOpenFileName(
            self,
            'Open board file',
            '', 
            'Eagle board file (*.brd);;All files (*.*)'
        )
        if file[0] != '':
            QtWidgets.qApp.setOverrideCursor(QtCore.Qt.WaitCursor)
            try:
                workpiece = ImportFactory.importFile(file[0], filetype="eagle")
                self.setWorkpiece(workpiece)
            finally:
                QtWidgets.qApp.restoreOverrideCursor()
        
    
    @QtCore.pyqtSlot()
    def mnuSettings_triggered(self):
        dlg = SettingsDialog()
        AppBase.getSettings().restoreQtGeometry(dlg, "UI", "settingsDialog_geometry")
        if dlg.exec():
            AppBase.getSettings().updateSettings(dlg.settings, dlg.settingsChanged)
        if dlg.machineChanged:
            AppBase.changeMachine(dlg.machineName, signal=True)
        AppBase.getSettings().storeQtGeometry(dlg, "UI", "settingsDialog_geometry")
            
        
    @QtCore.pyqtSlot()
    def mnuAbout_triggered(self):
        QtWidgets.QMessageBox.about(
            self,
            "About ESCMillPCB",
            f"""
            ESCMillPCB v{AppBase.version}
            
            Milling PCBs with TinyG

            Developed for the electronics lab course (ESC) of the
            Friedrich-Alexander-Universität Erlangen-Nürnberg
            Department of Physics
            Chair of Applied Physics
            
            by Christian Ott 
            """
        )
        
        
    @QtCore.pyqtSlot()
    def mnuInitMachine_triggered(self):
        if AppBase.getMachine().isInitialized():
            if not (QtWidgets.QMessageBox.question(self, "Reinitialize machine?", "Do you really want to reinitialize the machine?",
                    QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No) == QtWidgets.QMessageBox.Yes):
                return;
        setup = (QtWidgets.QMessageBox.question(self, "Setup machine?", "Apply machine parameters?",
                    QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No) == QtWidgets.QMessageBox.Yes)
        QtWidgets.qApp.setOverrideCursor(QtCore.Qt.WaitCursor)
        try:
            AppBase.initMachine(setup)
        finally:
            QtWidgets.qApp.restoreOverrideCursor()
        if AppBase.getMachine().isInitialized():
            homing = (QtWidgets.QMessageBox.question(self, "Homing Cycle?", "Perform homing cycle?",
                        QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No) == QtWidgets.QMessageBox.Yes)
            if homing:
                AppBase.getMachine().homingCycle()
                
    @QtCore.pyqtSlot()
    def mnuApplyMachineParams_triggered(self):
        QtWidgets.qApp.setOverrideCursor(QtCore.Qt.WaitCursor)
        try:
            AppBase.setupMachine()
        finally:
            QtWidgets.qApp.restoreOverrideCursor()
        
    @QtCore.pyqtSlot()
    def mnuCloseMachine_triggered(self):
        AppBase.closeMachine()
        
    @QtCore.pyqtSlot()
    def mnuDocumentation_triggered(self):
        helppath = AppBase.getDocumentationPath()
        webbrowser.open(helppath, new=2, autoraise=True)
    
    @QtCore.pyqtSlot(dict)
    def workpieceViewer_sigGotoActionTriggered(self, data):
        target = np.array(data['pos'])
        if self.laserActive:
            target += self.laserOffset
        AppBase.getMachine().goTo(target, False)
        
    @QtCore.pyqtSlot(dict)
    def workpieceViewer_sigRef1ActionTriggered(self, data):
        AppBase.getWorkpiece().translate(-np.array(data['pos']))
        if self.laserActive:
            AppBase.getMachine().setWorkpieceOrigin(offset=-self.laserOffset)
        else:
            AppBase.getMachine().setWorkpieceOrigin()
        logger.info("Setting board origin to (%.3f, %.3f)", *data['pos'])
        self.sigCorrectionChanged.emit({'origin_corrected':True, 'rotation_corrected':False})
        self.btnStartCycle.setEnabled(True)
        
    @QtCore.pyqtSlot(dict)
    def workpieceViewer_sigRef2ActionTriggered(self, data):
        offset = np.array([0, 0])
        if self.laserActive:
            offset = -self.laserOffset
        matrix, angle = AppBase.getMachine().performAngleCorrection(np.array(data['pos']), offset=offset)
        AppBase.getWorkpiece().transform(matrix)
        logger.info("Performing angle correction by %.3f°", utils.radToDeg(angle))
        self.sigCorrectionChanged.emit({'origin_corrected':True, 'rotation_corrected':True})
        
        
    @QtCore.pyqtSlot(bool)
    def wdgControl_sigLaserCrosshairChanged(self, checked):
        self.laserActive = checked
        self.sigLaserCrosshairChanged.emit(checked)
        
        
    @QtCore.pyqtSlot(bool)
    def wdgCoordinateSetup_sigBoardMirroredChanged(self, mirrored):
        if AppBase.setWorkpieceMirrored(mirrored):
            self.sigNewWorkpiece.emit()
        
    
    @QtCore.pyqtSlot(dict)
    def wdgCoordinateSetup_sigBoardOutlinesChanged(self, params):
        if AppBase.getWorkpiece() is not None:
            AppBase.getWorkpiece().setSize(params['size'])
        self.workpieceViewer.setBoardOutlineVisible(params['show'])
        
        
    @QtCore.pyqtSlot()
    def btnStartCycle_clicked(self):
        if not AppBase.getMachine().isHomed():
            QtWidgets.QMessageBox.warning(self, "Machine not homed", "The machine is not homed! Perform homing cycle first.")
            return;
        self.lastLaserActive = self.laserActive
        AppBase.getWorkpiece().planMachining(AppBase.getMachine())
        self.wdgControl.enableLaserCrosshair(False)
        AppBase.getMachine().executeCycle()
        
        
    @QtCore.pyqtSlot()
    def settings_sigMachineChanged(self):
        self.updateMachineMenu()
        self.sigCorrectionChanged.emit({'origin_corrected':False, 'rotation_corrected':False})
        self.btnStartCycle.setEnabled(False)
        AppBase.getMachine().sigStatusUpdate.connect(self.machine_sigStatusUpdate)
        AppBase.getMachine().sigCycleCompleted.connect(self.machine_sigCycleCompleted)
        
    @QtCore.pyqtSlot(list)
    def settings_sigSettingsChanged(self, changed):
        if 'MachineBase' in changed:
            self.laserOffset = np.array([
                AppBase.getSettings().value('MachineBase', 'laser_offset_x'),
                AppBase.getSettings().value('MachineBase', 'laser_offset_y')
            ])
        
        
    @QtCore.pyqtSlot(str)
    def machine_sigStatusUpdate(self, status):
        self.statusbar.showMessage(status)
        
    @QtCore.pyqtSlot()
    def machine_sigCycleCompleted(self):
        self.wdgControl.enableLaserCrosshair(self.lastLaserActive)