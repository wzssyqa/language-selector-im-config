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
    local_conffile = os.path.expanduser("~/.xinputrc")
    bin = "/usr/bin/im-config"
    default_method = "ibus"
    blacklist_file = "/usr/share/language-selector/data/im-config.blacklist"

    def __init__(self):
        pass

    def available(self):
        " return True if im-config is available at all "
        return os.path.exists(self.bin)

    def removeDanglingSymlinks(self):
        if os.path.exists(self.local_conffile):
        	os.unlink(self.local_conffile)
        return True
    
    def enabledForLocale(self, locale):
        " check if we have a config for this specifc locale (e.g. ja_JP) "
        if os.path.exists(self.local_conffile):
        	os.unlink(self.local_conffile)
        return True

    def enable(self, locale):
        " enable input methods for locale"
        if os.path.exists(self.local_conffile):
        	os.unlink(self.local_conffile)
        return True

    def disable(self, locale):
        " disable input method for locale "
        f=open(self.local_conffile,'w')
        f.write('# Generate by Language-Selector, See im-config(8) for more information.\n')

    def getInputMethodForLocale(self, locale):
        """ im-config doesn't support it. """
        if os.path.exists(self.local_conffile):
        	progress=os.popen("grep 'run_im' ~/.xinputrc | awk -F ' ' '{print $2}'")
        	return progress.read().rstrip()
        else:
        	return os.path.basename(os.path.realpath(self.global_confdir+locale))
        return None
        
    def setInputMethodForLocale(self, im, locale):
        """ im-config doesn't support it. """
        f=open(self.local_conffile,'w')
        f.write('# Generate by Language-Selector, See im-config(8) for more information.\n')
        f.write('run_im '+im+'\n')
        return True
    
    def getAvailableInputMethods(self):
        """ return the input methods available via im-config """
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
        """ sets the default input method, the locale is deprecated
        """
        f=open(self.local_conffile,'w')
        f.write('# Generate by Language-Selector, See im-config(8) for more information.\n')
        f.write('run_im '+method+'\n')

    def resetDefaultInputMethod(self, locale="all_ALL"):
        """ reset the default input method to auto (controlled by
            im-config
        """
        if os.path.exists(self.local_conffile):
        	os.unlink(self.local_conffile)
        return True
        
    def getCurrentInputMethod(self, locale="all_ALL"):
        """ get the current default input method for the selected
            locale (in ll_CC form)
        """
        if os.path.exists(self.local_conffile):
        	progress=os.popen("grep 'run_im' ~/.xinputrc | awk -F ' ' '{print $2}'")
        	return progress.read().rstrip()
        else:
        	return os.path.basename(os.path.realpath(self.global_confdir+locale))
        
if __name__ == "__main__":
    im = ImSwitch()
#    print im.getInputMethodForLocale("ja_JP")
#    print im.enabledForLocale("all_ALL")
    print "available input methods: "
    print im.getAvailableInputMethods()
    print "current method: %s" % im.getCurrentInputMethod()
#    print im.getCurrentInputMethod()
    sys.exit(1)
    print "switching to 'th-xim': ",
    print im.setDefaultInputMethod("th-xim")
    print "current method: ",
    print im.getCurrentInputMethod()
    print "reset default: ",
    print im.resetDefaultInputMethod()
    print "current method: ",
    print im.getCurrentInputMethod()
