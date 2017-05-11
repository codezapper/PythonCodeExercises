'''
Handles all data queries, including filters
'''


import random
import os
from django.db import connection
from django.http import JsonResponse


INNER_SQL = '(search_key LIKE %s)'
INNER_SQL_REGEX = '(search_key REGEX %s)'
SELECTING_TABLES = ['lister_song', 'lister_album', 'lister_artist']
SELECTING_FIELDS = ['title', 'lister_album.description album',
                    'lister_artist.description artist', 'image_file',
                    'path', 'year', 'track_number', 'lister_song.id song_id']
COMMON_CONDITIONS = ['lister_artist.artist_id = lister_song.artist_id',
                     'lister_album.album_id = lister_song.album_id']
SORTING_FIELDS = ['artist', 'album', 'track_number']

if 'TESTING_DB' in os.environ:
    import sqlite3
    DB_CONNECTION = sqlite3.connect(os.environ.get('TESTING_DB'))
else:
    DB_CONNECTION = connection


def get_single_random(songs_list):
    return [random.choice(songs_list)]


def get_shuffled_list(songs_list):
    songs_list_copy = list(songs_list)
    random.shuffle(songs_list_copy)
    return songs_list_copy


PREFIXES = {
    'random': get_single_random,
    'shuffle': get_shuffled_list
}


def data_for_songs_list(request, search_string='', regex=False):
    if search_string == '':
        return JsonResponse({})

    search_filters = []
    for search_word in search_string.split():
        search_filters.append(get_search_filter(search_word))

    results_lookup = {}
    songs_list = []

    if search_filters:
        (queries, params, filter_actions) = get_filters_queries(search_filters)
        query_index = 0
        for query in queries:
            results = get_rows_as_dict(
                query, params[query_index], results_lookup)
            if results:
                if filter_actions[query_index]:
                    songs_list.extend(
                        PREFIXES[filter_actions[query_index]](results))
                else:
                    songs_list.extend(results)
            query_index += 1

    return JsonResponse({
        'songs_list': songs_list,
        'counters': get_counters()
    })


def get_rows_as_dict(sql, params, lookup={}):
    results = []
    cursor = DB_CONNECTION.cursor()
    cursor.execute(sql, params)
    row_dict = _row_as_dict(cursor.fetchone())
    while row_dict is not None:
        if lookup.get(row_dict['song_id']) is None:
            lookup[row_dict['song_id']] = 1
            results.append(row_dict)
        row_dict = _row_as_dict(cursor.fetchone())

    return results


def get_search_filter(search_word):
    search_filters = []

    for search_filter in search_word.split():
        if ':' in search_word:
            search_filters.extend(
                [refinement for refinement in search_word.split(':') if refinement != ''])
        else:
            search_filters.append(search_filter)

    return search_filters


def get_filters_queries(search_filters, regex=False):
    single_queries = []
    filter_actions = []
    for search_filter in search_filters:
        if search_filter[0] in PREFIXES.keys():
            if len(search_filter) > 1:
                filter_actions.append(search_filter[0])
                search_filter.pop(0)
        else:
            filter_actions.append(None)
        if regex:
            query_strings = [INNER_SQL_REGEX] * len(search_filter)
        else:
            query_strings = [INNER_SQL] * len(search_filter)
        single_queries.append('(' + ' AND '.join(query_strings) + ') ')

    single_statements = []
    index = 0
    for single_query in single_queries:
        sql = 'SELECT ' + ','.join(SELECTING_FIELDS) + \
              ' FROM ' + ','.join(SELECTING_TABLES) + \
              ' WHERE ' + ' AND '.join(COMMON_CONDITIONS) + \
              ' AND ' + single_query + \
              ' ORDER BY ' + ','.join(SORTING_FIELDS)
        single_statements.append(sql)
        index += 1

    search_params = []
    ret_search_params = []
    for search_filter_terms in search_filters:
        search_params = []
        for filter_term in search_filter_terms:
            search_params.extend(['%' + filter_term + '%'])
        ret_search_params.append(search_params)

    return (single_statements, ret_search_params, filter_actions)


def _row_as_dict(row):
    if row is None:
        return None

    return {
        'title': row[0], 'album': row[1], 'artist': row[2],
        'image_file': row[3], 'path': row[4], 'year': row[5],
        'track': row[6], 'song_id': row[7]
    }


def get_counters():
    counters = {}
    cursor = DB_CONNECTION.cursor()
    cursor.execute('''SELECT count(*) FROM lister_song''')
    counters['songs'] = cursor.fetchone()[0]
    cursor.execute('''SELECT count(*) FROM lister_album''')
    counters['albums'] = cursor.fetchone()[0]
    cursor.execute('''SELECT count(*) FROM lister_artist''')
    counters['artists'] = cursor.fetchone()[0]
    cursor.execute('''SELECT count(distinct year) FROM lister_song''')
    counters['years'] = cursor.fetchone()[0]

    return counters
