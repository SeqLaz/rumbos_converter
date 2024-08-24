# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'rumbos_creator_gui.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QHeaderView,
    QLabel, QLineEdit, QMainWindow, QMenu,
    QMenuBar, QPushButton, QSizePolicy, QSpacerItem,
    QStatusBar, QTableView, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1252, 868)
        self.actionAdd_CSV_File = QAction(MainWindow)
        self.actionAdd_CSV_File.setObjectName(u"actionAdd_CSV_File")
        self.actionClear = QAction(MainWindow)
        self.actionClear.setObjectName(u"actionClear")
        self.actionQuit = QAction(MainWindow)
        self.actionQuit.setObjectName(u"actionQuit")
        self.actionSave = QAction(MainWindow)
        self.actionSave.setObjectName(u"actionSave")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_2 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.upper_frame = QFrame(self.centralwidget)
        self.upper_frame.setObjectName(u"upper_frame")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.upper_frame.sizePolicy().hasHeightForWidth())
        self.upper_frame.setSizePolicy(sizePolicy)
        self.upper_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.upper_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout = QHBoxLayout(self.upper_frame)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.coordinate_table = QTableView(self.upper_frame)
        self.coordinate_table.setObjectName(u"coordinate_table")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.coordinate_table.sizePolicy().hasHeightForWidth())
        self.coordinate_table.setSizePolicy(sizePolicy1)
        self.coordinate_table.setMinimumSize(QSize(350, 0))
        self.coordinate_table.setMaximumSize(QSize(400, 16777215))

        self.horizontalLayout.addWidget(self.coordinate_table)

        self.frame = QFrame(self.upper_frame)
        self.frame.setObjectName(u"frame")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy2)
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout = QVBoxLayout(self.frame)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.coordinate_label = QLabel(self.frame)
        self.coordinate_label.setObjectName(u"coordinate_label")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Maximum)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.coordinate_label.sizePolicy().hasHeightForWidth())
        self.coordinate_label.setSizePolicy(sizePolicy3)
        self.coordinate_label.setMinimumSize(QSize(0, 50))

        self.verticalLayout.addWidget(self.coordinate_label)

        self.crs_tedit = QLineEdit(self.frame)
        self.crs_tedit.setObjectName(u"crs_tedit")

        self.verticalLayout.addWidget(self.crs_tedit)

        self.generate_btn = QPushButton(self.frame)
        self.generate_btn.setObjectName(u"generate_btn")
        self.generate_btn.setStyleSheet(u"")

        self.verticalLayout.addWidget(self.generate_btn)

        self.save_btn = QPushButton(self.frame)
        self.save_btn.setObjectName(u"save_btn")

        self.verticalLayout.addWidget(self.save_btn)

        self.clear_btn = QPushButton(self.frame)
        self.clear_btn.setObjectName(u"clear_btn")
        self.clear_btn.setStyleSheet(u"background-color: red;\n"
"color: white;")

        self.verticalLayout.addWidget(self.clear_btn)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.horizontalLayout.addWidget(self.frame)

        self.graph_label = QLabel(self.upper_frame)
        self.graph_label.setObjectName(u"graph_label")
        sizePolicy3.setHeightForWidth(self.graph_label.sizePolicy().hasHeightForWidth())
        self.graph_label.setSizePolicy(sizePolicy3)
        self.graph_label.setMinimumSize(QSize(640, 480))

        self.horizontalLayout.addWidget(self.graph_label)


        self.horizontalLayout_2.addWidget(self.upper_frame)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.rumbos_table = QTableView(self.centralwidget)
        self.rumbos_table.setObjectName(u"rumbos_table")

        self.verticalLayout_2.addWidget(self.rumbos_table)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1252, 23))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menuFile.addAction(self.actionAdd_CSV_File)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionClear)
        self.menuFile.addAction(self.actionQuit)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Generate Rumbos", None))
        self.actionAdd_CSV_File.setText(QCoreApplication.translate("MainWindow", u"Add CSV File", None))
        self.actionClear.setText(QCoreApplication.translate("MainWindow", u"Clear", None))
        self.actionQuit.setText(QCoreApplication.translate("MainWindow", u"Quit", None))
        self.actionSave.setText(QCoreApplication.translate("MainWindow", u"Save", None))
        self.coordinate_label.setText(QCoreApplication.translate("MainWindow", u"Establish Coordinate system", None))
        self.generate_btn.setText(QCoreApplication.translate("MainWindow", u"Generate", None))
        self.save_btn.setText(QCoreApplication.translate("MainWindow", u"Save", None))
        self.clear_btn.setText(QCoreApplication.translate("MainWindow", u"Clear", None))
        self.graph_label.setText(QCoreApplication.translate("MainWindow", u"Graph", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
    # retranslateUi

