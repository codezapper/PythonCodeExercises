from django.db import connection
from django.http import JsonResponse
import random

inner_sql = '(search_key like %s)'
selecting_tables = ['lister_song', 'lister_album', 'lister_artist']
selecting_fields = ['title', 'lister_album.description album',
                    'lister_artist.description artist', 'image_file',
                    'path', 'year', 'track_number', 'lister_song.id song_id']
common_conditions = ['lister_artist.artist_id = lister_song.artist_id',
                     'lister_album.album_id = lister_song.album_id']
sorting_fields = ['artist', 'album', 'track_number']


def get_single_random(songs_list):
    return [random.choice(songs_list)]


def get_shuffled_list(songs_list):
    random.shuffle(songs_list)
    return songs_list


do_something = {
    'random': get_single_random,
    'shuffle': get_shuffled_list
}


def data_for_songs_list(request, search_string=''):
    if (search_string == ''):
        return JsonResponse({})

    search_filters = get_search_filters(search_string)
    search_words = [word for word in search_string.split() if ':' not in word]

    results_lookup = {}
    songs_list = []

    if (len(search_filters) > 0):
        (queries, params, filter_actions) = get_filters_queries(search_filters)
        query_index = 0
        for query in queries:
            results = get_rows_as_dict(
                query, params[query_index], results_lookup)
            if (len(results) > 0):
                if (filter_actions[query_index]):
                    songs_list.extend(
                        do_something[filter_actions[query_index]](results))
                else:
                    songs_list.extend(results)
            query_index += 1

    if (len(search_words) > 0):
        songs_list.extend(get_rows_as_dict(*get_word_query_sql(search_words),
                                           lookup=results_lookup))

    return JsonResponse({
        'songs_list': songs_list,
        'counters': get_counters()
    })


def get_rows_as_dict(sql, params, lookup={}):
    results = []
    cursor = connection.cursor()
    cursor.execute(sql, params)
    row_dict = _row_as_dict(cursor.fetchone())
    while (row_dict is not None):
        if (lookup.get(row_dict['song_id']) is None):
            lookup[row_dict['song_id']] = 1
            results.append(row_dict)
        row_dict = _row_as_dict(cursor.fetchone())

    return results


def get_search_filters(search_string):
    search_filters = []
    if ':' in search_string:
        for search_word in search_string.split():
            if ':' in search_word:
                tmp_filter = []
                for search_filter in search_word.split(':'):
                    if (search_filter != ''):
                        tmp_filter.append(search_filter)
                search_filters.append(tmp_filter)
    return search_filters


def get_filters_queries(search_filters):
    global inner_sql
    single_queries = []
    filter_actions = []
    for search_filter in search_filters:
        if (search_filter[0] in do_something.keys()):
            if (len(search_filter) > 1):
                filter_actions.append(search_filter[0])
                search_filter.pop(0)
        else:
            filter_actions.append(None)
        query_strings = [inner_sql] * len(search_filter)
        single_queries.append('(' + ' AND '.join(query_strings) + ') ')

    single_statements = []
    index = 0
    for single_query in single_queries:
        sql = 'SELECT ' + ','.join(selecting_fields) + \
              ' FROM ' + ','.join(selecting_tables) + \
              ' WHERE ' + ' AND '.join(common_conditions) + \
              ' AND ' + single_query + \
              ' ORDER BY ' + ','.join(sorting_fields)
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


def get_word_query_sql(search_words):
    global inner_sql

    single_statements = [
        'SELECT ' + ','.join(selecting_fields) +
        ' FROM ' + ','.join(selecting_tables) +
        ' WHERE ' + ' AND '.join(common_conditions) +
        ' AND ' + inner_sql
    ] * len(search_words)
    word_query = ' UNION '.join(
        single_statements) + ' ORDER BY ' + ','.join(sorting_fields)
    search_params = []
    for search_word in search_words:
        search_params.append('%' + search_word + '%')
    return (word_query, search_params)


def _row_as_dict(row):
    if (row is None):
        return None

    return {
        'title': row[0], 'album': row[1], 'artist': row[2],
        'image_file': row[3], 'path': row[4], 'year': row[5],
        'track': row[6], 'song_id': row[7]
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
