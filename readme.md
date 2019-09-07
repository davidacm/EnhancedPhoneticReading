# Delayed character descriptions NVDA Add-on #
This add-on speaks the character description for the last read character after n miliseconds when the character was read by character review commands, E.G. left and right arrow keys, left, current or right character review commands, ETC.  
In general, any character sent with textInfos.UNIT_CHARACTER argument to speech.speakTextInfo will activate a delayed character description.  
This add-on consider the auto language switching also. So if the last read character captured by this add-on was spoken in another language of your current default language, and auto language switching is on, the description will be read in the detected language.
All characters that don't have a description available for the specified language (locale characterDescriptions.dic) will be ignored. E.G. if you read the character "4" and the current default or detected language is spanish, you won't get a delayed description because spanish  doesn't have a description for that symbol.

Copyright (C) 2019 David CM <dhf360@gmail.com>

This package is distributed under the terms of the GNU General Public License, version 3 or later.

## Download.
	The latest release is available to
[download in this link](https://davidacm.github.io/getlatest/gh/davidacm/delayedCharacterDescriptions)

## Requirements
  You need NVDA 2018.3 or later.

## Installation
  Just install it as a NVDA add-on.

## Usage
  The add-on functionality will be enabled once you install it.  
  To enable or disable it, go to NVDA settings and select Delayed character descriptions. In that category you can set the following parameters:

* Enable delayed descriptions for characters: this check enables or disables the add-on.
* Delay to announce  character descriptions (in ms): the time the add-on waits to speak the description for the read character. You can't set it greater than 20000 ms.

This add-on has a script that lets you toggle the delayed descriptions status.  
You can assign a command or gesture in speech category in the  NVDA input gestures dialog.