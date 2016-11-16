from __future__ import unicode_literals

from django.db import models


class Song(models.Model):
    album = models.CharField(max_length=256, null=True)
    artist = models.CharField(max_length=256, null=True)
    image_file = models.CharField(max_length=256, null=True)
    year = models.IntegerField(default=1900, null=True)
    rating = models.IntegerField(default=0, null=True)
    title = models.CharField(max_length=256)
    track_number = models.CharField(max_length=256, default='')
    path = models.CharField(max_length=256, default='')

    def __str__(self):
        return '{} ({}) by {}'.format(self.title, self.year or '----', self.artist)
