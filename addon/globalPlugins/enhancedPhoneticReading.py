# -*- coding: UTF-8 -*-
# Enhanced phonetic reading: This add-on add some features to phonetic reading.
# Copyright (C) 2019 David CM
# Author: David CM <dhf360@gmail.com>
# Released under GPL 2.0
#globalPlugins/enhancedPhoneticReading.py

import characterProcessing, config, controlTypes, core, globalPluginHandler, gui, addonHandler, six, speech, textInfos, threading, wx
from globalCommands import SCRCAT_SPEECH

addonHandler.initTranslation()

characterDescriptionTimer = None
confspec = {
	"delayedDescriptions": "boolean(default=True)",
	"delay": "integer(default=1000)"
}
config.conf.spec["enhancedPhoneticReading"] = confspec

def cancelTimer():
	global characterDescriptionTimer
	if characterDescriptionTimer  and characterDescriptionTimer.IsRunning():
		characterDescriptionTimer.Stop()
		characterDescriptionTimer = None

#saves the original speak function. We need it to cancel the timer if another speech sequence is received.
origSpeak = speech.speak
# alternate function to speak.
def speak(*args, **kwargs):
	origSpeak(*args, **kwargs)
	cancelTimer()

#saves the speakSpelling original  function. We need it to cancel the timer if another speech sequence is received.
origSpeakSpelling= speech.speakSpelling
# alternate function to speakSpelling.
def speakSpelling(*args, **kwargs):
	origSpeakSpelling(*args, **kwargs)
	cancelTimer()

#saves the cancelSpeech original  function. We need it to cancel the timer if the user send a stop speech command.
origCancelSpeech = speech.cancelSpeech
def cancelSpeech():
	origCancelSpeech()
	cancelTimer()

class _FakeTextInfo():
	"""
	this class is used to preserve the information of the old object that contain the text. Its useful to use with delayed descriptions.
	"""

	def __init__(self, origTextInfo: textInfos.TextInfo):
		self.text = origTextInfo.text
		self.fields = origTextInfo.getTextWithFields({})

	def getTextWithFields(self, _ = None):
		return self.fields

#saves the original speakTextInfo function
origSpeakTextInfo = speech.speakTextInfo
instantDescriptions = False
# alternate function to speakTextInfo. We determine here if a delayed description is needed base on textInfos.UNIT_CHARACTER.
def speakTextInfo(*args, **kwargs):
	global characterDescriptionTimer
	info = args[0]
	if instantDescriptions and kwargs.get('unit') == textInfos.UNIT_CHARACTER: return speech.spellTextInfo(info, True)
	tmp = origSpeakTextInfo(*args, **kwargs)
	if config.conf['enhancedPhoneticReading']['delayedDescriptions'] and kwargs.get('unit') == textInfos.UNIT_CHARACTER:
		characterDescriptionTimer = core.callLater(config.conf['enhancedPhoneticReading']['delay'], speakDelayedDescription, _FakeTextInfo(info))
	return tmp

def speakDelayedDescription(info: _FakeTextInfo):
	"""
	this function is used to announce the delayed descriptions, we can't call spellTextInfo directly because we need to check if the description is available first.
	"""
	if info.text.strip() == "": return
	curLang = speech.getCurrentLanguage()
	if config.conf['speech']['autoLanguageSwitching']:
		for k in info.fields:
			if isinstance(k, textInfos.FieldCommand) and k.command == "formatChange":
				curLang = k.field.get('language', curLang)
	_, description = speech.getCharDescListFromText(info.text, locale=curLang)[0]
	if description:
		speech.spellTextInfo(info, useCharacterDescriptions=True)

class EnhancedPhoneticReadingPanel(gui.SettingsPanel):
	# Translators: This is the label for the Enhanced phonetic reading settings category in NVDA Settings screen.
	title = _("Enhanced phonetic reading")

	def makeSettings(self, settingsSizer):
		sHelper = gui.guiHelper.BoxSizerHelper(self, sizer=settingsSizer)
		# Translators: label for a checkbox option in the settings panel.
		self.delayedDescriptions = sHelper.addItem(wx.CheckBox(self, label=_("&Enable delayed descriptions for characters")))
		self.delayedDescriptions.SetValue(config.conf['enhancedPhoneticReading']['delayedDescriptions'])
		# Translators: label for a edit field option in the settings panel.
		self.delay = sHelper.addLabeledControl(_("&Delay to announce  character descriptions (in ms)"), gui.nvdaControls.SelectOnFocusSpinCtrl, min=200, max=5000, initial=config.conf['enhancedPhoneticReading']['delay'])

	def onSave(self):
		config.conf['enhancedPhoneticReading']['delayedDescriptions'] = self.delayedDescriptions.GetValue()
		config.conf['enhancedPhoneticReading']['delay'] = int(self.delay.GetValue())

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	def __init__(self):
		super(globalPluginHandler.GlobalPlugin, self).__init__()
		gui.settingsDialogs.NVDASettingsDialog.categoryClasses.append(EnhancedPhoneticReadingPanel)
		self.validateConfig()
		speech.speakTextInfo = speakTextInfo
		speech.speak = speak
		speech.speakSpelling = speakSpelling
		speech.cancelSpeech = cancelSpeech

	def script_toggleDelayedDescriptions(self, gesture):
		config.conf['enhancedPhoneticReading']['delayedDescriptions'] = not config.conf['enhancedPhoneticReading']['delayedDescriptions']
		# Translators: message spoken if the user enables or disables delayed character descriptions.
		speech.speakMessage(_('Delayed descriptions %s') % (_('on') if config.conf['enhancedPhoneticReading']['delayedDescriptions'] else _('off')))
	# Translators: input help message for a delayed character descriptions command.
	script_toggleDelayedDescriptions.__doc__ = _("Toggles delayed character descriptions on or off")
	script_toggleDelayedDescriptions.category = SCRCAT_SPEECH

	def script_toggleInstantDescriptions(self, gesture):
		global instantDescriptions
		instantDescriptions = not instantDescriptions
		# Translators: message spoken if the user enables or disables instant character descriptions.
		speech.speakMessage(_('instant character descriptions %s') % (_('on') if instantDescriptions else _('off')))
	# Translators: input help message for a Enhanced phonetic reading command.
	script_toggleInstantDescriptions.__doc__ = _("Toggles instant character descriptions on or off")
	script_toggleInstantDescriptions.category = SCRCAT_SPEECH
	script_toggleInstantDescriptions.gestures =["kb(laptop):nvda+control+enter", "kb:nvda+control+numpad2"]

	def terminate(self):
		super(GlobalPlugin, self).terminate()
		speech.speakTextInfo = origSpeakTextInfo
		speech.speak = origSpeak
		speech.speakSpelling = origSpeakSpelling
		speech.cancelSpeech = origCancelSpeech
		gui.settingsDialogs.NVDASettingsDialog.categoryClasses.remove(EnhancedPhoneticReadingPanel)

	def validateConfig(self):
		try:
			config.conf['enhancedPhoneticReading']['delay']
		except:
			config.conf['enhancedPhoneticReading']['delay'] = 1000

	def handleConfigProfileSwitch(self):
		self.validateConfig()
