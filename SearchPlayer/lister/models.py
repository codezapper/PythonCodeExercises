from __future__ import unicode_literals

from django.db import models


class Song(models.Model):
    album_id = models.IntegerField(null=True)
    artist_id = models.IntegerField(null=True)
    image_file = models.CharField(max_length=256, null=True)
    year = models.IntegerField(default=1900, null=True)
    rating = models.IntegerField(default=0, null=True)
    title = models.CharField(max_length=256)
    track_number = models.CharField(max_length=256, default='')
    path = models.CharField(max_length=256, default='')
    search_key = models.CharField(max_length=1024, default='')

    def __str__(self):
        return '{} ({}) by {}'.format(self.title, self.year or '----', self.artist)


class Album(models.Model):
    album_id = models.IntegerField(null=True)
    description = models.CharField(max_length=256)

    def __str__(self):
        return '{}'.format(self.description)


class Artist(models.Model):
    artist_id = models.IntegerField(null=True)
    description = models.CharField(max_length=256)

    def __str__(self):
        return '{}'.format(self.description)
