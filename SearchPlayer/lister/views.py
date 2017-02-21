from django.http import HttpResponse
import os
import utils.general as gu
import utils.data as du
import utils.templating as tu
from utils.streaming import StreamWrapper


def search(request, search_string=''):
    return HttpResponse(du.data_for_songs_list(request, search_string))


def index(request):
    return HttpResponse(tu.render_wrapper(request))


def songs(request):
    return HttpResponse(tu.render_for_songs_list(request))


def play(request, song_id):
    file_path = gu.get_path_by_id(song_id)
    streaming_response = HttpResponse(StreamWrapper(
        file_path), content_type='audio/mpeg')
    streaming_response[
        'Content-Length'] = os.path.getsize(file_path)
    streaming_response['Content-Disposition'] = 'filename=' + \
        os.path.basename(file_path)
    return streaming_response
