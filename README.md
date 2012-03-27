# OpenLP to ProPresenter 5 converter

This is a simple fast converter from OpenLP's sqlite database to ProPresenter 5 XML files.

It works quickly, and does our 2800 song database in about 10 seconds.

Work in Progress, Please enjoy.

## How to use:

Currently a bit basic, written to run on OSX.  It should be very easy to port to Windows/Linux/etc.

> python converter.py

that's it.

The script will try to load the database from

~/Library/Application Support/openlp/Data/songs/songs.sqlite

( ~ means "Your home directory" )

To change that, edit the line which says "OPENLP_DATABASE" in converter.py

It will create all the XML files in /tmp/

On Mac, you can open /tmp/ with (in Finder) Menu->Go->Go To folder.

By default, the script will open the /tmp/ directory when it's finished running.

## Options:

By default, the converter will set the font as Helvetica,
the background color as black, and the text color as white.
It will put a maximum of 4 lines per slide.

These settings are all at the top of the converter.py script, and should be very easy to change.

## Requirements:

Python. (2.6ish) Should come built-in on OSX.

## TODO:

- Make it rugged
- Make it pretty
- Make a .app & .exe
- Make profit.

## Licence:

Public Domain.  It's so basic, do what you want with this.  If you do appreciate it, please
consider a donation to OMNIvision, which is a team in OM (www.om.org), we're the ones who 
actually wrote this script.

http://www.omnivision.om.org


