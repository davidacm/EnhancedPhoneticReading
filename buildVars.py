# -*- coding: UTF-8 -*-

# Build customizations
# Change this file instead of sconstruct or manifest files, whenever possible.

# Full getext (please don't change)
_ = lambda x : x

# Add-on information variables
addon_info = {
	# for previously unpublished addons, please follow the community guidelines at:
	# https://bitbucket.org/nvdaaddonteam/todo/raw/master/guideLines.txt
	# add-on Name, internal for nvda
	"addon_name" : "EnhancedPhoneticReading",
	# Add-on summary, usually the user visible name of the addon.
	# Translators: Summary for this add-on to be shown on installation and add-on information.
	"addon_summary" : _("Enhanced Phonetic Reading"),
	# Add-on description
	# Translators: Long description to be shown for this add-on on add-on information from add-ons manager
	"addon_description" : _("""This add-on add some features to phonetic reading as the following:
	announce the character description for the last read character after n milliseconds when the character was read by character review commands, E.G. left and right arrow keys, left, current or right character review commands, ETC.
	Read the character description instead of the current character. This feature must be enabled or disabled manually and will be deactivated when NVDA is closed."""),
	# version
	"addon_version" : ,
	# Author(s)
	"addon_author" : u"David CM <dhf360@gmail.com>",
	# URL for the add-on documentation support
	"addon_url" : "https://github.com/david-acm/EnhancedPhoneticReading",
	# Documentation file name
	"addon_docFileName" : "readme.html",
	# Minimum NVDA version supported (e.g. "2018.3.0")
	"addon_minimumNVDAVersion" : "2018.3.0",
	# Last NVDA version supported/tested (e.g. "2018.4.0", ideally more recent than minimum version)
	"addon_lastTestedNVDAVersion" : "2021.3.1",
	# Add-on update channel (default is stable or None)
	"addon_updateChannel": "dev",
}

from os import path

# Define the python files that are the sources of your add-on.
# You can use glob expressions here, they will be expanded.
pythonSources = [path.join("addon", "globalPlugins", "enhancedPhoneticReading.py")]

# Files that contain strings for translation. Usually your python sources
i18nSources = pythonSources + ["buildVars.py"]

# Files that will be ignored when building the nvda-addon file
# Paths are relative to the addon directory, not to the root directory of your addon sources.
excludedFiles = []
