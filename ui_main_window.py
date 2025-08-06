# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.9.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QGridLayout, QHBoxLayout,
    QHeaderView, QLabel, QLineEdit, QMainWindow,
    QMenuBar, QPushButton, QSizePolicy, QStatusBar,
    QTreeView, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(973, 709)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.treeView = QTreeView(self.centralwidget)
        self.treeView.setObjectName(u"treeView")
        self.treeView.setEnabled(True)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.treeView.sizePolicy().hasHeightForWidth())
        self.treeView.setSizePolicy(sizePolicy)

        self.verticalLayout.addWidget(self.treeView)

        self.editPanel = QWidget(self.centralwidget)
        self.editPanel.setObjectName(u"editPanel")
        self.editPanelLayout = QHBoxLayout(self.editPanel)
        self.editPanelLayout.setSpacing(0)
        self.editPanelLayout.setObjectName(u"editPanelLayout")
        self.editPanelLayout.setContentsMargins(0, 0, 0, 0)
        self.editNameLabel = QLabel(self.editPanel)
        self.editNameLabel.setObjectName(u"editNameLabel")

        self.editPanelLayout.addWidget(self.editNameLabel)

        self.editNameEdit = QLineEdit(self.editPanel)
        self.editNameEdit.setObjectName(u"editNameEdit")

        self.editPanelLayout.addWidget(self.editNameEdit)

        self.editSaveBtn = QPushButton(self.editPanel)
        self.editSaveBtn.setObjectName(u"editSaveBtn")

        self.editPanelLayout.addWidget(self.editSaveBtn)

        self.editCancelBtn = QPushButton(self.editPanel)
        self.editCancelBtn.setObjectName(u"editCancelBtn")

        self.editPanelLayout.addWidget(self.editCancelBtn)


        self.verticalLayout.addWidget(self.editPanel)

        self.colorBar = QHBoxLayout()
        self.colorBar.setSpacing(0)
        self.colorBar.setObjectName(u"colorBar")
        self.inputBar = QHBoxLayout()
        self.inputBar.setObjectName(u"inputBar")
        self.typeCombo = QComboBox(self.centralwidget)
        self.typeCombo.setObjectName(u"typeCombo")

        self.inputBar.addWidget(self.typeCombo)

        self.ofLabel = QLabel(self.centralwidget)
        self.ofLabel.setObjectName(u"ofLabel")

        self.inputBar.addWidget(self.ofLabel)

        self.catCombo = QComboBox(self.centralwidget)
        self.catCombo.setObjectName(u"catCombo")

        self.inputBar.addWidget(self.catCombo)

        self.nameEdit = QLineEdit(self.centralwidget)
        self.nameEdit.setObjectName(u"nameEdit")

        self.inputBar.addWidget(self.nameEdit)


        self.colorBar.addLayout(self.inputBar)

        self.gradientLabel = QLabel(self.centralwidget)
        self.gradientLabel.setObjectName(u"gradientLabel")

        self.colorBar.addWidget(self.gradientLabel)

        self.startColorLabel = QLabel(self.centralwidget)
        self.startColorLabel.setObjectName(u"startColorLabel")

        self.colorBar.addWidget(self.startColorLabel)

        self.startColorEdit = QLineEdit(self.centralwidget)
        self.startColorEdit.setObjectName(u"startColorEdit")

        self.colorBar.addWidget(self.startColorEdit)

        self.startColorBtn = QPushButton(self.centralwidget)
        self.startColorBtn.setObjectName(u"startColorBtn")

        self.colorBar.addWidget(self.startColorBtn)

        self.endColorLabel = QLabel(self.centralwidget)
        self.endColorLabel.setObjectName(u"endColorLabel")

        self.colorBar.addWidget(self.endColorLabel)

        self.endColorEdit = QLineEdit(self.centralwidget)
        self.endColorEdit.setObjectName(u"endColorEdit")

        self.colorBar.addWidget(self.endColorEdit)

        self.endColorBtn = QPushButton(self.centralwidget)
        self.endColorBtn.setObjectName(u"endColorBtn")

        self.colorBar.addWidget(self.endColorBtn)


        self.verticalLayout.addLayout(self.colorBar)

        self.gridLayout = QGridLayout()
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(u"gridLayout")
        self.removeBtn = QPushButton(self.centralwidget)
        self.removeBtn.setObjectName(u"removeBtn")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.removeBtn.sizePolicy().hasHeightForWidth())
        self.removeBtn.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.removeBtn, 1, 1, 1, 1)

        self.addBtn = QPushButton(self.centralwidget)
        self.addBtn.setObjectName(u"addBtn")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.addBtn.sizePolicy().hasHeightForWidth())
        self.addBtn.setSizePolicy(sizePolicy2)

        self.gridLayout.addWidget(self.addBtn, 0, 1, 1, 1)

        self.genBtn = QPushButton(self.centralwidget)
        self.genBtn.setObjectName(u"genBtn")
        sizePolicy1.setHeightForWidth(self.genBtn.sizePolicy().hasHeightForWidth())
        self.genBtn.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.genBtn, 2, 1, 1, 1)

        self.moveUpBtn = QPushButton(self.centralwidget)
        self.moveUpBtn.setObjectName(u"moveUpBtn")
        sizePolicy1.setHeightForWidth(self.moveUpBtn.sizePolicy().hasHeightForWidth())
        self.moveUpBtn.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.moveUpBtn, 0, 0, 3, 1)

        self.moveDownBtn = QPushButton(self.centralwidget)
        self.moveDownBtn.setObjectName(u"moveDownBtn")
        sizePolicy1.setHeightForWidth(self.moveDownBtn.sizePolicy().hasHeightForWidth())
        self.moveDownBtn.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.moveDownBtn, 0, 2, 3, 1)


        self.verticalLayout.addLayout(self.gridLayout)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 973, 33))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MO2 Separator Generator (Qt)", None))
        self.editNameLabel.setText(QCoreApplication.translate("MainWindow", u"Category Name:", None))
        self.editSaveBtn.setText(QCoreApplication.translate("MainWindow", u"Save", None))
        self.editCancelBtn.setText(QCoreApplication.translate("MainWindow", u"Cancel", None))
        self.ofLabel.setText(QCoreApplication.translate("MainWindow", u"of", None))
        self.gradientLabel.setText(QCoreApplication.translate("MainWindow", u"Category Separator Gradient:", None))
        self.startColorBtn.setText(QCoreApplication.translate("MainWindow", u"Choose Start Color", None))
        self.endColorBtn.setText(QCoreApplication.translate("MainWindow", u"Choose End Color", None))
        self.removeBtn.setText(QCoreApplication.translate("MainWindow", u"Remove Separator", None))
        self.addBtn.setText(QCoreApplication.translate("MainWindow", u"Add Separator", None))
        self.genBtn.setText(QCoreApplication.translate("MainWindow", u"Generate Files", None))
        self.moveUpBtn.setText(QCoreApplication.translate("MainWindow", u"Move \u2191", None))
        self.moveDownBtn.setText(QCoreApplication.translate("MainWindow", u"Move \u2193", None))
    # retranslateUi

