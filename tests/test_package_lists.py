#!/usr/bin/python

import unittest
import sys
import apt
import apt_pkg
sys.path.insert(0, "../")

from LanguageSelector.LanguageSelector import LanguageSelectorBase

class TestLanguageSelector(unittest.TestCase):

    def test_package_lists_good(self):
        " test for non networked sources "
        apt_pkg.Config.set("Dir::State::lists","./test-data/var/lib/apt/lists")
        apt_pkg.Config.set("Dir::State::status","./test-data/empty")
        apt_pkg.Config.set("Dir::Etc::SourceList","./test-data/etc/apt/sources.list.good")
        apt_pkg.Config.set("Dir::Etc::SourceParts","./xxx")
        ls = LanguageSelectorBase(datadir="../")
        ls.openCache(apt.progress.OpProgress())
        self.assert_(ls._cache.havePackageLists == True,
                      "verifyPackageLists returned False for a good list")

    def test_package_lists_fail(self):
        " test for non networked sources "
        apt_pkg.Config.set("Dir::State::lists","./test-data/var/lib/apt/lists")
        apt_pkg.Config.set("Dir::State::status","./test-data/empty")
        apt_pkg.Config.set("Dir::Etc::SourceList","./test-data/etc/apt/sources.list.fail")
        ls = LanguageSelectorBase(datadir="../")
        ls.openCache(apt.progress.OpProgress())
        self.assert_(ls._cache.havePackageLists == False,
                      "verifyPackageLists returned True for a list with missing indexfiles")
        


if __name__ == "__main__":
    apt_pkg.Config.set("Apt::Architecture","i386")
    unittest.main()
