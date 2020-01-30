"""
Created on 15.05.2018

@author: Christian Ott
"""

from PyQt5 import QtCore, QtWidgets
import json

from Base import Errors

from ui.templates.Ui_TinyGTestpanel import Ui_TinyGTestpanel

class TinyGTestpanel(QtWidgets.QDialog, Ui_TinyGTestpanel):
    """
    Communication test panel for TinyG board.
    """

    def __init__(self, tinyg, parent=None):
        """
        Constructor
        """
        super().__init__(parent)
        self.setupUi(self)
        self.machine = tinyg
        
        self.btnSend.clicked.connect(self.btnSend_clicked)
        self.btnQuery.clicked.connect(self.btnQuery_clicked)
        
        self.machine.receiver.sigResponseReceived.connect(self.machine_responseReceived)
        self.machine.receiver.sigStatusReportReceived.connect(self.machine_responseReceived)
        self.machine.receiver.sigQueueReportReceived.connect(self.machine_responseReceived)
        
    
    def interpreteInput(self):
        raw = self.txtCommand.text().strip()
        if raw == "!":
            self.machine.feedhold()
        elif raw == "~":
            self.machine.resume()
        elif raw == "%" or raw == "!%":
            self.machine.stop()
        else:
            try:
                cmd = json.loads(raw)
                return cmd
            except json.JSONDecodeError:
                QtWidgets.QMessageBox.warning(self, "Invalid input",
                    "Invalid command syntax. Use JSON command syntax.")
        return None
        
        
    QtCore.pyqtSlot()
    def btnSend_clicked(self):
        entry = ">> " + self.txtCommand.text().strip()
        self.lstMessages.addItem(QtWidgets.QListWidgetItem(entry))
        cmd = self.interpreteInput()
        if cmd is not None:
            self.machine.executeCommand(cmd)
        self.txtCommand.setText("")
    
    QtCore.pyqtSlot()
    def btnQuery_clicked(self):
        entry = ">> " + self.txtCommand.text().strip() + " ..."
        self.lstMessages.addItem(QtWidgets.QListWidgetItem(entry))
        cmd = self.interpreteInput()
        if cmd is not None:
            try:
                self.machine.executeQuery(cmd)
            except Errors.CommunicationError as e:
                entry = str(e)
                self.lstMessages.addItem(QtWidgets.QListWidgetItem(entry))
        self.txtCommand.setText("")
    
    
    QtCore.pyqtSlot(dict)
    def machine_responseReceived(self, msg):
        entry = "<< " + str(msg)
        self.lstMessages.addItem(QtWidgets.QListWidgetItem(entry))