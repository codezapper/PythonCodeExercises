from django.db import connection
from django.http import JsonResponse
import random

inner_sql = '(artist like %s or album like %s or title like %s)'
selecting_tables = ['lister_song', 'lister_album', 'lister_artist']
selecting_fields = ['title', 'lister_album.description album',
                    'lister_artist.description artist', 'image_file',
                    'path', 'year', 'track_number', 'lister_song.id song_id']
common_conditions = ['lister_artist.artist_id = lister_song.artist_id',
                     'lister_album.album_id = lister_song.album_id']
sorting_fields = ['lister_song.artist_id',
                  'lister_album.album_id', 'track_number']


def data_for_songs_list(request, search_string=''):
    if (search_string == ''):
        return JsonResponse({})

    all_words = search_string.split()
    search_filters = []

    if ':' in search_string:
        for search_word in all_words:
            if ':' in search_word:
                tmp_filter = []
                for search_filter in search_word.split(':'):
                    if (search_filter != ''):
                        tmp_filter.append(search_filter)
                search_filters.append(tmp_filter)

    search_words = [
        search_word for search_word in all_words if ':' not in search_word]

    search_params = []
    cursor = connection.cursor()
    sql = ''
    word_query_sql = ''
    songs_list = []
    results_lookup = {}

    if (len(search_filters) > 0):
        (sql_queries, params, must_shuffle) = get_filters_sql(search_filters)
        query_index = 0
        for sql_query in sql_queries:
            cursor.execute(sql_query, params[query_index])
            row = cursor.fetchone()
            results = []
            while (row):
                if (results_lookup.get(row[7]) is None):
                    results_lookup[row[7]] = 1
                    results.append(_row_as_dict(row))
                row = cursor.fetchone()
            if (must_shuffle[query_index]):
                songs_list.extend(random.shuffle(results))
            else:
                songs_list.extend(results)
            query_index += 1

    if (len(search_words) > 0):
        (word_query_sql, params) = get_word_query_sql(search_words)
        search_params.extend(params)
        sql = word_query_sql

    cursor.execute(sql, search_params)
    row = cursor.fetchone()
    while (row):
        if (results_lookup.get(row[7]) is None):
            results_lookup[row[7]] = 1
            songs_list.append({
                'title': row[0],
                'album': row[1],
                'artist': row[2],
                'image_file': row[3],
                'path': row[4],
                'year': row[5],
                'track': row[6],
            })
        row = cursor.fetchone()

    context = {'songs_list': songs_list,
               'counters': get_counters()}
    return JsonResponse(context)


def get_filters_sql(search_filters):
    global inner_sql
    single_queries = []
    must_shuffle = []
    for search_filter in search_filters:
        if (search_filter[0] == 'shuffle'):
            search_filter.pop(0)
            must_shuffle.append(True)
        else:
            must_shuffle.append(False)
        query_strings = [inner_sql] * len(search_filter)
        single_queries.append('(' + ' AND '.join(query_strings) + ') ')

    single_statements = []
    index = 0
    for single_query in single_queries:
        sql = 'SELECT ' + ','.join(selecting_fields) + ' FROM ' + \
            ','.join(selecting_tables) + ' WHERE ' + \
            ' AND '.join(common_conditions) + ' AND ' + \
            single_query + ' ORDER BY ' + ','.join(sorting_fields)
        single_statements.append(sql)
        index += 1

    search_params = []
    new_search_params = []
    for search_filter in search_filters:
        temp_params = []
        for filter_term in search_filter:
            search_params.extend(['%' + filter_term + '%'] * 3)
            temp_params.extend(['%' + filter_term + '%'] * 3)
        new_search_params.append(temp_params)

    return (single_statements, new_search_params, must_shuffle)


def get_word_query_sql(search_words):
    global inner_sql
    single_statements = []
    for i in (range(len(search_words))):
        single_statements.append(
            'SELECT ' + ','.join(selecting_fields) + ' FROM ' +
            ','.join(selecting_tables) + ' WHERE ' +
            ' AND '.join(common_conditions) + ' AND ' + inner_sql)
    word_query = ' UNION '.join(
        single_statements) + ' ORDER BY ' + ','.join(sorting_fields)
    search_params = []
    for search_word in search_words:
        for i in range(0, 3):
            search_params.append('%' + search_word + '%')
    return (word_query, search_params)


def _row_as_dict(row):
    return {
        'title': row[0], 'album': row[1], 'artist': row[2],
        'image_file': row[3], 'path': row[4], 'year': row[5], 'track': row[6]
    }


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
