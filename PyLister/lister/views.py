from django.db import connection
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from .models import Song
import utils


def index(request):
    return songs(request)


def songs(request):
    songs_list = [song
                  for song in Song.objects.order_by('-artist', 'album', 'track_number')]
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
    return HttpResponse('ARTISTS')


def years(request):
    return HttpResponse('YEARS')


def detail(request, song_id):
    try:
        song = Song.objects.get(pk=song_id)
    except Song.DoesNotExist:
        raise Http404("Song does not exist")
    return render(request, 'lister/detail.html', {'song': song})


def vote(request, song_id):
    return HttpResponse("You're voting on song %s." % song_id)
