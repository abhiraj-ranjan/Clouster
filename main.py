from PyQt5 import QtWidgets, QtCore, QtGui
import sys, os, sqlite3, subprocess
from request_api import call
import pandas as pd
import numpy as np


class pandasModel(QtCore.QAbstractTableModel):
    def __init__(self, data):
        QtCore.QAbstractTableModel.__init__(self)
        self._data = data

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parent=None):
        return self._data.shape[1]

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if index.isValid():
            if role == QtCore.Qt.DisplayRole:
                return str(self._data.iloc[index.row(), index.column()])
        return None

    def headerData(self, col, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self._data.columns[col]
        return None

class WorkerSignals(QtCore.QObject):
    result   = QtCore.pyqtSignal(object)
    error    = QtCore.pyqtSignal()
    finished = QtCore.pyqtSignal()

class Worker(QtCore.QRunnable):
    def __init__(self, fn,*args , **kwargs):
        super().__init__()
        self.fn      = fn
        self.args    = args
        self.kwargs  = kwargs
        self.signals = WorkerSignals()
        
    QtCore.pyqtSlot()
    def run(self):
        try:
            result = self.fn(*self.args, **self.kwargs)
        except:
            self.signals.error.emit()
        else:
            self.signals.result.emit(result)
        finally:
            self.signals.finished.emit()


class Signals(QtCore.QObject):
    finished = QtCore.pyqtSignal()
    error = QtCore.pyqtSignal(object)

class btn(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.signals = Signals()
        
        self.frame = QtWidgets.QFrame(self)
        self.frame.hide()
        
        self.framebar = QtWidgets.QFrame(self)
        self.framebar.hide()

        self.Mainframe = QtWidgets.QFrame(self)
        self.Mainframe.resize(self.size())

        self.label = QtWidgets.QLabel(self.Mainframe)
        self.label2 = QtWidgets.QLabel(self.Mainframe)
        self.label2.setText('')
        self.hlayout = QtWidgets.QHBoxLayout(self.Mainframe)
        self.hlayout.setContentsMargins(0, 0, 0, 0)
        self.hlayout.addWidget(self.label2)
        self.label2.setMaximumSize(QtCore.QSize(0,0))
        self.hlayout.addWidget(self.label)

        self.hoverbaranim = False

        self.label.setStyleSheet('color: #fff;border: None')        
        self.label2.setStyleSheet('color: #fff;border: None')
        self.Mainframe.setStyleSheet('border: 1px solid rgb(255, 32, 35)')
        self.frame.setStyleSheet('background-color: rgb(255, 32, 35)')
        self.framebar.setStyleSheet('background-color: rgba(255, 32, 35, 130)')

    def setIcon(self, Icon, *args, **kwargs):
        pass

    def setIconSize(self, *args):
        pass

    def setFlat(self, *args):
        pass

    def emitfinished(self):
        self.signals.finished.emit()
        
    def setText(self, text, *args, **kwargs):
        _translate = QtCore.QCoreApplication.translate
        self.label.setText(_translate("Form", "<html><head/><body><p align=\"center\">{0}</p></body></html>".format(text)))

    def enterEvent(self, *args, **kwargs):
        if not self.hoverbaranim:
            self.hoverbaranim = True
            timerinevent = QtCore.QTimer()
            timerinevent.setObjectName('timerinEnterevent')
            self.btanim('enterEvent')

    def mousePressEvent(self, *args):
        self.lsanim()

    def btanim(self, event):
        self.framebar.show()
        self.minanimation = QtCore.QPropertyAnimation(self.framebar, b"geometry")
        self.minanimation.setObjectName('minanimation')
        self.minanimation.setDuration(500)
        self.minanimation.setStartValue(QtCore.QRect(self.size().width(), 0, self.size().width(), 30))
        self.minanimation.setEndValue(QtCore.QRect(0, 0, self.size().width(), 30))
        self.minanimation.setEasingCurve(QtCore.QEasingCurve.OutCubic)
        self.minanimation.finished.connect(self.finishedanim_)
        self.minanimation.start()
        if event !='enterEvent':
            QtCore.QTimer.singleShot(310, self.lsanim)

    def finishedanim_(self):
        self.hoverbaranim = False
        
    def lsanim(self):
        self.frame.show()
        self.loadingsolidanim = QtCore.QPropertyAnimation(self.frame, b'geometry')
        self.loadingsolidanim.setObjectName('loadingbarsolidanim')
        self.loadingsolidanim.setDuration(400)
        self.loadingsolidanim.setStartValue(QtCore.QRect(self.size().width(), 0, self.size().width(), 30))
        self.loadingsolidanim.setEndValue(QtCore.QRect(0, 0, self.size().width(), 30))
        self.loadingsolidanim.setEasingCurve(QtCore.QEasingCurve.OutCubic)
        self.loadingsolidanim.finished.connect(self.finishedanim)
        self.loadingsolidanim.start()        
        
    def finishedanim(self):
        self.hoverbaranim = False
        self.framebar.hide()
        self.emitfinished()
       
    def leaveEvent(self, *args):
        if not self.frame.isHidden():
            self.frame.hide()
        if not self.framebar.isHidden():
            if not self.hoverbaranim:
                self.framebar.hide()


class testclicked(QtCore.QObject):
    def __init__(self, id):
        super().__init__()
        import os
        self.signals = Signals()
        selfid = id
        
    QtCore.pyqtSlot()
    def run(self):
        try:
            print('https://vbpsdelf.accevate.com/app121/student/google-form-test/?id='+self.id)
            subprocess.Popen('~/program_files/firefox/firefox --new-tab '+'https://vbpsdelf.accevate.com/app121/student/google-form-test/?id='+self.id)
        except Exception as e:
            self.signals.error.emit(e)
        finally:
            self.signals.finished.emit()

class Window(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.___horizontalLayout = QtWidgets.QHBoxLayout(self)
        self.___horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.___horizontalLayout.setSpacing(0)
        
        self.stackedWidget = QtWidgets.QStackedWidget(self)
        self.stackedWidget.setGeometry(QtCore.QRect(80, 40, 201, 141))
        self.stackedWidget.setStyleSheet("background:transparent;")
        
        self.customizeStacks()
        self.loadingbar   = QtWidgets.QFrame(self)
        self.loadingsolid = QtWidgets.QFrame(self)
        self.Mainframe    = QtWidgets.QFrame(self)
        self.Mainframe.hide()

        self.resize(900, 400)
        self.Mainframe.setGeometry(self.size().width(), self.size().height(), self.size().width(), self.size().height())
        self.loadingbar.setGeometry(0,0, self.size().width(), self.size().height())
        self.loadingsolid.setGeometry(self.size().width(), self.size().height(), self.size().width(), self.size().height())

        self.loadingsolid.setStyleSheet('background-color: rgb(255, 32, 35)')
        self.Mainframe.setStyleSheet('background-color: rgb(255, 255, 255)')
        self.loadingbar.setStyleSheet('background-color: rgba(255, 32, 35, 130);')#243, 31, 81, 130)

        self.vlayoutmain = QtWidgets.QVBoxLayout(self.loadingsolid)
        self.txtlabl     = QtWidgets.QLabel(self.loadingsolid)
        self.vlayoutmain.addWidget(self.txtlabl, 0, QtCore.Qt.AlignHCenter)
        self.txtlabl.setText("<html><head/><body><p align=\"center\"><span style= \"font-size:36pt; font-weight:600; color: rgba(255, 255, 255, 150);\">Clouster</span></body></html>")
        self.txtlabl.setStyleSheet('font: 57 9px \"Quicksand\"')
        self.txtlabl.setMaximumSize(QtCore.QSize(200, 200))
        self.txtlabl.setMinimumSize(QtCore.QSize(200, 200))
        
        self.initialize()

    def customizeStacks(self):
        self.setStyleSheet('background-color: qradialgradient(spread:pad, cx:0.515789, cy:0.0568182, radius:1.591, fx:0.510526, fy:0.063, stop:0 rgba(24, 21, 41, 255), stop:1 rgba(0, 0, 0, 255));')
        self.stackedWidget.setStyleSheet('background: transparent')

        self.test()

        self.pushButton_2.signals.finished.connect(self.pbConnect_2)
        self.pushButton.signals.finished.connect(self.pbConnect)
        self.classes.signals.finished.connect(self._classes)
        self.bckassig.signals.finished.connect(self.bck)
        self.bckcls.signals.finished.connect(self.bck)
        self.pushButton_6.signals.finished.connect(self._logout)
        self.pushButton_7.signals.finished.connect(self._logout)
        self.pushButton_5.signals.finished.connect(self._logout)
        #self.test.signals.finished.connect(self._testclicked)
        
        self.___horizontalLayout.addWidget(self.stackedWidget)

    def _testclicked(self):
        self.thread = QtCore.QThread()
        self.toExecute = testclicked(self.df.id)
        self.toExecute.moveToThread(self.thread)
        self.thread.started.connect(self.toExecute.run)
        self.toExecute.signals.error.connect(self.errorRaised)
        self.toExecute.signals.finished.connect(self.toExecute.deleteLater)
        self.toExecute.signals.finished.connect(self.thread.quit)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.run()

    def errorRaised(self, e):
        print(e)

    def _classes(self):
        self.toreach = 'classTab'
        self.animstart()

    def bck(self):
        self.toreach = "hometab"
        self.animstart()

    def _logout(self):
        self.toreach = '_login'
        self.animstart()

    def pbConnect_2(self):
        self.toreach = 'hometab'
        self.animstart()

    def pbConnect(self):
        self.toreach = 'assignment'
        self.animstart()

    
    def test(self):
        self.login = QtWidgets.QWidget()
        self.login.setStyleSheet("background: transparent")
        self.login.setObjectName("login")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.login)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame = QtWidgets.QFrame(self.login)
        self.frame.setStyleSheet("background: transparent")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.frame_2 = QtWidgets.QFrame(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_2.sizePolicy().hasHeightForWidth())
        self.frame_2.setSizePolicy(sizePolicy)
        self.frame_2.setStyleSheet("background : transparent;")
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.frame_2)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label = QtWidgets.QLabel(self.frame_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMinimumSize(QtCore.QSize(71, 30))
        self.label.setMaximumSize(QtCore.QSize(71, 30))
        self.label.setStyleSheet("font: 58 13pt \"Quicksand Medium\";")
        self.label.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.label.setFrameShadow(QtWidgets.QFrame.Plain)
        self.label.setLineWidth(0)
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.verticalLayout_3.addWidget(self.label)
        self.verticalLayout_2.addWidget(self.frame_2)
        spacerItem = QtWidgets.QSpacerItem(52, 32, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        self.verticalLayout_2.addItem(spacerItem)
        self.frame_3 = QtWidgets.QFrame(self.frame)
        self.frame_3.setStyleSheet("/*background:transparent;*/")
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame_3)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.frame_6 = QtWidgets.QFrame(self.frame_3)
        self.frame_6.setMinimumSize(QtCore.QSize(223, 100))
        self.frame_6.setMaximumSize(QtCore.QSize(578, 400))
        self.frame_6.setStyleSheet("background:transparent")
        self.frame_6.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_6.setObjectName("frame_6")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.frame_6)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.frame_7 = QtWidgets.QFrame(self.frame_6)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_7.sizePolicy().hasHeightForWidth())
        self.frame_7.setSizePolicy(sizePolicy)
        self.frame_7.setMinimumSize(QtCore.QSize(230, 0))
        self.frame_7.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_7.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_7.setObjectName("frame_7")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.frame_7)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_4 = QtWidgets.QLabel(self.frame_7)
        self.label_4.setMinimumSize(QtCore.QSize(247, 0))
        font = QtGui.QFont()
        font.setFamily("Cascadia Code PL")
        font.setPointSize(9)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(3)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("font: 25 9pt \"Cascadia Code PL\";")
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_3.addWidget(self.label_4)
        self.verticalLayout_5.addWidget(self.frame_7)
        spacerItem1 = QtWidgets.QSpacerItem(17, 32, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        self.verticalLayout_5.addItem(spacerItem1)
        self.frame_4 = QtWidgets.QFrame(self.frame_6)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_4.sizePolicy().hasHeightForWidth())
        self.frame_4.setSizePolicy(sizePolicy)
        self.frame_4.setStyleSheet("font: 9pt \"DejaVu Sans\";")
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.frame_4)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setHorizontalSpacing(9)
        self.gridLayout.setVerticalSpacing(34)
        self.gridLayout.setObjectName("gridLayout")
        self.label_2 = QtWidgets.QLabel(self.frame_4)
        self.label_2.setStyleSheet("")
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.frame_4)
        self.label_3.setStyleSheet("color: rgb(211, 211, 211);")
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)
        self.pushButton_2 = btn(self.frame_4)
        self.pushButton_2.setMinimumSize(QtCore.QSize(100, 30))
        self.pushButton_2.setMaximumSize(QtCore.QSize(100, 30))
        self.pushButton_2.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.pushButton_2.setStyleSheet("")
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout.addWidget(self.pushButton_2, 2, 0, 1, 2, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.lineEdit = QtWidgets.QLineEdit(self.frame_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit.sizePolicy().hasHeightForWidth())
        self.lineEdit.setSizePolicy(sizePolicy)
        self.lineEdit.setMinimumSize(QtCore.QSize(200, 0))
        self.lineEdit.setMaximumSize(QtCore.QSize(200, 16777215))
        self.lineEdit.setAutoFillBackground(False)
        self.lineEdit.setStyleSheet("border-bottom: 1px solid rgb(243, 31, 81);\n"
"color: rgb(211, 211, 211);\n"
"border-top: 2px solid transparent;\n"
"selection-color: rgb(255, 255, 127);\n"
"selection-background-color: rgb(85, 255, 127);\n")
        self.lineEdit.setInputMask("")
        self.lineEdit.setText("")
        self.lineEdit.setFrame(True)
        self.lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit.setCursorMoveStyle(QtCore.Qt.VisualMoveStyle)
        self.lineEdit.setClearButtonEnabled(True)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 0, 1, 1, 1)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.frame_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_2.sizePolicy().hasHeightForWidth())
        self.lineEdit_2.setSizePolicy(sizePolicy)
        self.lineEdit_2.setMinimumSize(QtCore.QSize(200, 0))
        self.lineEdit_2.setMaximumSize(QtCore.QSize(200, 16777215))
        self.lineEdit_2.setStyleSheet("border-bottom: 1px solid rgb(243, 31, 81);\n"
"color: rgb(211, 211, 211);\n"
"border-top: 2px solid transparent;\n")
        self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.PasswordEchoOnEdit)
        self.lineEdit_2.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_2.setCursorMoveStyle(QtCore.Qt.VisualMoveStyle)
        self.lineEdit_2.setClearButtonEnabled(True)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.gridLayout.addWidget(self.lineEdit_2, 1, 1, 1, 1)
        self.verticalLayout_4.addLayout(self.gridLayout)
        self.verticalLayout_5.addWidget(self.frame_4, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.horizontalLayout_2.addWidget(self.frame_6, 0, QtCore.Qt.AlignHCenter)
        self.verticalLayout_2.addWidget(self.frame_3, 0, QtCore.Qt.AlignHCenter)
        self.verticalLayout.addWidget(self.frame)
        self.stackedWidget.addWidget(self.login)
        self.home = QtWidgets.QWidget()
        self.home.setObjectName("home")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.home)
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.frame_5 = QtWidgets.QFrame(self.home)
        self.frame_5.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_5.setObjectName("frame_5")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.frame_5)
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_7.setSpacing(0)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.frame_17 = QtWidgets.QFrame(self.frame_5)
        self.frame_17.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_17.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_17.setObjectName("frame_17")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.frame_17)
        self.horizontalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_7.setSpacing(0)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.frame_8 = QtWidgets.QFrame(self.frame_17)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_8.sizePolicy().hasHeightForWidth())
        self.frame_8.setSizePolicy(sizePolicy)
        self.frame_8.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_8.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_8.setObjectName("frame_8")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.frame_8)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.label_5 = QtWidgets.QLabel(self.frame_8)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        self.label_5.setMinimumSize(QtCore.QSize(71, 30))
        self.label_5.setMaximumSize(QtCore.QSize(71, 30))
        self.label_5.setStyleSheet("font: 58 13pt \"Quicksand Medium\";")
        self.label_5.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.label_5.setFrameShadow(QtWidgets.QFrame.Plain)
        self.label_5.setLineWidth(0)
        self.label_5.setScaledContents(True)
        self.label_5.setObjectName("label_5")
        self.verticalLayout_8.addWidget(self.label_5)
        self.horizontalLayout_7.addWidget(self.frame_8)
        self.frame_21 = QtWidgets.QFrame(self.frame_17)
        self.frame_21.setMinimumSize(QtCore.QSize(100, 0))
        self.frame_21.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_21.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_21.setObjectName("frame_21")
        self.horizontalLayout_7.addWidget(self.frame_21)
        self.frame_19 = QtWidgets.QFrame(self.frame_17)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_19.sizePolicy().hasHeightForWidth())
        self.frame_19.setSizePolicy(sizePolicy)
        self.frame_19.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_19.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_19.setObjectName("frame_19")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout(self.frame_19)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.pushButton_5 = btn(self.frame_19)
        self.pushButton_5.setMinimumSize(QtCore.QSize(100, 30))
        self.pushButton_5.setStyleSheet("border : 1px solid rgb(255, 32, 35);\n"
"font: 57 10pt \"Quicksand Medium\";\n"
"color: rgb(255, 255, 255);")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(".icons/breeze/actions/16/document-decrypt.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_5.setIcon(icon)
        self.pushButton_5.setObjectName("pushButton_5")
        self.horizontalLayout_8.addWidget(self.pushButton_5)
        self.horizontalLayout_7.addWidget(self.frame_19)
        self.verticalLayout_7.addWidget(self.frame_17)
        self.frame_9 = QtWidgets.QFrame(self.frame_5)
        self.frame_9.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_9.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_9.setObjectName("frame_9")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.frame_9)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.frame_10 = QtWidgets.QFrame(self.frame_9)
        self.frame_10.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_10.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_10.setObjectName("frame_10")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout(self.frame_10)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.frame_14 = QtWidgets.QFrame(self.frame_10)
        self.frame_14.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_14.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_14.setObjectName("frame_14")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.frame_14)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.frame_12 = QtWidgets.QFrame(self.frame_14)
        self.frame_12.setMinimumSize(QtCore.QSize(150, 150))
        self.frame_12.setMaximumSize(QtCore.QSize(150, 150))
        self.frame_12.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_12.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_12.setObjectName("frame_12")
        self.horizontalLayout_15 = QtWidgets.QHBoxLayout(self.frame_12)
        self.horizontalLayout_15.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_15.setSpacing(0)
        self.horizontalLayout_15.setObjectName("horizontalLayout_15")
        self.label_11 = QtWidgets.QLabel(self.frame_12)
        self.label_11.setText("")
        
        self.label_11.setObjectName("label_11")
        self.horizontalLayout_15.addWidget(self.label_11)
        self.horizontalLayout_4.addWidget(self.frame_12)
        self.frame_15 = QtWidgets.QFrame(self.frame_14)
        self.frame_15.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_15.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_15.setObjectName("frame_15")
        self.verticalLayout_12 = QtWidgets.QVBoxLayout(self.frame_15)
        self.verticalLayout_12.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_12.setSpacing(0)
        self.verticalLayout_12.setObjectName("verticalLayout_12")
        self.label_6 = QtWidgets.QLabel(self.frame_15)
        self.label_6.setStyleSheet("font: 25 9pt \"Cascadia Code PL\";")
        self.label_6.setObjectName("label_6")
        self.verticalLayout_12.addWidget(self.label_6)
        self.horizontalLayout_4.addWidget(self.frame_15)
        self.verticalLayout_10.addWidget(self.frame_14)
        self.frame_13 = QtWidgets.QFrame(self.frame_10)
        self.frame_13.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_13.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_13.setObjectName("frame_13")
        self.verticalLayout_13 = QtWidgets.QHBoxLayout(self.frame_13)
        self.verticalLayout_13.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_13.setSpacing(10)
        self.verticalLayout_13.setObjectName("verticalLayout_13")
        self.pushButton = btn(self.frame_13)
        self.classes = btn(self.frame_13)
        self.test = btn(self.frame_13)
        self.pushButton.setObjectName("pushButton")
        
        self.pushButton.setMinimumSize(QtCore.QSize(100, 30))
        self.pushButton.setMaximumSize(QtCore.QSize(100, 30))

        self.classes.setMaximumSize(QtCore.QSize(100, 30))
        self.classes.setMinimumSize(QtCore.QSize(100, 30))

        self.test.setMaximumSize(QtCore.QSize(100, 30))
        self.test.setMinimumSize(QtCore.QSize(100, 30))
        
        self.verticalLayout_13.addWidget(self.pushButton)
        self.verticalLayout_13.addWidget(self.classes)
        self.verticalLayout_13.addWidget(self.test)

        self.verticalLayout_10.addWidget(self.frame_13, 0, QtCore.Qt.AlignHCenter)
        self.verticalLayout_9.addWidget(self.frame_10)
        self.frame_11 = QtWidgets.QFrame(self.frame_9)
        self.frame_11.setMinimumSize(QtCore.QSize(0, 100))
        self.frame_11.setMaximumSize(QtCore.QSize(16777215, 100))
        self.frame_11.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_11.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_11.setObjectName("frame_11")
        self.verticalLayout_11 = QtWidgets.QVBoxLayout(self.frame_11)
        self.verticalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_11.setSpacing(0)
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.textEdit = QtWidgets.QTextEdit(self.frame_11)
        self.textEdit.setStyleSheet("color: rgb(255, 255, 255);\n"
"border:1px solid rgb(85, 170, 127);\n"
"border-radius: 10px;")
        self.textEdit.setObjectName("textEdit")
        self.verticalLayout_11.addWidget(self.textEdit)
        self.verticalLayout_9.addWidget(self.frame_11)
        self.verticalLayout_7.addWidget(self.frame_9)
        self.verticalLayout_6.addWidget(self.frame_5)
        self.stackedWidget.addWidget(self.home)
        self.menupage = QtWidgets.QWidget()
        self.menupage.setObjectName("menupage")
        self.verticalLayout_14 = QtWidgets.QVBoxLayout(self.menupage)
        self.verticalLayout_14.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_14.setSpacing(0)
        self.verticalLayout_14.setObjectName("verticalLayout_14")
        self.frame_16 = QtWidgets.QFrame(self.menupage)
        self.frame_16.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_16.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_16.setObjectName("frame_16")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.frame_16)
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.nextprev = QtWidgets.QFrame(self.frame_16)
        self.nextprev.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0.5, y1:0, x2:0.5, y2:1, stop:0 rgba(0, 0, 0, 255), stop:1 rgba(29, 27, 29, 255));")
        self.nextprev.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.nextprev.setFrameShadow(QtWidgets.QFrame.Raised)
        self.nextprev.setObjectName("nextprev")
        self.verticalLayout_15 = QtWidgets.QVBoxLayout(self.nextprev)
        self.verticalLayout_15.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_15.setSpacing(0)
        self.verticalLayout_15.setObjectName("verticalLayout_15")
        self.frame_20 = QtWidgets.QFrame(self.nextprev)
        self.frame_20.setStyleSheet("background:transparent")
        self.frame_20.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_20.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_20.setObjectName("frame_20")
        self.verticalLayout_17 = QtWidgets.QVBoxLayout(self.frame_20)
        self.verticalLayout_17.setObjectName("verticalLayout_17")
        self.frame_18 = QtWidgets.QFrame(self.frame_20)
        self.frame_18.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_18.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_18.setObjectName("frame_18")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.frame_18)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.pushButton_3 = QtWidgets.QPushButton(self.frame_18)
        self.pushButton_3.setMinimumSize(QtCore.QSize(25, 25))
        self.pushButton_3.setMaximumSize(QtCore.QSize(25, 25))
        self.pushButton_3.setStyleSheet("border:1px solid rgb(255, 32, 35);\n"
"background: transparent;")
        self.pushButton_3.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(os.path.join(os.getcwd(), "icons/arrow-left.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_3.setIcon(icon1)
        self.pushButton_3.setIconSize(QtCore.QSize(16, 16))
        self.pushButton_3.setFlat(True)
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout_6.addWidget(self.pushButton_3)
        self.pushButton_4 = QtWidgets.QPushButton(self.frame_18)
        self.pushButton_4.setMinimumSize(QtCore.QSize(25, 25))
        self.pushButton_4.setMaximumSize(QtCore.QSize(25, 25))
        self.pushButton_4.setStyleSheet("border: 1px solid rgb(255, 32, 35);\n"
"background: transparent;")
        self.pushButton_4.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(os.path.join(os.getcwd(), "icons/arrow-right.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_4.setIcon(icon2)
        self.pushButton_4.setObjectName("pushButton_4")
        self.horizontalLayout_6.addWidget(self.pushButton_4)
        self.verticalLayout_17.addWidget(self.frame_18)
        self.verticalLayout_15.addWidget(self.frame_20, 0, QtCore.Qt.AlignVCenter)
        self.horizontalLayout_5.addWidget(self.nextprev)
        self.hometab = QtWidgets.QFrame(self.frame_16)
        self.hometab.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0.5, y1:0, x2:0.5, y2:1, stop:0 rgba(0, 0, 0, 255), stop:1 rgba(29, 27, 29, 255));")
        self.hometab.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.hometab.setFrameShadow(QtWidgets.QFrame.Raised)
        self.hometab.setObjectName("hometab")
        self.horizontalLayout_5.addWidget(self.hometab)
        self.onlineclasstab = QtWidgets.QFrame(self.frame_16)
        self.onlineclasstab.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0.5, y1:0, x2:0.5, y2:1, stop:0 rgba(0, 0, 0, 255), stop:1 rgba(29, 27, 29, 255));")
        self.onlineclasstab.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.onlineclasstab.setFrameShadow(QtWidgets.QFrame.Raised)
        self.onlineclasstab.setObjectName("onlineclasstab")
        self.horizontalLayout_5.addWidget(self.onlineclasstab)
        self.assignmenttab = QtWidgets.QFrame(self.frame_16)
        self.assignmenttab.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0.5, y1:0, x2:0.5, y2:1, stop:0 rgba(0, 0, 0, 255), stop:1 rgba(29, 27, 29, 255));")
        self.assignmenttab.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.assignmenttab.setFrameShadow(QtWidgets.QFrame.Raised)
        self.assignmenttab.setObjectName("assignmenttab")
        self.horizontalLayout_5.addWidget(self.assignmenttab)
        self.onlinetesttab = QtWidgets.QFrame(self.frame_16)
        self.onlinetesttab.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0.5, y1:0, x2:0.5, y2:1, stop:0 rgba(0, 0, 0, 255), stop:1 rgba(29, 27, 29, 255));")
        self.onlinetesttab.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.onlinetesttab.setFrameShadow(QtWidgets.QFrame.Raised)
        self.onlinetesttab.setObjectName("onlinetesttab")
        self.horizontalLayout_5.addWidget(self.onlinetesttab)
        self.verticalLayout_14.addWidget(self.frame_16)
        self.stackedWidget.addWidget(self.menupage)
        self.page = QtWidgets.QWidget()
        self.page.setObjectName("page")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout(self.page)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.frame_22 = QtWidgets.QFrame(self.page)
        self.frame_22.setStyleSheet("")
        self.frame_22.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_22.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_22.setObjectName("frame_22")
        self.verticalLayout_18 = QtWidgets.QVBoxLayout(self.frame_22)
        self.verticalLayout_18.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_18.setSpacing(0)
        self.verticalLayout_18.setObjectName("verticalLayout_18")
        self.frame_23 = QtWidgets.QFrame(self.frame_22)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_23.sizePolicy().hasHeightForWidth())
        self.frame_23.setSizePolicy(sizePolicy)
        self.frame_23.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_23.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_23.setObjectName("frame_23")
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout(self.frame_23)
        self.horizontalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_10.setSpacing(0)
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.frame_25 = QtWidgets.QFrame(self.frame_23)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_25.sizePolicy().hasHeightForWidth())
        self.frame_25.setSizePolicy(sizePolicy)
        self.frame_25.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_25.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_25.setObjectName("frame_25")
        self.verticalLayout_16 = QtWidgets.QVBoxLayout(self.frame_25)
        self.verticalLayout_16.setObjectName("verticalLayout_16")
        self.label_7 = QtWidgets.QLabel(self.frame_25)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy)
        self.label_7.setMinimumSize(QtCore.QSize(71, 30))
        self.label_7.setMaximumSize(QtCore.QSize(71, 30))
        self.label_7.setStyleSheet("font: 58 13pt \"Quicksand Medium\";")
        self.label_7.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.label_7.setFrameShadow(QtWidgets.QFrame.Plain)
        self.label_7.setLineWidth(0)
        self.label_7.setScaledContents(True)
        self.label_7.setObjectName("label_7")
        self.verticalLayout_16.addWidget(self.label_7)
        self.horizontalLayout_10.addWidget(self.frame_25)
        self.frame_26 = QtWidgets.QFrame(self.frame_23)
        self.frame_26.setMinimumSize(QtCore.QSize(100, 0))
        self.frame_26.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_26.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_26.setObjectName("frame_26")
        self.horizontalLayout_10.addWidget(self.frame_26)
        self.frame_27 = QtWidgets.QFrame(self.frame_23)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_27.sizePolicy().hasHeightForWidth())
        self.frame_27.setSizePolicy(sizePolicy)
        self.frame_27.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_27.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_27.setObjectName("frame_27")
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout(self.frame_27)
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.pushButton_6 = btn(self.frame_27)
        self.pushButton_6.setMinimumSize(QtCore.QSize(100, 30))
        self.pushButton_6.setMaximumSize(QtCore.QSize(100, 30))
        self.pushButton_6.setStyleSheet("border : 1px solid rgb(255, 32, 35);\n"
"font: 57 10pt \"Quicksand Medium\";\n"
"color: rgb(255, 255, 255);")
        self.pushButton_6.setIcon(icon)
        self.pushButton_6.setObjectName("pushButton_6")
        self.horizontalLayout_11.addWidget(self.pushButton_6)
        self.horizontalLayout_10.addWidget(self.frame_27)
        self.verticalLayout_18.addWidget(self.frame_23)
        self.frame_24 = QtWidgets.QFrame(self.frame_22)
        self.frame_24.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_24.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_24.setObjectName("frame_24")
        self.verticalLayout_19 = QtWidgets.QVBoxLayout(self.frame_24)
        self.verticalLayout_19.setObjectName("verticalLayout_19")
        self.label_8 = QtWidgets.QLabel(self.frame_24)
        font = QtGui.QFont()
        font.setFamily("Cascadia Code PL")
        font.setPointSize(9)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(3)
        self.label_8.setFont(font)
        self.label_8.setStyleSheet("font: 25 9pt \"Cascadia Code PL\";\n"
"color: rgb(221, 51, 74);")
        self.label_8.setObjectName("label_8")
        self.verticalLayout_19.addWidget(self.label_8)
        self.bckassig = btn(self.frame_24)

        self.bckassig.setMaximumSize(QtCore.QSize(100, 30))
        self.bckassig.setMinimumSize(QtCore.QSize(100, 30))

        
        self.frame_29 = QtWidgets.QFrame(self.frame_24)
        self.frame_29.setStyleSheet("")
        self.frame_29.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_29.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_29.setObjectName("frame_29")
        self.verticalLayout_21 = QtWidgets.QVBoxLayout(self.frame_29)
        self.verticalLayout_21.setObjectName("verticalLayout_21")
        self.scrollArea_6 = QtWidgets.QScrollArea(self.frame_29)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollArea_6.sizePolicy().hasHeightForWidth())
        self.scrollArea_6.setSizePolicy(sizePolicy)
        self.scrollArea_6.setMinimumSize(QtCore.QSize(400, 266))
        self.scrollArea_6.setStyleSheet("")
        self.scrollArea_6.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scrollArea_6.setFrameShadow(QtWidgets.QFrame.Plain)
        self.scrollArea_6.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.scrollArea_6.setWidgetResizable(True)
        self.scrollArea_6.setAlignment(QtCore.Qt.AlignCenter)
        self.scrollArea_6.setObjectName("scrollArea_6")
        self.scrollAreaWidgetContents_6 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_6.setGeometry(QtCore.QRect(0, 0, 695, 266))
        self.scrollAreaWidgetContents_6.setObjectName("scrollAreaWidgetContents_6")
        self.verticalLayout_20 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents_6)
        self.verticalLayout_20.setObjectName("verticalLayout_20")
        self.tableView = QtWidgets.QTableView(self.scrollAreaWidgetContents_6)
        self.tableView.setStyleSheet("QTableView {\n"
"    color: rgb(222, 222, 222);    \n"
"    background: rgba(0,0,0,0);\n"
"    padding: 10px;\n"
"    border-radius: 5px;\n"
"    gridline-color: rgb(44, 49, 60);\n"
"    border-bottom: 1px solid rgb(44, 49, 60);\n"
"}\n"
"QTableView::item{\n"
"    border-color: rgb(44, 49, 60);\n"
"    padding-left: 5px;\n"
"    padding-right: 5px;\n"
"    gridline-color: rgb(44, 49, 60);\n"
"}\n"
"QTableView::item:selected{\n"
"    background-color: rgb(85, 170, 255);\n"
"}\n"
"QScrollBar:horizontal {\n"
"    border: none;\n"
"    background: rgb(52, 59, 72);\n"
"    height: 14px;\n"
"    margin: 0px 21px 0 21px;\n"
"    border-radius: 0px;\n"
"}\n"
" QScrollBar:vertical {\n"
"    border: none;\n"
"    background: rgb(52, 59, 72);\n"
"    width: 14px;\n"
"    margin: 21px 0 21px 0;\n"
"    border-radius: 0px;\n"
" }\n"
"QHeaderView::section{\n"
"    color: rgb(222, 222, 222);\n"
"    Background-color: rgb(39, 44, 54);\n"
"    max-width: 30px;\n"
"    border: 1px solid rgb(44, 49, 60);\n"
"    border-style: none;\n"
"    border-bottom: 1px solid rgb(44, 49, 60);\n"
"    border-right: 1px solid rgb(44, 49, 60);\n"
"}\n"
"QTableView::horizontalHeader {\n"
"    color: rgb(222, 222, 222);    \n"
"    background-color: rgb(81, 255, 0);\n"
"}\n"
"QHeaderView::section:horizontal\n"
"{\n"
"    color: rgb(222, 222, 222);\n"
"    border: 1px solid rgb(32, 34, 42);\n"
"    background-color: rgb(27, 29, 35);\n"
"    padding: 3px;\n"
"    border-top-left-radius: 7px;\n"
"    border-top-right-radius: 7px;\n"
"}\n"
"QHeaderView::section:vertical\n"
"{\n"
"    color: rgb(222, 222, 222);\n"
"    border: 1px solid rgb(44, 49, 60);\n"
"}\n"
"")
        self.tableView.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.tableView.setFrameShadow(QtWidgets.QFrame.Plain)
        self.tableView.setLineWidth(0)
        self.tableView.setEditTriggers(QtWidgets.QAbstractItemView.AnyKeyPressed|QtWidgets.QAbstractItemView.DoubleClicked|QtWidgets.QAbstractItemView.EditKeyPressed|QtWidgets.QAbstractItemView.SelectedClicked)
        self.tableView.setObjectName("tableView")
        self.tableView.verticalHeader().setVisible(False)
        self.verticalLayout_20.addWidget(self.tableView)
        self.scrollArea_6.setWidget(self.scrollAreaWidgetContents_6)
        self.verticalLayout_21.addWidget(self.scrollArea_6)
        self.verticalLayout_19.addWidget(self.frame_29)

        self.verticalLayout_19.addWidget(self.bckassig, 0, QtCore.Qt.AlignHCenter)
        
        self.verticalLayout_18.addWidget(self.frame_24)
        self.horizontalLayout_9.addWidget(self.frame_22)
        self.stackedWidget.addWidget(self.page)
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setObjectName("page_2")
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout(self.page_2)
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        self.frame_28 = QtWidgets.QFrame(self.page_2)
        self.frame_28.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_28.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_28.setObjectName("frame_28")
        self.verticalLayout_23 = QtWidgets.QVBoxLayout(self.frame_28)
        self.verticalLayout_23.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_23.setSpacing(0)
        self.verticalLayout_23.setObjectName("verticalLayout_23")
        self.frame_32 = QtWidgets.QFrame(self.frame_28)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_32.sizePolicy().hasHeightForWidth())
        self.frame_32.setSizePolicy(sizePolicy)
        self.frame_32.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_32.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_32.setObjectName("frame_32")
        self.horizontalLayout_13 = QtWidgets.QHBoxLayout(self.frame_32)
        self.horizontalLayout_13.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_13.setSpacing(0)
        self.horizontalLayout_13.setObjectName("horizontalLayout_13")
        self.frame_33 = QtWidgets.QFrame(self.frame_32)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_33.sizePolicy().hasHeightForWidth())
        self.frame_33.setSizePolicy(sizePolicy)
        self.frame_33.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_33.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_33.setObjectName("frame_33")
        self.verticalLayout_22 = QtWidgets.QVBoxLayout(self.frame_33)
        self.verticalLayout_22.setObjectName("verticalLayout_22")
        self.label_9 = QtWidgets.QLabel(self.frame_33)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_9.sizePolicy().hasHeightForWidth())
        self.label_9.setSizePolicy(sizePolicy)
        self.label_9.setMinimumSize(QtCore.QSize(71, 30))
        self.label_9.setMaximumSize(QtCore.QSize(71, 30))
        self.label_9.setStyleSheet("font: 58 13pt \"Quicksand Medium\";")
        self.label_9.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.label_9.setFrameShadow(QtWidgets.QFrame.Plain)
        self.label_9.setLineWidth(0)
        self.label_9.setScaledContents(True)
        self.label_9.setObjectName("label_9")
        self.verticalLayout_22.addWidget(self.label_9)
        self.horizontalLayout_13.addWidget(self.frame_33)
        self.frame_34 = QtWidgets.QFrame(self.frame_32)
        self.frame_34.setMinimumSize(QtCore.QSize(100, 0))
        self.frame_34.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_34.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_34.setObjectName("frame_34")
        self.horizontalLayout_13.addWidget(self.frame_34)
        self.frame_35 = QtWidgets.QFrame(self.frame_32)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_35.sizePolicy().hasHeightForWidth())
        self.frame_35.setSizePolicy(sizePolicy)
        self.frame_35.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_35.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_35.setObjectName("frame_35")
        self.horizontalLayout_14 = QtWidgets.QHBoxLayout(self.frame_35)
        self.horizontalLayout_14.setObjectName("horizontalLayout_14")
        self.pushButton_7 = btn(self.frame_35)
        self.pushButton_7.setMinimumSize(QtCore.QSize(100, 30))
        self.pushButton_7.setMaximumSize(QtCore.QSize(100, 30))
        self.pushButton_7.setStyleSheet("border : 1px solid rgb(255, 32, 35);\n"
"font: 57 10pt \"Quicksand Medium\";\n"
"color: rgb(255, 255, 255);")
        self.pushButton_7.setIcon(icon)
        self.pushButton_7.setObjectName("pushButton_7")
        self.horizontalLayout_14.addWidget(self.pushButton_7)
        self.horizontalLayout_13.addWidget(self.frame_35)
        self.verticalLayout_23.addWidget(self.frame_32)
        self.frame_31 = QtWidgets.QFrame(self.frame_28)
        self.frame_31.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_31.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_31.setObjectName("frame_31")
        self.verticalLayout_24 = QtWidgets.QVBoxLayout(self.frame_31)
        self.verticalLayout_24.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_24.setSpacing(6)
        self.verticalLayout_24.setObjectName("verticalLayout_24")
        self.label_10 = QtWidgets.QLabel(self.frame_31)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_10.sizePolicy().hasHeightForWidth())
        self.label_10.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Cascadia Code PL")
        font.setPointSize(9)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(3)
        self.label_10.setFont(font)
        self.label_10.setStyleSheet("font: 25 9pt \"Cascadia Code PL\";\n"
"color: rgb(221, 51, 74);")
        self.label_10.setObjectName("label_10")
        self.verticalLayout_24.addWidget(self.label_10)

        self.bckcls = btn(self)
        self.bckcls.setMinimumSize(QtCore.QSize(100, 30))
        self.bckcls.setMaximumSize(QtCore.QSize(100, 30))
        
        self.frame_30 = QtWidgets.QFrame(self.frame_31)
        self.frame_30.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_30.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_30.setObjectName("frame_30")
        self.verticalLayout_26 = QtWidgets.QVBoxLayout(self.frame_30)
        self.verticalLayout_26.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_26.setSpacing(0)
        self.verticalLayout_26.setObjectName("verticalLayout_26")
        self.scrollArea_5 = QtWidgets.QScrollArea(self.frame_30)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollArea_5.sizePolicy().hasHeightForWidth())
        self.scrollArea_5.setSizePolicy(sizePolicy)
        self.scrollArea_5.setMinimumSize(QtCore.QSize(400, 266))
        self.scrollArea_5.setStyleSheet("QScrollBar:horizontal {\n"
"    border: none;\n"
"    background: rgb(52, 59, 72);\n"
"    height: 14px;\n"
"    margin: 0px 21px 0 21px;\n"
"    border-radius: 0px;\n"
"}\n"
" QScrollBar:vertical {\n"
"    border: none;\n"
"    background: rgb(52, 59, 72);\n"
"    width: 14px;\n"
"    margin: 21px 0 21px 0;\n"
"    border-radius: 0px;\n"
" }")
        self.scrollArea_5.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.scrollArea_5.setWidgetResizable(True)
        self.scrollArea_5.setAlignment(QtCore.Qt.AlignCenter)
        self.scrollArea_5.setObjectName("scrollArea_5")
        self.scrollAreaWidgetContents_5 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_5.setGeometry(QtCore.QRect(0, 0, 729, 264))
        self.scrollAreaWidgetContents_5.setObjectName("scrollAreaWidgetContents_5")
        self.verticalLayout_25 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents_5)
        self.verticalLayout_25.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_25.setSpacing(0)
        self.verticalLayout_25.setObjectName("verticalLayout_25")
        self.View = QtWidgets.QTableView(self.scrollAreaWidgetContents_5)
        '''self.View.setStyleSheet("QTableView {\n"
"    color: rgb(222, 222, 222);    \n"
"    background: rgba(0,0,0,0);\n"
"    padding: 10px;\n"
"    border-radius: 5px;\n"
"    gridline-color: rgb(44, 49, 60);\n"
"    border-bottom: 1px solid rgb(44, 49, 60);\n"
"}\n"
"QTableView::item{\n"
"    border-color: rgb(44, 49, 60);\n"
"    padding-left: 5px;\n"
"    padding-right: 5px;\n"
"    gridline-color: rgb(44, 49, 60);\n"
"}\n"
"QTableView::item:selected{\n"
"    background-color: rgb(85, 170, 255);\n"
"}\n"
"QScrollBar:horizontal {\n"
"    border: none;\n"
"    background: rgb(52, 59, 72);\n"
"    height: 14px;\n"
"    margin: 0px 21px 0 21px;\n"
"    border-radius: 0px;\n"
"}\n"
" QScrollBar:vertical {\n"
"    border: none;\n"
"    background: rgb(52, 59, 72);\n"
"    width: 14px;\n"
"    margin: 21px 0 21px 0;\n"
"    border-radius: 0px;\n"
" }\n"
"QHeaderView::section{\n"
"    color: rgb(222, 222, 222);\n"
"    Background-color: rgb(39, 44, 54);\n"
"    max-width: 30px;\n"
"    border: 1px solid rgb(44, 49, 60);\n"
"    border-style: none;\n"
"    border-bottom: 1px solid rgb(44, 49, 60);\n"
"    border-right: 1px solid rgb(44, 49, 60);\n"
"}\n"
"QTableView::horizontalHeader {\n"
"    color: rgb(222, 222, 222);    \n"
"    background-color: rgb(81, 255, 0);\n"
"}\n"
"QHeaderView::section:horizontal\n"
"{\n"
"    color: rgb(222, 222, 222);\n"
"    border: 1px solid rgb(32, 34, 42);\n"
"    background-color: rgb(27, 29, 35);\n"
"    padding: 3px;\n"
"    border-top-left-radius: 7px;\n"
"    border-top-right-radius: 7px;\n"
"}\n"
"QHeaderView::section:vertical\n"
"{\n"
"    color: rgb(222, 222, 222);\n"
"    border: 1px solid rgb(44, 49, 60);\n"
"}\n"
"")'''
        self.View.setObjectName("View")
        self.verticalLayout_25.addWidget(self.View)
        self.scrollArea_5.setWidget(self.scrollAreaWidgetContents_5)
        self.verticalLayout_26.addWidget(self.scrollArea_5)
        self.verticalLayout_24.addWidget(self.frame_30)
        self.verticalLayout_24.addWidget(self.bckcls, 0, QtCore.Qt.AlignHCenter)
        self.verticalLayout_23.addWidget(self.frame_31)
        self.horizontalLayout_12.addWidget(self.frame_28)
        self.stackedWidget.addWidget(self.page_2)

        _translate = QtCore.QCoreApplication.translate

        self.label.setText(_translate("Form", "<html><head/><body><p><span style=\" color:#ffffff;\">Clouster</span></p></body></html>"))
        self.label_4.setText(_translate("Form", "<html><head/><body><p align=\"center\"><span style=\" font-size:26pt; color:#ffffff;\">Vishwa Bharti Public School</span></p><p align=\"center\"><span style=\" font-size:26pt; color:#ffffff;\">Dwarka</span></p></body></html>"))
        self.label_2.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:10pt; color:#d3d3d3;\">Username ::</span></p></body></html>"))
        self.label_3.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:10pt;\">Password   ::</span></p></body></html>"))
        self.pushButton_2.setText(_translate("Form", "Sign In"))
        self.label_5.setText(_translate("Form", "<html><head/><body><p><span style=\" color:#ffffff;\">Clouster</span></p></body></html>"))
        self.pushButton_5.setText(_translate("Form", "Log Out"))
        self.bckcls.setText(_translate("Form", "Home"))

        self.pushButton.setText(_translate("Form", "Assignments"))
        self.test.setText(_translate("Form", "Test"))
        self.classes.setText(_translate("Form", "Classes"))
        self.bckassig.setText(_translate("Form", "Home"))
        self.label_7.setText(_translate("Form", "<html><head/><body><p><span style=\" color:#ffffff;\">Clouster</span></p></body></html>"))
        self.pushButton_6.setText(_translate("Form", "Log Out"))
        self.label_8.setText(_translate("Form", "<html><head/><body><p align=\"center\"><span style=\" font-size:22pt;\">My Assignments</span></p></body></html>"))
        self.label_9.setText(_translate("Form", "<html><head/><body><p><span style=\" color:#ffffff;\">Clouster</span></p></body></html>"))
        self.pushButton_7.setText(_translate("Form", "Log Out"))
        self.label_10.setText(_translate("Form", "<html><head/><body><p align=\"center\"><span style=\" font-size:22pt;\">My Classes</span></p></body></html>"))

    def animstart(self):
        QtCore.QTimer.singleShot(100, self.btanim)

    def initialize(self):
        self.__login = False
        self.loading = False
        self.loadingbar.hide()
        self.loadingsolid.hide()
        self.threadpool  = QtCore.QThreadPool()
        self.stackedWidget.setCurrentIndex(0)
        ptrtn = self.autoLogin()
        if ptrtn:
            self.afterLoginResults(ptrtn[0], username=ptrtn[1], password=ptrtn[2])
            self.stackedWidget.setCurrentIndex(1)
        else:
            self.afterLoginError(autoLoginconn=True)

    def btanim(self):
        self.loadingbar.show()
        self.minanimation = QtCore.QPropertyAnimation(self.loadingbar, b"geometry")
        self.minanimation.setObjectName('minanimation')
        self.minanimation.setDuration(500)
        self.minanimation.setStartValue(QtCore.QRect(0, self.size().height(), self.size().width(), self.size().height()))
        self.minanimation.setEndValue(QtCore.QRect(0, 0, self.size().width(), self.size().height()))
        self.minanimation.setEasingCurve(QtCore.QEasingCurve.OutCubic)
        self.minanimation.start()
        QtCore.QTimer.singleShot(310, self.lsanim)
        
    def lsanim(self):
        self.loadingsolid.show()
        self.loadingsolidanim = QtCore.QPropertyAnimation(self.loadingsolid, b'geometry')
        self.loadingsolidanim.setObjectName('loadingbarsolidanim')
        self.loadingsolidanim.setDuration(400)
        self.loadingsolidanim.setStartValue(QtCore.QRect(0, self.size().height(), self.size().width(), self.size().height()))
        self.loadingsolidanim.setEndValue(QtCore.QRect(0, 0, self.size().width(), self.size().height()))
        self.loadingsolidanim.setEasingCurve(QtCore.QEasingCurve.OutCubic)
        self.loadingsolidanim.finished.connect(self._rmanim)
        #self.loadingsolidanim.valueChanged.connect(self.printm)
        self.loadingsolidanim.start()

    def autoLogin(self):

        if os.path.exists(os.path.join(os.getcwd(), 'database.db')) :
        
            conn = sqlite3.Connection('database.db')
            self.df   = pd.read_sql('select * from userData', conn)
            conn.close()
            if self.df.shape[0] == 2 :
                if 1 in self.df.primaryID.to_dict():
                    username, pasword = self.df.username[1], self.df.password[1]
                    print(username, pasword)
                    try:
                        result = self.API(usrname=username,passwrd=pasword)
                    except Exception as e:
                        print(e)
                        return False
                    else:
                        print('auto login tured var login True and toreach hometab')
                        self.__login = True
                        self.toreach = "hometab"
                        return result, username, pasword

    def submitForm(self):
        if self.lineEdit.text():
            if self.lineEdit_2.text():
                if os.path.exists(os.path.join(os.getcwd(), 'database.db')):                                  
                    self.afterLogin()
                else:
                    conn = sqlite3.Connection('database.db')
                    df = pd.DataFrame(columns = ['primaryID','username', 'password', 'id', 'name', 'Class', 'dob', 'doa', 'permaadd', 'corradd', 'cat', 'religion', 'fname', 'mname', 'mob', 'cast', 'nationality'])
                    df = df.append({'primaryID':'0', 'username':'root', 'password':'toor', 'id':'2757', 'name':'Abhiraj Ranjan', 'Class':'XII-A', 'dob':'23 June, 2004', 'doa':'28 Feb 2012', 'permaadd':'...', 'corradd':'...', 'cat':"Humanity", 'religion':'Humanity', 'fname':'...', 'mname':'...', 'mob':'100', 'cast':'Humanity', 'nationality':'INDIAN'}, ignore_index = True)
                    df.to_sql('userData', conn)
                    conn.commit()
                    conn.close()
                    self.afterLogin()

    def API(self, usrname='',passwrd=''):
        APIcall = call(username=usrname, password=passwrd)
        return APIcall

    def afterLogin(self):    
        worker = Worker(self.API,usrname=self.lineEdit.text(),passwrd=self.lineEdit_2.text())
        worker.signals.result.connect(self.afterLoginResults)
        worker.signals.error.connect(self.afterLoginError)

        self.threadpool.start(worker)

    def afterLoginError(self, autoLoginconn=False):
        if autoLoginconn:
            print("error goin' online, loading from database stored")
        conn = sqlite3.Connection('database.db')
        df   = pd.read_sql('select * from userData', conn)
        self.df = df
        conn.close()
        
        if 1 in df.primaryID.to_dict():
            if autoLoginconn:
                self.testnoticetableWidget()
                self.testassigtableWidget()

                print(os.path.join(os.getcwd(), 'icons/user.jpeg'))
                
                #self.ui.stackedWidget.setCurrentWidget(self.ui.userTab)
                self.label_11.setPixmap(QtGui.QPixmap(os.path.join(os.getcwd(), 'icons/user.jpeg')))
                self.label_11.setScaledContents(True)
                self.stackedWidget.setCurrentIndex(1)
                self.label_6.setText("<html><head/><body><p align=\"center\"><span style=\" font-size:26pt; color:#ffffff;\">Welcome, {0}</span></p></body></html>".format(self.df.name[1]))


            elif self.lineEdit.text() == df.username[1] :
                if self.lineEdit_2.text() == df.password[1]:
                    self.testnoticetableWidget()
                    self.testassigtableWidget()
                    #self.dbinfeditor()

                    #self.ui.stackedWidget.setCurrentWidget(self.ui.userTab)
                    self.label_11.setPixmap(QPixmap(os.path.abspath('icons/user.jpeg')))
                    self.stackedWidget.setCurrentIndex(1)
                    ...
                else:
                    print('incorrect set of username and password')
                    if not autoLoginconn :
                        ...
                        
            else:
                print('incorrect set of username and password')
                if not autoLoginconn :
                    ...
        else:
            print('incorrect set of password and username')
            self.lineEdit.setText('')
            self.lineEdit_2.setText('')

    def afterLoginResults(self, api, username=False, password=False):
        self.APIcall = api
        print(api)
        id = self.APIcall.id

        a            = self.APIcall.Assig
        df3          = pd.DataFrame(columns=['subject', 'topic', 'date', 'link'])
        for i in a:
            subject  = i[0] if i[0] else None
            topic    = i[1] if i[1] else None
            date     = i[2] if i[2] else None
            link     = i[3] if i[3] else None
            df3      = df3.append({'subject':subject, 'topic':topic, 'date':date,'link':link}, ignore_index=True)


        data         = self.APIcall.personalData
        zoomlinks    = self.APIcall.zoomlinks

        conn         = sqlite3.Connection('database.db')
        df           = pd.DataFrame(columns = ['primaryID','username', 'password', 'id', 'name', 'Class', 'dob', 'doa', 'permaadd', 'corradd', 'cat', 'religion', 'fname', 'mname', 'mob', 'cast', 'nationality'])
        df           = df.append({'primaryID':'0', 'username':'root', 'password':'toor', 'id':'2757', 'name':'Abhiraj Ranjan', 'Class':'XII-A', 'dob':'23 June, 2004', 'doa':'28 Feb, 2012', 'permaadd':'...', 'corradd':'...', 'cat':"Humanity", 'religion':'Humanity', 'fname':'...', 'mname':'...', 'mob':'100', 'cast':'Humanity', 'nationality':'INDIAN'}, ignore_index = True)
        
        
        if username:
            df       = df.append({'primaryID':'1', 'username':username, 'password':password, 'id':id, 'name':data['name'], 'Class':data['class'], 'dob':data['Date Of Birth'], 'doa':data['Date Of Admission'], 'permaadd':data['Permanent Address'], 'corradd':data["Correspondance Address"], 'cat':data["Category"], 'religion':data["Religion"], 'fname':data["Father's Name"], 'mname':data["Mother's Name"], 'mob':data['Mobile NO.'], 'cast':data["Cast"], 'nationality':data["Nationality"]}, ignore_index = True)
        else:
            df       = df.append({'primaryID':'1', 'username':self.lineEdit.text(), 'password':self.lineEdit_2.text(), 'id':id, 'name':data['name'], 'Class':data['class'], 'dob':data['Date Of Birth'], 'doa':data['Date Of Admission'], 'permaadd':data['Permanent Address'], 'corradd':data["Correspondance Address"], 'cat':data["Category"], 'religion':data["Religion"], 'fname':data["Father's Name"], 'mname':data["Mother's Name"], 'mob':data['Mobile NO.'], 'cast':data["Cast"], 'nationality':data["Nationality"]}, ignore_index = True)
        
        try:
            conn.execute('drop table userData')
            conn.execute('drop table zoomData')
            conn.execute('drop table assigData')
        except:
            pass

        conn.commit()
        df.to_sql('userData', conn)
        zoomlinks.to_sql('zoomData', conn)
        df3.to_sql('assigData', conn)
        conn.commit()
        conn.close()
        
        self.noticetableWidget()
        self.assigtableWidget()
        self.label_11.setPixmap(QtGui.QPixmap(os.path.join(os.getcwd(), 'icons/user.jpeg')))
        self.label_11.setScaledContents(True)
        self.__login = True
        self._rmanim()
        
    def noticetableWidget(self):
        a = self.APIcall.zoomlinks
        model = pandasModel(a)
    
        self.View.setModel(model)
        self.View.setStyleSheet("QTableView {\n"
"    color: rgb(222, 222, 222);    \n"
"    background: rgba(0,0,0,0);\n"
"    padding: 10px;\n"
"    border-radius: 5px;\n"
"    gridline-color: rgb(44, 49, 60);\n"
"    border-bottom: 1px solid rgb(44, 49, 60);\n"
"}\n"
"QTableView::item{\n"
"    border-color: rgb(44, 49, 60);\n"
"    padding-left: 5px;\n"
"    padding-right: 5px;\n"
"    gridline-color: rgb(44, 49, 60);\n"
"}\n"
"QTableView::item:selected{\n"
"    background-color: rgb(85, 170, 255);\n"
"}\n"
"QScrollBar:horizontal {\n"
"    border: none;\n"
"    background: rgb(52, 59, 72);\n"
"    height: 14px;\n"
"    margin: 0px 21px 0 21px;\n"
"    border-radius: 0px;\n"
"}\n"
" QScrollBar:vertical {\n"
"    border: none;\n"
"    background: rgb(52, 59, 72);\n"
"    width: 14px;\n"
"    margin: 21px 0 21px 0;\n"
"    border-radius: 0px;\n"
" }\n"
"QHeaderView::section{\n"
"    color: rgb(222, 222, 222);\n"
"    Background-color: rgb(39, 44, 54);\n"
"    max-width: 30px;\n"
"    border: 1px solid rgb(44, 49, 60);\n"
"    border-style: none;\n"
"    border-bottom: 1px solid rgb(44, 49, 60);\n"
"    border-right: 1px solid rgb(44, 49, 60);\n"
"}\n"
"QTableView::horizontalHeader {\n"
"    color: rgb(222, 222, 222);    \n"
"    background-color: rgb(81, 255, 0);\n"
"}\n"
"QHeaderView::section:horizontal\n"
"{\n"
"    color: rgb(222, 222, 222);\n"
"    border: 1px solid rgb(32, 34, 42);\n"
"    background-color: rgb(27, 29, 35);\n"
"    padding: 3px;\n"
"    border-top-left-radius: 7px;\n"
"    border-top-right-radius: 7px;\n"
"}\n"
"QHeaderView::section:vertical\n"
"{\n"
"    color: rgb(222, 222, 222);\n"
"    border: 1px solid rgb(44, 49, 60);\n"
"}\n"
"")
        self.scrollArea_5.setStyleSheet('')
        self.View.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.View.customContextMenuRequested.connect(self.ViewRightClick)
        
        self.View.resizeColumnsToContents()
        

    def ViewRightClick(self, point):
        index = self.View.indexAt(point)
        if index.column() == 2:
            subprocess.Popen(['/home/abhiraj/program_files/firefox/firefox', index.sibling(index.row(), index.column()).data()])
     

    def assigtableWidget(self):
        a = self.APIcall.Assig
        a = np.array(a)
        table = {}
        
        headers = ['subject', 'title','date', 'link']
        for ind, i in enumerate(a.T):
                table[headers[ind]] = i
        table = pd.DataFrame(table)

        table['join'] = ['' for i in range(table.shape[0])]

        model = pandasModel(pd.DataFrame(a))
        self.tableView.setModel(model)
        self.tableView.setStyleSheet("QTableView {\n"
"    color: rgb(222, 222, 222);    \n"
"    background: rgba(0,0,0,0);\n"
"    padding: 10px;\n"
"    border-radius: 5px;\n"
"    gridline-color: rgb(44, 49, 60);\n"
"    border-bottom: 1px solid rgb(44, 49, 60);\n"
"}\n"
"QTableView::item{\n"
"    border-color: rgb(44, 49, 60);\n"
"    padding-left: 5px;\n"
"    padding-right: 5px;\n"
"    gridline-color: rgb(44, 49, 60);\n"
"}\n"
"QTableView::item:selected{\n"
"    background-color: rgb(85, 170, 255);\n"
"}\n"
"QScrollBar:horizontal {\n"
"    border: none;\n"
"    background: rgb(52, 59, 72);\n"
"    height: 14px;\n"
"    margin: 0px 21px 0 21px;\n"
"    border-radius: 0px;\n"
"}\n"
" QScrollBar:vertical {\n"
"    border: none;\n"
"    background: rgb(52, 59, 72);\n"
"    width: 14px;\n"
"    margin: 21px 0 21px 0;\n"
"    border-radius: 0px;\n"
" }\n"
"QHeaderView::section{\n"
"    color: rgb(222, 222, 222);\n"
"    Background-color: rgb(39, 44, 54);\n"
"    max-width: 30px;\n"
"    border: 1px solid rgb(44, 49, 60);\n"
"    border-style: none;\n"
"    border-bottom: 1px solid rgb(44, 49, 60);\n"
"    border-right: 1px solid rgb(44, 49, 60);\n"
"}\n"
"QTableView::horizontalHeader {\n"
"    color: rgb(222, 222, 222);    \n"
"    background-color: rgb(81, 255, 0);\n"
"}\n"
"QHeaderView::section:horizontal\n"
"{\n"
"    color: rgb(222, 222, 222);\n"
"    border: 1px solid rgb(32, 34, 42);\n"
"    background-color: rgb(27, 29, 35);\n"
"    padding: 3px;\n"
"    border-top-left-radius: 7px;\n"
"    border-top-right-radius: 7px;\n"
"}\n"
"QHeaderView::section:vertical\n"
"{\n"
"    color: rgb(222, 222, 222);\n"
"    border: 1px solid rgb(44, 49, 60);\n"
"}\n"
"")
        self.scrollArea_6.setStyleSheet("QScrollBar:horizontal {\n"
"    border: none;\n"
"    background: rgb(52, 59, 72);\n"
"    height: 14px;\n"
"    margin: 0px 21px 0 21px;\n"
"    border-radius: 0px;\n"
"}\n"
" QScrollBar:vertical {\n"
"    border: none;\n"
"    background: rgb(52, 59, 72);\n"
"    width: 14px;\n"
"    margin: 21px 0 21px 0;\n"
"    border-radius: 0px;\n"
" }\n")

        self.tableView.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.tableView.customContextMenuRequested.connect(self.tableViewRightClick)
        
        self.tableView.resizeColumnsToContents()
        
    def tableViewRightClick(self, point):
        index = self.tableView.indexAt(point)
        if index.column() == 3:
            subprocess.Popen(['/home/abhiraj/program_files/firefox/firefox', index.sibling(index.row(), index.column()).data()])

    def logout(self):
        self.lineEdit.setText('')
        self.lineEdit_2.setText('')
        self.label_6.setText('')
        self.label_11.clear()

        conn = sqlite3.Connection('database.db')
        df = pd.read_sql('select * from userData', conn)
        if df.shape[0] == 2 :
            df = df.drop(index=1)
        conn.execute('drop table userData')
        conn.commit()
        df.to_sql('userData', conn)
        conn.commit()
        conn.close()
        self.stackedWidget.setCurrentIndex(0)

    def testnoticetableWidget(self):
        conn  = sqlite3.Connection('database.db')
        
        df    = pd.read_sql('select * from zoomData',conn)
        conn.close()
        model = pandasModel(df)
    
        self.View.setModel(model)
        self.View.setStyleSheet('background: transparent')
        self.scrollArea_5.setStyleSheet('background: transparent')

        self.View.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.View.customContextMenuRequested.connect(self.ViewRightClick)
        
        self.View.resizeColumnsToContents()

    def testassigtableWidget(self):
        conn  = sqlite3.Connection('database.db')
        df    = pd.read_sql('select * from assigData', conn)
        conn.close()
        model = pandasModel(pd.DataFrame(df))
        
        self.tableView.setModel(model)

        self.tableView.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.tableView.customContextMenuRequested.connect(self.tableViewRightClick)
        
        self.tableView.resizeColumnsToContents()
        
        
    def closeanimComp(self):
        self._rightMenu.setGeometry(QtCore.QRect(self.ui.frame_9.width() - 210, 0, 210, self.ui.frame_9.height()))

    def _rmanim(self):
        if self.restanim():
            self.rmanim = QtCore.QPropertyAnimation(self.loadingsolid, b'geometry')
            self.rmanim.setObjectName('rmanim')
            self.rmanim.setDuration(200)
            self.rmanim.setStartValue(QtCore.QRect(0, 0, self.loadingsolid.size().width(), self.loadingsolid.size().height()))
            self.rmanim.setEndValue(QtCore.QRect(0, -self.loadingsolid.size().height(), self.loadingsolid.size().width(), self.loadingsolid.size().height()))
            self.rmanim.setEasingCurve(QtCore.QEasingCurve.InCubic)
            self.rmanim.start()

    def restanim(self):
        self.loadingbar.hide()
        print(self.__login)
        if self.toreach == 'hometab'and (self.__login == True):
            print(self.df)
            try:
                self.label_6.setText("<html><head/><body><p align=\"center\"><span style=\" font-size:26pt; color:#ffffff;\">Welcome, {0}</span></p></body></html>".format(self.df.name[1]))
            except Exception as e:
                self.lineEdit.setText('')
                self.lineEdit_2.setText('')
                return True

            self.stackedWidget.setCurrentIndex(1)
            return True
        if self.toreach == 'hometab'and (self.__login == False) and  not self.loading:
            self.submitForm()
            self.loading = True
            #self.stackedWidget.setCurrentIndex(1)
        if self.toreach == 'assignment':
            self.stackedWidget.setCurrentIndex(3)
            return True
        if self.toreach == 'classTab':
            self.stackedWidget.setCurrentIndex(4)
            return True
        if self.toreach == '_login':
            self.logout()
            self.stackedWidget.setCurrentIndex(0)
            self.__login = False
            return True
        
    def restoreanim(self):
        self.loadingsolid.hide()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.show()
    app.exec()
