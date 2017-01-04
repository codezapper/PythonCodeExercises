from django.http import HttpResponse, Http404
from django.shortcuts import render
from .models import Song
import os
import utils
import data_utils as du
import templating_utils as tu
from streaming_utils import StreamWrapper


def search(request, search_string=''):
    return HttpResponse(du.data_for_songs_list(request, search_string))


def albums_data(request, album_id=''):
    if (album_id == ''):
        return HttpResponse(du.data_for_albums_list(request))
    return HttpResponse(du.data_for_songs_list(request, '', album_id))


def artists_data(request, artist_id=''):
    if (artist_id == ''):
        return HttpResponse(du.data_for_artists_list(request))
    return HttpResponse(du.data_for_songs_list(request, '', artist_id))


def years_data(request, year_id=''):
    if (year_id == ''):
        return HttpResponse(du.data_for_years_list(request))
    return HttpResponse(du.data_for_songs_list(request, '', '', '', year_id))


def index(request):
    return HttpResponse(tu.render_wrapper(request))


def songs(request):
    return HttpResponse(tu.render_for_songs_list(request))


def albums(request, album_id=''):
    return HttpResponse(tu.template_for_albums_overview(request))


def artists(request, artist_id=''):
    return HttpResponse(tu.template_for_artists_overview(request))


def years(request, year=''):
    if (year == ''):
        return HttpResponse(tu.render_for_years_list(request))
    return HttpResponse(tu.render_for_songs_list(request, '', '', year))


def detail(request, song_id):
    try:
        song = Song.objects.get(pk=song_id)
    except Song.DoesNotExist:
        raise Http404("Song does not exist")
    return render(request, 'lister/detail.html', {'song': song})


def play(request, song_id):
    file_path = utils.get_path_by_id(song_id)
    streaming_response = HttpResponse(StreamWrapper(
        file_path), content_type='audio/mpeg')
    streaming_response[
        'Content-Length'] = os.path.getsize(file_path)
    streaming_response['Content-Disposition'] = 'filename=' + \
        os.path.basename(file_path)
    return streaming_response
