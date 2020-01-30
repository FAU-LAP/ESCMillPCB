# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources\ui\TinyGTestpanel.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_TinyGTestpanel(object):
    def setupUi(self, TinyGTestpanel):
        TinyGTestpanel.setObjectName("TinyGTestpanel")
        TinyGTestpanel.resize(573, 575)
        self.verticalLayout = QtWidgets.QVBoxLayout(TinyGTestpanel)
        self.verticalLayout.setObjectName("verticalLayout")
        self.lstMessages = QtWidgets.QListWidget(TinyGTestpanel)
        self.lstMessages.setObjectName("lstMessages")
        self.verticalLayout.addWidget(self.lstMessages)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.txtCommand = QtWidgets.QLineEdit(TinyGTestpanel)
        self.txtCommand.setObjectName("txtCommand")
        self.horizontalLayout.addWidget(self.txtCommand)
        self.btnSend = QtWidgets.QPushButton(TinyGTestpanel)
        self.btnSend.setObjectName("btnSend")
        self.horizontalLayout.addWidget(self.btnSend)
        self.btnQuery = QtWidgets.QPushButton(TinyGTestpanel)
        self.btnQuery.setObjectName("btnQuery")
        self.horizontalLayout.addWidget(self.btnQuery)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(TinyGTestpanel)
        QtCore.QMetaObject.connectSlotsByName(TinyGTestpanel)

    def retranslateUi(self, TinyGTestpanel):
        _translate = QtCore.QCoreApplication.translate
        TinyGTestpanel.setWindowTitle(_translate("TinyGTestpanel", "TinyG Testpanel"))
        self.btnSend.setText(_translate("TinyGTestpanel", "Send"))
        self.btnQuery.setText(_translate("TinyGTestpanel", "Query"))

