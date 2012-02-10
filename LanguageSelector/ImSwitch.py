# ImSwitch.py (c) 2006 Canonical, released under the GPL
#
# This file implements a interface to im-switch
#

import os
import sys
import subprocess

class ImSwitch(object):
    
    # some global data
    global_confdir = "/etc/X11/xinit/xinput.d/"
    local_confdir = os.path.expanduser("~/.xinput.d/")
    bin = "/usr/bin/im-switch"
    default_method = "ibus"
    blacklist_file = "/usr/share/language-selector/data/im-switch.blacklist"

    def __init__(self):
        pass

    def available(self):
        " return True if im-switch is available at all "
        return os.path.exists(self.bin)

    def removeDanglingSymlinks(self):
        for dir in (self.local_confdir, self.global_confdir):
            if os.path.exists(dir):
                for dentry in os.listdir(dir):
                    if not os.path.exists("%s/%s" % (dir, dentry)):
                        os.unlink("%s/%s" % (dir, dentry))
    
    def enabledForLocale(self, locale):
        " check if we have a config for this specifc locale (e.g. ja_JP) "
        for dir in (self.local_confdir, self.global_confdir):
            for name in (locale, "all_ALL"):
                target = os.path.join(dir,name)
                #print "checking im-switch config: ", target, os.path.basename(os.path.realpath(target))
                if os.path.exists(target):
                    im_name = os.path.basename(os.path.realpath(target))
                    if im_name in ("none", "default"):
                        #print "points to none or default"
                        return False
                    #print "points to real config"
                    return True
        return False

    def enable(self, locale):
        " enable input methods for locale"
        # try auto first
        subprocess.call(["im-switch","-z",locale,"-a"])
        # if no config is set, force the default
        if not self.enabledForLocale(locale):
            subprocess.call(["im-switch","-z",locale,
                             "-s", self.default_method])

    def disable(self, locale):
        " disable input method for locale "
        # remove local config first
        if os.path.exists(os.path.join(self.local_confdir, locale)):
            os.unlink(os.path.join(self.local_confdir, locale))
        # see if we still have a input method and if so, force "none"
        if self.enabledForLocale(locale):
            subprocess.call(["im-switch","-z",locale,"-s","none"])

    def getInputMethodForLocale(self, locale):
        for dir in (self.local_confdir, self.global_confdir):
            if os.path.exists(dir):
                for name in (locale, "all_ALL"):
                    target = os.path.join(dir,name)
                    if os.path.exists(target):
                        return os.path.basename(os.path.realpath(target))
        return None
        
    def setInputMethodForLocale(self, im, locale):
        if not os.path.exists(self.local_confdir):
            os.mkdir(self.local_confdir)
        subprocess.call(["im-switch","-z",locale,"-s",im])
    
    def getAvailableInputMethods(self):
        """ return the input methods available via im-switch """
        # load blacklist
        blacklist = []
        for l in open(self.blacklist_file):
            l = l.strip()
            if l and not l.startswith('#'):
                blacklist.append(l)
        # now get available methods 
        inputMethods = []
        for dentry in os.listdir(self.global_confdir):
            if (not os.path.islink(self.global_confdir+dentry) and 
                not dentry in blacklist):
                inputMethods.append(dentry)
        return ['none']+sorted(inputMethods)

    def setDefaultInputMethod(self, method, locale="all_ALL"):
        """ sets the default input method for the given locale
            (in ll_CC form)
        """
        l = self.confdir+locale
        if os.path.islink(l):
            os.unlink(l)
        os.symlink(self.confdir+method, l)
        return True

    def resetDefaultInputMethod(self, locale="all_ALL"):
        """ reset the default input method to auto (controlled by
            im-switch
        """
        d = "/etc/alternatives/xinput-%s" % locale
        l = self.confdir+locale
        if os.path.islink(l):
            os.unlink(l)
        os.symlink(d, self.confdir+locale)
        return True
        
    def getCurrentInputMethod(self, locale="all_ALL"):
        """ get the current default input method for the selected
            locale (in ll_CC form)
        """
        return os.path.basename(os.path.realpath(self.local_confdir+locale))
        
if __name__ == "__main__":
    im = ImSwitch()
#    print im.getInputMethodForLocale("ja_JP")
#    print im.enabledForLocale("all_ALL")
    print "available input methods: "
    print im.getAvailableInputMethods()
    print "current method: ",
    print im.getCurrentInputMethod()
    sys.exit(1)
    print "switching to 'th-xim': ",
    print im.setDefaultInputMethod("th-xim")
    print "current method: ",
    print im.getCurrentInputMethod()
    print "reset default: ",
    print im.resetDefaultInputMethod()
    print "current method: ",
    print im.getCurrentInputMethod()
