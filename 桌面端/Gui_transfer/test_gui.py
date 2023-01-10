import cv2
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from PyQt5.QtWidgets import QVBoxLayout, QMainWindow, QApplication, QLabel, QWidget, QFileDialog
from PyQt5.QtGui import QPalette, QPixmap, QBrush
from PyQt5.QtCore import Qt
import numpy as np

from DeeplabTest import deeplab
from train_vgg_resnet import stylize, stylized


class Ui_MainWindow(QWidget):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1600, 900)
        ############################################################
        MainWindow.setFixedSize(MainWindow.width(), MainWindow.height())
        ##############################################################
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        font = QtGui.QFont()
        font.setFamily("Constantia")
        font.setPointSize(13)
        font.setBold(True)
        font.setWeight(75)
        self.centralwidget.setFont(font)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.main_gui = QtWidgets.QTabWidget(self.centralwidget)
        font = QtGui.QFont()
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.main_gui.setFont(font)
        self.main_gui.setFocusPolicy(QtCore.Qt.TabFocus)
        self.main_gui.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.main_gui.setAcceptDrops(False)
        self.main_gui.setTabShape(QtWidgets.QTabWidget.Triangular)
        self.main_gui.setObjectName("main_gui")
        self.photo_trtansfer = QtWidgets.QWidget()
        self.photo_trtansfer.setObjectName("photo_trtansfer")
        self.photo_pushButton_choice = QtWidgets.QPushButton(self.photo_trtansfer)
        self.photo_pushButton_choice.setGeometry(QtCore.QRect(160, 700, 200, 50))
        self.photo_pushButton_choice.setObjectName("photo_pushButton_choice")
        self.photo_label_input = QtWidgets.QLabel(self.photo_trtansfer)
        self.photo_label_input.setGeometry(QtCore.QRect(20, 200, 500, 400))
        self.photo_label_input.setObjectName("photo_label_input")
        ###############################################################
        self.photo_label_input.setFrameShape(QtWidgets.QFrame.Box)
        self.photo_label_input.setFrameShadow(QtWidgets.QFrame.Raised)
        self.photo_label_input.setLineWidth(2)
        # self.photo_label_title.setStyleSheet('background-color: rgb(178, 200, 187)')
        ###################################################################
        self.photo_label_title = QtWidgets.QLabel(self.photo_trtansfer)
        self.photo_label_title.setGeometry(QtCore.QRect(20, 80, 500, 100))
        self.photo_label_title.setWordWrap(False)
        self.photo_label_title.setIndent(-1)
        self.photo_label_title.setObjectName("photo_label_title")
        self.photo_label_title2 = QtWidgets.QLabel(self.photo_trtansfer)
        self.photo_label_title2.setGeometry(QtCore.QRect(615, 113, 70, 35))
        self.photo_label_title2.setObjectName("photo_label_title2")
        self.photo_label_title3 = QtWidgets.QLabel(self.photo_trtansfer)
        self.photo_label_title3.setGeometry(QtCore.QRect(615, 383, 70, 35))
        self.photo_label_title3.setObjectName("photo_label_title3")
        self.photo_comboBox_net = QtWidgets.QComboBox(self.photo_trtansfer)
        self.photo_comboBox_net.setGeometry(QtCore.QRect(685, 113, 200, 35))
        self.photo_comboBox_net.setObjectName("photo_comboBox_net")
        self.photo_comboBox_net.addItem("")
        self.photo_comboBox_net.addItem("")
        self.photo_comboBox_net.addItem("")
        self.photo_comboBox_type = QtWidgets.QComboBox(self.photo_trtansfer)
        self.photo_comboBox_type.setGeometry(QtCore.QRect(685, 383, 200, 35))
        self.photo_comboBox_type.setObjectName("photo_comboBox_type")
        self.photo_comboBox_type.addItem("")
        self.photo_comboBox_type.addItem("")
        self.photo_comboBox_type.addItem("")
        self.photo_comboBox_type.addItem("")
        self.photo_comboBox_type.addItem("")
        self.photo_comboBox_type.addItem("")
        self.photo_comboBox_type.addItem("")
        self.photo_comboBox_type.addItem("")
        self.photo_comboBox_type.addItem("")
        self.photo_comboBox_type.addItem("")
        self.photo_comboBox_type.addItem("")
        self.photo_comboBox_type.addItem("")
        self.photo_pushButton_start = QtWidgets.QPushButton(self.photo_trtansfer)
        self.photo_pushButton_start.setGeometry(QtCore.QRect(520, 700, 200, 50))
        self.photo_pushButton_start.setObjectName("photo_pushButton_start")
        self.photo_label_title4 = QtWidgets.QLabel(self.photo_trtansfer)
        self.photo_label_title4.setGeometry(QtCore.QRect(1050, 80, 500, 100))
        self.photo_label_title4.setObjectName("photo_label_title4")
        self.photo_label_output = QtWidgets.QLabel(self.photo_trtansfer)
        self.photo_label_output.setGeometry(QtCore.QRect(1050, 200, 500, 400))
        self.photo_label_output.setObjectName("photo_label_output")
        ###############################################################
        self.photo_label_output.setFrameShape(QtWidgets.QFrame.Box)
        self.photo_label_output.setFrameShadow(QtWidgets.QFrame.Raised)
        self.photo_label_output.setLineWidth(2)
        ###################################################################
        self.photo_pushButton_cancel = QtWidgets.QPushButton(self.photo_trtansfer)
        self.photo_pushButton_cancel.setGeometry(QtCore.QRect(880, 700, 200, 50))
        self.photo_pushButton_cancel.setObjectName("photo_pushButton_cancel")
        self.photo_pushButton_download = QtWidgets.QPushButton(self.photo_trtansfer)
        self.photo_pushButton_download.setGeometry(QtCore.QRect(1240, 700, 200, 50))
        self.photo_pushButton_download.setObjectName("photo_pushButton_download")
        self.main_gui.addTab(self.photo_trtansfer, "")
        self.video_transfer = QtWidgets.QWidget()
        self.video_transfer.setObjectName("video_transfer")
        self.main_gui.addTab(self.video_transfer, "")
        self.photo_cut = QtWidgets.QWidget()
        self.photo_cut.setObjectName("photo_cut")
        self.cutphoto_label_title_2 = QtWidgets.QLabel(self.photo_cut)
        self.cutphoto_label_title_2.setGeometry(QtCore.QRect(20, 80, 450, 100))
        self.cutphoto_label_title_2.setWordWrap(False)
        self.cutphoto_label_title_2.setIndent(-1)
        self.cutphoto_label_title_2.setObjectName("cutphoto_label_title_2")
        self.cutphoto_label_input = QtWidgets.QLabel(self.photo_cut)
        self.cutphoto_label_input.setGeometry(QtCore.QRect(20, 230, 450, 300))
        self.cutphoto_label_input.setObjectName("cutphoto_label_input")
        ###############################################################
        self.cutphoto_label_input.setFrameShape(QtWidgets.QFrame.Box)
        self.cutphoto_label_input.setFrameShadow(QtWidgets.QFrame.Raised)
        self.cutphoto_label_input.setLineWidth(2)
        # self.photo_label_title.setStyleSheet('background-color: rgb(178, 200, 187)')
        ###################################################################
        self.cutphoto_pushButton_choice = QtWidgets.QPushButton(self.photo_cut)
        self.cutphoto_pushButton_choice.setGeometry(QtCore.QRect(160, 700, 200, 50))
        self.cutphoto_pushButton_choice.setObjectName("cutphoto_pushButton_choice")
        self.cutphoto_label_title_3 = QtWidgets.QLabel(self.photo_cut)
        self.cutphoto_label_title_3.setGeometry(QtCore.QRect(850, 80, 500, 100))
        self.cutphoto_label_title_3.setObjectName("cutphoto_label_title_3")
        self.cutphoto_label_output_main = QtWidgets.QLabel(self.photo_cut)
        self.cutphoto_label_output_main.setGeometry(QtCore.QRect(600, 230, 450, 300))
        self.cutphoto_label_output_main.setObjectName("cutphoto_label_output_main")
        ###############################################################
        self.cutphoto_label_output_main.setFrameShape(QtWidgets.QFrame.Box)
        self.cutphoto_label_output_main.setFrameShadow(QtWidgets.QFrame.Raised)
        self.cutphoto_label_output_main.setLineWidth(2)
        # self.photo_label_title.setStyleSheet('background-color: rgb(178, 200, 187)')
        ###################################################################
        self.cutphoto_pushButton_cancel = QtWidgets.QPushButton(self.photo_cut)
        self.cutphoto_pushButton_cancel.setGeometry(QtCore.QRect(880, 700, 200, 50))
        self.cutphoto_pushButton_cancel.setObjectName("cutphoto_pushButton_cancel")
        self.cutphoto_pushButton_start = QtWidgets.QPushButton(self.photo_cut)
        self.cutphoto_pushButton_start.setGeometry(QtCore.QRect(520, 700, 200, 50))
        self.cutphoto_pushButton_start.setObjectName("cutphoto_pushButton_start")
        self.cutphoto_label_output_back = QtWidgets.QLabel(self.photo_cut)
        self.cutphoto_label_output_back.setGeometry(QtCore.QRect(1100, 230, 450, 300))
        self.cutphoto_label_output_back.setObjectName("cutphoto_label_output_back")
        ###############################################################
        self.cutphoto_label_output_back.setFrameShape(QtWidgets.QFrame.Box)
        self.cutphoto_label_output_back.setFrameShadow(QtWidgets.QFrame.Raised)
        self.cutphoto_label_output_back.setLineWidth(2)
        # self.photo_label_title.setStyleSheet('background-color: rgb(178, 200, 187)')
        ###################################################################
        self.cutphoto_label = QtWidgets.QLabel(self.photo_cut)
        self.cutphoto_label.setGeometry(QtCore.QRect(530, 340, 41, 61))
        self.cutphoto_label.setText("")
        self.cutphoto_label.setPixmap(QtGui.QPixmap("img/箭头.png"))
        self.cutphoto_label.setScaledContents(True)
        self.cutphoto_label.setObjectName("cutphoto_label")
        self.cutphoto_pushButton_download = QtWidgets.QPushButton(self.photo_cut)
        self.cutphoto_pushButton_download.setGeometry(QtCore.QRect(1240, 700, 200, 50))
        self.cutphoto_pushButton_download.setObjectName("cutphoto_pushButton_download")
        self.main_gui.addTab(self.photo_cut, "")
        self.deeplabv3 = QtWidgets.QWidget()
        self.deeplabv3.setObjectName("deeplabv3")
        self.cut_label_title1 = QtWidgets.QLabel(self.deeplabv3)
        self.cut_label_title1.setGeometry(QtCore.QRect(20, 80, 500, 100))
        self.cut_label_title1.setWordWrap(False)
        self.cut_label_title1.setIndent(-1)
        self.cut_label_title1.setObjectName("cut_label_title1")
        self.cut_label_input = QtWidgets.QLabel(self.deeplabv3)
        self.cut_label_input.setGeometry(QtCore.QRect(20, 200, 500, 400))
        self.cut_label_input.setObjectName("cut_label_input")
        ###############################################################
        self.cut_label_input.setFrameShape(QtWidgets.QFrame.Box)
        self.cut_label_input.setFrameShadow(QtWidgets.QFrame.Raised)
        self.cut_label_input.setLineWidth(2)
        # self.photo_label_title.setStyleSheet('background-color: rgb(178, 200, 187)')
        ###################################################################
        self.cut_pushButton_choice = QtWidgets.QPushButton(self.deeplabv3)
        self.cut_pushButton_choice.setGeometry(QtCore.QRect(160, 700, 200, 50))
        self.cut_pushButton_choice.setObjectName("cut_pushButton_choice")
        self.cut_label_title2 = QtWidgets.QLabel(self.deeplabv3)
        self.cut_label_title2.setGeometry(QtCore.QRect(615, 113, 70, 35))
        self.cut_label_title2.setObjectName("cut_label_title2")
        self.cut_comboBox_net = QtWidgets.QComboBox(self.deeplabv3)
        self.cut_comboBox_net.setGeometry(QtCore.QRect(685, 113, 200, 35))
        self.cut_comboBox_net.setObjectName("cut_comboBox_net")
        self.cut_comboBox_net.addItem("")
        self.cut_comboBox_net.addItem("")
        self.cut_comboBox_net.addItem("")
        self.cut_label_title3 = QtWidgets.QLabel(self.deeplabv3)
        self.cut_label_title3.setGeometry(QtCore.QRect(615, 383, 70, 35))
        self.cut_label_title3.setObjectName("cut_label_title3")
        self.cut_comboBox_type = QtWidgets.QComboBox(self.deeplabv3)
        self.cut_comboBox_type.setGeometry(QtCore.QRect(685, 383, 200, 35))
        self.cut_comboBox_type.setObjectName("cut_comboBox_type")
        self.cut_comboBox_type.addItem("")
        self.cut_comboBox_type.addItem("")
        self.cut_comboBox_type.addItem("")
        self.cut_comboBox_type.addItem("")
        self.cut_comboBox_type.addItem("")
        self.cut_comboBox_type.addItem("")
        self.cut_comboBox_type.addItem("")
        self.cut_comboBox_type.addItem("")
        self.cut_comboBox_type.addItem("")
        self.cut_comboBox_type.addItem("")
        self.cut_comboBox_type.addItem("")
        self.cut_comboBox_type.addItem("")
        self.cut_pushButton_start = QtWidgets.QPushButton(self.deeplabv3)
        self.cut_pushButton_start.setGeometry(QtCore.QRect(520, 700, 200, 50))
        self.cut_pushButton_start.setObjectName("cut_pushButton_start")
        self.cut_label_title4 = QtWidgets.QLabel(self.deeplabv3)
        self.cut_label_title4.setGeometry(QtCore.QRect(1050, 80, 500, 100))
        self.cut_label_title4.setObjectName("cut_label_title4")
        self.cut_label_title5 = QtWidgets.QLabel(self.deeplabv3)
        self.cut_label_title5.setGeometry(QtCore.QRect(1050, 200, 500, 400))
        self.cut_label_title5.setObjectName("cut_label_title5")
        ###############################################################
        self.cut_label_title5.setFrameShape(QtWidgets.QFrame.Box)
        self.cut_label_title5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.cut_label_title5.setLineWidth(2)
        # self.photo_label_title.setStyleSheet('background-color: rgb(178, 200, 187)')
        ###################################################################
        self.cut_pushButton_cancel = QtWidgets.QPushButton(self.deeplabv3)
        self.cut_pushButton_cancel.setGeometry(QtCore.QRect(880, 700, 200, 50))
        self.cut_pushButton_cancel.setObjectName("cut_pushButton_cancel")
        self.cut_pushButton_download = QtWidgets.QPushButton(self.deeplabv3)
        self.cut_pushButton_download.setGeometry(QtCore.QRect(1240, 700, 200, 50))
        self.cut_pushButton_download.setObjectName("cut_pushButton_download")
        self.main_gui.addTab(self.deeplabv3, "")
        self.transfer_type = QtWidgets.QWidget()
        self.transfer_type.setObjectName("transfer_type")
        self.transfer_label_title1 = QtWidgets.QLabel(self.transfer_type)
        self.transfer_label_title1.setGeometry(QtCore.QRect(20, 50, 450, 100))
        self.transfer_label_title1.setWordWrap(False)
        self.transfer_label_title1.setIndent(-1)
        self.transfer_label_title1.setObjectName("transfer_label_title1")
        self.transfer_label_input = QtWidgets.QLabel(self.transfer_type)
        self.transfer_label_input.setGeometry(QtCore.QRect(10, 230, 450, 300))
        self.transfer_label_input.setObjectName(
            "transfer_label_input")  ###############################################################
        self.transfer_label_input.setFrameShape(QtWidgets.QFrame.Box)
        self.transfer_label_input.setFrameShadow(QtWidgets.QFrame.Raised)
        self.transfer_label_input.setLineWidth(2)
        # self.photo_label_title.setStyleSheet('background-color: rgb(178, 200, 187)')
        ###################################################################
        self.transfer_pushButton_choice = QtWidgets.QPushButton(self.transfer_type)
        self.transfer_pushButton_choice.setGeometry(QtCore.QRect(50, 700, 200, 50))
        self.transfer_pushButton_choice.setObjectName("transfer_pushButton_choice")
        self.transfer_label_intype = QtWidgets.QLabel(self.transfer_type)
        self.transfer_label_intype.setGeometry(QtCore.QRect(550, 230, 450, 300))
        self.transfer_label_intype.setObjectName("transfer_label_intype")
        ###############################################################
        self.transfer_label_intype.setFrameShape(QtWidgets.QFrame.Box)
        self.transfer_label_intype.setFrameShadow(QtWidgets.QFrame.Raised)
        self.transfer_label_intype.setLineWidth(2)
        # self.photo_label_title.setStyleSheet('background-color: rgb(178, 200, 187)')
        ###################################################################
        self.transfer_label_output = QtWidgets.QLabel(self.transfer_type)
        self.transfer_label_output.setGeometry(QtCore.QRect(1100, 230, 450, 300))
        self.transfer_label_output.setObjectName("transfer_label_output")
        ###############################################################
        self.transfer_label_output.setFrameShape(QtWidgets.QFrame.Box)
        self.transfer_label_output.setFrameShadow(QtWidgets.QFrame.Raised)
        self.transfer_label_output.setLineWidth(2)
        # self.photo_label_title.setStyleSheet('background-color: rgb(178, 200, 187)')
        ###################################################################
        self.transfer_label_title2 = QtWidgets.QLabel(self.transfer_type)
        self.transfer_label_title2.setGeometry(QtCore.QRect(590, 50, 450, 100))
        self.transfer_label_title2.setObjectName("transfer_label_title2")
        self.transfer_label_title3 = QtWidgets.QLabel(self.transfer_type)
        self.transfer_label_title3.setGeometry(QtCore.QRect(1110, 50, 450, 100))
        self.transfer_label_title3.setObjectName("transfer_label_title3")
        self.label_2 = QtWidgets.QLabel(self.transfer_type)
        self.label_2.setGeometry(QtCore.QRect(1030, 350, 40, 60))
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap("img/箭头.png"))
        self.label_2.setScaledContents(True)
        self.label_2.setObjectName("label_2")
        self.transfer_pushButton_start = QtWidgets.QPushButton(self.transfer_type)
        self.transfer_pushButton_start.setGeometry(QtCore.QRect(700, 700, 200, 50))
        self.transfer_pushButton_start.setObjectName("transfer_pushButton_start")
        self.transfer_pushButton_cancel = QtWidgets.QPushButton(self.transfer_type)
        self.transfer_pushButton_cancel.setGeometry(QtCore.QRect(1025, 700, 200, 50))
        self.transfer_pushButton_cancel.setObjectName("transfer_pushButton_cancel")
        self.transfer_pushButton_type = QtWidgets.QPushButton(self.transfer_type)
        self.transfer_pushButton_type.setGeometry(QtCore.QRect(375, 700, 200, 50))
        self.transfer_pushButton_type.setObjectName("transfer_pushButton_type")
        self.photo_label_title2_2 = QtWidgets.QLabel(self.transfer_type)
        self.photo_label_title2_2.setGeometry(QtCore.QRect(970, 580, 70, 35))
        self.photo_label_title2_2.setObjectName("photo_label_title2_2")
        self.photo_comboBox_net_2 = QtWidgets.QComboBox(self.transfer_type)
        self.photo_comboBox_net_2.setGeometry(QtCore.QRect(1040, 580, 200, 35))
        self.photo_comboBox_net_2.setObjectName("photo_comboBox_net_2")
        self.photo_comboBox_net_2.addItem("")
        self.photo_comboBox_net_2.addItem("")
        self.photo_comboBox_net_2.addItem("")
        self.transfer_pushButton_download = QtWidgets.QPushButton(self.transfer_type)
        self.transfer_pushButton_download.setGeometry(QtCore.QRect(1350, 700, 200, 50))
        self.transfer_pushButton_download.setObjectName("transfer_pushButton_download")
        self.main_gui.addTab(self.transfer_type, "")
        self.horizontalLayout.addWidget(self.main_gui)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.main_gui.setCurrentIndex(0)
        ###############################################################
        self.photo_pushButton_choice.clicked.connect(self.photo_pushButton_choice_def)  ####快速_选择
        self.photo_pushButton_start.clicked.connect(self.photo_pushButton_start_def)  ####快速_开始
        self.photo_pushButton_cancel.clicked.connect(self.photo_pushButton_cancel_def)  ####快速_取消
        self.photo_pushButton_download.clicked.connect(self.photo_pushButton_download_def)
        self.cutphoto_pushButton_download.clicked.connect(self.cutphoto_pushButton_download_def)
        self.cut_pushButton_download.clicked.connect(self.cut_pushButton_download_def)
        self.transfer_pushButton_download.clicked.connect(self.transfer_pushButton_download_def)
        self.cutphoto_pushButton_choice.clicked.connect(self.cutphoto_pushButton_choice_def)  ####图像分割_选择
        self.cutphoto_pushButton_start.clicked.connect(self.cutphoto_pushButton_start_def)  ####图像分割_开始
        self.cutphoto_pushButton_cancel.clicked.connect(self.cutphoto_pushButton_cancel_def)  ####图像分割_取消
        self.cut_pushButton_choice.clicked.connect(self.cut_pushButton_choice_def)  ####局部分割_选择
        self.cut_pushButton_start.clicked.connect(self.cut_pushButton_start_def)  ####局部分割_开始
        self.cut_pushButton_cancel.clicked.connect(self.cut_pushButton_cancel_def)  ####局部分割_取消
        self.transfer_pushButton_choice.clicked.connect(self.transfer_pushButton_choiced_def)  ####高级_选择
        self.transfer_pushButton_start.clicked.connect(self.transfer_pushButton_start_def)  ####高级_开始
        self.transfer_pushButton_type.clicked.connect(self.transfer_pushButton_type_def)  ####高级_风格
        self.transfer_pushButton_cancel.clicked.connect(self.transfer_pushButton_cancel_def)  ####高级_取消
        self.photo_comboBox_type.currentIndexChanged.connect(self.photo_comboBox_type_def)
        self.cut_comboBox_net.currentIndexChanged.connect(self.cut_comboBox_net_def)
        self.cut_comboBox_type.currentIndexChanged.connect(self.cut_comboBox_type_def)
        self.photo_comboBox_net.currentIndexChanged.connect(self.photo_comboBox_net_def)
        self.photo_comboBox_net_2.currentIndexChanged.connect(self.photo_comboBox_net_2_def)
        ###################################################################
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.photo_pushButton_choice.setText(_translate("MainWindow", "选择"))
        self.photo_label_input.setText(_translate("MainWindow",
                                                  "<html><head/><body><p align=\"center\"><span style=\" font-size:14pt; color:#c2c2c2;\">输入图片</span></p></body></html>"))
        self.photo_label_title.setText(_translate("MainWindow",
                                                  "<html><head/><body><p align=\"center\"><span style=\" font-size:14pt; font-weight:600; color:#000000;\">原图片</span></p></body></html>"))
        self.photo_label_title2.setText(_translate("MainWindow",
                                                   "<html><head/><body><p align=\"center\"><span style=\" font-size:14pt; font-weight:600; color:#000000;\">网络:</span></p></body></html>"))
        self.photo_label_title3.setText(_translate("MainWindow",
                                                   "<html><head/><body><p align=\"center\"><span style=\" font-size:14pt; font-weight:600; color:#000000;\">风格:</span></p></body></html>"))
        self.photo_comboBox_net.setItemText(0, _translate("MainWindow", "Vgg"))
        self.photo_comboBox_net.setItemText(1, _translate("MainWindow", "Resnet"))
        self.photo_comboBox_net.setItemText(2, _translate("MainWindow", "CycleGan"))
        self.photo_comboBox_type.setItemText(0, _translate("MainWindow", "Candy"))
        self.photo_comboBox_type.setItemText(1, _translate("MainWindow", "Cezanne"))
        self.photo_comboBox_type.setItemText(2, _translate("MainWindow", "Cubist"))
        self.photo_comboBox_type.setItemText(3, _translate("MainWindow", "Monet"))
        self.photo_comboBox_type.setItemText(4, _translate("MainWindow", "Muse"))
        self.photo_comboBox_type.setItemText(5, _translate("MainWindow", "Rain"))
        self.photo_comboBox_type.setItemText(6, _translate("MainWindow", "Screen"))
        self.photo_comboBox_type.setItemText(7, _translate("MainWindow", "Shipwreck"))
        self.photo_comboBox_type.setItemText(8, _translate("MainWindow", "Strarry"))
        self.photo_comboBox_type.setItemText(9, _translate("MainWindow", "Udnie"))
        self.photo_comboBox_type.setItemText(10, _translate("MainWindow", "ukiyoe"))
        self.photo_comboBox_type.setItemText(11, _translate("MainWindow", "vangogh"))
        self.photo_pushButton_start.setText(_translate("MainWindow", "开始"))
        self.photo_label_title4.setText(_translate("MainWindow",
                                                   "<html><head/><body><p align=\"center\"><span style=\" font-size:14pt; color:#000000;\">生成图片</span></p></body></html>"))
        self.photo_label_output.setText(_translate("MainWindow",
                                                   "<html><head/><body><p align=\"center\"><span style=\" font-size:14pt; color:#c2c2c2;\">生成图片</span></p></body></html>"))
        self.photo_pushButton_cancel.setText(_translate("MainWindow", "取消"))
        self.photo_pushButton_download.setText(_translate("MainWindow", "保存"))
        self.main_gui.setTabText(self.main_gui.indexOf(self.photo_trtansfer), _translate("MainWindow", "图像风格迁移"))
        self.main_gui.setTabText(self.main_gui.indexOf(self.video_transfer), _translate("MainWindow", "视频风格迁移"))
        self.cutphoto_label_title_2.setText(_translate("MainWindow",
                                                       "<html><head/><body><p align=\"center\"><span style=\" font-size:14pt; font-weight:600; color:#000000;\">原图片</span></p></body></html>"))
        self.cutphoto_label_input.setText(_translate("MainWindow",
                                                     "<html><head/><body><p align=\"center\"><span style=\" font-size:14pt; color:#c2c2c2;\">输入图片</span></p></body></html>"))
        self.cutphoto_pushButton_choice.setText(_translate("MainWindow", "选择"))
        self.cutphoto_label_title_3.setText(_translate("MainWindow",
                                                       "<html><head/><body><p align=\"center\"><span style=\" font-size:14pt; color:#000000;\">生成图片</span></p></body></html>"))
        self.cutphoto_label_output_main.setText(_translate("MainWindow",
                                                           "<html><head/><body><p align=\"center\"><span style=\" font-size:14pt; color:#c2c2c2;\">生成主图片</span></p></body></html>"))
        self.cutphoto_pushButton_cancel.setText(_translate("MainWindow", "取消"))
        self.cutphoto_pushButton_start.setText(_translate("MainWindow", "开始"))
        self.cutphoto_label_output_back.setText(_translate("MainWindow",
                                                           "<html><head/><body><p align=\"center\"><span style=\" font-size:14pt; color:#c2c2c2;\">生成背景图片</span></p></body></html>"))
        self.cutphoto_pushButton_download.setText(_translate("MainWindow", "保存"))
        self.main_gui.setTabText(self.main_gui.indexOf(self.photo_cut), _translate("MainWindow", "图像分割"))
        self.cut_label_title1.setText(_translate("MainWindow",
                                                 "<html><head/><body><p align=\"center\"><span style=\" font-size:14pt; font-weight:600; color:#000000;\">原图片</span></p></body></html>"))
        self.cut_label_input.setText(_translate("MainWindow",
                                                "<html><head/><body><p align=\"center\"><span style=\" font-size:14pt; color:#c2c2c2;\">输入图片</span></p></body></html>"))
        self.cut_pushButton_choice.setText(_translate("MainWindow", "选择"))
        self.cut_label_title2.setText(_translate("MainWindow",
                                                 "<html><head/><body><p align=\"center\"><span style=\" font-size:14pt; font-weight:600; color:#000000;\">网络:</span></p></body></html>"))
        self.cut_comboBox_net.setItemText(0, _translate("MainWindow", "Vgg"))
        self.cut_comboBox_net.setItemText(1, _translate("MainWindow", "Resnet"))
        self.cut_comboBox_net.setItemText(2, _translate("MainWindow", "CycleGan"))
        self.cut_label_title3.setText(_translate("MainWindow",
                                                 "<html><head/><body><p align=\"center\"><span style=\" font-size:14pt; font-weight:600; color:#000000;\">风格:</span></p></body></html>"))
        self.cut_comboBox_type.setItemText(0, _translate("MainWindow", "Candy"))
        self.cut_comboBox_type.setItemText(1, _translate("MainWindow", "Cezanne"))
        self.cut_comboBox_type.setItemText(2, _translate("MainWindow", "Cubist"))
        self.cut_comboBox_type.setItemText(3, _translate("MainWindow", "Monet"))
        self.cut_comboBox_type.setItemText(4, _translate("MainWindow", "Muse"))
        self.cut_comboBox_type.setItemText(5, _translate("MainWindow", "Rain"))
        self.cut_comboBox_type.setItemText(6, _translate("MainWindow", "Screen"))
        self.cut_comboBox_type.setItemText(7, _translate("MainWindow", "Shipwreck"))
        self.cut_comboBox_type.setItemText(8, _translate("MainWindow", "Strarry"))
        self.cut_comboBox_type.setItemText(9, _translate("MainWindow", "Udnie"))
        self.cut_comboBox_type.setItemText(10, _translate("MainWindow", "ukiyoe"))
        self.cut_comboBox_type.setItemText(11, _translate("MainWindow", "vangogh"))
        self.cut_pushButton_start.setText(_translate("MainWindow", "开始"))
        self.cut_label_title4.setText(_translate("MainWindow",
                                                 "<html><head/><body><p align=\"center\"><span style=\" font-size:14pt; color:#000000;\">生成图片</span></p></body></html>"))
        self.cut_label_title5.setText(_translate("MainWindow",
                                                 "<html><head/><body><p align=\"center\"><span style=\" font-size:14pt; color:#c2c2c2;\">生成图片</span></p></body></html>"))
        self.cut_pushButton_cancel.setText(_translate("MainWindow", "取消"))
        self.cut_pushButton_download.setText(_translate("MainWindow", "保存"))
        self.main_gui.setTabText(self.main_gui.indexOf(self.deeplabv3), _translate("MainWindow", "局部风格迁移"))
        self.transfer_label_title1.setText(_translate("MainWindow",
                                                      "<html><head/><body><p align=\"center\"><span style=\" font-size:14pt; font-weight:600; color:#000000;\">原图片</span></p></body></html>"))
        self.transfer_label_input.setText(_translate("MainWindow",
                                                     "<html><head/><body><p align=\"center\"><span style=\" font-size:14pt; color:#c2c2c2;\">输入图片</span></p></body></html>"))
        self.transfer_pushButton_choice.setText(_translate("MainWindow", "选择图片"))
        self.transfer_label_intype.setText(_translate("MainWindow",
                                                      "<html><head/><body><p align=\"center\"><span style=\" font-size:14pt; color:#c2c2c2;\">风格图片</span></p></body></html>"))
        self.transfer_label_output.setText(_translate("MainWindow",
                                                      "<html><head/><body><p align=\"center\"><span style=\" font-size:14pt; color:#c2c2c2;\">生成图片</span></p></body></html>"))
        self.transfer_label_title2.setText(_translate("MainWindow",
                                                      "<html><head/><body><p align=\"center\"><span style=\" font-size:14pt; color:#000000;\">生成图片</span></p></body></html>"))
        self.transfer_label_title3.setText(_translate("MainWindow",
                                                      "<html><head/><body><p align=\"center\"><span style=\" font-size:14pt; color:#000000;\">生成图片</span></p></body></html>"))
        self.transfer_pushButton_start.setText(_translate("MainWindow", "开始"))
        self.transfer_pushButton_cancel.setText(_translate("MainWindow", "取消"))
        self.transfer_pushButton_type.setText(_translate("MainWindow", "选择风格"))
        self.photo_label_title2_2.setText(_translate("MainWindow",
                                                     "<html><head/><body><p align=\"center\"><span style=\" font-size:14pt; font-weight:600; color:#000000;\">网络:</span></p></body></html>"))
        self.photo_comboBox_net_2.setItemText(0, _translate("MainWindow", "Vgg"))
        self.photo_comboBox_net_2.setItemText(1, _translate("MainWindow", "Resnet"))
        self.photo_comboBox_net_2.setItemText(2, _translate("MainWindow", "CycleGan"))
        self.transfer_pushButton_download.setText(_translate("MainWindow", "保存"))
        self.main_gui.setTabText(self.main_gui.indexOf(self.transfer_type), _translate("MainWindow", "高级功能"))

        ############################################################################################################

    def photo_pushButton_choice_def(self):
        self.photo_pushButton_input_imgName, imgType = QFileDialog.getOpenFileName(self.centralwidget, "打开图片", "",
                                                                                   "*.jpg;;*.png;;All Files(*)")
        jpg = QtGui.QPixmap(self.photo_pushButton_input_imgName).scaled(self.photo_label_input.width(),
                                                                        self.photo_label_input.height())
        self.photo_label_input.setPixmap(jpg)
        self.photo_label_input.setScaledContents(True)

    def photo_pushButton_start_def(self):
        stylize("checkpoint/b_resnet.pth", self.photo_pushButton_input_imgName)
        self.photo_pushButton_output_image = "photo/photo_transfer/{}_transfer.png".format(
            self.photo_pushButton_input_imgName.split('/')[-1][:-4])
        jpg = QtGui.QPixmap(self.photo_pushButton_output_image).scaled(self.photo_label_output.width(),
                                                                       self.photo_label_output.height())
        self.photo_label_output.setPixmap(jpg)
        self.photo_label_output.setScaledContents(True)

    def photo_pushButton_cancel_def(self):
        _translate = QtCore.QCoreApplication.translate
        self.photo_label_input.clear()
        self.photo_label_output.clear()
        self.photo_label_input.setText(_translate("MainWindow",
                                                  "<html><head/><body><p align=\"center\"><span style=\" font-size:14pt; color:#c2c2c2;\">输入图片</span></p></body></html>"))
        self.photo_label_output.setText(_translate("MainWindow",
                                                   "<html><head/><body><p align=\"center\"><span style=\" font-size:14pt; color:#c2c2c2;\">生成图片</span></p></body></html>"))

    def cutphoto_pushButton_choice_def(self):
        self.cutpushButton_input_imgName, imgType = QFileDialog.getOpenFileName(self.centralwidget, "打开图片", "",
                                                                                "*.jpg;;*.png;;All Files(*)")
        jpg = QtGui.QPixmap(self.cutpushButton_input_imgName).scaled(self.cutphoto_label_input.width(),
                                                                     self.cutphoto_label_input.height())
        self.cutphoto_label_input.setPixmap(jpg)
        self.cutphoto_label_input.setScaledContents(True)

    def cutphoto_pushButton_start_def(self):
        deeplab(self.cutpushButton_input_imgName)
        self.cutpushButton_output_back = "photo/photo_cut/cut_back/{}_back.png".format(
            self.cutpushButton_input_imgName.split('/')[-1][:-4])
        jpg_back = QtGui.QPixmap(self.cutpushButton_output_back).scaled(self.cutphoto_label_output_back.width(),
                                                                        self.cutphoto_label_output_back.height())
        self.cutpushButton_output_main = "photo/photo_cut/cut_main/{}_main.png".format(
            self.cutpushButton_input_imgName.split('/')[-1][:-4])
        jpg_main = QtGui.QPixmap(self.cutpushButton_output_main).scaled(self.cutphoto_label_output_main.width(),
                                                                        self.cutphoto_label_output_main.height())
        self.cutphoto_label_output_back.setPixmap(jpg_back)
        self.cutphoto_label_output_back.setScaledContents(True)
        self.cutphoto_label_output_main.setPixmap(jpg_main)
        self.cutphoto_label_output_main.setScaledContents(True)

    def cutphoto_pushButton_cancel_def(self):
        _translate = QtCore.QCoreApplication.translate
        self.cutphoto_label_input.clear()
        self.cutphoto_label_output_back.clear()
        self.cutphoto_label_output_main.clear()
        self.cutphoto_label_input.setText(_translate("MainWindow",
                                                     "<html><head/><body><p align=\"center\"><span style=\" font-size:14pt; color:#c2c2c2;\">输入图片</span></p></body></html>"))
        self.cutphoto_label_output_back.setText(_translate("MainWindow",
                                                           "<html><head/><body><p align=\"center\"><span style=\" font-size:14pt; color:#c2c2c2;\">生成背景图片</span></p></body></html>"))
        self.cutphoto_label_output_main.setText(_translate("MainWindow",
                                                           "<html><head/><body><p align=\"center\"><span style=\" font-size:14pt; color:#c2c2c2;\">生成主图片</span></p></body></html>"))

    def cut_pushButton_choice_def(self):
        self.cut_pushButton_input_imgName, imgType = QFileDialog.getOpenFileName(self.centralwidget, "打开图片", "",
                                                                                 "*.jpg;;*.png;;All Files(*)")
        jpg = QtGui.QPixmap(self.cut_pushButton_input_imgName).scaled(self.cut_label_input.width(),
                                                                      self.cut_label_input.height())
        self.cut_label_input.setPixmap(jpg)
        self.cut_label_input.setScaledContents(True)

    def cut_pushButton_start_def(self):
        deeplab(self.cut_pushButton_input_imgName)
        stylized("checkpoint/b_resnet.pth",  #################
                 "photo/photo_cut/cut_back/{}_back.png".format(self.cut_pushButton_input_imgName.split('/')[-1][:-4]),
                 'photo/photo_cut/cut_back_transfer/' + "{}_back_transfer.jpg".format(
                     self.cut_pushButton_input_imgName.split('/')[-1][:-4]))

        masked = cv2.imread(
            'photo/photo_cut/cut_main/' + "{}_main.png".format(self.cut_pushButton_input_imgName.split('/')[-1][:-4]))
        mained = cv2.imread('photo/photo_cut/cut_back_transfer/' + "{}_back_transfer.jpg".format(
            self.cut_pushButton_input_imgName.split('/')[-1][:-4]))
        real_mask = cv2.imread(
            'photo/photo_cut/cut_mask/' + "{}_mask.png".format(self.cut_pushButton_input_imgName.split('/')[-1][:-4]))
        img_info = masked.shape
        image_height = img_info[0]
        image_weight = img_info[1]
        dst_back = np.full((image_height, image_weight, 3), 255, np.uint8)
        for i in range(image_height):
            for j in range(image_weight):
                (ra, rb, rc) = real_mask[i][j]
                (b, g, r) = masked[i][j]
                (a, c, d) = mained[i][j]
                if (ra, rb, rc) == (0, 0, 0):
                    dst_back[i][j] = (a, c, d)
                else:
                    dst_back[i][j] = (b, g, r)
        cv2.imwrite('photo/photo_cut/cut_transfer/' + "{}_transfer.png".format(
            self.cut_pushButton_input_imgName.split('/')[-1][:-4]), dst_back)
        cv2.waitKey(0)
        jpg = QtGui.QPixmap('photo/photo_cut/cut_transfer/' + "{}_transfer.png".format(
            self.cut_pushButton_input_imgName.split('/')[-1][:-4])).scaled(self.cut_label_title5.width(),
                                                                           self.cut_label_title5.height())
        self.cut_label_title5.setPixmap(jpg)
        self.cut_label_title5.setScaledContents(True)

    def cut_pushButton_cancel_def(self):
        _translate = QtCore.QCoreApplication.translate
        self.cut_label_title5.clear()
        self.cut_label_input.clear()
        self.cut_label_title5.setText(_translate("MainWindow",
                                                 "<html><head/><body><p align=\"center\"><span style=\" font-size:14pt; color:#c2c2c2;\">生成图片</span></p></body></html>"))
        self.cut_label_input.setText(_translate("MainWindow",
                                                "<html><head/><body><p align=\"center\"><span style=\" font-size:14pt; color:#c2c2c2;\">输入图片</span></p></body></html>"))

    def transfer_pushButton_choiced_def(self):
        self.transfer_pushButton_input_inimgName, imgType = QFileDialog.getOpenFileName(self.centralwidget, "打开图片", "",
                                                                                        "*.jpg;;*.png;;All Files(*)")
        jpg = QtGui.QPixmap(self.transfer_pushButton_input_inimgName).scaled(self.transfer_label_input.width(),
                                                                             self.transfer_label_input.height())
        self.transfer_label_input.setPixmap(jpg)
        self.transfer_label_input.setScaledContents(True)

    def transfer_pushButton_start_def(self):
        pass

    def transfer_pushButton_type_def(self):
        self.transfer_pushButton_input_typeimgName, imgType = QFileDialog.getOpenFileName(self.centralwidget, "打开图片",
                                                                                          "",
                                                                                          "*.jpg;;*.png;;All Files(*)")
        jpg = QtGui.QPixmap(self.transfer_pushButton_input_typeimgName).scaled(self.transfer_label_intype.width(),
                                                                               self.transfer_label_intype.height())
        self.transfer_label_intype.setPixmap(jpg)
        self.transfer_label_intype.setScaledContents(True)

    def transfer_pushButton_cancel_def(self):
        _translate = QtCore.QCoreApplication.translate
        self.transfer_label_intype.clear()
        self.transfer_label_input.clear()
        self.transfer_label_output.clear()
        self.transfer_label_intype.setText(_translate("MainWindow",
                                                      "<html><head/><body><p align=\"center\"><span style=\" font-size:14pt; color:#c2c2c2;\">风格图片</span></p></body></html>"))
        self.transfer_label_input.setText(_translate("MainWindow",
                                                     "<html><head/><body><p align=\"center\"><span style=\" font-size:14pt; color:#c2c2c2;\">输入图片</span></p></body></html>"))
        self.transfer_label_output.setText(_translate("MainWindow",
                                                      "<html><head/><body><p align=\"center\"><span style=\" font-size:14pt; color:#c2c2c2;\">生成图片</span></p></body></html>"))

    def photo_pushButton_download_def(self):

        temp = cv2.imread(self.photo_pushButton_output_image)
        fileName2, ok2 = QFileDialog.getSaveFileName(self.centralwidget, "另保存图片", "", "*.jpg;;*.png;;All Files(*)")
        cv2.imwrite(fileName2, temp)

    def cutphoto_pushButton_download_def(self):
        temp = cv2.imread(self.cutpushButton_output_back)
        fileName2, ok2 = QFileDialog.getSaveFileName(self.centralwidget, "另保存图片", "", "*.jpg;;*.png;;All Files(*)")
        cv2.imwrite(fileName2, temp)

        temp = cv2.imread(self.cutpushButton_output_main)
        fileName2, ok2 = QFileDialog.getSaveFileName(self.centralwidget, "另保存图片", "", "*.jpg;;*.png;;All Files(*)")
        cv2.imwrite(fileName2, temp)

    def cut_pushButton_download_def(self):
        temp = cv2.imread('photo/photo_cut/cut_transfer/' + "{}_transfer.png".format(
            self.cut_pushButton_input_imgName.split('/')[-1][:-4]))
        fileName2, ok2 = QFileDialog.getSaveFileName(self.centralwidget, "另保存图片", "", "*.jpg;;*.png;;All Files(*)")
        cv2.imwrite(fileName2, temp)

    def transfer_pushButton_download_def(self):
        pass
        # temp = cv2.imread('photo/photo_cut/cut_transfer/' + "{}_transfer.png".format(
        #     self.cut_pushButton_input_imgName.split('/')[-1][:-4]))
        # fileName2, ok2 = QFileDialog.getSaveFileName(None, "文件保存", "H:/")
        # cv2.imwrite(fileName2, temp)

    def photo_comboBox_type_def(self,i):
        self.photo_comboBox_type_choice=self.photo_comboBox_type.currentText()
        # print(self.photo_comboBox_type_choice)

    def cut_comboBox_net_def(self,i):
        self.cut_comboBox_net_choice = self.cut_comboBox_net.currentText()

    def cut_comboBox_type_def(self,i):
        self.cut_comboBox_type_choice = self.cut_comboBox_type.currentText()


    def photo_comboBox_net_def(self,i):
        self.photo_comboBox_net_choice = self.photo_comboBox_net.currentText()

    def photo_comboBox_net_2_def(self,i):
        self.photo_comboBox_net_2_choice = self.photo_comboBox_net_2.currentText()




if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
