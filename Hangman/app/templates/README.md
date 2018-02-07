*Hangman**


***Description***


This is a simple implementation of the hangman game.

- Purpose of the game is to guess the word by choosing one character at a time.
- When the game starts you can use the keyboard to input the letter that you want to try.
- In this version a maximum of six mistakes are allowed before game over.
- You start with 60 points, and for every mistake you lose 10 points.
- Game is over when you've used up all your possible mistakes or the word has been completely uncovered.
- If at the end of the game your score is higher than your current high score, it will be saved as your new highscore.
- On game over you can use the `n` key to start a new game.


***Setup***


The project is done with Python and Flask as a web framework.
The current dependencies are:
- flask
- flask-login
- flask-migrate
- flask-sqlalchemy
- flask-wtf
- sqlite

Once you have all the dependencies you can run a local instance by using the provided `run.sh` script, if you're on Linux or OS X.
If you're running on Windows, it should still be able to run with the `flask run hangman` command, but I don't officially support it.


***Technical details***

The game requires a login for you to be able to play, and that is true also for the API calls in case you want to build a different client for it (maybe with better graphics?).

- `<server>/hangman/new_word`: This call will choose a new word and return a JSON containing the length of the word and the initial score. It is used to start a new game. The word will be the same for the duration of the session.
Sample JSON output:


- `<server>/hangman/character?c=<character>`: This call will match the character against the current chosen word. It will return a JSON with the partial unmasked word, a boolean indicating whether it was a successful match or not, the updated score, and a boolean indicating whether it game over or not.
Sample JSON output:

