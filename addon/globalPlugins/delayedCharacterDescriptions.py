# -*- coding: UTF-8 -*-
# Delayed character descriptions: This add-on speaks the character description for the last read character after n miliseconds.
# Copyright (C) 2019 David CM
# Author: David CM <dhf360@gmail.com>
# Released under GPL 3
#globalPlugins/delayedCharacterDescriptions.py

import characterProcessing, config, controlTypes, globalPluginHandler, gui, addonHandler, six, speech, textInfos, threading, wx
addonHandler.initTranslation()

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

#saves the speakSpelling original  function. We need it to cancel the timer if another speech sequence is received.
origSpeakSpelling= speech.speakSpelling
# alternate function to speakSpelling.
def speakSpelling(*args, **kwargs):
	origSpeakSpelling(*args, **kwargs)
	if characterDescriptionTimer.isAlive(): characterDescriptionTimer.cancel()
lastRead = None
#saves the original speakTextInfo function
origSpeakTextInfo = speech.speakTextInfo
# alternate function to speakTextInfo.
def speakTextInfo(*args, **kwargs):
	global characterDescriptionTimer
	info = args[0]
	tmp = origSpeakTextInfo(*args, **kwargs)
	if kwargs.get('unit') == textInfos.UNIT_CHARACTER:
		characterDescriptionTimer = threading.Timer(config.conf['delayedCharacterDescriptions']['delay'], speakDescription, [info.text, info.getTextWithFields({})])
		characterDescriptionTimer.start()
	return tmp

def speakDescription(text, fields):
	curLanguage=speech.getCurrentLanguage()
	if not config.conf['speech']['autoLanguageSwitching'] and characterProcessing.getCharacterDescription(curLanguage, text.lower()):
		speakSpelling(text, curLanguage, useCharacterDescriptions=True)
		return
	for field in fields:
		if isinstance(field, six.string_types) and characterProcessing.getCharacterDescription(curLanguage, field.lower()):
			speakSpelling(field,curLanguage,useCharacterDescriptions=True)
		elif isinstance(field,textInfos.FieldCommand) and field.command=="formatChange":
			curLanguage=field.field.get('language', curLanguage)

class DelayedCharactersPanel(gui.SettingsPanel):
	# Translators: This is the label for the delayed character   descriptions settings category in NVDA Settings screen.
	title = _("Delayed character descriptions")
	def makeSettings(self, settingsSizer):
		sHelper = gui.guiHelper.BoxSizerHelper(self, sizer=settingsSizer)
		# Translators: label for a checkbox option in the settings panel.
		self.enabled = sHelper.addItem(wx.CheckBox(self, label=_("&Enable delayed descriptions for characters")))
		self.enabled.SetValue(config.conf['delayedCharacterDescriptions']['enabled'])
		# Translators: label for a edit field option in the settings panel.
		self.delay = sHelper.addLabeledControl(_("&Delay to announce  character descriptions (in ms)"), gui.nvdaControls.SelectOnFocusSpinCtrl, min=1, max=20000, initial=config.conf['delayedCharacterDescriptions']['delay']*1000)

	def onSave(self):
		config.conf['delayedCharacterDescriptions']['enabled'] = self.enabled.GetValue()
		config.conf['delayedCharacterDescriptions']['delay'] = float(self.delay.GetValue())/1000.0
		config.post_configProfileSwitch.notify()
		
class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	def __init__(self):
		super(globalPluginHandler.GlobalPlugin, self).__init__()
		self.handleConfigProfileSwitch()
		gui.settingsDialogs.NVDASettingsDialog.categoryClasses.append(DelayedCharactersPanel)
		config.post_configProfileSwitch.register(self.handleConfigProfileSwitch)
		
	def handleConfigProfileSwitch(self): self.switch(config.conf['delayedCharacterDescriptions']['enabled'])

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
		gui.settingsDialogs.NVDASettingsDialog.categoryClasses.remove(DelayedCharactersPanel)
		config.post_configProfileSwitch.unregister(self.handleConfigProfileSwitch)
