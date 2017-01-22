from django.db import connection
from django.http import JsonResponse


def data_for_songs_list(request, search_string='', album='', artist='', year=''):
    if (search_string == '' and album == '' and artist == '' and year == ''):
        return JsonResponse({})

    all_search_words = search_string.split()
    search_filters = []

    if ':' in search_string:
        search_filters = [search_word.split(':')
                          for search_word in all_search_words if ':' in search_word]
    search_words = [
        search_word for search_word in all_search_words if ':' not in search_word]

    section = ''
    search_params = []
    cursor = connection.cursor()
    sql = 'SELECT title, lister_album.description album, lister_artist.description artist, image_file, path, year, track_number FROM lister_song, lister_album, lister_artist WHERE lister_artist.artist_id = lister_song.artist_id AND lister_album.album_id = lister_song.album_id '''

    if (len(search_filters) > 0):
        query_strings = []
        for search_filter in search_filters:
            query_strings.append(
                '((artist like %s or album like %s) and title like %s)')
        full_query = ' AND (' + ' OR '.join(query_strings) + ')'

        sql += full_query
        for search_filter in search_filters:
            search_params.append('%' + search_filter[0] + '%')
            search_params.append('%' + search_filter[0] + '%')
            search_params.append('%' + search_filter[1] + '%')

    if (len(search_words) > 0):
        section = 'songs'
        string_conditions = []
        for i in (range(len(search_words))):
            string_conditions.append(
                '( title like %s or lister_album.description like %s or lister_artist.description like %s)')
        search_condition = '(' + ' OR '.join(string_conditions) + ')'
        sql += ' OR ' + search_condition
        for search_word in search_words:
            for i in range(0, 3):
                search_params.append('%' + search_word + '%')

    sql += ' ORDER BY lister_song.artist_id, lister_album.album_id, track_number'

    songs_list = []
    track_index = 0
    cursor.execute(sql, search_params)
    row = cursor.fetchone()
    while (row):
        row_type = track_index % 2
        songs_list.append(
            {'title': row[0], 'album': row[1], 'artist': row[2], 'image_file': row[3], 'path': row[4], 'year': row[5], 'track': row[6], 'row_type': row_type, 'track_index': track_index})
        track_index += 1
        row = cursor.fetchone()

    context = {'songs_list': songs_list,
               'counters': get_counters(), 'section': section}
    return JsonResponse(context)


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
