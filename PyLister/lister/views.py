from django.db.models import Count
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


def songs(request):
    songs_list = [song
                  for song in Song.objects.order_by('-year')]
    template = loader.get_template('lister/index_with_menu.html')
    context = {'songs_list': songs_list, }
    return HttpResponse(template.render(context, request))


def albums(request):
    albums_list = [album
                   for album in Song.objects.values('album').annotate(dcount=Count('album'))]
    template = loader.get_template('lister/index_with_menu.html')
    context = {'songs_list': albums_list, }
    return HttpResponse(template.render(context, request))


def artists(request):
    return HttpResponse('ARTISTS')


def years(request):
    return HttpResponse('YEARS')


def detail(request, song_id):
    try:
        song = Song.objects.get(pk=song_id)
    except Song.DoesNotExist:
        raise Http404("Song does not exist")
    return render(request, 'lister/detail.html', {'song': song})


def vote(request, song_id):
    return HttpResponse("You're voting on song %s." % song_id)
