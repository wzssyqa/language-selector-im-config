

QtLanguageSelectorGUI.py: QtLanguageSelectorGUI.ui
	# this makes baby jesus cry 
	# (but we want gettext() for the i18n strings, not __tr() to 
	# make intltool-update happy
        #no -tr option in pyuic4 - jriddell
	#echo "import gettext" > $@
	#pyuic -tr gettext.gettext $< >> $@
	pyuic4 $< >> $@
