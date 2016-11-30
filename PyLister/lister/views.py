from django.db import connection
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from .models import Song
import os
import utils
import templating_utils as tu
from streaming_utils import StreamWrapper


def index(request):
    return songs(request)


def songs(request):
    return HttpResponse(tu.render_for_songs_list(request))


def albums(request, album_id=''):
    if (album_id == ''):
        return HttpResponse(tu.render_for_albums_list(request))
    return HttpResponse(tu.render_for_songs_list(request, album_id))


def artists(request, artist_id=''):
    if (artist_id == ''):
        return HttpResponse(tu.render_for_artists_list(request))
    return HttpResponse(tu.render_for_songs_list(request, '', artist_id))


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
    response = HttpResponse(content_type = 'audio/mpeg', status=206)
    response['Content-Disposition'] = "attachment; filename=%s" % (file_path)
    response['Accept-Ranges'] = 'bytes'
    # response['X-Accel-Redirect'] = settings.MEDIA_URL + '/' + fileModel.FileData.MD5
    response['X-Accel-Buffering'] = 'no'
    return response

    # file_path = utils.get_path_by_id(song_id)
    # streaming_response = HttpResponse(StreamWrapper(
    #     file_path), content_type='audio/mpeg')
    # streaming_response[
    #     'Content-Length'] = os.path.getsize(file_path)
    # streaming_response['Content-Disposition'] = 'filename=' + \
    #     os.path.basename(file_path)
    # return streaming_response
