import glob2
from .models import Song


def get_files():
    return glob2.glob('/home/gabriele/Music/**/*.mp3')


def get_path_by_id(song_id):
    return '/home/gabriele/' + Song.objects.filter(id=song_id)[0].path
