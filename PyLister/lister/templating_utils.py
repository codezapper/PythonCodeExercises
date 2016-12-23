from django.db import connection
from django.template import loader
import data_utils as du


def render_wrapper(request):
    template = loader.get_template('lister/wrapper.html')
    context = {'counters': get_counters()}

    return template.render(context, request)


def render_for_songs_list(request, album='', artist='', year=''):
    template = loader.get_template('lister/songs.html')
    context = {}
    return template.render(context, request)


def template_for_albums_overview(request):
    template = loader.get_template('lister/albums_with_menu.html')
    context = {'albums_list': du.data_for_albums_overview(),
               'counters': get_counters(), 'section': 'album'}
    return template.render(context, request)


def template_for_artists_overview(request):
    template = loader.get_template('lister/artists_with_menu.html')
    context = {'artists_list': du.data_for_artists_overview(),
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
