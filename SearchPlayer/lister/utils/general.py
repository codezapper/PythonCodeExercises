import glob2
from ..models import Song


def get_files():
    return glob2.glob('Music/**/*.mp3')


def get_path_by_id(song_id):
    return Song.objects.filter(id=song_id)[0].path
