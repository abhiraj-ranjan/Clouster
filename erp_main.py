from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5.QtCore import (QCoreApplication, QMetaObject, QObject, QPoint,
    QRect, QSize, QUrl, Qt)
from PyQt5.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QLinearGradient, QPalette, QPainter, QPixmap,
    QRadialGradient)
from PyQt5.QtWidgets import *
import erpUI
import sys
from request_api import call
import sqlite3
import pandas as pd
import numpy as np
import os
import webbrowser


class TranslucentWidgetSignals(QtCore.QObject):
    # SIGNALS
    CLOSE = QtCore.pyqtSignal()

class TranslucentWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(TranslucentWidget, self).__init__(parent)

        # make the window frameless
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.fillColor = QtGui.QColor(30, 30, 30, 120)
        self.penColor = QtGui.QColor("#000000")

        self.popup_fillColor = QtGui.QColor(240, 240, 240, 255)
        self.popup_penColor = QtGui.QColor(200, 200, 200, 255)
        
        self._layout = QtWidgets.QVBoxLayout(self)
        self._layout.setSpacing(0)
        self._layout.setContentsMargins(0,0,0,0)
        
        self.Frame = QtWidgets.QFrame(self)
        self.Frame.setStyleSheet('background-Color:rgba(21, 21, 21, 170)')        
        self._layout.addWidget(self.Frame)
        self.setLayout(self._layout)

        self.mainframe = QtWidgets.QFrame(self.Frame)
        self.mainframe.setStyleSheet('Background-color:rgb(0, 0, 0)')
       
        self.verticalLayout = QtWidgets.QVBoxLayout(self.mainframe)
        self.label = QtWidgets.QLabel(self.mainframe)

        self.vb = QtWidgets.QHBoxLayout(self.label)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)

        self.gif = QtGui.QMovie(os.path.abspath('./icons/window/lm.gif'))
        self.label.setMovie(self.gif)
    
        self.label.setScaledContents(True)
        self.verticalLayout.addWidget(self.label)
        self.gif.start()
        self.mainframe.setLayout(self.verticalLayout)

        self.SIGNALS = TranslucentWidgetSignals()

    def resizeEvent(self, event):
        s = self.size()
        popup_width = 400
        popup_height = 200
        ow = int(s.width() / 2 - popup_width / 2)
        oh = int(s.height() / 2 - popup_height / 2)
        #self.close_btn.move(ow + 265, oh + 5)
        self.mainframe.setGeometry(ow, oh, popup_width, popup_height)

    def _onclose(self):
        self.SIGNALS.CLOSE.emit()

        

class rightMenuSignals(QtCore.QObject):
    CLOSE = QtCore.pyqtSignal()

class rightMenu(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(rightMenu, self).__init__(parent)
        global homework

        # make the window frameless
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self._layout = QtWidgets.QVBoxLayout(self)
        self._layout.setSpacing(0)
        self._layout.setContentsMargins(0,0,0,0)

        self.right_bar = QFrame(self)
        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.right_bar.sizePolicy().hasHeightForWidth())
        self.right_bar.setSizePolicy(sizePolicy)
        self.right_bar.setMinimumSize(QSize(0, 0))
        self.right_bar.setMaximumSize(QSize(16777215, 16777215))
        self.right_bar.setStyleSheet(u"\n"
"    background-color: rgb(56, 56, 56);\n"
"	alternate-background-color: rgb(100, 100, 100);\n"
"	color:rgb(243, 231, 255);\n"
"	selection-color: rgb(255, 230, 243);\n"
"	selection-background-color: rgb(57, 57, 57);\n"
"\n"
"")
        self.right_bar.setFrameShape(QFrame.StyledPanel)
        self.right_bar.setFrameShadow(QFrame.Raised)
        self.verticalLayout_48 = QVBoxLayout(self.right_bar)
        self.verticalLayout_48.setSpacing(10)
        self.verticalLayout_48.setContentsMargins(0, 0, 0, 0)
        self.right_bar_title = QFrame(self.right_bar)
        self.right_bar_title.setFrameShape(QFrame.StyledPanel)
        self.right_bar_title.setFrameShadow(QFrame.Raised)
        
        self.horizontalLayout_5 = QHBoxLayout(self.right_bar_title)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        
        self.label_6 = QLabel(self.right_bar_title)
        self.label_6.setStyleSheet(u"font: 20pt \"Segoe UI light\";\n"
"color: rgb(255, 71, 120);")
        self.label_6.setMargin(0)
        self.label_6.setIndent(3)

        self.horizontalLayout_5.addWidget(self.label_6)

        self.pushButton_6 = QPushButton(self.right_bar_title)
        self.pushButton_6.setObjectName(u"pushButton_6")
        self.pushButton_6.setStyleSheet(u"QPushButton {	\n"
"	border: none;\n"
"	background-color:rgb(255, 71, 120);\n"
"}\n"
"QPushButton:hover {\n"
"	background-color:rgb(255, 131, 133);\n"
"}\n"
"QPushButton:pressed {	\n"
"	background-color: rgb(85, 170, 255);\n"
"}")
        icon = QIcon()
        icon.addFile(u"./icons/window/cil-chevron-circle-right-alt.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton_6.setIcon(icon)
        self.pushButton_6.setIconSize(QSize(37, 37))

        self.horizontalLayout_5.addWidget(self.pushButton_6, 0, Qt.AlignRight)

        self.verticalLayout_48.addWidget(self.right_bar_title)

        self.listWidget_2 = QListWidget(self.right_bar)

        for i in range(len(homework)):
            __qlistwidgetitem = QListWidgetItem(self.listWidget_2)
            __qlistwidgetitem.setCheckState(Qt.Unchecked);
        
        self.listWidget_2.setObjectName(u"listWidget_2")
        self.listWidget_2.setMinimumSize(QSize(207, 0))
        self.listWidget_2.setStyleSheet(u"QListWidget{\n"
"	padding:5px;\n"
"	alternate-background-color: rgb(74, 74, 74);\n"
"	\n"
"	background-color: rgb(62, 62, 62);\n"
"}\n"
"QListWidget::item{\n"
"	margin:10px;\n"
"\n"
"}")
        self.listWidget_2.setFrameShadow(QFrame.Raised)
        self.listWidget_2.setTabKeyNavigation(True)
        self.listWidget_2.setAlternatingRowColors(True)
        self.listWidget_2.setProperty("isWrapping", False)
        self.listWidget_2.setWordWrap(True)
        self.listWidget_2.setSelectionRectVisible(False)
        self.listWidget_2.setItemAlignment(Qt.AlignLeading)

        self.verticalLayout_48.addWidget(self.listWidget_2)
        self._layout.addWidget(self.right_bar)
        self.setLayout(self._layout)
        self.pushButton_6.clicked.connect(self._onclose)
        
        self.SIGNALS = rightMenuSignals()

    def _onclose(self):
        self.SIGNALS.CLOSE.emit()

    def resizeEvent(self, event):
        global homework
        s = self.size()
        width = 200
        ow = int(s.width() - width)
        oh = 0
        #self.close_btn.move(ow + 265, oh + 5)
        self.right_bar.setGeometry(ow, oh, width, s.height())

        self.label_6.setText(u"HomeWork")
        self.pushButton_6.setText("")
        
        __sortingEnabled = self.listWidget_2.isSortingEnabled()
        self.listWidget_2.setSortingEnabled(False)
        for i in range(len(homework)):
            ___qlistwidgetitem = self.listWidget_2.item(i)
            ___qlistwidgetitem.setText(u"".join(homework[i]))
            
        self.listWidget_2.setSortingEnabled(__sortingEnabled)

        

class leftMenuClassSignals(QtCore.QObject):
    # SIGNALS
    onLeaveEvent = QtCore.pyqtSignal()
    OlinkTab     = QtCore.pyqtSignal()
    OassigTab    = QtCore.pyqtSignal()
    OtestTab     = QtCore.pyqtSignal()

class leftMenuClass(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(leftMenuClass, self).__init__(parent)
        self.vbpx = QtWidgets.QVBoxLayout(self)
        self.vbpx.setContentsMargins(0, 0, 0, 0)
        
        self.frame_5 = QFrame(self)
        self.frame_5.setGeometry(QRect(0, 0, 70, 487))
        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_5.sizePolicy().hasHeightForWidth())
        self.frame_5.setSizePolicy(sizePolicy)
        self.frame_5.setMaximumSize(QSize(16777215, 16777215))
        self.frame_5.setStyleSheet(u"background-color: rgb(56, 56, 56);")
        self.frame_5.setFrameShape(QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QFrame.Raised)
        self.verticalLayout_22 = QVBoxLayout(self.frame_5)
        self.verticalLayout_22.setSpacing(0)
        self.verticalLayout_22.setObjectName(u"verticalLayout_22")
        self.verticalLayout_22.setContentsMargins(0, 0, 0, 0)
        self.frame_27 = QFrame(self.frame_5)
        self.frame_27.setObjectName(u"frame_27")
        sizePolicy.setHeightForWidth(self.frame_27.sizePolicy().hasHeightForWidth())
        self.frame_27.setSizePolicy(sizePolicy)
        self.frame_27.setMaximumSize(QSize(16777215, 16777215))
        self.frame_27.setFrameShape(QFrame.StyledPanel)
        self.frame_27.setFrameShadow(QFrame.Raised)
        self.verticalLayout_23 = QVBoxLayout(self.frame_27)
        self.verticalLayout_23.setSpacing(0)
        self.verticalLayout_23.setObjectName(u"verticalLayout_23")
        self.verticalLayout_23.setContentsMargins(0, 0, 0, 0)
        self.frame_28 = QFrame(self.frame_27)
        self.frame_28.setObjectName(u"frame_28")
        sizePolicy1 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.frame_28.sizePolicy().hasHeightForWidth())
        self.frame_28.setSizePolicy(sizePolicy1)
        self.frame_28.setStyleSheet(u"Background-color:transparent;")
        self.frame_28.setFrameShape(QFrame.NoFrame)
        self.frame_28.setFrameShadow(QFrame.Plain)
        self.frame_28.setLineWidth(0)
        self.verticalLayout_24 = QVBoxLayout(self.frame_28)
        self.verticalLayout_24.setSpacing(0)
        self.verticalLayout_24.setObjectName(u"verticalLayout_24")
        self.verticalLayout_24.setContentsMargins(0, 0, 0, 0)
        self.external_links = QPushButton(self.frame_28)
        self.external_links.setObjectName(u"links")
        sizePolicy2 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.external_links.sizePolicy().hasHeightForWidth())
        self.external_links.setSizePolicy(sizePolicy2)
        self.external_links.setMinimumSize(QSize(70, 60))
        self.external_links.setToolTipDuration(1)
        self.external_links.setLayoutDirection(Qt.RightToLeft)
        self.external_links.setStyleSheet(u"QPushButton {	\n"
"	border: none;\n"
"	background-color: transparent;\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(52, 59, 72);\n"
"}\n"
"QPushButton:pressed {	\n"
"	background-color: rgb(85, 170, 255);\n"
"}")
        icon = QIcon()
        icon.addFile(u"./icons/window/cil-external-link.png", QSize(), QIcon.Normal, QIcon.Off)
        self.external_links.setIcon(icon)
        self.external_links.setIconSize(QSize(30, 40))

        self.verticalLayout_24.addWidget(self.external_links, 0, Qt.AlignTop)

        self.tests = QPushButton(self.frame_28)
        self.tests.setObjectName(u"tests")
        sizePolicy2.setHeightForWidth(self.tests.sizePolicy().hasHeightForWidth())
        self.tests.setSizePolicy(sizePolicy2)
        self.tests.setMinimumSize(QSize(70, 60))
        self.tests.setStyleSheet(u"QPushButton {	\n"
"	border: none;\n"
"	background-color: transparent;\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(52, 59, 72);\n"
"}\n"
"QPushButton:pressed {	\n"
"	background-color: rgb(85, 170, 255);\n"
"}")
        icon1 = QIcon()
        icon1.addFile(u"./icons/window/cil-pencil.png", QSize(), QIcon.Normal, QIcon.Off)
        self.tests.setIcon(icon1)
        self.tests.setIconSize(QSize(30, 40))

        self.verticalLayout_24.addWidget(self.tests, 0, Qt.AlignTop)

        self.assignments = QPushButton(self.frame_28)
        self.assignments.setObjectName(u"assignments")
        sizePolicy2.setHeightForWidth(self.assignments.sizePolicy().hasHeightForWidth())
        self.assignments.setSizePolicy(sizePolicy2)
        self.assignments.setMinimumSize(QSize(70, 60))
        self.assignments.setStyleSheet(u"QPushButton {	\n"
"	border: none;\n"
"	background-color: transparent;\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(52, 59, 72);\n"
"}\n"
"QPushButton:pressed {	\n"
"	background-color: rgb(85, 170, 255);\n"
"}\n"
"\n"
"")
        icon2 = QIcon()
        icon2.addFile(u"./icons/window/cil-notes.png", QSize(), QIcon.Normal, QIcon.Off)
        self.assignments.setIcon(icon2)
        self.assignments.setIconSize(QSize(30, 40))

        self.verticalLayout_24.addWidget(self.assignments)


        self.verticalLayout_23.addWidget(self.frame_28)

        self.frame_29 = QFrame(self.frame_27)
        self.frame_29.setObjectName(u"frame_29")
        sizePolicy.setHeightForWidth(self.frame_29.sizePolicy().hasHeightForWidth())
        self.frame_29.setSizePolicy(sizePolicy)
        self.frame_29.setFrameShape(QFrame.StyledPanel)
        self.frame_29.setFrameShadow(QFrame.Raised)

        self.verticalLayout_23.addWidget(self.frame_29)

        self.frame_30 = QFrame(self.frame_27)
        self.frame_30.setObjectName(u"frame_30")
        sizePolicy.setHeightForWidth(self.frame_30.sizePolicy().hasHeightForWidth())
        self.frame_30.setSizePolicy(sizePolicy)
        self.frame_30.setFrameShape(QFrame.StyledPanel)
        self.frame_30.setFrameShadow(QFrame.Raised)
        self.verticalLayout_32 = QVBoxLayout(self.frame_30)
        self.verticalLayout_32.setSpacing(0)
        self.verticalLayout_32.setObjectName(u"verticalLayout_32")
        self.verticalLayout_32.setContentsMargins(0, 0, 0, 0)
        self.my_profile = QPushButton(self.frame_30)
        self.my_profile.setObjectName(u"my_profile")
        sizePolicy1.setHeightForWidth(self.my_profile.sizePolicy().hasHeightForWidth())
        self.my_profile.setSizePolicy(sizePolicy1)
        self.my_profile.setMinimumSize(QSize(60, 60))
        self.my_profile.setMaximumSize(QSize(60, 60))
        font = QFont()
        font.setFamily(u"Segoe UI")
        font.setPointSize(12)
        self.my_profile.setFont(font)
        self.my_profile.setStyleSheet(u"QPushButton {\n"
"	border-radius: 30px;\n"
"	background-color: rgb(100, 100, 100);\n"
"	border: 7px solid rgb(74, 74, 74);\n"
"	background-position: center;\n"
"	background-repeat: no-repeat;\n"
"}"
"       QPushButton:pressed{\n"
"       background-color: rgb(221, 54, 72);\n"
"}	")
        icon5 = QIcon()
        icon5.addFile(u"./icons/window/cil-user.png", QSize(), QIcon.Normal, QIcon.Off)
        self.my_profile.setIcon(icon5)
        self.my_profile.setIconSize(QSize(20, 30))
        self.verticalLayout_32.addWidget(self.my_profile, 0, Qt.AlignHCenter|Qt.AlignBottom)


        self.verticalLayout_23.addWidget(self.frame_30, 0, Qt.AlignHCenter|Qt.AlignBottom)


        self.verticalLayout_22.addWidget(self.frame_27)
        self.initUI()
        self.vbpx.addWidget(self.frame_5)
        self.setLayout(self.vbpx)

    def initUI(self):
#if QT_CONFIG(tooltip)
        self.external_links.setToolTip(u"Online Classes")
        self.external_links.clicked.connect(self.changeView)
#endif // QT_CONFIG(tooltip)
        self.external_links.setText("")
#if QT_CONFIG(tooltip)
        self.tests.setToolTip(u"online test")
#endif // QT_CONFIG(tooltip)
        self.tests.setText("")
#if QT_CONFIG(tooltip)
        self.assignments.setToolTip(u"assignments")
#endif // QT_CONFIG(tooltip)
        self.assignments.setText("")
        self.my_profile.setText("")
        self.signals = leftMenuClassSignals()

    def leaveEvent(self, event):
        self.signals.onLeaveEvent.emit()

    def changeView(self):
        wid = self.sender()
        if wid.objectName() == 'links':
            self.signals.OlinkTab.emit()

            

class hoverMenuClassSignals(QtCore.QObject):
    EnterEventTriggered = QtCore.pyqtSignal()
    
class hoverMenuClass(QtWidgets.QLabel):
     def __init__(self, parent=None):
        super(hoverMenuClass, self).__init__(parent)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.initUI()

     def initUI(self):
        self.frame = QtWidgets.QFrame(self)
        self.vlayout = QtWidgets.QVBoxLayout(self)
        self.vlayout.setSpacing(10)
        self.vlayout.setContentsMargins(0, 0, 3, 0)
        self.vlayout.addWidget(self.frame)
        self.setLayout(self.vlayout)
        self.frame.setStyleSheet('background-color:rgb(255, 82, 85);border:1px solid rgb(255, 82, 85);')
        self.Signal = hoverMenuClassSignals()

     def enterEvent(self, event):
        #self.expandMenu()
        self.Signal.EnterEventTriggered.emit()

             
     def expandMenu(self):
        wid = self.sender()
        
        self.minanimation = QtCore.QPropertyAnimation(self.ui.stackedWidget, b"geometry")
        self.minanimation.setDuration(500)
        x, y, w, h = self.ui.stackedWidget.x(), self.ui.stackedWidget.y(), self.ui.stackedWidget.width(), self.ui.stackedWidget.height()
        self.minanimation.setStartValue(QtCore.QRect(9, 0, w, h))
        self.minanimation.setEndValue(QtCore.QRect(9 + self.ui.leftMenu.width(), 0, w, h))
        self.minanimation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)

        self.posanimation = QtCore.QPropertyAnimation(self.ui.leftMenu, b"geometry")
        self.posanimation.setDuration(500)       
        x, y, w, h = self.ui.leftMenu.x(), self.ui.leftMenu.y(), self.ui.leftMenu.width(), self.ui.leftMenu.height()
        self.posanimation.setStartValue(QtCore.QRect(-70, 0, w, h))
        self.posanimation.setEndValue(QtCore.QRect(0,0,w,h))
        self.posanimation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        #self.posanimation.start()

        '''
        self.maxanimation = QtCore.QPropertyAnimation(ui.hoverMenu, b"geometry")
        self.maxanimation.setDuration(500)       
        self.maxanimation.setStartValue(ui.widget_3.geometry())
        self.maxanimation.setEndValue(ui.widget_3.geometry())
        self.maxanimation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        #self.posanimation.start()
        '''

        self.animationgrp = QtCore.QParallelAnimationGroup(self)
        #self.animationgrp.addAnimation(self.maxanimation)
        self.animationgrp.addAnimation(self.posanimation)
        self.animationgrp.addAnimation(self.minanimation)

        self.animationgrp.start()
        self._hideMenus = True
        
        #self.minanimation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        #self.minanimation.start()



class pandasModel(QtCore.QAbstractTableModel):
        def __init__(self, data):
            QtCore.QAbstractTableModel.__init__(self)
            self._data = data

        def rowCount(self, parent=None):
            return self._data.shape[0]

        def columnCount(self, parent=None):
            return self._data.shape[1]

        def data(self, index, role=Qt.DisplayRole):
            if index.isValid():
                if role == Qt.DisplayRole:
                    return str(self._data.iloc[index.row(), index.column()])
            return None

        def headerData(self, col, orientation, role):
            if orientation == Qt.Horizontal and role == Qt.DisplayRole:
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

            

class Window(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        #self.ui = erpUI_main.Ui_Form()
        self.ui = erpUI.Ui_Form()
        self.ui.setupUi(self)
        #uic.loadUi('erpUI.ui', self)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.initUI()
        self.declareVar()

    def declareVar(self):
        global homework
        self._toggleMax           = 0
        self._hideMenu            = True
        self._popframe            = None
        self._popflag             = False
        self._rightMenuDrivenTrue = False
        homework                  = ['never seen homework here', 'Hw for All classes, B, C, D MAHT-Ex 7.2 Do questions 11 , 12, 12, , 12, 12 in registers in case if any doubt discuss the same in class, VBPSDEL', 'Hw for all classes, B, C, D MAHT-Ex 7.2 Do questions 11 , 12, 12, , 12, 12 in registers in case oif any doubt sicuss the sa,e in class, VBPSDEL']
        notepadText               = ''
        self._leftMenuhovered     = False
        
    def linkup(self):
        self.ui.closeBtn.clicked.connect(self.close)
        self.ui.maxBtn.clicked.connect(self.toggleMax)
        self.ui.miniBtn.clicked.connect(self.showMinimized)
        self.ui.pushButton_4.clicked.connect(self.submitForm)
        self.ui.pushButton_8.clicked.connect(self._rightMenuDrive)
        self.ui.leftMenu.external_links.clicked.connect(self.leftMenuLinkup)
        self.ui.leftMenu.assignments.clicked.connect(self.leftMenuLinkup)
        #self.ui.textEdit_3.textChanged.connect(self.notepadTextChangedFunc)
        #self.ui.textEdit_2.textChanged.connect(self.notepadTextChangedFunc)
        #self.ui.textEdit_4.textChanged.connect(self.notepadTextChangedFunc)
        self.ui.leftMenu.my_profile.clicked.connect(self.leftMenuLinkup)
        self.ui.about.clicked.connect(self.aboutchange)
        self.ui.pushButton_7.clicked.connect(self.logout)

    def aboutchange(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.settingsTab)

    def testclicked(self):
        webbrowser.open('https://vbpsdelf.accevate.com/app121/student/google-form-test/?id='+self.APIcall.id)

        
    def notepadTextChangedFunc(self):
        wid = self.sender()
        notepadText = wid.toPlainText()
        
        if wid.objectName() == 'textEdit_2':
            self.ui.textEdit_3.setText(notepadText)
            self.ui.textEdit_4.setText(notepadText)

        elif wid.objectName() == 'textEdit_3':
            self.ui.textEdit_2.setText(notepadText)
            self.ui.textEdit_4.setText(notepadText)

        if wid.objectName() == 'textEdit_4':
            self.ui.textEdit_2.setText(notepadText)
            self.ui.textEdit_3.setText(notepadText)

            
    def leftMenuLinkup(self):
        wid = self.sender()
        
        if wid.objectName() == 'links':
            self.ui.stackedWidget.setCurrentWidget(self.ui.linkTab)
            
        if wid.objectName() == 'assignments':
            self.ui.stackedWidget.setCurrentWidget(self.ui.assigTab)

        if wid.objectName() == 'my_profile':
            self.ui.stackedWidget.setCurrentWidget(self.ui.userTab)
            
        x, y, w, h = self.ui.stackedWidget.x(), self.ui.stackedWidget.y(), self.ui.stackedWidget.width(), self.ui.stackedWidget.height()
        self.ui.stackedWidget.setGeometry(QtCore.QRect(9+self.ui.leftMenu.width(), 0, w, h))

            
    def submitForm(self):
        if self.ui.lineEdit.text():
            if self.ui.lineEdit_4.text():
                if os.path.exists(os.path.join(os.getcwd(), 'database.db')):                                  
                    self.classicLogin()                    
                else:
                    conn = sqlite3.Connection('database.db')
                    df = pd.DataFrame(columns = ['primaryID','username', 'password', 'id', 'name', 'Class', 'dob', 'doa', 'permaadd', 'corradd', 'cat', 'religion', 'fname', 'mname', 'mob', 'cast', 'nationality'])
                    df = df.append({'primaryID':'0', 'username':'root', 'password':'toor', 'id':'2757', 'name':'Abhiraj Ranjan', 'Class':'XII-A', 'dob':'23 June, 2004', 'doa':'28 Feb 2012', 'permaadd':'...', 'corradd':'...', 'cat':"Humanity", 'religion':'Humanity', 'fname':'...', 'mname':'...', 'mob':'100', 'cast':'Humanity', 'nationality':'INDIAN'}, ignore_index = True)
                    df.to_sql('userData', conn)
                    conn.commit()
                    conn.close()
                    self.classicLogin()
                    

    def classicLogin(self):
        if self.ui.lineEdit.text() == 'root' and self.ui.lineEdit_4.text() == 'toor':
            self.testlogindb()
        else:
            self._onpopup()
            self.afterLogin()
            
                    
    def API(self, usrname='',passwrd=''):
        APIcall = call(username=usrname, password=passwrd)
        return APIcall
    

    def initUI(self):
        prestrtn = self.autoLogin()
        if prestrtn:
            result, username, pasword = prestrtn
        
        self.ui.leftMenu = leftMenuClass(self.ui.frame_9)
        
        self.ui.leftMenu.signals.onLeaveEvent.connect(self.leftMenuLeaveFunc)
        self.ui.leftMenu.move(-70, 0)
        self.ui.leftMenu.resize(70, self.height()-42-18)

        self.hoverMenu   = hoverMenuClass(self.ui.frame_9)
        
        self.hoverMenu.resize(9, self.height())
        self.hoverMenu.Signal.EnterEventTriggered.connect(self.hoverMenuEnterFunc)
        self.hoverMenu.move(0, 0)

        self.ui.label_credits.setText('')

        self.threadpool  = QtCore.QThreadPool()
        self.linkup()
        self.ui.stackedWidget.setCurrentWidget(self.ui.loginTab)
        if prestrtn:
            self.afterLoginResults(result, popupclose=False, username=username, password=pasword)
        else:
            self.afterLoginError(autoLoginconn=True)
            #self.ui.stackedWidget.setCurrentWidget(self.ui.loginTab)
            
    def autoLogin(self):

        if os.path.exists(os.path.join(os.getcwd(), 'database.db')) :
        
            conn = sqlite3.Connection('database.db')
            df   = pd.read_sql('select * from userData', conn)
            conn.close()
            if df.shape[0] == 2 :
                if 1 in df.primaryID.to_dict():
                    username, pasword = df.username[1], df.password[1]
                    print(username, pasword)
                    #self._onpopup()
                    try:
                        result = self.API(usrname=username,passwrd=pasword)
                    except:
                        print('error while going online')
                        
                        #self.ui.stackedWidget.setCurrentWidget(self.ui.loginTab)
                        return False
                    else:
                        return result, username, pasword
        
    def afterLoginResults(self, api, popupclose=True, username=False, password=False):
        print('result')
        self.APIcall = api
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
            df       = df.append({'primaryID':'1', 'username':self.ui.lineEdit.text(), 'password':self.ui.lineEdit_4.text(), 'id':id, 'name':data['name'], 'Class':data['class'], 'dob':data['Date Of Birth'], 'doa':data['Date Of Admission'], 'permaadd':data['Permanent Address'], 'corradd':data["Correspondance Address"], 'cat':data["Category"], 'religion':data["Religion"], 'fname':data["Father's Name"], 'mname':data["Mother's Name"], 'mob':data['Mobile NO.'], 'cast':data["Cast"], 'nationality':data["Nationality"]}, ignore_index = True)
        
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
        self.infoedior()
        self.ui.leftMenu.tests.clicked.connect(self.testclicked)
        self.ui.stackedWidget.setCurrentWidget(self.ui.userTab)
        if popupclose:
            self._popframe.close()
            self._popflag = False


    def afterLoginError(self, autoLoginconn=False):
        print("error goin' online, loading from database stored")
        conn = sqlite3.Connection('database.db')
        df   = pd.read_sql('select * from userData', conn)
        conn.close()
        
        if 1 in df.primaryID.to_dict():
            if autoLoginconn:
                self.testnoticetableWidget()
                self.testassigtableWidget()
                self.dbinfeditor()

                self.ui.stackedWidget.setCurrentWidget(self.ui.userTab)
                self.ui.label_11.setPixmap(QPixmap(os.path.abspath('icons/user.jpeg')))


            elif self.ui.lineEdit.text() == df.username[1] :
                if self.ui.lineEdit_4.text() == df.password[1]:
                    self.testnoticetableWidget()
                    self.testassigtableWidget()
                    self.dbinfeditor()

                    self.ui.stackedWidget.setCurrentWidget(self.ui.userTab)
                    self.ui.label_11.setPixmap(QPixmap(os.path.abspath('icons/user.jpeg')))
                    self._popframe.close()
                    self._popflag = False
                else:
                    print('incorrect set of username and password')
                    if not autoLoginconn :
                        self._popframe.close()
                        self._popflag = False
                        
            else:
                print('incorrect set of username and password')
                if not autoLoginconn :
                    self._popframe.close()
                    self._popflag = False
        else:
            print('cannot connect to database or probaby this problem can be raised by fees issues, net reset and various other reasons')
            self.ui.stackedWidget.setCurrentWidget(self.ui.loginTab)
            if not autoLoginconn:
                self._popframe.close()
                self._popflag = False

        
    def afterLogin(self):
        
        worker = Worker(self.API,usrname=self.ui.lineEdit.text(),passwrd=self.ui.lineEdit_4.text())
        worker.signals.result.connect(self.afterLoginResults)
        worker.signals.error.connect(self.afterLoginError)

        self.threadpool.start(worker)

    def afterLoginFunc(self):
        ...
        #self.ui.stackedWidget.setCurrentWidget(self.ui.userTab)
        
    def leftMenuLeaveFunc(self):

        self.minanimation = QtCore.QPropertyAnimation(self.ui.stackedWidget, b"geometry")
        self.minanimation.setDuration(500)
        x, y, w, h = self.ui.stackedWidget.x(), self.ui.stackedWidget.y(), self.ui.stackedWidget.width(), self.ui.stackedWidget.height()
        self.minanimation.setStartValue(QtCore.QRect(9+self.ui.leftMenu.width(), 0, w, h))
        self.minanimation.setEndValue(QtCore.QRect(9, 0, w, h))
        self.minanimation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)

        self.posanimation = QtCore.QPropertyAnimation(self.ui.leftMenu, b"geometry")
        self.posanimation.setDuration(500)       
        x, y, w, h = self.ui.leftMenu.x(), self.ui.leftMenu.y(), self.ui.leftMenu.width(), self.ui.leftMenu.height()
        self.posanimation.setStartValue(self.ui.leftMenu.geometry())
        self.posanimation.setEndValue(QtCore.QRect(x-100, y, w, h))
        self.posanimation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        #self.posanimation.start()

        '''
        self.maxanimation = QtCore.QPropertyAnimation(ui.hoverMenu, b"geometry")
        self.maxanimation.setDuration(500)       
        self.maxanimation.setStartValue(ui.widget_3.geometry())
        self.maxanimation.setEndValue(ui.widget_3.geometry())
        self.maxanimation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        #self.posanimation.start()
        '''

        self.animationgrp = QtCore.QParallelAnimationGroup(self)
        #self.animationgrp.addAnimation(self.maxanimation)
        self.animationgrp.addAnimation(self.posanimation)
        self.animationgrp.addAnimation(self.minanimation)

        self.animationgrp.start()
        self._hideMenus = True
        self._leftMenuhovered = False
        
        #self.minanimation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        #self.minanimation.start()

    def hoverMenuEnterFunc(self):
        if self.ui.stackedWidget.currentWidget().objectName() == 'loginTab': return
        
        if self._leftMenuhovered: return 
            
        self.minanimation = QtCore.QPropertyAnimation(self.ui.stackedWidget, b"geometry")
        self.minanimation.setDuration(500)
        x, y, w, h = self.ui.stackedWidget.x(), self.ui.stackedWidget.y(), self.ui.stackedWidget.width(), self.ui.stackedWidget.height()
        self.minanimation.setStartValue(QtCore.QRect(9, 0, w, h))
        self.minanimation.setEndValue(QtCore.QRect(9 + self.ui.leftMenu.width(), 0, w, h))
        self.minanimation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)

        self.posanimation = QtCore.QPropertyAnimation(self.ui.leftMenu, b"geometry")
        self.posanimation.setDuration(500)       
        x, y, w, h = self.ui.leftMenu.x(), self.ui.leftMenu.y(), self.ui.leftMenu.width(), self.ui.leftMenu.height()
        self.posanimation.setStartValue(QtCore.QRect(-70, 0, w, h))
        self.posanimation.setEndValue(QtCore.QRect(0,0,w,h))
        self.posanimation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        
        self.animationgrp = QtCore.QParallelAnimationGroup(self)
        #self.animationgrp.addAnimation(self.maxanimation)
        self.animationgrp.addAnimation(self.posanimation)
        self.animationgrp.addAnimation(self.minanimation)
        self.animationgrp.start()
        self._hideMenus = True
        
    
    def noticetableWidget(self):
        a = self.APIcall.zoomlinks
        model = pandasModel(a)
    
        self.ui.View.setModel(model)

        self.ui.View.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.View.customContextMenuRequested.connect(self.ViewRightClick)
        
        self.ui.View.resizeColumnsToContents()
        

    def ViewRightClick(self, point):
        index = self.ui.View.indexAt(point)
        if index.column() == 2:
            webbrowser.open(index.sibling(index.row(), index.column()).data())
            

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
        self.ui.tableView.setModel(model)

        self.ui.tableView.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.tableView.customContextMenuRequested.connect(self.tableViewRightClick)
        
        self.ui.tableView.resizeColumnsToContents()
        

    def tableViewRightClick(self, point):
        index = self.ui.tableView.indexAt(point)
        if index.column() == 3:
            webbrowser.open(index.sibling(index.row(), index.column()).data())


    def infoedior(self):
        data = self.APIcall.personalData
        self.ui._dob.setText(data['Date Of Birth'])
        self.ui._doa.setText(data['Date Of Admission'])
        self.ui._fathername.setText(data["Father's Name"])
        self.ui._mothername.setText(data["Mother's Name"])
        self.ui._permaadd.setText(data['Permanent Address'][:12]+'...')
        self.ui._corradd.setText(data["Correspondance Address"][:12]+'...')
        self.ui._cast.setText(data["Cast"])
        self.ui._cat.setText(data["Category"])
        self.ui._nationality.setText(data["Nationality"])
        self.ui._phoneno.setText(data['Mobile NO.'])
        self.ui._religion.setText(data["Religion"])
        self.ui._studentname.setText(data['name'])
        self.ui.label_credits.setText('Logged in as {0}'.format(data["name"]))
        self.ui._class.setText(data['class'])
        self.ui.label_11.setPixmap(QPixmap(os.path.abspath('icons/user.jpeg')))
        self.ui.label_11.setScaledContents(True)

        self.toottipAddon(data)
        
    
    def toottipAddon(self, data):
        self.ui._permaadd.setToolTip(data['Permanent Address'])
        self.ui._corradd.setToolTip(data["Correspondance Address"])
        self.ui.leftMenu.external_links.setToolTip('online classes')
        

    def logout(self):
        self.ui.lineEdit.setText('')
        self.ui.lineEdit_4.setText('')
        conn = sqlite3.Connection('database.db')
        df = pd.read_sql('select * from userData', conn)
        if df.shape[0] == 2 :
            df = df.drop(index=1)
        conn.execute('drop table userData')
        conn.commit()
        df.to_sql('userData', conn)
        conn.commit()
        conn.close()
        self.ui.stackedWidget.setCurrentWidget(self.ui.loginTab)
      

    def toggleMax(self):
        if self.isFullScreen():
            self.showNormal()
            
        else:
            self.showFullScreen()    

            """
            global screenavailGeo
            print(screenavailGeo)
            self.prop = QtCore.QPropertyAnimation(self, b'geometry')
            self.prop.setDuration(100)
            self.prop.setStartValue(self.geometry())
            self.prop.setEndValue(screenavailGeo)
            self.prop.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            self.prop.start()
            self._toggleMax = 1
            
        
        if self._toggleMax == 1:
            
            self.prop = QtCore.QPropertyAnimation(self, b'geometry')
            #ui.frame_5.setMaximumSize(QtCore.QSize(QtWidgets.QWIDGETSIZE_MAX, QtWidgets.QWIDGETSIZE_MAX))
            self.prop.setDuration(200)
            self.prop.setEndValue(self.defaultsize)
            self.prop.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            self.prop.start()
            self._toggleMax = 0
            
            """
    def resizeEvent(self, event):
        if self._popflag:
            self._popframe.move(0, 0)
            self._popframe.resize(self.ui.frame_9.width(), self.ui.frame_9.height())

        self.ui.leftMenu.resize(70, self.height()-42-18)
        self.hoverMenu.resize(9, self.height())
        
            
        if self._rightMenuDrivenTrue:
            self._rightMenu.move(self.ui.frame_9.width() - 210, 0)
            self._rightMenu.resize(210, self.ui.frame_9.height())
            
            
    def _rightMenuDrive(self):
        if self._rightMenuDrivenTrue : return
        global frameHeight, frameWidth, screenavailGeo, screenSize
        frameWidth  = self.ui.frame_9.width()
        frameHeight = self.ui.frame_9.height()
        self._rightMenuDrivenTrue = True
        self._rightMenu = rightMenu(self.ui.frame_9)
        #self._rightMenu.move(ui.frame_9.width() - 200, 0)
        self._rightMenu.move(0 , 0)

        self._rightMenu.SIGNALS.CLOSE.connect(self.closeMenu)
        
        self._rightMenu.resize(200, self.ui.frame_9.height())
        self._rightMenu.show()
        
        self.prop = QtCore.QPropertyAnimation(self._rightMenu, b'geometry')
        self.prop.setDuration(300)
        self.prop.setStartValue(QtCore.QRect(self.ui.frame_9.width() , 0, 210, self.ui.frame_9.height()))
        self.prop.setEndValue(QtCore.QRect(self.ui.frame_9.width() - 210, 0, 210, self.ui.frame_9.height()))
        self.prop.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        
        self.prop.start()
        self.prop.finished.connect(self.closeanimComp)
        

    def testlogindb(self):
        self.testnoticetableWidget()
        self.testassigtableWidget()
        self.gettestlogindb()
        
        self.ui.stackedWidget.setCurrentWidget(self.ui.userTab)

    def gettestlogindb(self):
        conn = sqlite3.Connection('database.db')
        df = pd.read_sql_query('select * from userData', conn)
        conn.close()
        self.testinfoeditor(df, 0)

    def testinfoeditor(self, df, i):
        self.ui._dob.setText(df.dob[i])
        self.ui._doa.setText(df.doa[i])
        self.ui._fathername.setText(df.fname[i])
        self.ui._mothername.setText(df.mname[i])
        self.ui._permaadd.setText(df.permaadd[i][:12]+'...')
        self.ui._corradd.setText(df.corradd[i][:12]+'...')
        self.ui._cast.setText(df.cast[i])
        self.ui._cat.setText(df.cat[i])
        self.ui._nationality.setText(df.nationality[i])
        self.ui._phoneno.setText(df.mob[i])
        self.ui._religion.setText(df.religion[i])
        self.ui._studentname.setText(df.name[i])
        self.ui.label_credits.setText('Logged in as {0}'.format(df.name[i]))
        self.ui._class.setText(df.Class[i])
        self.ui.label_11.setPixmap(QPixmap(os.path.abspath('./icons/default.png')))
        self.ui.label_11.setScaledContents(True)
        
        self.testooltipAddon(df)

    def dbinfeditor(self):
        conn = sqlite3.Connection('database.db')
        df = pd.read_sql_query('select * from userData', conn)
        conn.close()
        self.testinfoeditor(df, 1)

        
    def testooltipAddon(self, df):
        self.ui._permaadd.setToolTip(df.permaadd[0])
        self.ui._corradd.setToolTip(df.corradd[0])
        self.ui.leftMenu.external_links.setToolTip('online classes')

    def testnoticetableWidget(self):
        conn  = sqlite3.Connection('database.db')
        
        df    = pd.read_sql('select * from zoomData',conn)
        conn.close()
        model = pandasModel(df)
    
        self.ui.View.setModel(model)

        self.ui.View.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.View.customContextMenuRequested.connect(self.ViewRightClick)
        
        self.ui.View.resizeColumnsToContents()

    def testassigtableWidget(self):
        conn  = sqlite3.Connection('database.db')
        df    = pd.read_sql('select * from assigData', conn)
        conn.close()
        model = pandasModel(pd.DataFrame(df))
        
        self.ui.tableView.setModel(model)

        self.ui.tableView.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.tableView.customContextMenuRequested.connect(self.tableViewRightClick)
        
        self.ui.tableView.resizeColumnsToContents()
        
        
    def closeanimComp(self):
        self._rightMenu.setGeometry(QtCore.QRect(self.ui.frame_9.width() - 210, 0, 210, self.ui.frame_9.height()))

    def closeMenu(self):
        self.prop = QtCore.QPropertyAnimation(self._rightMenu, b'geometry')
        self.prop.setDuration(300)
        self.prop.setStartValue(QtCore.QRect(self.ui.frame_9.width() - 210, 0, 210, self.ui.frame_9.height()))
        self.prop.setEndValue(QtCore.QRect(self.ui.frame_9.width() , 0, 210, self.ui.frame_9.height()))
        self.prop.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        self.prop.start()
        self._rightMenuDrivenTrue = False
        self.prop.finished.connect(self._closeMenu)

    def _closeMenu(self):
        self._rightMenu.setGeometry(QtCore.QRect(self.ui.frame_9.width() , 0, 0, 0))

    def _onpopup(self):
        self._popframe = TranslucentWidget(self.ui.frame_9)
        self._popframe.move(0, 0)
        self._popframe.resize(self.ui.frame_9.width(), self.ui.frame_9.height())
        self._popframe.SIGNALS.CLOSE.connect(self._closepopup)
        self._popflag  = True
        self._popframe.show()
        
    def _closepopup(self):
        if self._returnText == 'STUDENTS_ACCESS':
            self.ui.stackedWidget.setCurrentWidget(self.ui.userTab)
            self._popframe.close()
            self._popflag = False
        else :
            self._popframe.close()
            self._popflag = False

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QtCore.QPoint(event.globalPos()-self.oldPos)
        self.move(self.x()+delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()


if __name__ == '__main__':
    import sys
    
    app = QtWidgets.QApplication(sys.argv)
    screen = app.primaryScreen()
    global screenSize
    screenSize = screen.size()
    screenavailGeo = screen.availableGeometry()
    print(screen , screenSize, screenavailGeo)
    
    window = Window()
    window.show()
    app.exec()
