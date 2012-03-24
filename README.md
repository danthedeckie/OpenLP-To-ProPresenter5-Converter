# OpenLP to ProPresenter 5 converter

This is a quick fast converter from OpenLP's sqlite database to ProPresenter 5 XML files.

It works very fast, and does our 2800 song database in about 10 seconds.

Work in Progress, Please enjoy.

## Use:

Currently a bit basic.

The script will try to load the database from

~/Library/Application Support/openlp/Data/songs/songs.sqlite

( ~ means "Your home directory" )

To change that, edit the line which says "OPENLP_DATABASE" in converter.py

It will create all the XML files in /tmp/

On Mac, you can open /tmp/ with (in Finder) Menu->Go->Go To folder.

By default, the script will open the /tmp/ directory when it's finished running.

## TODO:

- Make it rugged
- Make it pretty
- Make a .app & .exe
- Make profit.

## Licence:

Public Domain.  It's so basic, do what you want with this.  If you do appreciate it, please
consider a donation to OMNIvision, which is a team in OM (www.om.org), who actually wrote this
script. http://www.omnivision.om.org


