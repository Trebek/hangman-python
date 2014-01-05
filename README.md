Hangman, in Python
=============================

My version of the classic word guessing game, Hangman. I'm sure there are much 
better/easier ways of making this game, and it's probably more elaborate than 
it needs to be, but it seems to work. Maybe I'll refine it a bit at some point. 
I wrote this from sratch, it is not based on anyone else's code, so if you use 
it, or modify it, please give me a little credit. It is all that I ask.

When playing, enter "/q" (or "/end", "/exit", or "/quit") as a guess to quit the 
game.

You can make your own txt file of words by following these three easy steps:
    
1. Create a new txt file, called "words.txt" in the same folder as this 
   game.
2. Open the txt file and enter each word on it's own line. 
3. Save the txt.

#### Features

- 3 main difficulty levels, determining the players starting men (lives).
- Words separated into 3 "word levels", depending on word length. When a player 
solves (or doesn't solve) all of the words in a level, the player is moved to 
the next level.
- Game keeps score.
- Easy to edit word list built into source, or you can load words from an easy 
to edit txt file of words.
- Displays the secret word, with any rightly guessed letters revealed.
- Displays all of the letters player has guessed, in alphabetical order.
- No duplicate words. Once a word is solved (or not), it's removed from the list.
    - When all of the words from every list have been solved (or not), the game 
    ends.
- Awesome ASCII art hangman! Okay, so it's not that awesome.

#### Relevant links

[Hangman Wikipedia Article](http://en.wikipedia.org/wiki/Hangman_(game))  
