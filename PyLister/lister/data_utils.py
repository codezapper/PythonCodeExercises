from django.db import connection
from django.http import JsonResponse


def data_for_songs_list(request, search_string=''):
    if (search_string == ''):
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
        (filter_query, query_params) = get_data_for_search_filters(search_filters)
        search_params.extend(query_params)

    if (len(search_words) > 0):
        (word_query, query_params) = get_data_for_search_words(search_words)
        search_params.extend(query_params)

    if (len(search_filters) > 0) and (len(search_words) > 0):
        sql += ' AND (' + filter_query + ' OR ' + word_query + ')'
    elif len(search_filters) > 0:
        sql += ' AND ' + filter_query
    elif len(search_words) > 0:
        sql += ' AND ' + word_query

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


def get_data_for_search_filters(search_filters):
    single_queries = []
    for search_filter in search_filters:
        query_strings = ['(artist like %s or album like %s or title like %s)'] * len(search_filter)
        single_queries.append(' AND '.join(query_strings))

    filter_query = ' (' + ' OR '.join(single_queries) + ') '

    search_params = []
    for search_filter in search_filters:
        for filter_term in search_filter:
            search_params.extend(['%' + filter_term + '%'] * 3)

    return (filter_query, search_params)


def get_data_for_search_words(search_words):
    string_conditions = []
    for i in (range(len(search_words))):
        string_conditions.append(
            '( title like %s or lister_album.description like %s or lister_artist.description like %s)')
    word_query = '(' + ' OR '.join(string_conditions) + ')'
    search_params = []
    for search_word in search_words:
        for i in range(0, 3):
            search_params.append('%' + search_word + '%')
    return (word_query, search_params)


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
