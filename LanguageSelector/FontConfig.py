# FontConfig.py (c) 2006 Canonical, released under the GPL
#
# This file implements the fontconfig hack
# 
# The problem is that different languages have different needs for
# fontconfig preferences. While it would be really good to have a single
# config file it seems to be not feasible right now for practial purposes
# (see https://wiki.ubuntu.com/DapperL10nSprint for more information)
#
# so this file implements a hack to add prefered languages based on the
# configuration we got from the CJK community

import glob
import os.path

from LocaleInfo import LocaleInfo
import macros
from utils import language2locale

class ExceptionMultipleConfigurations(Exception):
    " error when multiple languages are symlinked "
    pass
class ExceptionUnconfigured(Exception):
    " error if no configuration is set "
    pass
class ExceptionNoConfigForLocale(Exception):
    " error if there is no config for the given locale "
    pass

class FontConfigHack(object):
    """ abstract the fontconfig hack """
    def __init__(self,
                 datadir="/usr/share/language-selector/",
                 globalConfDir="/etc/fonts"):
        self.datadir="%s/fontconfig" % datadir
        self._datadir = datadir
        self.globalConfDir=globalConfDir
        self.li = LocaleInfo("languagelist", datadir)
    def _getLocaleCountryFromFileName(self, name):
        """ 
        internal helper to extracr from our fontconfig filenames
        of the form 69-language-selector-zh-tw.conf the locale
        and country

        returns string of the form locale_COUTNRY (e.g. zh_TW)
        """
        fname = os.path.splitext(os.path.basename(name))[0]
        (head, ll, cc) = fname.rsplit("-", 2)
        return "%s_%s" % (ll, cc.upper())
    def getAvailableConfigs(self):
        """ get the configurations we have as a list of languages
            (returns a list of ['zh_CN','zh_TW'])
        """
        res = []
        pattern = "%s/conf.avail/69-language-selector-*" % self.globalConfDir
        for name in glob.glob(pattern):
            res.append(self._getLocaleCountryFromFileName(name))
        return res
    def getCurrentConfig(self):
        """ returns the current language configuration as a string (e.g. zh_CN)
        
            if the configfile is not a symlink it raises a
             ExceptionNotSymlink exception
            if the file dosn't exists raise a
             ExceptionUnconfigured exception
        """
        pattern = "%s/conf.d/69-language-selector-*" % self.globalConfDir
        current_config = glob.glob(pattern)
        if len(current_config) == 0:
            raise ExceptionUnconfigured()
        if len(current_config) > 1:
            raise ExceptionMultipleConfigurations()
        return self._getLocaleCountryFromFileName(current_config[0])

    def removeConfig(self):
        """ removes the current fontconfig-voodoo configuration
            and do some sanity checking
        """
        pattern = "%s/conf.d/*-language-selector-*" % self.globalConfDir
        for f in glob.glob(pattern):
            if os.path.exists(f):
                os.unlink(f)

    def setConfig(self, locale):
        """ set the configuration for 'locale'. if locale can't be
            found a NoConfigurationForLocale exception it thrown
        """
        macr = macros.LangpackMacros(self._datadir, locale)
        locale = macr["LOCALE"]
        # check if we have a config
        if locale not in self.getAvailableConfigs():
            raise ExceptionNoConfigForLocale()
        # remove old symlink
        self.removeConfig()
        # do the symlinks, link from /etc/fonts/conf.avail in /etc/fonts/conf.d
        basedir = "%s/conf.avail/" % self.globalConfDir
        for pattern in ["*-language-selector-%s-%s.conf" % (macr["LCODE"], macr["CCODE"].lower()),
                        "*-language-selector-%s.conf" % macr["LCODE"],
                       ]:
            for f in glob.glob(os.path.join(basedir,pattern)):
                fname = os.path.basename(f)
                from_link = os.path.join(self.globalConfDir,"conf.avail",fname)
                to_link = os.path.join(self.globalConfDir, "conf.d", fname)
                os.symlink(from_link, to_link)
        return True
        
    def setConfigBasedOnLocale(self):
        """ set the configuration based on the locale in LocaleInfo. If
            no configuration is found the fontconfig config is set to
            'none'
            Can throw a exception
        """
        lang = self.li.getUserDefaultLanguage()[1]
        if len(lang) == 0:
            lang = self.li.getSystemDefaultLanguage()[1]
        locale = language2locale(lang)
        self.setConfig(locale)
        

if __name__ == "__main__":
    fc = FontConfigHack()
    # available
    print "available: ", fc.getAvailableConfigs()

    # current 
    try:
        config = fc.getCurrentConfig()
    except ExceptionUnconfigured:
        print "unconfigured"

    # set config
    print "set config: ", fc.setConfig("zh_CN")
    print "current: ", fc.getCurrentConfig()

    # auto mode
    try:
        print "run auto mode: ", fc.setConfigBasedOnLocale()
    except ExceptionNoConfigForLocale:
        print "no config for this locale"

    # remove
    print "removeConfig()"
    fc.removeConfig()
    try:
        config = fc.getCurrentConfig()
        print "ERROR: have config after calling removeConfig()"
    except ExceptionUnconfigured:
        print "unconfigured (as expected)"
