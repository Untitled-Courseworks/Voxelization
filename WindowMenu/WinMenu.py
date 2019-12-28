# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'WinMenu.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(460, 160)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(460, 160))
        MainWindow.setMaximumSize(QtCore.QSize(460, 160))
        MainWindow.setMouseTracking(False)
        MainWindow.setTabletTracking(False)
        MainWindow.setStatusTip("")
        MainWindow.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.button_FileChoose = QtWidgets.QPushButton(self.centralwidget)
        self.button_FileChoose.setGeometry(QtCore.QRect(10, 10, 101, 41))
        self.button_FileChoose.setObjectName("button_FileChoose")
        self.label_FilePath = QtWidgets.QLabel(self.centralwidget)
        self.label_FilePath.setGeometry(QtCore.QRect(120, 10, 331, 41))
        self.label_FilePath.setText("")
        self.label_FilePath.setObjectName("label_FilePath")
        self.label_TextVoxelSize = QtWidgets.QLabel(self.centralwidget)
        self.label_TextVoxelSize.setGeometry(QtCore.QRect(20, 60, 91, 31))
        self.label_TextVoxelSize.setObjectName("label_TextVoxelSize")
        self.doubleSpinBox_VoxelSize = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.doubleSpinBox_VoxelSize.setGeometry(QtCore.QRect(120, 60, 81, 41))
        self.doubleSpinBox_VoxelSize.setDecimals(3)
        self.doubleSpinBox_VoxelSize.setMinimum(0.001)
        self.doubleSpinBox_VoxelSize.setMaximum(10.0)
        self.doubleSpinBox_VoxelSize.setSingleStep(0.001)
        self.doubleSpinBox_VoxelSize.setProperty("value", 1.0)
        self.doubleSpinBox_VoxelSize.setObjectName("doubleSpinBox_VoxelSize")
        self.button_Reset = QtWidgets.QPushButton(self.centralwidget)
        self.button_Reset.setGeometry(QtCore.QRect(280, 70, 171, 81))
        self.button_Reset.setObjectName("button_Reset")
        self.button_Show = QtWidgets.QPushButton(self.centralwidget)
        self.button_Show.setGeometry(QtCore.QRect(20, 110, 111, 41))
        self.button_Show.setObjectName("button_Show")
        self.button_Save = QtWidgets.QPushButton(self.centralwidget)
        self.button_Save.setGeometry(QtCore.QRect(150, 110, 121, 41))
        self.button_Save.setObjectName("button_Save")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Mesh To Voxel"))
        self.button_FileChoose.setText(_translate("MainWindow", "Выбрать файл"))
        self.label_TextVoxelSize.setText(_translate("MainWindow", "Размер вокселя: "))
        self.button_Reset.setText(_translate("MainWindow", "Сброс"))
        self.button_Show.setText(_translate("MainWindow", "Показать"))
        self.button_Save.setText(_translate("MainWindow", "Сохранить"))
