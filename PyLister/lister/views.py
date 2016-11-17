from django.db import connection
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from .models import Song
import os
import utils


def index(request):
    return songs(request)


def songs(request):
    songs_list = [song
                  for song in Song.objects.order_by('artist', 'album', 'track_number')]
    template = loader.get_template('lister/index_with_menu.html')
    context = {'songs_list': songs_list, }
    return HttpResponse(template.render(context, request))


def albums(request):
    cursor = connection.cursor()
    cursor.execute(
        '''SELECT album, image_file, artist, year FROM lister_song GROUP BY album, image_file, artist, year ORDER BY album''')
    row = cursor.fetchone()

    albums_list = []
    while (row):
        albums_list.append(
            {'album': row[0], 'image_file': row[1].replace('/home/gabriele/', ''), 'artist': row[2], 'year': row[3]})
        row = cursor.fetchone()
    template = loader.get_template('lister/albums_with_menu.html')
    context = {'albums_list': albums_list, }
    return HttpResponse(template.render(context, request))


def artists(request):
    cursor = connection.cursor()
    cursor.execute(
        '''SELECT artist, count(artist) FROM lister_song GROUP BY artist ORDER BY artist''')
    row = cursor.fetchone()

    artists_list = []
    while (row):
        artists_list.append(
            {'artist': row[0], 'count': row[1]})
        row = cursor.fetchone()
    template = loader.get_template('lister/artists_with_menu.html')
    context = {'artists_list': artists_list, }
    return HttpResponse(template.render(context, request))


def years(request):
    cursor = connection.cursor()
    cursor.execute(
        '''SELECT year, count(year) FROM lister_song GROUP BY year ORDER BY year''')
    row = cursor.fetchone()

    years_list = []
    while (row):
        years_list.append(
            {'year': row[0], 'count': row[1]})
        row = cursor.fetchone()
    template = loader.get_template('lister/years_with_menu.html')
    context = {'years_list': years_list, }
    return HttpResponse(template.render(context, request))


def detail(request, song_id):
    try:
        song = Song.objects.get(pk=song_id)
    except Song.DoesNotExist:
        raise Http404("Song does not exist")
    return render(request, 'lister/detail.html', {'song': song})


'''It is possible (and documented) to use a response like:
HttpResponse(open('test.file')) but Django emits bytes using iter(),
and calling next() to get more bytes. The problem is that the
default behaviour is to check for newlines in the input file.
This does not work well for binary files (there is no real concept
of "line"), so I want an iterator that reads chunks of data
of a specified size.'''

class StreamWrapper():
  def __init__(self, input_file, buffer_size = 1024**2):
    self.file_handle = open(input_file, 'rb')
    self.buffer_size = buffer_size

  def next(self):
    stream_data = self.file_handle.read(self.buffer_size)
    if stream_data:
      return stream_data
    else:
      raise StopIteration

  def __iter__(self):
    return self


def play(request, song_id):  
    streaming_response =  HttpResponse(StreamWrapper('/home/gabriele/Music/test.mp3'),content_type='audio/mpeg')
    streaming_response['Content-Length'] = os.path.getsize("/home/gabriele/Music/test.mp3")  
    streaming_response['Content-Disposition'] = 'filename=test.mp3'  
    return streaming_response
