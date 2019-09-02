# -*- coding: UTF-8 -*-
# Delayed character descriptions: This add-on speaks the character description for the last read character after n miliseconds.
# Copyright (C) 2019 David CM
# Author: David CM <dhf360@gmail.com>
# Released under GPL 3
#globalPlugins/delayedCharacterDescriptions.py

import config, controlTypes, globalPluginHandler, gui, speech, textInfos, threading, wx
characterDescriptionTimer = threading.Timer(0.3, zip) # fake timer because this can't be None.

confspec = {
	"enabled": "boolean(default=True)",
	"delay": "float(default=1)"
}
config.conf.spec["delayedCharacterDescriptions"] = confspec

#saves the original speak function. We need it to cancel the timer if another speech sequence is received.
origSpeak = speech.speak
# alternate function to speak.
def speak(*args, **kwargs):
	origSpeak(*args, **kwargs)
	if characterDescriptionTimer.isAlive(): characterDescriptionTimer.cancel()

#saves the speakSpelling original  function. We need it to cancel the timer if another speech sequence is received. For some reason, this function does't call the replaced speak function so we replace it also.
origSpeakSpelling= speech.speakSpelling
# alternate function to speakSpelling.
def speakSpelling(*args, **kwargs):
	origSpeakSpelling(*args, **kwargs)
	if characterDescriptionTimer.isAlive(): characterDescriptionTimer.cancel()

#saves the original speakTextInfo function
origSpeakTextInfo = speech.speakTextInfo
# alternate function to speakTextInfo.
def speakTextInfo(*args, **kwargs):
	global characterDescriptionTimer
	tmp = origSpeakTextInfo(*args, **kwargs)
	info = args[0]
	if kwargs.get('unit', None) == textInfos.UNIT_CHARACTER and info.text.isalpha():
		characterDescriptionTimer = threading.Timer(config.conf['delayedCharacterDescriptions']['delay'], speech.spellTextInfo, [info.copy()], {'useCharacterDescriptions': True})
		characterDescriptionTimer.start()
	return tmp

class DelayedCharactersPanel(gui.SettingsPanel):
	# Translators: This is the label for the delayed character   descriptions settings category in NVDA Settings screen.
	title = _("Delayed character descriptions")

	def makeSettings(self, settingsSizer):
		sHelper = gui.guiHelper.BoxSizerHelper(self, sizer=settingsSizer)
		# Translators: label for a checkbox option in the settings panel.
		self.enabled = sHelper.addItem(wx.CheckBox(self, label=_("&Enable delayed descriptions for characters")))
		self.enabled.SetValue(config.conf['delayedCharacterDescriptions']['enabled'])
		self.delay = sHelper.addLabeledControl(_("&Delay to announce  character descriptions"), wx.TextCtrl)
		self.delay.SetValue(str(config.conf['delayedCharacterDescriptions']['delay']))

	def onSave(self):
		config.conf['delayedCharacterDescriptions']['enabled'] = self.enabled.GetValue()
		config.conf['delayedCharacterDescriptions']['delay'] = float(self.delay.GetValue())
		if hasattr(config, "post_configProfileSwitch"): config.post_configProfileSwitch.notify()
		else: config.configProfileSwitched.notify()

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	def __init__(self):
		super(globalPluginHandler.GlobalPlugin, self).__init__()
		self.handleConfigProfileSwitch()
		gui.settingsDialogs.NVDASettingsDialog.categoryClasses.append(DelayedCharactersPanel)
		if hasattr(config, "post_configProfileSwitch"): config.post_configProfileSwitch.register(self.handleConfigProfileSwitch)
		else: config.configProfileSwitched.register(self.handleConfigProfileSwitch)

	def handleConfigProfileSwitch(self):
		self.switch(config.conf['delayedCharacterDescriptions']['enabled'])

	def switch(self, status):
		if status:
			speech.speakTextInfo = speakTextInfo
			speech.speak = speak
			speech.speakSpelling = speakSpelling
		else:
			speech.speakTextInfo = origSpeakTextInfo
			speech.speak = origSpeak
			speech.speakSpelling = origSpeakSpelling

	def terminate(self):
		super(GlobalPlugin, self).terminate()
		self.switch(False)
