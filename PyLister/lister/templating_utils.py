from django.db import connection
from django.template import loader


def render_wrapper(request):
    template = loader.get_template('lister/wrapper.html')
    context = {}

    return template.render(context, request)


def render_for_songs_list(request, album='', artist='', year=''):
    template = loader.get_template('lister/songs.html')
    context = {}
    return template.render(context, request)


def render_for_albums_list(request):
    print request
    cursor = connection.cursor()
    cursor.execute(
        '''SELECT lister_album.album_id, lister_album.description, image_file, lister_artist.description, year FROM lister_song, lister_album, lister_artist WHERE lister_artist.artist_id = lister_song.artist_id AND lister_album.album_id = lister_song.album_id GROUP BY lister_album.description, lister_artist.description, image_file, year ORDER BY lister_album.description''')
    row = cursor.fetchone()

    albums_list = []
    while (row):
        albums_list.append(
            {'album_id': row[0], 'album': row[1], 'image_file': row[2], 'artist': row[3], 'year': row[4]})
        row = cursor.fetchone()
    template = loader.get_template('lister/albums_with_menu.html')
    context = {'albums_list': albums_list,
               'counters': get_counters(), 'section': 'album'}
    return template.render(context, request)


def render_for_artists_list(request):
    print request
    cursor = connection.cursor()
    cursor.execute(
        '''SELECT lister_artist.artist_id, lister_artist.description, count(*) FROM lister_song, lister_artist WHERE lister_artist.artist_id = lister_song.artist_id GROUP BY lister_artist.artist_id, lister_artist.description ORDER BY lister_artist.description''')
    row = cursor.fetchone()

    artists_list = []
    while (row):
        artists_list.append(
            {'artist_id': row[0], 'artist': row[1], 'count': row[2]})
        row = cursor.fetchone()
    template = loader.get_template('lister/artists_with_menu.html')
    context = {'artists_list': artists_list,
               'counters': get_counters(), 'section': 'artist'}
    return template.render(context, request)


def render_for_years_list(request):
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
    context = {'years_list': years_list,
               'counters': get_counters(), 'section': 'year'}
    return template.render(context, request)


def get_counters():
    counters = {}
    cursor = connection.cursor()
    cursor.execute('''SELECT count(*) FROM lister_song''')
    counters['songs'] = cursor.fetchone()[0]
    cursor.execute('''SELECT count(*) FROM lister_album''')
    counters['albums'] = cursor.fetchone()[0]
    cursor.execute('''SELECT count(*) FROM lister_artist''')
    counters['artists'] = cursor.fetchone()[0]
    cursor.execute('''SELECT count(distinct year) FROM lister_song''')
    counters['years'] = cursor.fetchone()[0]

    return counters
