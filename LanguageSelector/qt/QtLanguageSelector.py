# -*- coding: utf-8 -*-
#
# © 2005 Canonical Ltd
# © 2009 Harald Sitter
# © 2011 Romain Perier
# Author: Michael Vogt <michael.vogt@ubuntu.com>
# Author: Jonathan Riddell <jriddell@ubuntu.com>
# Author: Harald Sitter <apachelogger@ubuntu.com>
# Author: Romain Perier <romain.perier@gmail.com>
#
# Released under the GNU GPL version 2 or later
#

import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyKDE4.kdecore import ki18n, KAboutData, KCmdLineArgs, KCmdLineOptions
from PyKDE4.kdeui import KApplication, KIcon,  KMessageBox, KGuiItem, KCModule

from LanguageSelector.LanguageSelector import *
from LanguageSelector.ImSwitch import ImSwitch
from QtLanguageSelectorGUI import Ui_QtLanguageSelectorGUI
from LanguageSelector.LangCache import ExceptionPkgCacheBroken
from gettext import gettext as i18n

def utf8(str):
  if isinstance(str, unicode):
      return str
  return unicode(str, 'UTF-8')

def _(string):
    return utf8(i18n(string))

class QtLanguageSelector(KCModule, LanguageSelectorBase):
    """ actual implementation of the qt GUI """

    def __init__(self, datadir, component_data=None, parent=None):
        LanguageSelectorBase.__init__(self, datadir)
        KCModule.__init__(self, component_data, parent)
        
        self.parentApp = KApplication.kApplication()
        self.ui = Ui_QtLanguageSelectorGUI()
        self.ui.setupUi(self)
        self.about = MakeAboutData()
        self.setAboutData(self.about)
        
        self.setWindowIcon(KIcon("preferences-desktop-locale"))
        
        self.imSwitch = ImSwitch()
        # remove dangling ImSwitch symlinks if present
        self.imSwitch.removeDanglingSymlinks()
        self.init()

        # connect the signals
        self.connect(self.ui.listViewLanguagesInst, SIGNAL("itemSelectionChanged()"), self.checkInstallableComponents)
        self.connect(self.ui.listViewLanguagesUninst, SIGNAL("itemSelectionChanged()"), self.onChanged)
        self.connect(self.ui.ktabwidget, SIGNAL("currentChanged(int)"), self.onTabChangeRevertApply)
        self.connect(self.ui.listBoxDefaultLanguage, SIGNAL("itemSelectionChanged()"), self.checkInputMethods)
        self.connect(self.ui.checkBoxTr, SIGNAL("stateChanged(int)"), self.onChanged)
        self.connect(self.ui.checkBoxIm, SIGNAL("stateChanged(int)"), self.onChanged)
        self.connect(self.ui.checkBoxSpell, SIGNAL("stateChanged(int)"), self.onChanged)
        self.connect(self.ui.checkBoxFonts, SIGNAL("stateChanged(int)"), self.onChanged)

    def init(self):
        self.translateUI()
        try:
            self.openCache(apt.progress.OpProgress())
        except ExceptionPkgCacheBroken:
            s = _("Software database is broken")
            t = _("It is impossible to install or remove any software. "
                  "Please use the package manager \"Adept\" or run "
                  "\"sudo apt-get install -f\" in a terminal to fix "
                  "this issue at first.")
            KMessageBox.error(self, t, s)
            sys.exit(1)
        self.updateLanguagesList()
        self.updateSystemDefaultListbox()

        if not self._cache.havePackageLists:
            yesText = _("_Update").replace("_", "&")
            noText = _("_Remind Me Later").replace("_", "&")
            yes = KGuiItem(yesText, "dialog-ok")
            no = KGuiItem(noText, "process-stop")
            text = "<big><b>%s</b></big>\n\n%s" % (
              _("No language information available"),
              _("The system does not have information about the "
                "available languages yet. Do you want to perform "
                "a network update to get them now? "))
            text = text.replace("\n", "<br />")
            res = KMessageBox.questionYesNo(self, text, "", yes, no)
            if res == KMessageBox.Yes:
                self.setEnabled(False)
                self.update()
                self.openCache(apt.progress.OpProgress())
                self.updateLanguagesList()
                self.setEnabled(True)

    def load(self):
      # See if something is missing
      self.verifyInstalledLangPacks()

    def save(self):
        idx = self.ui.ktabwidget.currentIndex()

        if idx == 0:
            self.pkgChanges("install")
        elif idx == 1:
            self.pkgChanges("uninstall")
        else:
            self.onSystemLanguageApply()

    def translateUI(self):
        """ translate the strings in the UI, needed because Qt designer doesn't use gettext """
        self.ui.ktabwidget.setTabText(self.ui.ktabwidget.indexOf(self.ui.SystemDefaultTab), _("Set System Language"))
        self.ui.defaultSystemLabel.setText(_("Default system language:"))
        self.ui.labelInputMethod.setText(_("Keyboard input method:"))
        self.ui.selectLanguageLabel.setText(_("Select language to install:"))
        self.ui.selectLanguageLabel_2.setText(_("Select language to uninstall:"))
        self.ui.checkBoxTr.setText(_("Translations"))
        self.ui.checkBoxIm.setText(_("Input methods"))
        self.ui.checkBoxSpell.setText(_("Spellchecking and writing aids"))
        self.ui.checkBoxFonts.setText(_("Extra fonts"))
        self.ui.ComponentsLabel.setText(_("Components:"))
         
    def updateSystemDefaultListbox(self):
        self.ui.listBoxDefaultLanguage.clear()
        self._localeinfo.localeToCodeMap = {}
        # get the current default lang
        defaultLangName = None
        defaultLangCode = self._localeinfo.getSystemDefaultLanguage()[0]
        if defaultLangCode:
            defaultLangName = utf8(self._localeinfo.translate(defaultLangCode, native=True))
        locales = []
        for locale in self._localeinfo.generated_locales():
            name = utf8(self._localeinfo.translate(locale, native=True))
            locales.append(name)
            self._localeinfo.localeToCodeMap[name] = locale
        locales.sort()
        for localeName in locales:
            item = QListWidgetItem(utf8(localeName), self.ui.listBoxDefaultLanguage)
            if defaultLangName == localeName:
                item.setSelected(True)
        if (not os.path.exists("/etc/alternatives/xinput-all_ALL") or
            not os.path.exists("/usr/bin/im-switch")):
            self.ui.comboBoxInputMethod.setEnabled(False)

    def verifyInstalledLangPacks(self):
        """ called at the start to inform about possible missing
            langpacks (e.g. gnome/kde langpack transition)
        """
        print "verifyInstalledLangPacks"
        missing = self.getMissingLangPacks()

        print "Missing: %s " % missing
        if len(missing) > 0:
            # FIXME: add "details"
            yesText = _("_Install").replace("_", "&")
            noText = _("_Remind Me Later").replace("_", "&")
            yes = KGuiItem(yesText, "dialog-ok")
            no = KGuiItem(noText, "process-stop")
            text = "<big><b>%s</b></big>\n\n%s" % (
                _("The language support is not installed completely"),
                _("Some translations or writing aids available for your "
                  "chosen languages are not installed yet. Do you want "
                  "to install them now?"))
            text = text.replace("\n", "<br />")
            res = KMessageBox.questionYesNo(self, text, "", yes, no)
            if res == KMessageBox.Yes:
                self.setEnabled(False)
                self.commit(missing, [])
                self.updateLanguagesList()
                self.setEnabled(True)

    def update(self):
        self.run_pkg_manager_update()

    def commit(self, inst, rm):
        # unlock here to make sure that lock/unlock are always run
        # pair-wise (and don't explode on errors)
        if len(inst) == 0 and len(rm) == 0:
            return
        self.run_pkg_manager(inst,rm)

    def updateLanguagesList(self):
        self.ui.listViewLanguagesInst.clear()
        self.ui.listViewLanguagesUninst.clear()
        # get the language names and sort them alphabetically
        languageList = self._cache.getLanguageInformation()
        self._localeinfo.listviewStrToLangInfoMap = {}
        for lang in languageList:
            self._localeinfo.listviewStrToLangInfoMap[utf8(self._localeinfo.translate(lang.languageCode))] = lang
        languages = self._localeinfo.listviewStrToLangInfoMap.keys()
        languages.sort()

        for langName in languages:
            lang = self._localeinfo.listviewStrToLangInfoMap[langName]
            elmIn = QListWidgetItem(utf8(self._localeinfo.translate(lang.languageCode)), self.ui.listViewLanguagesInst)
            elmUn = QListWidgetItem(utf8(self._localeinfo.translate(lang.languageCode)), self.ui.listViewLanguagesUninst)
            
            if lang.fullInstalled:
                elmIn.setFlags(Qt.ItemIsDropEnabled)  #not sure how to unset all flags, but this disables the item
                elmIn.setToolTip(_("Already installed"))
                elmUn.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            elif lang.inconsistent:
                elmIn.setToolTip(_("Partially Installed"))
            else:
                elmUn.setFlags(Qt.ItemIsDropEnabled)  #not sure how to unset all flags, but this disables the item
                elmUn.setToolTip(_("Not installed"))
                elmUn.setHidden(True)
                elmIn.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)

    def onChanged(self, state = 1):
        if state:
            self.changed()
        else:
            for button in [ "checkBoxTr", "checkBoxIm", "checkBoxSpell", "checkBoxFonts" ]:
                if getattr(self.ui, button).isEnabled() and getattr(self.ui, button).isChecked():
                    return
            self.emit(SIGNAL("changed(bool)"), False)

    def onTabChangeRevertApply(self):
        for listView in [ "listViewLanguagesInst", "listViewLanguagesUninst", "listBoxDefaultLanguage" ]:
          getattr(self.ui, listView).clearSelection()
        for button in [ "checkBoxTr", "checkBoxIm", "checkBoxSpell", "checkBoxFonts" ]:
          getattr(self.ui, button).setChecked(False)
          getattr(self.ui, button).setEnabled(False)
        self.emit(SIGNAL("changed(bool)"), False)

    def checkInstallableComponents(self):
        """ check available components for the selected language
            and set/unset the corresponding checkbutton accordingly
        """
        items = self.ui.listViewLanguagesInst.selectedItems()

        if len(items) == 1:
            li = self._localeinfo.listviewStrToLangInfoMap[unicode(items[0].text())]
            langPkg = li.languagePkgList["languagePack"]
            self.ui.checkBoxTr.setEnabled(langPkg.available)
            self.ui.checkBoxTr.setChecked(False)
            if langPkg.installed:
                self.ui.checkBoxTr.setChecked(True)
                self.ui.checkBoxTr.setEnabled(False)
                self.ui.checkBoxTr.setToolTip(_("Component already installed"))
            elif not langPkg.available:
                self.ui.checkBoxTr.setToolTip(_("Component not available"))
            else:
                self.ui.checkBoxTr.setToolTip(_("Component not installed"))
        
    def checkInputMethods(self):
        """ check if the selected language has input method support
            and set checkbutton_enable_input_methods accordingly
        """
        if (not self.imSwitch.available()) or (not self.getSystemLanguage()):
            return
        self.changed()
        (lang, code) = self.getSystemLanguage()

        combo = self.ui.comboBoxInputMethod
        combo.clear()

        currentIM = self.imSwitch.getInputMethodForLocale(code)
        if currentIM == None:
            currentIM = 'none'

        for (i, IM) in enumerate(self.imSwitch.getAvailableInputMethods()):
            combo.insertItem(i,IM)
            if IM == currentIM:
                combo.setCurrentIndex(i)

    def run_pkg_manager_update(self):
        self.returncode = 0
        self.returncode = subprocess.call(["qapt-batch", "--attach", str(self.winId()), "--update"])

    def run_pkg_manager(self, to_inst, to_rm):
        self.returncode = 0
        if len(to_inst) > 0:
            print str(["qapt-batch","--install"]+to_inst)
            self.returncode = subprocess.call(["qapt-batch", "--attach", str(self.winId()), "--install"]+to_inst)
        # then remove
        if len(to_rm) > 0:
            print str(["qapt-batch","--uninstall"]+to_rm)
            self.returncode = subprocess.call(["qapt-batch", "--attach", str(self.winId()), "--uninstall"]+to_rm)

    def onSystemLanguageApply(self):
        (lang, code) = self.getSystemLanguage()
        self.writeSysLanguageSetting(code)
        self.writeSysLangSetting(code)
        self.updateInputMethods(code)
        KMessageBox.information(self, _("Default system Language now set to %s.") % lang, _("Language Set"))

    def updateInputMethods(self,code):
        IM_choice = self.ui.comboBoxInputMethod.currentText()
        self.imSwitch.setInputMethodForLocale(IM_choice, code)

    def getSystemLanguage(self):
        """ returns tuple of (lang, code) strings """
        items = self.ui.listBoxDefaultLanguage.selectedItems()
        if len(items) == 1:
            item = items[0]
            lang = item.text()
            new_locale = ("%s"%lang)
            try:
                code = self._localeinfo.localeToCodeMap[new_locale]
                return (lang, code)
            except KeyError:
                print "ERROR: can not find new_locale: '%s'"%new_locale
      
    def pkgChanges(self, mode):

        if mode == "install":
            items = self.ui.listViewLanguagesInst.selectedItems()
        else:
            items = self.ui.listViewLanguagesUninst.selectedItems()
            
        if len(items) == 1:
            elm = items[0]
            li = self._localeinfo.listviewStrToLangInfoMap[unicode(elm.text())]
            langPkg = li.languagePkgList["languagePack"]
            if langPkg.available:
                if (mode == "install") and (not langPkg.installed):
                    langPkg.doChange = self.ui.checkBoxTr.isChecked()
                elif (mode == "uninstall") and langPkg.installed:
                    langPkg.doChange = True
            try:
                self._cache.tryChangeDetails(li)
                for langPkg in li.languagePkgList.values():
                  langPkg.doChange = False
            except ExceptionPkgCacheBroken:
                s = _("Software database is broken")
                t = _("It is impossible to install or remove any software. "
                      "Please use the package manager \"Adept\" or run "
                      "\"sudo apt-get install -f\" in a terminal to fix "
                      "this issue at first.")
                KMessageBox.error(self, t, s)
                sys.exit(1)

        (to_inst, to_rm) = self._cache.getChangesList()
        if len(to_inst) == len(to_rm) == 0:
            return
        # first install
        self.setCursor(Qt.WaitCursor)
        self.setEnabled(False)
        self.run_pkg_manager(to_inst,to_rm)
        self.setCursor(Qt.ArrowCursor)
        self.setEnabled(True)
        
#        kdmscript = "/etc/init.d/kdm"
#        if os.path.exists("/var/run/kdm.pid") and os.path.exists(kdmscript):
#            subprocess.call(["invoke-rc.d","kdm","reload"])

        #self.run_pkg_manager(to_inst, to_rm)

        if self.returncode == 0:
            if (mode == "install"):
                KMessageBox.information( self, _("All selected components have now been installed for %s.  Select them from Country/Region & Language.") % unicode(items[0].text()), _("Language Installed") )
            elif (mode == "uninstall"):
                KMessageBox.information( self, _("Translations and support have now been uninstalled for %s.") % unicode(items[0].text()), _("Language Uninstalled") )
            # Resync the cache to match packageManager changes, then update views
            self._cache.open(None)
            self.updateLanguagesList()
            self.updateSystemDefaultListbox()
            if mode == "install":
                self.checkInstallableComponents()
        else:
            KMessageBox.sorry(self, _("Failed to set system language."), _("Language Not Set"))
            self._cache.clear() # undo all selections
            
def MakeAboutData():
  appName     = "language-selector"
  catalog     = ""
  programName = ki18n ("Language Selector")
  version     = "0.3.4"
  description = ki18n ("Language Selector")
  license     = KAboutData.License_GPL
  copyright   = ki18n ("(c) 2008 Canonical Ltd")
  text        = ki18n ("none")
  homePage    = "https://launchpad.net/language-selector"
  bugEmail    = ""

  aboutData   = KAboutData (appName, catalog, programName, version, description, license, copyright, text, homePage, bugEmail)
  aboutData.addAuthor(ki18n("Michael Vogt"), ki18n("Developer"))
  aboutData.addAuthor(ki18n("Jonathan Riddell"), ki18n("Developer"))
  aboutData.addAuthor(ki18n("Harald Sitter"), ki18n("Developer"))
  aboutData.addAuthor(ki18n("Romain Perier"), ki18n("Developer"))
  
  return aboutData

if __name__ == "__main__":

    appName     = "language-selector"
    catalog     = ""
    programName = ki18n ("Language Selector")
    version     = "0.3.4"
    description = ki18n ("Language Selector")
    license     = KAboutData.License_GPL
    copyright   = ki18n ("(c) 2008 Canonical Ltd")
    text        = ki18n ("none")
    homePage    = "https://launchpad.net/language-selector"
    bugEmail    = ""

    aboutData	= KAboutData (appName, catalog, programName, version, description, license, copyright, text, homePage, bugEmail)

    aboutData.addAuthor(ki18n("Rob Bean"), ki18n("PyQt4 to PyKDE4 port"))
    aboutData.addAuthor(ki18n("Harald Sitter"), ki18n("Developer"))

    options = KCmdLineOptions()
    options.add("!mode ", ki18n("REQUIRED: install, uninstall or select must follow"),  "select")
    options.add("+[install]", ki18n("install a language"))
    options.add("+[uninstall]", ki18n("uninstall a language"))
    options.add("+[select]", ki18n("select a language"))

    KCmdLineArgs.init (sys.argv, aboutData)
    KCmdLineArgs.addCmdLineOptions(options)

    gettext.bindtextdomain("language-selector", "/usr/share/locale")
    gettext.textdomain("language-selector")

    app = KApplication()

    args = KCmdLineArgs.parsedArgs()

    if args.isSet("mode"):
        whattodo = args.getOption("mode")
        if whattodo in ["install", "uninstall", "select"]:
            pass
        else:
            print whattodo, "is not a valid argument"
            args.usage()
    else:
        print "Please review the usage."
        args.usage()

    if os.getuid() != 0:
        KMessageBox.sorry(None, _("Please run this software with administrative rights."),  _("Not Root User"))
        sys.exit(1)

    lc = QtLanguageSelector("/usr/share/language-selector/")

    lc.show()

    app.exec_()

# kate: space-indent on; indent-width 4; mixedindent off; indent-mode python;
