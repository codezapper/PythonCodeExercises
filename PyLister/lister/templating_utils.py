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
