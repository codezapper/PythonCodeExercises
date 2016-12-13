from django.db import connection
from django.template import loader


# response = render_to_response(template_name, context)

# response.set_cookie('use_shuffle', '0')
# return response

# request.COOKIES.get('use_shuffle')

def render_for_songs_list(request, album='', artist='', year=''):
    # songs_list = [song for song in Song.objects.order_by(
    #     'artist_id', 'album_id', 'track_number')]
    cursor = connection.cursor()
    if (album != ''):
        sql = '''SELECT title, lister_album.description, lister_artist.description, image_file, path, year, track_number FROM lister_song, lister_album, lister_artist WHERE lister_artist.artist_id = lister_song.artist_id AND lister_album.album_id = lister_song.album_id AND lister_album.album_id = %s ORDER BY lister_song.artist_id, lister_album.album_id, track_number'''
        cursor.execute(sql, [album])
    elif (artist != ''):
        sql = '''SELECT title, lister_album.description, lister_artist.description, image_file, path, year, track_number FROM lister_song, lister_album, lister_artist WHERE lister_artist.artist_id = lister_song.artist_id AND lister_album.album_id = lister_song.album_id AND lister_artist.artist_id = %s ORDER BY lister_song.artist_id, lister_album.album_id, track_number'''
        cursor.execute(sql, [artist])
    elif (year != ''):
        sql = '''SELECT title, lister_album.description, lister_artist.description, image_file, path, year, track_number FROM lister_song, lister_album, lister_artist WHERE lister_artist.artist_id = lister_song.artist_id AND lister_album.album_id = lister_song.album_id AND lister_song.year = %s ORDER BY lister_song.artist_id, lister_album.album_id, track_number'''
        cursor.execute(sql, [year])
    else:
        sql = '''SELECT title, lister_album.description, lister_artist.description, image_file, path, year, track_number FROM lister_song, lister_album, lister_artist WHERE lister_artist.artist_id = lister_song.artist_id AND lister_album.album_id = lister_song.album_id ORDER BY lister_song.artist_id, lister_album.album_id, track_number'''
        cursor.execute(sql)
    row = cursor.fetchone()

    songs_list = []
    while (row):
        songs_list.append(
            {'title': row[0], 'album': row[1], 'artist': row[2], 'image_file': row[3], 'path': row[4], 'year': row[5], 'track_number': row[6]})
        row = cursor.fetchone()

    template = loader.get_template('lister/index_with_menu.html')
    context = {'songs_list': songs_list, 'counters': get_counters()}
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
    context = {'albums_list': albums_list, 'counters': get_counters()}
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
    context = {'artists_list': artists_list, 'counters': get_counters()}
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
    context = {'years_list': years_list, 'counters': get_counters()}
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
