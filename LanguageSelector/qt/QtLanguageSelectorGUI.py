# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'QtLanguageSelectorGUI.ui'
#
# Created: Tue Jun 21 14:19:40 2011
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_QtLanguageSelectorGUI(object):
    def setupUi(self, QtLanguageSelectorGUI):
        QtLanguageSelectorGUI.setObjectName(_fromUtf8("QtLanguageSelectorGUI"))
        QtLanguageSelectorGUI.resize(557, 407)
        self.verticalLayout = QtGui.QVBoxLayout(QtLanguageSelectorGUI)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.ktabwidget = KTabWidget(QtLanguageSelectorGUI)
        self.ktabwidget.setObjectName(_fromUtf8("ktabwidget"))
        self.InstallTab = QtGui.QWidget()
        self.InstallTab.setObjectName(_fromUtf8("InstallTab"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.InstallTab)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.selectLanguageLabel = QtGui.QLabel(self.InstallTab)
        self.selectLanguageLabel.setWordWrap(False)
        self.selectLanguageLabel.setObjectName(_fromUtf8("selectLanguageLabel"))
        self.verticalLayout_2.addWidget(self.selectLanguageLabel)
        self.listViewLanguagesInst = QtGui.QListWidget(self.InstallTab)
        self.listViewLanguagesInst.setObjectName(_fromUtf8("listViewLanguagesInst"))
        self.verticalLayout_2.addWidget(self.listViewLanguagesInst)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.checkBoxTr = QtGui.QCheckBox(self.InstallTab)
        self.checkBoxTr.setEnabled(False)
        self.checkBoxTr.setObjectName(_fromUtf8("checkBoxTr"))
        self.gridLayout.addWidget(self.checkBoxTr, 1, 0, 1, 1)
        self.checkBoxIm = QtGui.QCheckBox(self.InstallTab)
        self.checkBoxIm.setEnabled(False)
        self.checkBoxIm.setObjectName(_fromUtf8("checkBoxIm"))
        self.gridLayout.addWidget(self.checkBoxIm, 2, 0, 1, 1)
        self.checkBoxSpell = QtGui.QCheckBox(self.InstallTab)
        self.checkBoxSpell.setEnabled(False)
        self.checkBoxSpell.setObjectName(_fromUtf8("checkBoxSpell"))
        self.gridLayout.addWidget(self.checkBoxSpell, 1, 1, 1, 1)
        self.checkBoxFonts = QtGui.QCheckBox(self.InstallTab)
        self.checkBoxFonts.setEnabled(False)
        self.checkBoxFonts.setObjectName(_fromUtf8("checkBoxFonts"))
        self.gridLayout.addWidget(self.checkBoxFonts, 2, 1, 1, 1)
        self.ComponentsLabel = QtGui.QLabel(self.InstallTab)
        self.ComponentsLabel.setObjectName(_fromUtf8("ComponentsLabel"))
        self.gridLayout.addWidget(self.ComponentsLabel, 0, 0, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout)
        self.ktabwidget.addTab(self.InstallTab, _fromUtf8(""))
        self.UninstallTab = QtGui.QWidget()
        self.UninstallTab.setObjectName(_fromUtf8("UninstallTab"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.UninstallTab)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.selectLanguageLabel_2 = QtGui.QLabel(self.UninstallTab)
        self.selectLanguageLabel_2.setWordWrap(False)
        self.selectLanguageLabel_2.setObjectName(_fromUtf8("selectLanguageLabel_2"))
        self.verticalLayout_3.addWidget(self.selectLanguageLabel_2)
        self.listViewLanguagesUninst = QtGui.QListWidget(self.UninstallTab)
        self.listViewLanguagesUninst.setObjectName(_fromUtf8("listViewLanguagesUninst"))
        self.verticalLayout_3.addWidget(self.listViewLanguagesUninst)
        self.ktabwidget.addTab(self.UninstallTab, _fromUtf8(""))
        self.SystemDefaultTab = QtGui.QWidget()
        self.SystemDefaultTab.setObjectName(_fromUtf8("SystemDefaultTab"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.SystemDefaultTab)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.defaultSystemLabel = QtGui.QLabel(self.SystemDefaultTab)
        self.defaultSystemLabel.setWordWrap(False)
        self.defaultSystemLabel.setObjectName(_fromUtf8("defaultSystemLabel"))
        self.verticalLayout_4.addWidget(self.defaultSystemLabel)
        self.listBoxDefaultLanguage = QtGui.QListWidget(self.SystemDefaultTab)
        self.listBoxDefaultLanguage.setObjectName(_fromUtf8("listBoxDefaultLanguage"))
        self.verticalLayout_4.addWidget(self.listBoxDefaultLanguage)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem)
        self.labelInputMethod = QtGui.QLabel(self.SystemDefaultTab)
        self.labelInputMethod.setObjectName(_fromUtf8("labelInputMethod"))
        self.horizontalLayout_4.addWidget(self.labelInputMethod)
        self.comboBoxInputMethod = QtGui.QComboBox(self.SystemDefaultTab)
        self.comboBoxInputMethod.setObjectName(_fromUtf8("comboBoxInputMethod"))
        self.horizontalLayout_4.addWidget(self.comboBoxInputMethod)
        self.verticalLayout_4.addLayout(self.horizontalLayout_4)
        self.ktabwidget.addTab(self.SystemDefaultTab, _fromUtf8(""))
        self.verticalLayout.addWidget(self.ktabwidget)

        self.retranslateUi(QtLanguageSelectorGUI)
        self.ktabwidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(QtLanguageSelectorGUI)

    def retranslateUi(self, QtLanguageSelectorGUI):
        QtLanguageSelectorGUI.setWindowTitle(QtGui.QApplication.translate("QtLanguageSelectorGUI", "Language Installer", None, QtGui.QApplication.UnicodeUTF8))
        self.selectLanguageLabel.setText(QtGui.QApplication.translate("QtLanguageSelectorGUI", "Select language to install:", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxTr.setText(QtGui.QApplication.translate("QtLanguageSelectorGUI", "Translations", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxIm.setText(QtGui.QApplication.translate("QtLanguageSelectorGUI", "Input methods", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxSpell.setText(QtGui.QApplication.translate("QtLanguageSelectorGUI", "Spellchecking and writing aids", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxFonts.setText(QtGui.QApplication.translate("QtLanguageSelectorGUI", "Extra fonts", None, QtGui.QApplication.UnicodeUTF8))
        self.ComponentsLabel.setText(QtGui.QApplication.translate("QtLanguageSelectorGUI", "Components:", None, QtGui.QApplication.UnicodeUTF8))
        self.ktabwidget.setTabText(self.ktabwidget.indexOf(self.InstallTab), QtGui.QApplication.translate("QtLanguageSelectorGUI", "Install", None, QtGui.QApplication.UnicodeUTF8))
        self.selectLanguageLabel_2.setText(QtGui.QApplication.translate("QtLanguageSelectorGUI", "Select language to uninstall:", None, QtGui.QApplication.UnicodeUTF8))
        self.ktabwidget.setTabText(self.ktabwidget.indexOf(self.UninstallTab), QtGui.QApplication.translate("QtLanguageSelectorGUI", "Uninstall", None, QtGui.QApplication.UnicodeUTF8))
        self.defaultSystemLabel.setText(QtGui.QApplication.translate("QtLanguageSelectorGUI", "Default system language:", None, QtGui.QApplication.UnicodeUTF8))
        self.labelInputMethod.setText(QtGui.QApplication.translate("QtLanguageSelectorGUI", "Keyboard input method:", None, QtGui.QApplication.UnicodeUTF8))
        self.ktabwidget.setTabText(self.ktabwidget.indexOf(self.SystemDefaultTab), QtGui.QApplication.translate("QtLanguageSelectorGUI", "Set System Language", None, QtGui.QApplication.UnicodeUTF8))

from PyKDE4.kdeui import KTabWidget
