# SearchPlayer

The purpose of this project is to provide a "power user" kind of interface for a desktop music player.
The basic idea is that for power users, typing is faster than clicking.

## Usage

A basic search will return results that include the search term in the artist name, album name or song title.
When more search terms are used, the results include *ANY* of the terms.
To filter the results using *ALL* of the terms, it's possible to combine multiple terms with a ":" (colon) separator.

For instance:
  - "meta" will return all matches from the word "meta" (e.g. "metallica")
  - "meta mega" will return all matches from the words "meta" *OR* "mega" (e.g. "metallica" or "megadeth")
  - "meta:one" will return all matches from the words "meta" *AND* "one" (e.g. song "one" by "metallica")
  - "meta:one mega" will return all matches from the words "meta" *AND* "one" plus all the matches from the word "mega" (e.g. song "one" by "metallica" plus all songs by "megadeth")

The search is done on a search key based on the combination of the three elements, so that looking for multiple words
in a single song can also be done by typing the title with no spaces (e.g. "blackice" will return the album "black ice").

## Keyboard

Pressing the enter key will either:
  - start playback if a song is *NOT* already being played.
  - add the results to the queue if a song is already being played.
  - add the results to the top of the queue if the *SHIFT* button is also pressed.
  - replace the current playlist with the current results if the *CTRL* button is also pressed.

Pressing the arrow down button will move to the next track.
Pressing the arrow up button will move to the prev track.
