#!/usr/bin/env python

from setuptools import setup
from DistUtilsExtra.command import (build_extra, build_i18n, build_help,
                                    build_icons)
import os
import sys

PREFIX='/usr/local'
ROOT='/'

if sys.argv[1] == "build":
    assert(os.system("cd LanguageSelector/qt; make") == 0)
elif sys.argv[1] == "install":
    for arg in sys.argv[2:]:
        if "--prefix" in arg:
            PREFIX=arg.split("=")[1]
        if "--root" in arg:
            ROOT=arg.split("=")[1]

setup(name='language-selector',
      version='0.1',
      py_modules = ['language_support_pkgs'],
      packages=['LanguageSelector',
                'LanguageSelector.gtk',
                'LanguageSelector.qt'],
      scripts=['gnome-language-selector',
               'check-language-support',
               'fontconfig-voodoo'],
      data_files=[('share/language-selector/data',
                   ["data/language-selector.png",
                    "data/languagelist",
                    "data/langcode2locale",
                    "data/locale2langpack",
                    "data/pkg_depends",
                    "data/variants",
                    "data/im-switch.blacklist",
                    "data/LanguageSelector.ui"]),
                  # kcm stuff
                  ('share/kde4/apps/language-selector',
                   ['kde-language-selector']),
                  # dbus stuff
                  ('share/dbus-1/system-services',
                   ['dbus_backend/com.ubuntu.LanguageSelector.service']),
                  ('../etc/dbus-1/system.d/',
                   ["dbus_backend/com.ubuntu.LanguageSelector.conf"]),
                  ('lib/language-selector/',
                   ["dbus_backend/ls-dbus-backend"]),
                  # help
                  ('share/gnome/help/language-selector/C',
                   ['help/C/language-selector.xml']),
                  # pretty pictures
                  ('share/pixmaps',
                   ["data/language-selector.png"]),
                  ],
      entry_points='''[aptdaemon.plugins]
modify_cache_after=language_support_pkgs:apt_cache_add_language_packs
[packagekit.apt.plugins]
what_provides=language_support_pkgs:packagekit_what_provides_locale
''',
      cmdclass={"build": build_extra.build_extra,
                "build_i18n": build_i18n.build_i18n,
                "build_help": build_help.build_help,
                "build_icons": build_icons.build_icons,
                },

      )
if sys.argv[1] == "install":
    os.rename(ROOT+"/"+PREFIX+"/share/kde4/services/kde-language-selector.desktop", ROOT+"/"+PREFIX+"/share/kde4/services/language-selector.desktop")
    os.rename(ROOT+"/"+PREFIX+"/share/kde4/apps/language-selector/kde-language-selector", ROOT+"/"+PREFIX+"/share/kde4/apps/language-selector/language-selector.py")
