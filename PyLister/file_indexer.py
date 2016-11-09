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
    for file in get_files():
        song = taglib.File(file)
        songs.append((song.tags['ALBUM'][0], song.tags['ARTIST'][
            0], os.path.dirname(os.path.realpath(file)) + '/Folder.jpg', song.tags['DATE'][0], 0, song.tags['TITLE'][0], file))
    cursor.execute('DELETE FROM lister_song')
    cursor.executemany(
        'INSERT INTO lister_song (album, artist, image_file, year, rating, title, path) VALUES(?, ?, ?, ?, ?, ?, ?)', songs)

    db_main.commit()

if __name__ == '__main__':
    update_db()
