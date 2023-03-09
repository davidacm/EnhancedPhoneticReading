# Enhanced phonetic reading NVDA Add-on #
This add-on add some features to phonetic reading like delayed character descriptions and instant character descriptions.

Copyright (C) 2022 - 2023 David CM <dhf360@gmail.com>

This package is distributed under the terms of the GNU General Public License, version 2 or later.

## Download.
	The latest release is available to
[download in this link](https://davidacm.github.io/getlatest/gh/davidacm/EnhancedPhoneticReading)

## Features.

* Delayed descriptions: Announce the character description for the last read character after n milliseconds when the character was read by character review commands, E.G. left and right arrow keys, left, current or right character review commands, ETC.  
* Instant character descriptions: Read the character description instead of the current character. This feature must be enabled or disabled manually and will be deactivated when NVDA is closed.

## Notes.

* When instant character descriptions are enabled, delayed descriptions won't be announced.
* This add-on considers the auto language switching also. So if the last read character captured by this add-on was spoken in another language of your current default language, and auto language switching is on, the description will be read in the detected language.
* For delayed descriptions only: all characters that don't have a description available for the specified language (locale characterDescriptions.dic) will be ignored. E.G. if you read the character "4" and the current default or detected language is Spanish, you won't get a delayed description because Spanish  doesn't have a description for that symbol.
* For developers: In general, any character sent with textInfos.UNIT_CHARACTER argument to speech.speakTextInfo will activate a delayed character description.

## Requirements
  You need NVDA 2018.3 or later.

## Installation
  Just install it as a NVDA add-on.

## Usage
  The add-on functionality will be enabled once you install it.  
  To enable or disable it, go to NVDA settings and select "Enhanced phonetic reading". In that category you can set the following parameters:

* Enable delayed descriptions for characters.
* Delay to announce  character descriptions (in ms): the time the add-on waits to speak the description for the read character. You can't set it greater than 20000 ms.

## Scripts

* toggle instant character descriptions: Assigned to "nvda + control + numpad2" or "nvda+ control + enter" for laptop keyboards. This script enables or disables the instant character descriptions feature.
* toggle delayed descriptions: no gestures assigned. This script lets you toggle the delayed descriptions status.  

You can assign a command or gesture in speech category in the  NVDA input gestures dialog.

## contributions, reports and donations

If you like my project or this software is useful for you in your daily life and you would like to contribute in some way, you can donate via the following methods:

* [PayPal.](https://paypal.me/davicm)
* [Ko-fi.](https://ko-fi.com/davidacm)
* [cryptocurrencies and other methods.](https://davidacm.github.io/donations/)

If you want to fix bugs, report problems or new features, you can contact me at: <dhf360@gmail.com>.

  Or in the github repository of this project:
  [Enhanced phonetic reading on GitHub](https://github.com/davidacm/enhancedphoneticreading)

    You can get the latest release of this add-on in that repository.
