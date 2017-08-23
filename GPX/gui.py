# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(381, 495)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.grpOutput = QtGui.QGroupBox(self.centralwidget)
        self.grpOutput.setObjectName(_fromUtf8("grpOutput"))
        self.formLayout_2 = QtGui.QFormLayout(self.grpOutput)
        self.formLayout_2.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_2.setObjectName(_fromUtf8("formLayout_2"))
        self.label_5 = QtGui.QLabel(self.grpOutput)
        self.label_5.setScaledContents(False)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_5)
        self.txtOutputDir = QtGui.QLineEdit(self.grpOutput)
        self.txtOutputDir.setObjectName(_fromUtf8("txtOutputDir"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.FieldRole, self.txtOutputDir)
        self.label_3 = QtGui.QLabel(self.grpOutput)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_3)
        self.txtOutputFile = QtGui.QLineEdit(self.grpOutput)
        self.txtOutputFile.setText(_fromUtf8(""))
        self.txtOutputFile.setObjectName(_fromUtf8("txtOutputFile"))
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.FieldRole, self.txtOutputFile)
        self.prgbarAvancement = QtGui.QProgressBar(self.grpOutput)
        self.prgbarAvancement.setProperty("value", 0)
        self.prgbarAvancement.setTextVisible(False)
        self.prgbarAvancement.setObjectName(_fromUtf8("prgbarAvancement"))
        self.formLayout_2.setWidget(2, QtGui.QFormLayout.SpanningRole, self.prgbarAvancement)
        self.txtOutputPy = QtGui.QTextBrowser(self.grpOutput)
        self.txtOutputPy.setLineWrapMode(QtGui.QTextEdit.NoWrap)
        self.txtOutputPy.setObjectName(_fromUtf8("txtOutputPy"))
        self.formLayout_2.setWidget(3, QtGui.QFormLayout.SpanningRole, self.txtOutputPy)
        self.gridLayout.addWidget(self.grpOutput, 2, 0, 1, 3)
        self.btnCheck = QtGui.QPushButton(self.centralwidget)
        self.btnCheck.setObjectName(_fromUtf8("btnCheck"))
        self.gridLayout.addWidget(self.btnCheck, 3, 0, 1, 1)
        self.btnGo = QtGui.QPushButton(self.centralwidget)
        self.btnGo.setObjectName(_fromUtf8("btnGo"))
        self.gridLayout.addWidget(self.btnGo, 3, 1, 1, 1)
        self.btnEnregistrer = QtGui.QPushButton(self.centralwidget)
        self.btnEnregistrer.setObjectName(_fromUtf8("btnEnregistrer"))
        self.gridLayout.addWidget(self.btnEnregistrer, 3, 2, 1, 1)
        self.grpInput = QtGui.QGroupBox(self.centralwidget)
        self.grpInput.setObjectName(_fromUtf8("grpInput"))
        self.gridLayout_2 = QtGui.QGridLayout(self.grpInput)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.lblInputDir = QtGui.QLabel(self.grpInput)
        self.lblInputDir.setScaledContents(False)
        self.lblInputDir.setObjectName(_fromUtf8("lblInputDir"))
        self.gridLayout_2.addWidget(self.lblInputDir, 0, 0, 1, 1)
        self.txtInputDir = QtGui.QLineEdit(self.grpInput)
        self.txtInputDir.setObjectName(_fromUtf8("txtInputDir"))
        self.gridLayout_2.addWidget(self.txtInputDir, 0, 1, 1, 1)
        self.label = QtGui.QLabel(self.grpInput)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout_2.addWidget(self.label, 1, 0, 1, 1)
        self.dateFrom = QtGui.QDateEdit(self.grpInput)
        self.dateFrom.setDate(QtCore.QDate(2016, 9, 14))
        self.dateFrom.setMaximumDateTime(QtCore.QDateTime(QtCore.QDate(2020, 12, 31), QtCore.QTime(23, 59, 59)))
        self.dateFrom.setMinimumDateTime(QtCore.QDateTime(QtCore.QDate(2016, 8, 1), QtCore.QTime(0, 0, 0)))
        self.dateFrom.setObjectName(_fromUtf8("dateFrom"))
        self.gridLayout_2.addWidget(self.dateFrom, 1, 1, 1, 1)
        self.label_2 = QtGui.QLabel(self.grpInput)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout_2.addWidget(self.label_2, 2, 0, 1, 1)
        self.dateTo = QtGui.QDateEdit(self.grpInput)
        self.dateTo.setDateTime(QtCore.QDateTime(QtCore.QDate(2020, 12, 31), QtCore.QTime(23, 59, 59)))
        self.dateTo.setDate(QtCore.QDate(2020, 12, 31))
        self.dateTo.setMaximumDateTime(QtCore.QDateTime(QtCore.QDate(2020, 12, 31), QtCore.QTime(23, 59, 59)))
        self.dateTo.setMinimumDateTime(QtCore.QDateTime(QtCore.QDate(2016, 8, 1), QtCore.QTime(0, 0, 0)))
        self.dateTo.setObjectName(_fromUtf8("dateTo"))
        self.gridLayout_2.addWidget(self.dateTo, 2, 1, 1, 1)
        self.chkLocation = QtGui.QCheckBox(self.grpInput)
        self.chkLocation.setChecked(True)
        self.chkLocation.setObjectName(_fromUtf8("chkLocation"))
        self.gridLayout_2.addWidget(self.chkLocation, 3, 0, 1, 1)
        self.chkEquipments = QtGui.QCheckBox(self.grpInput)
        self.chkEquipments.setChecked(True)
        self.chkEquipments.setObjectName(_fromUtf8("chkEquipments"))
        self.gridLayout_2.addWidget(self.chkEquipments, 3, 1, 1, 1)
        self.gridLayout.addWidget(self.grpInput, 0, 0, 1, 3)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 381, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.grpOutput.setTitle(_translate("MainWindow", "Sortie", None))
        self.label_5.setText(_translate("MainWindow", "Répertoire de sortie", None))
        self.txtOutputDir.setText(_translate("MainWindow", "D:\\Users\\Papa\\Documents\\Courses\\python\\GPX", None))
        self.label_3.setText(_translate("MainWindow", "Fichier", None))
        self.btnCheck.setText(_translate("MainWindow", "Chercher les *.sml", None))
        self.btnGo.setText(_translate("MainWindow", "Go !", None))
        self.btnEnregistrer.setText(_translate("MainWindow", "Enregistrer le fitlog", None))
        self.grpInput.setTitle(_translate("MainWindow", "Entrée", None))
        self.lblInputDir.setText(_translate("MainWindow", "Répertoire d\'origine", None))
        self.txtInputDir.setText(_translate("MainWindow", "C:\\Users\\Papa\\AppData\\Roaming\\Suunto\\Moveslink2", None))
        self.label.setText(_translate("MainWindow", "Après le", None))
        self.label_2.setText(_translate("MainWindow", "Avant le", None))
        self.chkLocation.setText(_translate("MainWindow", "Cherche la localisation", None))
        self.chkEquipments.setText(_translate("MainWindow", "Cherche les équipements", None))

