# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'design.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ExMachinaRandomizer(object):
    def setupUi(self, ExMachinaRandomizer):
        ExMachinaRandomizer.setObjectName("ExMachinaRandomizer")
        ExMachinaRandomizer.resize(500, 420)
        ExMachinaRandomizer.setMinimumSize(QtCore.QSize(500, 420))
        ExMachinaRandomizer.setMaximumSize(QtCore.QSize(500, 420))
        self.centralwidget = QtWidgets.QWidget(ExMachinaRandomizer)
        self.centralwidget.setObjectName("centralwidget")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(10, 10, 241, 401))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setGeometry(QtCore.QRect(50, 40, 141, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setGeometry(QtCore.QRect(20, 120, 201, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.frame)
        self.label_3.setGeometry(QtCore.QRect(40, 180, 161, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.frame)
        self.label_4.setGeometry(QtCore.QRect(30, 360, 181, 20))
        self.label_4.setObjectName("label_4")
        self.DestFolder = QtWidgets.QLineEdit(self.frame)
        self.DestFolder.setGeometry(QtCore.QRect(10, 70, 221, 20))
        self.DestFolder.setText("")
        self.DestFolder.setObjectName("DestFolder")
        self.btnBrowse = QtWidgets.QPushButton(self.frame)
        self.btnBrowse.setGeometry(QtCore.QRect(10, 90, 75, 23))
        self.btnBrowse.setObjectName("btnBrowse")
        self.btnOptions = QtWidgets.QPushButton(self.frame)
        self.btnOptions.setGeometry(QtCore.QRect(30, 150, 171, 23))
        self.btnOptions.setObjectName("btnOptions")
        self.rbtn_steam = QtWidgets.QRadioButton(self.frame)
        self.rbtn_steam.setGeometry(QtCore.QRect(10, 210, 91, 17))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.rbtn_steam.setFont(font)
        self.rbtn_steam.setObjectName("rbtn_steam")
        self.rbtn_cr = QtWidgets.QRadioButton(self.frame)
        self.rbtn_cr.setGeometry(QtCore.QRect(10, 250, 181, 17))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.rbtn_cr.setFont(font)
        self.rbtn_cr.setObjectName("rbtn_cr")
        self.rbtn_isl = QtWidgets.QRadioButton(self.frame)
        self.rbtn_isl.setGeometry(QtCore.QRect(10, 270, 181, 17))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.rbtn_isl.setFont(font)
        self.rbtn_isl.setObjectName("rbtn_isl")
        self.btnStart = QtWidgets.QPushButton(self.frame)
        self.btnStart.setGeometry(QtCore.QRect(10, 300, 221, 51))
        self.btnStart.setObjectName("btnStart")
        self.rbtn_cp = QtWidgets.QRadioButton(self.frame)
        self.rbtn_cp.setGeometry(QtCore.QRect(10, 230, 161, 17))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.rbtn_cp.setFont(font)
        self.rbtn_cp.setObjectName("rbtn_cp")
        self.label_5 = QtWidgets.QLabel(self.frame)
        self.label_5.setGeometry(QtCore.QRect(70, 380, 91, 16))
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.frame)
        self.label_6.setGeometry(QtCore.QRect(10, 10, 101, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.LangSelect = QtWidgets.QComboBox(self.frame)
        self.LangSelect.setGeometry(QtCore.QRect(110, 10, 121, 22))
        self.LangSelect.setObjectName("LangSelect")
        self.frame_2 = QtWidgets.QFrame(self.centralwidget)
        self.frame_2.setGeometry(QtCore.QRect(250, 10, 241, 401))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.in_logger = QtWidgets.QTextBrowser(self.frame_2)
        self.in_logger.setGeometry(QtCore.QRect(10, 10, 221, 381))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(240, 240, 240))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(240, 240, 240))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(240, 240, 240))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        self.in_logger.setPalette(palette)
        self.in_logger.setObjectName("in_logger")
        self.errors = QtWidgets.QLabel(self.frame_2)
        self.errors.setGeometry(QtCore.QRect(10, 390, 47, 13))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(240, 240, 240))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(240, 240, 240))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        self.errors.setPalette(palette)
        self.errors.setObjectName("errors")
        ExMachinaRandomizer.setCentralWidget(self.centralwidget)

        self.retranslateUi(ExMachinaRandomizer)
        QtCore.QMetaObject.connectSlotsByName(ExMachinaRandomizer)

    def retranslateUi(self, ExMachinaRandomizer):
        _translate = QtCore.QCoreApplication.translate
        ExMachinaRandomizer.setWindowTitle(_translate("ExMachinaRandomizer", "Ex Machina Randomizer beta v1.1"))
        self.label.setText(_translate("ExMachinaRandomizer", "1. Укажите путь к игре"))
        self.label_2.setText(_translate("ExMachinaRandomizer", "2. Выберите опции рандомизации"))
        self.label_3.setText(_translate("ExMachinaRandomizer", "3. Выберите версию игры"))
        self.label_4.setText(_translate("ExMachinaRandomizer", "Powered by PavlikRPG © 2021-2022"))
        self.btnBrowse.setText(_translate("ExMachinaRandomizer", "Обзор"))
        self.btnOptions.setText(_translate("ExMachinaRandomizer", "Параметры рандомизации"))
        self.rbtn_steam.setText(_translate("ExMachinaRandomizer", "Steam 1.02"))
        self.rbtn_cr.setText(_translate("ExMachinaRandomizer", "Community Remaster v1.10"))
        self.rbtn_isl.setText(_translate("ExMachinaRandomizer", "Improved Storyline v1.0.5.3"))
        self.btnStart.setText(_translate("ExMachinaRandomizer", "Начать рандомизацию"))
        self.rbtn_cp.setText(_translate("ExMachinaRandomizer", "Community Patch v1.10"))
        self.label_5.setText(_translate("ExMachinaRandomizer", "All rights reserved"))
        self.label_6.setText(_translate("ExMachinaRandomizer", "Язык/Language:"))
        self.errors.setText(_translate("ExMachinaRandomizer", "0"))
