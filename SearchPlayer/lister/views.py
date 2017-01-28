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


def index(request):
    return HttpResponse(tu.render_wrapper(request))


def songs(request):
    return HttpResponse(tu.render_for_songs_list(request))


def play(request, song_id):
    file_path = utils.get_path_by_id(song_id)
    streaming_response = HttpResponse(StreamWrapper(
        file_path), content_type='audio/mpeg')
    streaming_response[
        'Content-Length'] = os.path.getsize(file_path)
    streaming_response['Content-Disposition'] = 'filename=' + \
        os.path.basename(file_path)
    return streaming_response
