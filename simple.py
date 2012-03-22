#!/usr/bin/python

import sqlite3 as sql
import sys

import xml.dom.minidom
from xml.dom.minidom import Node

from base64 import b64encode # For RTF Data blobs
from uuid import uuid4 # For Slide UUIDs
from datetime import datetime # Guess.

# Bits and pieces

def MakeUUID():
    return uuid4().__str__().upper()

def MakeRTFBlob(text):
    return b64encode(u'{\\rtf1\\ansi\\ansicpg1252\\cocoartf1038\\cocoasubrtf360\n{\\fonttbl\\f0\\fswiss\\fcharset0 Helvetica;}\n{\\colortbl;\\red255\\green255\\blue255;}\n\\pard\\tx560\\tx1120\\tx1680\\tx2240\\tx2800\\tx3360\\tx3920\\tx4480\\tx5040\\tx5600\\tx6160\\tx6720\\qc\\pardirnatural\n\n\\f0\\fs102\\fsmilli51200 \\cf1 \\expnd0\\expndtw0\\kerning0\n\\outl0\\strokewidth-20 \\strokec0 ' + text.replace("\n",'\\\n') + u'}')

# XML sections.

def VerseBlock(block_name, block_type, text_sections, color=u'0 0 0 0'):
    first_sections = []
    for section in text_sections:
        first_sections += map( lambda x: x.strip(), section.split('\n\n'))
    all_sections = []
    for section in first_sections:
        all_sections += map( lambda x: x.strip(), section.split('[---]'))

    return u'<RVSlideGrouping name="' + block_name + u'" uuid="'+ MakeUUID() + u'" color="' + color + u'" serialization-array-index="0"><slides containerClass="NSMutableArray">' + u''.join(map(SlideBlock, all_sections)) + u'</slides></RVSlideGrouping>'

def SlideBlock(text):
    return u'<RVDisplaySlide backgroundColor="0 0 0 1" enabled="1" highlightColor="0 0 0 0" hotKey="" label="" notes="" slideType="1" sort_index="0" UUID="' + MakeUUID() + u'" drawingBackgroundColor="0" chordChartPath="" serialization-array-index="0"><cues containerClass="NSMutableArray"></cues><displayElements containerClass="NSMutableArray"><RVTextElement displayDelay="0" displayName="Default" locked="0" persistent="0" typeID="0" fromTemplate="1" bezelRadius="0" drawingFill="0" drawingShadow="1" drawingStroke="0" fillColor="0 0 0 0" rotation="0" source="" adjustsHeightToFit="0" verticalAlignment="0" RTFData="' + MakeRTFBlob(text) + u'" revealType="0" serialization-array-index="0"><_-RVRect3D-_position x="30" y="30" z="0" width="964" height="708"></_-RVRect3D-_position><_-D-_serializedShadow containerClass="NSMutableDictionary"><NSNumber serialization-native-value="4" serialization-dictionary-key="shadowBlurRadius"></NSNumber><NSColor serialization-native-value="0 0 0 1" serialization-dictionary-key="shadowColor"></NSColor><NSMutableString serialization-native-value="{2.82843, -2.82843}" serialization-dictionary-key="shadowOffset"></NSMutableString></_-D-_serializedShadow><stroke containerClass="NSMutableDictionary"><NSColor serialization-native-value="0 0 0 0" serialization-dictionary-key="RVShapeElementStrokeColorKey"></NSColor><NSNumber serialization-native-value="0" serialization-dictionary-key="RVShapeElementStrokeWidthKey"></NSNumber></stroke></RVTextElement></displayElements><_-RVProTransitionObject-_transitionObject transitionType="-1" transitionDuration="1" motionEnabled="0" motionDuration="20" motionSpeed="100"></_-RVProTransitionObject-_transitionObject></RVDisplaySlide>'

def HeaderBlock(Name=u'New Song', 
                Authors=u'', 
                Artist=u'', 
                CCLICopyRightInfo=u'', 
                CCLILicenceNumber=u'', 
                Publisher=u'',
                Notes=u''):
    #map ( lambda x: x if x != None else u'', [Artist, Authors, CCLICopyRightInfo, CCLILicenceNumber,Publisher,Notes])
    return u'<RVPresentationDocument height="768" width="1024" versionNumber="500" docType="0" creatorCode="1349676880" lastDateUsed="' + datetime.now().strftime('%Y-%m-%dT%H:%M:%S') + u'" usedCount="0" category="Song" resourcesDirectory="" backgroundColor="0 0 0 1" drawingBackgroundColor="0" notes="' + Notes + u'" artist="' + Artist + u'" author="'+ Authors +u'" album="" CCLIDisplay="0" CCLIArtistCredits="" CCLISongTitle="' + Name + u'" CCLIPublisher="' + Publisher + u'" CCLICopyrightInfo="' + CCLICopyRightInfo + u'" CCLILicenseNumber="' + CCLILicenceNumber + u'" chordChartPath=""><timeline timeOffSet="0" selectedMediaTrackIndex="0" unitOfMeasure="60" duration="0" loop="0"><timeCues containerClass="NSMutableArray"></timeCues><mediaTracks containerClass="NSMutableArray"></mediaTracks></timeline><bibleReference containerClass="NSMutableDictionary"></bibleReference><_-RVProTransitionObject-_transitionObject transitionType="-1" transitionDuration="1" motionEnabled="0" motionDuration="20" motionSpeed="100"></_-RVProTransitionObject-_transitionObject><groups containerClass="NSMutableArray">'

def FooterBlock():
    return u'</groups><arrangements containerClass="NSMutableArray"></arrangements></RVPresentationDocument>' 

def uni(x):
    """ Unicode None! """
    return x if x != None else u''


def Verbose_names(key):
    VERBOSE_NAMES = {u'c':u'Chorus',u'v':u'Verse',u'':u'','':u'',u'b':u'Bridge',u'e':u'Ending',u'p':u'Pre-Chorus'}
    if key in VERBOSE_NAMES:
        return VERBOSE_NAMES[key]
    else:
        return key


VERSE_COLORS = [u'0 0 1 1', 
                u'0 1 0 1',
                u'1 0.5 0 1',
                u'1 0 1 1', 
                u'0 1 1 1', 
                u'0.5 1 0 1',
                u'1 1 0.5 1', 
                u'0 0 1 1',
                u'0 1 0 1',
                u'1 0.5 0 1',
                u'1 0 1 1',
                u'0 1 1 1',
                u'0.5 1 0 1',
                u'1 1 0.5 1']

###################################################
#
# Actually do stuff:
#
###################################################

con = None

#try:

## Fetch all the data first. Gets it in memory to use, rather than loads of SQLlite queries.

con = sql.connect('songs.sqlite')
con.row_factory = sql.Row

cur = con.cursor()
cur.execute('SELECT id, title, ccli_number, song_number, copyright, comments, lyrics FROM songs')

songs = cur.fetchall()

cur.execute('SELECT id, display_name FROM authors')

authors = cur. fetchall()

cur.execute('SELECT song_id, author_id FROM authors_songs')

authors_songs = cur.fetchall()


def filterbyfield(id,table,field='id'):
    return filter(lambda x: x[field]==id, table)

def get_authorname(id):
    names = filterbyfield(id,authors)
    if len(names) == 0:
        return ''
    else:
        return names[0]['display_name']

def get_song_authors(song_id):
    return filterbyfield(song_id,authors_songs,'song_id')


def get_song_authornames(song_id):
    return ' & '.join(map (get_authorname, map (lambda x: x['author_id'], get_song_authors(song_id))))


for song in songs:
    song_lyrics = xml.dom.minidom.parseString(song['lyrics'])

    song_authors = get_song_authornames(song['id'])

    f = open('/tmp/' + song['title'].replace('/','') + '.pro5','w')

    song_sections = song_lyrics.getElementsByTagName('verse')#.reverse()
    song_sections.reverse()

    f.write ( HeaderBlock(Name=uni(song['title']),
                          CCLILicenceNumber=uni(song['ccli_number']),
                          Notes=uni(song['comments']),
                          CCLICopyRightInfo=uni(song['copyright']),
                          Authors=song_authors) )

    for verse in song_sections:
        # Verse
        f.write ( VerseBlock( Verbose_names(verse.getAttribute('type')) + ' ' + verse.getAttribute('label'),
                              verse.getAttribute('type'),
                              map(lambda x: x.nodeValue, verse.childNodes) ,
                              color = '1 0 0 1' if verse.getAttribute('type') == 'c' else VERSE_COLORS[int(verse.getAttribute('label'))]  ) )
    f.write ( FooterBlock() )
    #for c in verse.childNodes:
    #    # Slide
    #    f.write(c.nodeValue)
    f.close()

#except:
#    print ('something went wrong. Sorry.')
