# (c) 2006 Canonical
# Author: Michael Vogt <michael.vogt@ubuntu.com>
#
# Released under the GPL
#

import os
import subprocess
import tempfile

def find_string_and_replace(findString, setString, file_list, 
                            startswith=True, append=True):
    """ find all strings that startswith findString and replace them with
        setString
    """
    for fname in file_list:
        out = tempfile.NamedTemporaryFile(delete=False,
                                          dir=os.path.dirname(fname))
        foundString = False
        if (os.path.exists(fname) and
            os.access(fname, os.R_OK)):
            # look for the line
            for line in open(fname):
                tmp = line.strip()
                if startswith and tmp.startswith(findString):
                    foundString = True
                    line = setString
                if not startswith and tmp == findString:
                    foundString = True
                    line = setString
                out.write(line)
        # if we have not found them append them
        if not foundString and append:
            out.write(setString)
        out.flush()
        # rename is atomic
        os.rename(out.name, fname)
        os.chmod(fname, 0644)

def language2locale(language):
    """ generate locale name for LC_* environment variables
    """
    first_elem = language.split(':')[0]
    locale = subprocess.check_output(['/usr/share/language-tools/language2locale', first_elem])
    return locale.rstrip()

