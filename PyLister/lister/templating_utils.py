from django.db import models, connection
from django.template import loader
from .models import Song


def render_for_songs_list(request):
    songs_list = [song for song in Song.objects.order_by(
        'artist', 'album', 'track_number')]
    template = loader.get_template('lister/index_with_menu.html')
    context = {'songs_list': songs_list, }
    return template.render(context, request)


def render_for_albums_list(request):
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
    return template.render(context, request)


def render_for_artists(request):
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
    return template.render(context, request)


def render_for_years(request):
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
    return template.render(context, request)
