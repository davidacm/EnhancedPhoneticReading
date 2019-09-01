# -*- coding: UTF-8 -*-
# power status notiffications: This add-on plays a tone when the power status changes.
# Copyright (C) 2019 David CM
# Author: David CM <dhf360@gmail.com>
# Released under GPL 2
#globalPlugins/powerStatusNotiffications.py

from logHandler import log
import controlTypes, globalPluginHandler, speech, textInfos, threading
DELAY= 1
characterDescriptionTimer = threading.Timer(0.3, zip) # fake timer because this can't be None.

#saves the original speakTextInfo function
origSpeakTextInfo = speech.speakTextInfo
# alternate function to speakTextInfo.
def speakTextInfo(*args, **kwargs):
	global characterDescriptionTimer
	try:
		info = args[0]
		if kwargs.get('unit', None) == textInfos.UNIT_CHARACTER and info.text.isalpha():
			characterDescriptionTimer.cancel()
			characterDescriptionTimer = threading.Timer(DELAY, speech.spellTextInfo, [info], {'useCharacterDescriptions': True})
			characterDescriptionTimer.start()
		else: characterDescriptionTimer.cancel()
	except:
		log.exception("Error when delay character")
	return origSpeakTextInfo(*args, **kwargs)

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	def __init__(self):
		super(globalPluginHandler.GlobalPlugin, self).__init__()
		speech.speakTextInfo = speakTextInfo

	def terminate(self):
		super(GlobalPlugin, self).terminate()
		speech.speakTextInfo = origSpeakTextInfo
