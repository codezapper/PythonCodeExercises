from __future__ import unicode_literals

from django.db import models


class Song(models.Model):
    album = models.CharField(max_length=256)
    artist = models.CharField(max_length=256)
    image_file = models.CharField(max_length=256)
    year = models.DateTimeField(default=1900)
    rating = models.IntegerField(default=0)
    title = models.CharField(max_length=256)

    def __str__(self):
        return '{} ({}) by {}'.format(self.title, self.year, self.artist)
