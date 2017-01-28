import glob2
import taglib
import sqlite3
import os.path


def get_files():
    return glob2.glob('Music/**/*.mp3')


def update_db():
    db_main = sqlite3.connect('db.sqlite3')
    cursor = db_main.cursor()
    songs = []
    albums = []
    artists = []
    album_id = 0
    artist_id = 0
    album_lookup = {}
    artist_lookup = {}
    for file in get_files():
        song = taglib.File(file)
        if (not song.tags['ALBUM'][0] in album_lookup):
            album_id += 1
            album_lookup[song.tags['ALBUM'][0]] = album_id
            albums.append((album_id, song.tags['ALBUM'][0]))
        if (not song.tags['ARTIST'][0] in artist_lookup):
            artist_id += 1
            artist_lookup[song.tags['ARTIST'][0]] = artist_id
            artists.append((artist_id, song.tags['ARTIST'][0]))
        songs.append((album_id, artist_id, os.path.dirname(os.path.realpath(file)) + '/Folder.jpg',
                      song.tags['DATE'][0], 0, song.tags['TITLE'][0], song.tags['TRACKNUMBER'][0], file))

    cursor.execute('DELETE FROM lister_song')
    cursor.executemany(
        'INSERT INTO lister_song (album_id, artist_id, image_file, year, rating, title, track_number, path) VALUES(?, ?, ?, ?, ?, ?, ?, ?)', songs)

    cursor.execute('DELETE FROM lister_album')
    cursor.executemany(
        'INSERT INTO lister_album (album_id, description) VALUES(?, ?)', albums)

    cursor.execute('DELETE FROM lister_artist')
    cursor.executemany(
        'INSERT INTO lister_artist (artist_id, description) VALUES(?, ?)', artists)

    db_main.commit()


if __name__ == '__main__':
    update_db()
