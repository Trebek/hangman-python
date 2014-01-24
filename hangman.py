#===============================================================================
# Hangman, in Python
#-------------------------------------------------------------------------------
# Version: 1.1.0
# Updated: 24-01-2014
# Author: Alex Crawford
# License: MIT
#===============================================================================

"""Overly complex Hangman, in Python (2.7.5)"""

#===============================================================================
# IMPORTS
#===============================================================================

import os
import random

#===============================================================================
# THE GAME
#===============================================================================

class Hangman(object):
    """Contains all of the methods the game needs."""

    ASCII_DICT = {
        0: [
            " +----+ ",
            " |/   | ",
            " |      ",
            " |      ",
            " |      ",
            " |      ",
            "========",
        ],
        1: [
            " +----+ ",
            " |/   | ",
            " |    O ",
            " |      ",
            " |      ",
            " |      ",
            "========",
        ],
        2: [
            " +----+ ",
            " |/   | ",
            " |    O ",
            " |    | ",
            " |      ",
            " |      ",
            "========",
        ],
        3: [
            " +----+ ",
            " |/   | ",
            " |    O ",
            " |   /| ",
            " |      ",
            " |      ",
            "========",
        ],
        4: [
            " +----+ ",
            " |/   | ",
            " |    O ",
            " |   /|\\ ",
            " |      ",
            " |      ",
            "========",
        ],
        5: [
            " +----+ ",
            " |/   | ",
            " |    O ",
            " |   /|\\ ",
            " |   /  ",
            " |      ",
            "========",
        ],
        6: [
            " +----+ ",
            " |/   | ",
            " |    O ",
            " |   /|\\ ",
            " |   / \\ ",
            " |      ",
            "========",
        ],
    }

    WORDS_DICT = {
        1: [],
        2: [],
        3: []
    }

    QUIT_MSGS = [
        "I hope you enjoyed playing! Good bye.\n",
        "May the force be with you.\n",
        "Live long, and prosper.\n",
        "Good bye, Mr. Anderson.\n",
        "Thank you! Come again!\n",
        "Something better to do?\n",
        "You'll be back...\n",
        "Later, alligator.\n",
        "Leaving so soon?\n",
        "The end.\n"
    ]

    GAME_OVER_MSGS = [
        "Game over, man! Game over!\n",
        "Better luck next time!\n",
        "Mission failed.\n",
        "Good thing it's only a game.\n",
        "Fatality!\n",
        "FUUUUUUUUUUU!\n",
        "Bummer, dude.\n",
        "GAME OVER.\n",
        "You can't win 'em all.\n",
        "Try, try again.\n"
    ]

    EXIT_WORDS = ["/q", "/exit", "/quit", "/end"]

    HORIZ_RULE = ("-" * 40)

    STATE_SETWORD = 1
    STATE_GUESS = 2
    STATE_END = 3
    STATE_QUIT = 4

    DIFF_EASY = 1
    DIFF_MEDIUM = 2
    DIFF_HARD = 3

    LIVES_EASY = 5
    LIVES_MEDIUM = 3
    LIVES_HARD = 1

    WORDS_FILENAME = "words.txt"

    GAME_TITLE = "HANGMAN, IN PYTHON"
    GAME_SUBTITLE = "A Game by Alex Crawford"
    GAME_VERSION = "v1.1.0"

    def __init__(self):
        """Game initialization method."""

        self.running = True
        self.game_state = self.STATE_SETWORD

        self.ascii_index = 0

        self.word = None
        self.word_hidden = []
        self.word_level = 1

        self.guess = None
        self.guessed = []
        self.guesses_left = 6
        
        self.diff_level = 2
        self.lives = 3
        self.score = 0
        self.score_total = 0

    def check_guess(self):
        """Checks the player's guess for a correct letter, and
        calls 'self.word_hide_set' which reconstructs the hidden 
        version of the word, with any correct letters filled in.

        """
        temp_hidden = []
        correct = False

        if self.guess.upper() not in self.guessed:
            self.guessed.append(self.guess[0].upper())
        else:
            print "\nYou've already guessed that letter!"
            self.ascii_index += 1
            self.guesses_left -= 1
            return

        for letter in self.word:
            letter_upper = letter.upper()
            if letter_upper == self.guess[0].upper():
                correct = True
                break

        if correct:
            print "\nGood guess! Don't let it go to your head though."
        elif not correct and self.guess.lower() not in self.EXIT_WORDS:
            self.ascii_index += 1
            self.guesses_left -= 1
            if self.guesses_left < 5 and self.score > 0:
                self.score -= 1
            print "\nIncorrect. No one can be right all of the time."

        self.word_hide_set()

    def check_word_level(self):
        """Checks the level the player is on, and whether the player 
        has solved all of the words in that level. If so, the player 
        is moved up a level.

        """
        if (self.lives > 0 and self.word_level < len(self.WORDS_DICT) and 
                len(self.WORDS_DICT[self.word_level]) == 0 and 
                len(self.WORDS_DICT[self.word_level + 1]) > 0):
            self.word_level = self.word_level + 1
            print "You've made it to level {0}!\n".format(self.word_level)

    def file_open_words(self):
        """Opens a file named 'words.txt' (by default), if it's present, 
        and uses that for the word list.

        """
        try:
            with open(self.WORDS_FILENAME, "r") as words_txt:
                words_temp = words_txt.read()
                words_temp = words_temp.splitlines()

                word_keys = self.WORDS_DICT.keys()

                for key in word_keys:
                    self.WORDS_DICT[key] = []

                self.sort_words(words_temp)

            print "Word list loaded successfully.\n"
        except:
            raise IOError(self.WORDS_FILENAME)

    def no_guesses_left(self):
        """Checks whether the player has any guesses left."""

        if self.guesses_left == 0:
            self.print_info()
            print "You've run out of guesses... Sorry about that.\n"
            print "The word was: " + self.word.upper() + "\n"
            self.lives -= 1
            return True
        else:
            return False

    def no_lives_left(self):
        """Checks whether the player has any lives left."""

        score_str = "Final score: {0}/{1}\n".format(self.score, 
                    self.score_total)

        if self.lives == 0:
            self.clear()
            print "All of your men have been hanged!\n"
            print random.choice(self.GAME_OVER_MSGS)
            print score_str
            return True
        else:
            return False

    def no_words_left(self):
        """Checks whether there are any words left to solve."""

        score_str = "Final score: {0}/{1}\n".format(self.score, 
                    self.score_total)

        if (len(self.WORDS_DICT[1]) == 0 and 
                len(self.WORDS_DICT[2]) == 0 and 
                len(self.WORDS_DICT[3]) == 0):
            self.clear()
            print "There are no more words left to solve.\n"
            print "Congratulations, you made it out alive!\n"
            if self.score == self.score_total:
                print "You got a perfect score! Truly impressive.\n"
            print score_str
            return True
        else:
            return False

    def clear(self):
        """OS dependant screen clear."""

        if os.name == "nt":
            os.system("cls")
        elif os.name == "posix":
            os.system("clear")

    def play(self):
        """The main game loop."""

        self.clear()

        self.print_title(
            self.GAME_TITLE, 
            self.GAME_SUBTITLE, 
            self.GAME_VERSION
        )

        self.query_difficulty()
        self.file_open_words()
        self.score_total_set()

        print "Enter '/q' as a guess to quit.\n"

        print self.HORIZ_RULE + "\n"

        while self.running:
            
            while self.game_state == self.STATE_SETWORD:
                self.word_set()
                self.word_hide_set()
                self.game_state = self.STATE_GUESS
                break
                 
            while self.game_state == self.STATE_GUESS:
                self.print_info()
                self.query_guess()
                self.check_guess()

                print "\n" + self.HORIZ_RULE + "\n"

                if self.no_guesses_left() or self.word_solved():
                    self.game_state = self.STATE_END
                    break

            while self.game_state == self.STATE_END:
                self.WORDS_DICT[self.word_level].remove(self.word)
                self.check_word_level()
                self.reset_guesses()

                print self.HORIZ_RULE + "\n"

                if self.no_lives_left() or self.no_words_left():
                    play_more = raw_input("Would you like to play again? ")
                    if play_more in ["y", "Y"]:
                        self.reset_game()
                    else:
                        self.running = False
                        break
                self.game_state = self.STATE_SETWORD
                break

            while self.game_state == self.STATE_QUIT:
                self.running = False
                score_str = "Final score: {0}/{1}\n".format(self.score, 
                            self.score_total)
                self.clear()
                print random.choice(self.QUIT_MSGS)
                print score_str
                break

    def print_info(self):
        """Prints the current hangman art, and other relevant information."""

        info_str = "Level: {0} | Lives: {1} | Score: {2}\n"
        print info_str.format(self.word_level, self.lives - 1, self.score)
        print "Guesses: {0}".format(" ".join(sorted(self.guessed)))
        print "Left: {0}\n".format(self.guesses_left)
        for line in self.ASCII_DICT[self.ascii_index]:
            print line
        print
        print "{0}\n".format(" ".join(self.word_hidden))

    def print_title(self, title, subtitle=None, version=None, nl=True):
        """Prints a title, with horizontal rules above and below it. 
        Also prints a subtitle below the title, and/or version, 
        if provided.

        """
        print "\n" + self.HORIZ_RULE
        print title
        print self.HORIZ_RULE
        if subtitle:
            print subtitle
        if version:
            print version
        if subtitle or version:
            print self.HORIZ_RULE
        if nl:
            print

    def query_difficulty(self):
        """Queries the player about what difficulty level they 
        would like to play at. 

        """
        diff_names = {1: "easy", 2: "medium", 3: "hard"}

        diff_str = "\nDifficulty set to {0} ({1})\n"

        command = raw_input("Difficulty level? (1-3) ")

        if command == "1":
            self.diff_level = self.DIFF_EASY
            self.lives = self.LIVES_EASY
        elif command == "2":
            self.diff_level = self.DIFF_MEDIUM
            self.lives = self.LIVES_MEDIUM
        elif command == "3":
            self.diff_level = self.DIFF_HARD
            self.lives = self.LIVES_HARD
        else:
            self.diff_level = self.DIFF_MEDIUM
            self.lives = self.LIVES_MEDIUM

        diff_name = diff_names[self.diff_level]

        print diff_str.format(diff_name, self.diff_level)

    def query_load_file(self):
        """Queries the player about whether or not they'd like to
        load the words from a txt file.

        """
        command = raw_input("Load the word list from a file? (y/n) ")
        
        try:
            if command in ["", "Y", "y"]:
                self.file_open_words()
                print "\nWord file loaded."
            else:
                print "\nDefault words loaded."
        except:
            print "\nCouldn't load file. Loading default words."
            pass

    def query_guess(self):
        """Get the player's guess."""

        while True:
            self.guess = raw_input("Guess: ")
            if self.guess.isalpha() and self.guess is not "":
                break
            elif self.guess.lower() in self.EXIT_WORDS:
                self.game_state = self.STATE_QUIT
                break
            else:
                print "\nInvalid guess. Must be a letter.\n"

    def reset_game(self):
        """Resets all of the required game variables, for a new game."""

        self.reset_guesses()
        self.game_state = self.STATE_SETWORD
        self.word_level = 1
        self.word = None
        self.word_hidden = []
        self.score = 0
        self.play()

    def reset_guesses(self):
        """Resets the guesses, and ascii key, and guesses left."""

        self.guess = None
        self.guessed = []
        self.ascii_index = 0
        self.guesses_left = 6

    def score_total_set(self):
        """Figures the total potential score for the game."""

        self.score_total = sum(
            [20 for words in self.WORDS_DICT.values() for word in words]
            )

    def sort_words(self, wordlist):
        """Sorts a given list of words into separate lists,
        for each word level, based on their length.

        """
        for word in wordlist:
            if len(word) in range(1, 5):
                self.WORDS_DICT[1].append(word)
            elif len(word) == 5:
                self.WORDS_DICT[2].append(word)
            else:
                self.WORDS_DICT[3].append(word)

    def word_hide_set(self):
        """Generates a hidden version of the current word."""

        temp_hidden = []

        for letter in self.word:
            letter_upper = letter.upper()
            if self.guess and letter_upper in self.guessed:
                temp_hidden.append(letter_upper)
            else:
                temp_hidden.append('_')
        
        self.word_hidden = temp_hidden

    def word_set(self):
        """Gets a random word from the list of words, and sets it 
        as the current word ('self.word').

        """
        if len(self.WORDS_DICT[self.word_level]) > 0:
            self.word = random.choice(self.WORDS_DICT[self.word_level])
        else:
            print "\nOops! No words to load. Exiting.\n"
            exit()

    def word_solved(self):
        """Checks whether the player has solved the word."""

        if "".join(self.word_hidden) == self.word.upper():
            print "{0}!\n".format(self.word.upper())
            print "You solved the word! Exciting, I know."
            print "+10 points\n"
            self.score += 10
            if self.guesses_left == 6:
                print "You didn't make a single wrong guess!"
                print "+10 bonus points\n"
                self.score += 10
            return True
        else:
            return False

#===============================================================================
# IF __MAIN__
#===============================================================================

if __name__ == '__main__':
    try:
        Hangman().play()
    except IOError as error:
        print "Couldn't open '{0}'.".format(error)
