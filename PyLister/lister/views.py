from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from .models import Song
import utils


def index(request):
    songs_list = [song
                  for song in Song.objects.order_by('-year')]
    template = loader.get_template('lister/index_with_menu.html')
    context = {'songs_list': songs_list, }
    return HttpResponse(template.render(context, request))


def detail(request, song_id):
    try:
        song = Song.objects.get(pk=song_id)
    except Song.DoesNotExist:
        raise Http404("Song does not exist")
    return render(request, 'lister/detail.html', {'song': song})


def vote(request, song_id):
    return HttpResponse("You're voting on song %s." % song_id)
