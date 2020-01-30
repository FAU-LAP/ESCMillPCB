"""
Created on 04.05.2018

@author: Christian Ott
"""

import logging
logger = logging.getLogger(__name__)

from PyQt5 import QtCore, QtWidgets
from ui.templates.Ui_TinyGCycleControl import Ui_TinyGCycleControl

class TinyGCycleControl(QtWidgets.QDialog, Ui_TinyGCycleControl):
    """
    Control dialog for TinyG displayed during running cycle.
    """

    def __init__(self, tinyg, plannerBuffer, parent=None):
        """
        Constructor

        :param tinyg: TinyG object
        :param plannerBuffer: Cycle planner buffer to display on the dialog.
        """
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.CustomizeWindowHint | QtCore.Qt.WindowTitleHint)

        self.initComplete = False
        self.finished = False
        self.machine = tinyg
        self.plannerBuffer = plannerBuffer[:]
        self.plansize = len(self.plannerBuffer)
        
        self.machine.sender.sigBufferChanged.connect(self.machine_outputBufferChanged)
        self.machine.receiver.sigQueueReportReceived.connect(self.machine_queueReport)
        self.machine.receiver.sigStatusReportReceived.connect(self.machine_statusReport)
        
        self.prgLinebuffer.setValue(0)
        self.prgOutputBuffer.setValue(0)
        self.prgPlannerQueue.setValue(0)
        
        self.btnFeedhold.clicked.connect(self.btnFeedhold_clicked)
        self.btnStop.clicked.connect(self.btnStop_clicked)
        
        # display cycle program in list
        self.lstCommandBuffer.clear()
        for cmd in plannerBuffer:
            self.lstCommandBuffer.addItem(cmd)
            
        self.prgLinebuffer.setValue(0)
        self.lblPlannerQueue.setText("Linebuffer: {} / {}".format(0, 8))
        self.prgOutputBuffer.setValue(0)
        self.lblOutputBuffer.setText("Command {} / {}".format(0, self.plansize))
        self.prgPlannerQueue.setValue(0)
        self.lblPlannerQueue.setText("Planner Queue: {} / {}".format(0, 32))
        logger.debug("Dialog created.")


    def closeEvent(self, event):
        logger.debug("Closing dialog.")
        self.finished = True
        self.deleteLater()
        super().closeEvent(event)


    @QtCore.pyqtSlot(bool)
    def btnFeedhold_clicked(self, checked):
        if checked:
            self.machine.feedhold()
            logger.info("Machine set to feedhold.")
        else:
            self.machine.resume()
            logger.info("Resuming cycle.")


    @QtCore.pyqtSlot()
    def btnStop_clicked(self):
        # if machine has never been in running state set initComplete anyways to correctly close this dialog
        logger.warning("Cycle canceled by user.")
        self.initComplete = True
        self.machine.stop()
        self.machine.setSpindle(False)
    
        
    @QtCore.pyqtSlot(dict)
    def machine_outputBufferChanged(self, bufferstatus):
        self.prgLinebuffer.setValue(bufferstatus['usedlines']/0.08)
        self.lblLinebuffer.setText("Linebuffer: {} / {}".format(bufferstatus['usedlines'], 8))
        self.prgOutputBuffer.setValue((self.plansize-bufferstatus['sendbuffersize'])*100/self.plansize)
        self.lblOutputBuffer.setText("Command {} / {}".format(self.plansize-bufferstatus['sendbuffersize'], self.plansize))
        
    @QtCore.pyqtSlot(dict)
    def machine_queueReport(self, report):
        self.prgPlannerQueue.setValue((32-report['qr'])/0.32)
        self.lblPlannerQueue.setText("Planner Queue: {} / {}".format(32-report['qr'], 32))
        
    @QtCore.pyqtSlot(dict)
    def machine_statusReport(self, report):
        if self.finished:
            return
        if 'stat' in report['sr'].keys():
            # close dialog if machine is not running (stat=5) or holding (stat=6)
            if self.initComplete and not report['sr']['stat'] in (5, 6):
                self.machine.sigCycleCompleted.emit()
                logger.info("Cycle completed.")
                self.close()
        # set init complete on first time the machine is in running state
        if not self.initComplete:
            if self.machine.lastStatus['stat'] in (5, 6):
                self.initComplete = True
                logger.info("TinyG cycle init complete.")