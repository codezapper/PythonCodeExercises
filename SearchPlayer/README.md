# SearchPlayer

The purpose of this project is to provide a "power user" kind of interface for a desktop music player.
The basic idea is that for power users, typing is faster than clicking.

**DEPENDENCIES NOTE**: This project is still in development. At the moment it is usable, but glitches may occur. Specifically, the interface is not responsive and works mostly for resolutions above 1024x768.
It depends on the modules:
  - `django-mathfilters`
  - `glob2`

**COMPATIBILITY NOTE**: To keep the player compatible cross-browser, the code will first check if the browser supports MP3 file playback. If it doesn't, it will look for a file with the same name, but extension '.ogg'

## Usage

![main interface](https://raw.githubusercontent.com/codezapper/PythonCodeExercises/master/SearchPlayer/search_player_screenshot.png)

A basic search will return results that include the search term in the artist name, album name or song title.
When more search terms are used, the results include *ANY* of the terms.
To filter the results using *ALL* of the terms, it's possible to combine multiple terms with a ":" (colon) separator.

For instance:
  - `meta` will return all matches from the word "meta" (e.g. "metallica")
  - `meta mega` will return all matches from the words "meta" *OR* "mega" (e.g. "metallica" or "megadeth")
  - `meta:one` will return all matches from the words "meta" *AND* "one" (e.g. song "one" by "metallica")
  - `meta:one mega` will return all matches from the words "meta" *AND* "one" plus all the matches from the word "mega" (e.g. song "one" by "metallica" plus all songs by "megadeth")

The standard search is done on a search key based on the combination of the three elements, so that looking for multiple words
in a single song can also be done by typing the title with no spaces (e.g. "blackice" will return the album "black ice").

The regex search is done applying the regular expression ONLY to the title.
This is not really for performance issues, but more for making it so that the query results are more intuitive.

There are two reserved words in the search:
  - "random" will pick a single result out of the current single query. This is done for a single search term. For instance:
    - `random:meta` will return a random match for the word "meta"
    - `random:meta:one` will return a random match for the word "meta" combined with the word "one"
    - `random:meta:one mega` will return a random match for the word "meta" combined with the word "one" plus all the matches for the word "mega"
  - "shuffle" will shuffle the results randomly for the current single query. By default, results are ordered by artist / album / track number. For instance:
    - `shuffle:meta` will return all result for the word "meta", but they will be randomly shuffled.
    - `shuffle:meta:one` will return all result for the word "meta:one", but they will be randomly shuffled.
    - `shuffle:meta:one mega` will return all result for the word "meta:one", but they will be randomly shuffled plus all the matches for the word "mega" which will instead be ordered as default.

The "random" and "shuffle" reserved words must be the first word in the current query.

## Keyboard

Pressing the enter key will either:
  - start playback if a song is *NOT* already being played.
  - add the results to the queue if a song is already being played.
  - add the results to the top of the queue if the *SHIFT* button is also pressed.
  - replace the current playlist with the current results if the *CTRL* button is also pressed.

Pressing the arrow down button will move to the next track.
Pressing the arrow up button will move to the prev track.

Pressing the Ctrl+X combination will enable regex mode. This will apply regular expressions to title, artist, album and show the results of those three matches combined. It is still possible to filter using the ":" (colon) separator as specified above.

## Setup

This project is done entirely in Python+Django and Javascript, so a working Python+Django environment is needed.
The database is a sqlite3 file, so it can be redistributed easily as a demo.

The "file_indexer.py" script will insert in the database the titles and paths of the music files.
It can be configured so that it reads files from a specific directory, the default one is "Music/" from where the script is run.
It works by reading the MP3 files metadata, so if some fields are missing, check that the metadata in the MP3 files is correct.
