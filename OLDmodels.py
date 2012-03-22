# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

from django.db import models

class Author(models.Model):
    id           = models.IntegerField(primary_key=True)
    first_name   = models.CharField(max_length=128, blank=True)
    last_name    = models.CharField(max_length=128, blank=True)
    display_name = models.CharField(max_length=255)
    songs        = models.ManyToManyField('Song', through='AuthorSong')
    def __unicode__(self):
        return self.first_name + ' ' + self.last_name + '(' + self.display_name + ')'
    class Meta:
        db_table = u'authors'

class AuthorSong(models.Model):
    author    = models.ForeignKey('Author', related_name='authors')
    song      = models.ForeignKey('Song', related_name='songs')
    class Meta:
        db_table = u'authors_songs'

class MediaFile(models.Model):
    id           = models.IntegerField(primary_key=True)
    file_name    = models.CharField(max_length=255)
    type         = models.CharField(max_length=64)
    song_id      = models.IntegerField(null=True, blank=True)
    weight       = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'media_files'

class Metadata(models.Model):
    key          = models.CharField(max_length=64, primary_key=True)
    value        = models.TextField(blank=True)
    def __unicode__(self):
        return self.key + '=' + self.value
    class Meta:
        db_table = u'metadata'

class SongBook(models.Model):
    id           = models.IntegerField(primary_key=True)
    name         = models.CharField(max_length=128)
    publisher    = models.CharField(max_length=128, blank=True)
    def __unicode__(self):
        return self.name

    class Meta:
        db_table = u'song_books'

class Song(models.Model):
    id              = models.IntegerField(primary_key=True)
    song_book_id    = models.IntegerField(null=True, blank=True)
    title           = models.CharField(max_length=255)
    alternate_title = models.CharField(max_length=255, blank=True)
    lyrics          = models.TextField()
    verse_order     = models.CharField(max_length=128, blank=True)
    copyright       = models.CharField(max_length=255, blank=True)
    comments        = models.TextField(blank=True)
    ccli_number     = models.CharField(max_length=64, blank=True)
    song_number     = models.CharField(max_length=64, blank=True)
    theme_name      = models.CharField(max_length=128, blank=True)
    search_title    = models.CharField(max_length=255)
    search_lyrics   = models.TextField()
    create_date     = models.DateTimeField(null=True, blank=True)
    last_modified   = models.DateTimeField(null=True, blank=True)
    authors         = models.ManyToManyField('Author', through='AuthorSong')
    topics          = models.ManyToManyField('Topic', through='SongTopic')
    
    def __unicode__(self):
        return self.title

    class Meta:
        db_table = u'songs'

class Topic(models.Model):
    id    = models.IntegerField(primary_key=True)
    name  = models.CharField(max_length=128)
    songs = models.ManyToManyField(Song, through='SongTopic')
    class Meta:
        db_table = u'topics'

class SongTopic(models.Model):
    song      = models.ForeignKey(Song)
    topic     = models.ForeignKey(Topic)
    class Meta:
        db_table = u'songs_topics'


