# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources\ui\controlwidget.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ControlWidget(object):
    def setupUi(self, ControlWidget):
        ControlWidget.setObjectName("ControlWidget")
        ControlWidget.resize(367, 804)
        self.gridLayout = QtWidgets.QGridLayout(ControlWidget)
        self.gridLayout.setContentsMargins(5, 5, 5, 5)
        self.gridLayout.setObjectName("gridLayout")
        self.scrollArea = QtWidgets.QScrollArea(ControlWidget)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollContents = QtWidgets.QWidget()
        self.scrollContents.setGeometry(QtCore.QRect(0, 0, 355, 792))
        self.scrollContents.setObjectName("scrollContents")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.scrollContents)
        self.verticalLayout.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.scrollContents)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.gridLayout_4 = QtWidgets.QGridLayout()
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.label_2 = QtWidgets.QLabel(self.scrollContents)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.gridLayout_4.addWidget(self.label_2, 0, 1, 1, 1)
        self.label_10 = QtWidgets.QLabel(self.scrollContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_10.sizePolicy().hasHeightForWidth())
        self.label_10.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_10.setFont(font)
        self.label_10.setObjectName("label_10")
        self.gridLayout_4.addWidget(self.label_10, 2, 0, 1, 1)
        self.txtCurrentBoardX = QtWidgets.QLineEdit(self.scrollContents)
        self.txtCurrentBoardX.setMinimumSize(QtCore.QSize(130, 0))
        self.txtCurrentBoardX.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setFamily("Courier New")
        font.setPointSize(10)
        self.txtCurrentBoardX.setFont(font)
        self.txtCurrentBoardX.setStyleSheet("background-color: #EEEEEE;")
        self.txtCurrentBoardX.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.txtCurrentBoardX.setReadOnly(True)
        self.txtCurrentBoardX.setObjectName("txtCurrentBoardX")
        self.gridLayout_4.addWidget(self.txtCurrentBoardX, 1, 1, 1, 1)
        self.txtCurrentAbsoluteX = QtWidgets.QLineEdit(self.scrollContents)
        self.txtCurrentAbsoluteX.setEnabled(True)
        self.txtCurrentAbsoluteX.setMinimumSize(QtCore.QSize(130, 0))
        self.txtCurrentAbsoluteX.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setFamily("Courier New")
        font.setPointSize(10)
        self.txtCurrentAbsoluteX.setFont(font)
        self.txtCurrentAbsoluteX.setStyleSheet("background-color: #EEEEEE;")
        self.txtCurrentAbsoluteX.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.txtCurrentAbsoluteX.setReadOnly(True)
        self.txtCurrentAbsoluteX.setObjectName("txtCurrentAbsoluteX")
        self.gridLayout_4.addWidget(self.txtCurrentAbsoluteX, 1, 2, 1, 1)
        self.txtCurrentBoardY = QtWidgets.QLineEdit(self.scrollContents)
        self.txtCurrentBoardY.setMinimumSize(QtCore.QSize(130, 0))
        self.txtCurrentBoardY.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setFamily("Courier New")
        font.setPointSize(10)
        self.txtCurrentBoardY.setFont(font)
        self.txtCurrentBoardY.setStyleSheet("background-color: #EEEEEE;")
        self.txtCurrentBoardY.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.txtCurrentBoardY.setReadOnly(True)
        self.txtCurrentBoardY.setObjectName("txtCurrentBoardY")
        self.gridLayout_4.addWidget(self.txtCurrentBoardY, 2, 1, 1, 1)
        self.txtCurrentBoardZ = QtWidgets.QLineEdit(self.scrollContents)
        self.txtCurrentBoardZ.setMinimumSize(QtCore.QSize(130, 0))
        self.txtCurrentBoardZ.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setFamily("Courier New")
        font.setPointSize(10)
        self.txtCurrentBoardZ.setFont(font)
        self.txtCurrentBoardZ.setStyleSheet("background-color: #EEEEEE;")
        self.txtCurrentBoardZ.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.txtCurrentBoardZ.setReadOnly(True)
        self.txtCurrentBoardZ.setObjectName("txtCurrentBoardZ")
        self.gridLayout_4.addWidget(self.txtCurrentBoardZ, 4, 1, 1, 1)
        self.label_11 = QtWidgets.QLabel(self.scrollContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_11.sizePolicy().hasHeightForWidth())
        self.label_11.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_11.setFont(font)
        self.label_11.setObjectName("label_11")
        self.gridLayout_4.addWidget(self.label_11, 4, 0, 1, 1)
        self.label_12 = QtWidgets.QLabel(self.scrollContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_12.sizePolicy().hasHeightForWidth())
        self.label_12.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_12.setFont(font)
        self.label_12.setObjectName("label_12")
        self.gridLayout_4.addWidget(self.label_12, 1, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.scrollContents)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.gridLayout_4.addWidget(self.label_3, 0, 2, 1, 1)
        self.txtCurrentAbsoluteY = QtWidgets.QLineEdit(self.scrollContents)
        self.txtCurrentAbsoluteY.setMinimumSize(QtCore.QSize(130, 0))
        self.txtCurrentAbsoluteY.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setFamily("Courier New")
        font.setPointSize(10)
        self.txtCurrentAbsoluteY.setFont(font)
        self.txtCurrentAbsoluteY.setStyleSheet("background-color: #EEEEEE;")
        self.txtCurrentAbsoluteY.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.txtCurrentAbsoluteY.setReadOnly(True)
        self.txtCurrentAbsoluteY.setObjectName("txtCurrentAbsoluteY")
        self.gridLayout_4.addWidget(self.txtCurrentAbsoluteY, 2, 2, 1, 1)
        self.txtCurrentAbsoluteZ = QtWidgets.QLineEdit(self.scrollContents)
        self.txtCurrentAbsoluteZ.setMinimumSize(QtCore.QSize(130, 0))
        self.txtCurrentAbsoluteZ.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setFamily("Courier New")
        font.setPointSize(10)
        self.txtCurrentAbsoluteZ.setFont(font)
        self.txtCurrentAbsoluteZ.setStyleSheet("background-color: #EEEEEE;")
        self.txtCurrentAbsoluteZ.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.txtCurrentAbsoluteZ.setReadOnly(True)
        self.txtCurrentAbsoluteZ.setObjectName("txtCurrentAbsoluteZ")
        self.gridLayout_4.addWidget(self.txtCurrentAbsoluteZ, 4, 2, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout_4)
        self.line_3 = QtWidgets.QFrame(self.scrollContents)
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.verticalLayout.addWidget(self.line_3)
        self.label_5 = QtWidgets.QLabel(self.scrollContents)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.verticalLayout.addWidget(self.label_5)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setSpacing(2)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.btnJogZDown = QtWidgets.QPushButton(self.scrollContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnJogZDown.sizePolicy().hasHeightForWidth())
        self.btnJogZDown.setSizePolicy(sizePolicy)
        self.btnJogZDown.setMinimumSize(QtCore.QSize(50, 50))
        self.btnJogZDown.setText("")
        self.btnJogZDown.setIconSize(QtCore.QSize(30, 30))
        self.btnJogZDown.setObjectName("btnJogZDown")
        self.gridLayout_2.addWidget(self.btnJogZDown, 2, 4, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 0, 5, 1, 1)
        self.btnJogZUp = QtWidgets.QPushButton(self.scrollContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnJogZUp.sizePolicy().hasHeightForWidth())
        self.btnJogZUp.setSizePolicy(sizePolicy)
        self.btnJogZUp.setMinimumSize(QtCore.QSize(50, 50))
        self.btnJogZUp.setText("")
        self.btnJogZUp.setIconSize(QtCore.QSize(30, 30))
        self.btnJogZUp.setObjectName("btnJogZUp")
        self.gridLayout_2.addWidget(self.btnJogZUp, 0, 4, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(30, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem1, 0, 3, 1, 1)
        self.btnStop = QtWidgets.QPushButton(self.scrollContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnStop.sizePolicy().hasHeightForWidth())
        self.btnStop.setSizePolicy(sizePolicy)
        self.btnStop.setMinimumSize(QtCore.QSize(50, 50))
        self.btnStop.setText("")
        self.btnStop.setIconSize(QtCore.QSize(30, 30))
        self.btnStop.setObjectName("btnStop")
        self.gridLayout_2.addWidget(self.btnStop, 1, 1, 1, 1)
        self.btnJogLeft = QtWidgets.QPushButton(self.scrollContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnJogLeft.sizePolicy().hasHeightForWidth())
        self.btnJogLeft.setSizePolicy(sizePolicy)
        self.btnJogLeft.setMinimumSize(QtCore.QSize(50, 50))
        self.btnJogLeft.setText("")
        self.btnJogLeft.setIconSize(QtCore.QSize(30, 30))
        self.btnJogLeft.setObjectName("btnJogLeft")
        self.gridLayout_2.addWidget(self.btnJogLeft, 1, 0, 1, 1)
        self.btnJogRight = QtWidgets.QPushButton(self.scrollContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnJogRight.sizePolicy().hasHeightForWidth())
        self.btnJogRight.setSizePolicy(sizePolicy)
        self.btnJogRight.setMinimumSize(QtCore.QSize(50, 50))
        self.btnJogRight.setText("")
        self.btnJogRight.setIconSize(QtCore.QSize(30, 30))
        self.btnJogRight.setObjectName("btnJogRight")
        self.gridLayout_2.addWidget(self.btnJogRight, 1, 2, 1, 1)
        self.btnJogUp = QtWidgets.QPushButton(self.scrollContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnJogUp.sizePolicy().hasHeightForWidth())
        self.btnJogUp.setSizePolicy(sizePolicy)
        self.btnJogUp.setMinimumSize(QtCore.QSize(50, 50))
        self.btnJogUp.setText("")
        self.btnJogUp.setIconSize(QtCore.QSize(30, 30))
        self.btnJogUp.setObjectName("btnJogUp")
        self.gridLayout_2.addWidget(self.btnJogUp, 0, 1, 1, 1)
        self.btnJogRightUp = QtWidgets.QPushButton(self.scrollContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnJogRightUp.sizePolicy().hasHeightForWidth())
        self.btnJogRightUp.setSizePolicy(sizePolicy)
        self.btnJogRightUp.setMinimumSize(QtCore.QSize(50, 50))
        self.btnJogRightUp.setText("")
        self.btnJogRightUp.setObjectName("btnJogRightUp")
        self.gridLayout_2.addWidget(self.btnJogRightUp, 0, 2, 1, 1)
        self.btnJogRightDown = QtWidgets.QPushButton(self.scrollContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnJogRightDown.sizePolicy().hasHeightForWidth())
        self.btnJogRightDown.setSizePolicy(sizePolicy)
        self.btnJogRightDown.setMinimumSize(QtCore.QSize(50, 50))
        self.btnJogRightDown.setText("")
        self.btnJogRightDown.setObjectName("btnJogRightDown")
        self.gridLayout_2.addWidget(self.btnJogRightDown, 2, 2, 1, 1)
        self.btnJogLeftUp = QtWidgets.QPushButton(self.scrollContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnJogLeftUp.sizePolicy().hasHeightForWidth())
        self.btnJogLeftUp.setSizePolicy(sizePolicy)
        self.btnJogLeftUp.setMinimumSize(QtCore.QSize(50, 50))
        self.btnJogLeftUp.setBaseSize(QtCore.QSize(50, 50))
        self.btnJogLeftUp.setText("")
        self.btnJogLeftUp.setObjectName("btnJogLeftUp")
        self.gridLayout_2.addWidget(self.btnJogLeftUp, 0, 0, 1, 1)
        self.btnJogLeftDown = QtWidgets.QPushButton(self.scrollContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnJogLeftDown.sizePolicy().hasHeightForWidth())
        self.btnJogLeftDown.setSizePolicy(sizePolicy)
        self.btnJogLeftDown.setMinimumSize(QtCore.QSize(50, 50))
        self.btnJogLeftDown.setText("")
        self.btnJogLeftDown.setObjectName("btnJogLeftDown")
        self.gridLayout_2.addWidget(self.btnJogLeftDown, 2, 0, 1, 1)
        self.btnJogDown = QtWidgets.QPushButton(self.scrollContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnJogDown.sizePolicy().hasHeightForWidth())
        self.btnJogDown.setSizePolicy(sizePolicy)
        self.btnJogDown.setMinimumSize(QtCore.QSize(50, 50))
        self.btnJogDown.setText("")
        self.btnJogDown.setIconSize(QtCore.QSize(30, 30))
        self.btnJogDown.setObjectName("btnJogDown")
        self.gridLayout_2.addWidget(self.btnJogDown, 2, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout_2)
        self.formLayout_2 = QtWidgets.QFormLayout()
        self.formLayout_2.setVerticalSpacing(0)
        self.formLayout_2.setObjectName("formLayout_2")
        self.label_13 = QtWidgets.QLabel(self.scrollContents)
        self.label_13.setObjectName("label_13")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_13)
        self.radioContinuous = QtWidgets.QRadioButton(self.scrollContents)
        self.radioContinuous.setChecked(True)
        self.radioContinuous.setObjectName("radioContinuous")
        self.btngrpStepSize = QtWidgets.QButtonGroup(ControlWidget)
        self.btngrpStepSize.setObjectName("btngrpStepSize")
        self.btngrpStepSize.addButton(self.radioContinuous)
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.radioContinuous)
        self.radio1mm = QtWidgets.QRadioButton(self.scrollContents)
        self.radio1mm.setObjectName("radio1mm")
        self.btngrpStepSize.addButton(self.radio1mm)
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.radio1mm)
        self.radio01mm = QtWidgets.QRadioButton(self.scrollContents)
        self.radio01mm.setObjectName("radio01mm")
        self.btngrpStepSize.addButton(self.radio01mm)
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.radio01mm)
        self.radio005mm = QtWidgets.QRadioButton(self.scrollContents)
        self.radio005mm.setObjectName("radio005mm")
        self.btngrpStepSize.addButton(self.radio005mm)
        self.formLayout_2.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.radio005mm)
        self.verticalLayout.addLayout(self.formLayout_2)
        self.chkSpindle = QtWidgets.QCheckBox(self.scrollContents)
        self.chkSpindle.setObjectName("chkSpindle")
        self.verticalLayout.addWidget(self.chkSpindle)
        self.line_2 = QtWidgets.QFrame(self.scrollContents)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.verticalLayout.addWidget(self.line_2)
        self.label_6 = QtWidgets.QLabel(self.scrollContents)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.verticalLayout.addWidget(self.label_6)
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.btnGoto = QtWidgets.QPushButton(self.scrollContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnGoto.sizePolicy().hasHeightForWidth())
        self.btnGoto.setSizePolicy(sizePolicy)
        self.btnGoto.setMinimumSize(QtCore.QSize(0, 0))
        self.btnGoto.setMaximumSize(QtCore.QSize(80, 16777215))
        self.btnGoto.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.btnGoto.setObjectName("btnGoto")
        self.gridLayout_3.addWidget(self.btnGoto, 4, 5, 1, 1)
        self.radioGotoRelative = QtWidgets.QRadioButton(self.scrollContents)
        self.radioGotoRelative.setObjectName("radioGotoRelative")
        self.btngrpGoto = QtWidgets.QButtonGroup(ControlWidget)
        self.btngrpGoto.setObjectName("btngrpGoto")
        self.btngrpGoto.addButton(self.radioGotoRelative)
        self.gridLayout_3.addWidget(self.radioGotoRelative, 3, 5, 1, 1)
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setFieldGrowthPolicy(QtWidgets.QFormLayout.ExpandingFieldsGrow)
        self.formLayout.setObjectName("formLayout")
        self.label_7 = QtWidgets.QLabel(self.scrollContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_7)
        self.txtGotoX = FocusLineEdit(self.scrollContents)
        self.txtGotoX.setMinimumSize(QtCore.QSize(130, 0))
        self.txtGotoX.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setFamily("Courier New")
        font.setPointSize(10)
        self.txtGotoX.setFont(font)
        self.txtGotoX.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.txtGotoX.setReadOnly(False)
        self.txtGotoX.setObjectName("txtGotoX")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.txtGotoX)
        self.gridLayout_3.addLayout(self.formLayout, 0, 3, 1, 1)
        self.radioGotoAbsolute = QtWidgets.QRadioButton(self.scrollContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.radioGotoAbsolute.sizePolicy().hasHeightForWidth())
        self.radioGotoAbsolute.setSizePolicy(sizePolicy)
        self.radioGotoAbsolute.setMinimumSize(QtCore.QSize(130, 0))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.radioGotoAbsolute.setFont(font)
        self.radioGotoAbsolute.setObjectName("radioGotoAbsolute")
        self.btngrpGoto.addButton(self.radioGotoAbsolute)
        self.gridLayout_3.addWidget(self.radioGotoAbsolute, 1, 5, 1, 1)
        self.radioGotoBoard = QtWidgets.QRadioButton(self.scrollContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.radioGotoBoard.sizePolicy().hasHeightForWidth())
        self.radioGotoBoard.setSizePolicy(sizePolicy)
        self.radioGotoBoard.setMinimumSize(QtCore.QSize(130, 0))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.radioGotoBoard.setFont(font)
        self.radioGotoBoard.setChecked(True)
        self.radioGotoBoard.setObjectName("radioGotoBoard")
        self.btngrpGoto.addButton(self.radioGotoBoard)
        self.gridLayout_3.addWidget(self.radioGotoBoard, 0, 5, 1, 1)
        self.formLayout_3 = QtWidgets.QFormLayout()
        self.formLayout_3.setFieldGrowthPolicy(QtWidgets.QFormLayout.ExpandingFieldsGrow)
        self.formLayout_3.setObjectName("formLayout_3")
        self.label_8 = QtWidgets.QLabel(self.scrollContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_8)
        self.txtGotoY = FocusLineEdit(self.scrollContents)
        self.txtGotoY.setMinimumSize(QtCore.QSize(130, 0))
        self.txtGotoY.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setFamily("Courier New")
        font.setPointSize(10)
        self.txtGotoY.setFont(font)
        self.txtGotoY.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.txtGotoY.setReadOnly(False)
        self.txtGotoY.setObjectName("txtGotoY")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.txtGotoY)
        self.gridLayout_3.addLayout(self.formLayout_3, 1, 3, 1, 1)
        self.formLayout_4 = QtWidgets.QFormLayout()
        self.formLayout_4.setFieldGrowthPolicy(QtWidgets.QFormLayout.ExpandingFieldsGrow)
        self.formLayout_4.setObjectName("formLayout_4")
        self.label_9 = QtWidgets.QLabel(self.scrollContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_9.sizePolicy().hasHeightForWidth())
        self.label_9.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")
        self.formLayout_4.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_9)
        self.txtGotoZ = FocusLineEdit(self.scrollContents)
        self.txtGotoZ.setMinimumSize(QtCore.QSize(130, 0))
        self.txtGotoZ.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setFamily("Courier New")
        font.setPointSize(10)
        self.txtGotoZ.setFont(font)
        self.txtGotoZ.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.txtGotoZ.setObjectName("txtGotoZ")
        self.formLayout_4.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.txtGotoZ)
        self.gridLayout_3.addLayout(self.formLayout_4, 3, 3, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout_3)
        self.gridLayout_5 = QtWidgets.QGridLayout()
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.btnGotoBoardOrigin = QtWidgets.QPushButton(self.scrollContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnGotoBoardOrigin.sizePolicy().hasHeightForWidth())
        self.btnGotoBoardOrigin.setSizePolicy(sizePolicy)
        self.btnGotoBoardOrigin.setMinimumSize(QtCore.QSize(130, 0))
        self.btnGotoBoardOrigin.setObjectName("btnGotoBoardOrigin")
        self.gridLayout_5.addWidget(self.btnGotoBoardOrigin, 0, 0, 1, 1)
        self.btnGotoParkPos = QtWidgets.QPushButton(self.scrollContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnGotoParkPos.sizePolicy().hasHeightForWidth())
        self.btnGotoParkPos.setSizePolicy(sizePolicy)
        self.btnGotoParkPos.setMinimumSize(QtCore.QSize(130, 0))
        self.btnGotoParkPos.setObjectName("btnGotoParkPos")
        self.gridLayout_5.addWidget(self.btnGotoParkPos, 0, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout_5)
        self.line = QtWidgets.QFrame(self.scrollContents)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.label_4 = QtWidgets.QLabel(self.scrollContents)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.verticalLayout.addWidget(self.label_4)
        self.btnHomingCycle = QtWidgets.QPushButton(self.scrollContents)
        self.btnHomingCycle.setObjectName("btnHomingCycle")
        self.verticalLayout.addWidget(self.btnHomingCycle)
        self.gridLayout_6 = QtWidgets.QGridLayout()
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.chkRotationCorrected = QtWidgets.QCheckBox(self.scrollContents)
        self.chkRotationCorrected.setEnabled(False)
        self.chkRotationCorrected.setCheckable(True)
        self.chkRotationCorrected.setChecked(False)
        self.chkRotationCorrected.setObjectName("chkRotationCorrected")
        self.gridLayout_6.addWidget(self.chkRotationCorrected, 3, 0, 1, 1)
        self.chkOriginCorrected = QtWidgets.QCheckBox(self.scrollContents)
        self.chkOriginCorrected.setEnabled(False)
        self.chkOriginCorrected.setObjectName("chkOriginCorrected")
        self.gridLayout_6.addWidget(self.chkOriginCorrected, 2, 0, 1, 1)
        self.chkLaserCrosshair = QtWidgets.QCheckBox(self.scrollContents)
        self.chkLaserCrosshair.setObjectName("chkLaserCrosshair")
        self.gridLayout_6.addWidget(self.chkLaserCrosshair, 0, 0, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout_6)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem2)
        self.scrollArea.setWidget(self.scrollContents)
        self.gridLayout.addWidget(self.scrollArea, 0, 0, 1, 1)

        self.retranslateUi(ControlWidget)
        QtCore.QMetaObject.connectSlotsByName(ControlWidget)

    def retranslateUi(self, ControlWidget):
        _translate = QtCore.QCoreApplication.translate
        ControlWidget.setWindowTitle(_translate("ControlWidget", "Form"))
        self.label.setText(_translate("ControlWidget", "Current Position"))
        self.label_2.setText(_translate("ControlWidget", "Board"))
        self.label_10.setText(_translate("ControlWidget", "Y"))
        self.txtCurrentBoardX.setText(_translate("ControlWidget", "000.000"))
        self.txtCurrentAbsoluteX.setText(_translate("ControlWidget", "000.000"))
        self.txtCurrentBoardY.setText(_translate("ControlWidget", "000.000"))
        self.txtCurrentBoardZ.setText(_translate("ControlWidget", "000.000"))
        self.label_11.setText(_translate("ControlWidget", "Z"))
        self.label_12.setText(_translate("ControlWidget", "X"))
        self.label_3.setText(_translate("ControlWidget", "Absolute"))
        self.txtCurrentAbsoluteY.setText(_translate("ControlWidget", "000.000"))
        self.txtCurrentAbsoluteZ.setText(_translate("ControlWidget", "000.000"))
        self.label_5.setText(_translate("ControlWidget", "Jog"))
        self.label_13.setText(_translate("ControlWidget", "Step size"))
        self.radioContinuous.setText(_translate("ControlWidget", "Continuous"))
        self.radio1mm.setText(_translate("ControlWidget", "1 mm"))
        self.radio01mm.setText(_translate("ControlWidget", "0.1 mm"))
        self.radio005mm.setText(_translate("ControlWidget", "0.05 mm"))
        self.chkSpindle.setText(_translate("ControlWidget", "Spindle"))
        self.label_6.setText(_translate("ControlWidget", "Go to"))
        self.btnGoto.setText(_translate("ControlWidget", "Go"))
        self.radioGotoRelative.setText(_translate("ControlWidget", "Relative"))
        self.label_7.setText(_translate("ControlWidget", "X"))
        self.txtGotoX.setText(_translate("ControlWidget", "000.000"))
        self.radioGotoAbsolute.setText(_translate("ControlWidget", "Absolute"))
        self.radioGotoBoard.setText(_translate("ControlWidget", "Board"))
        self.label_8.setText(_translate("ControlWidget", "Y"))
        self.txtGotoY.setText(_translate("ControlWidget", "000.000"))
        self.label_9.setText(_translate("ControlWidget", "Z"))
        self.txtGotoZ.setText(_translate("ControlWidget", "000.000"))
        self.btnGotoBoardOrigin.setText(_translate("ControlWidget", "Default Board Origin"))
        self.btnGotoParkPos.setText(_translate("ControlWidget", "Park Position"))
        self.label_4.setText(_translate("ControlWidget", "Calibration"))
        self.btnHomingCycle.setText(_translate("ControlWidget", "Run Homing Cycle"))
        self.chkRotationCorrected.setText(_translate("ControlWidget", "Board rotation corrected"))
        self.chkOriginCorrected.setText(_translate("ControlWidget", "Board origin corrected"))
        self.chkLaserCrosshair.setText(_translate("ControlWidget", "Use laser crosshair"))

from ui.FocusLineEdit import FocusLineEdit
