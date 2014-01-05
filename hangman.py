#===============================================================================
# Hangman, in Python
#-------------------------------------------------------------------------------
# Version: 1.0.0
# Updated: 04-01-2014
# Author: Alex Crawford
# License: MIT
#===============================================================================

"""Overly complex object oriented Hangman, in Python (2.7.5)"""

#===============================================================================
# IMPORTS
#===============================================================================

from random import choice

#===============================================================================
# THE GAME
#===============================================================================

class Game(object):
    """Contains all of the methods the game needs."""

    WORDS_DICT = {
        1: [
            "Ape",
            "Cat",
            "Dog",
            "Eye",
            "Atom",
            "Foot",
            "Hand",
            "Rain"
        ],
        2: [
            "Apple"
            "Chair",
            "Clown",
            "Green",
            "Human",
            "Mouse",
            "Snake",
            "Paper"
        ],
        3: [
            "Almond",
            "Banana",
            "Cactus",
            "Desert",
            "Earwig",
            "Falcon",
            "Knight",
            "Python"
        ]
    }

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

    STATE_SETWORD = 1
    STATE_GUESS = 2
    STATE_END = 3
    STATE_EXIT = 4

    EXIT_WORDS = ["/q", "/exit", "/quit", "/end"]

    EXIT_MSGS = [
        "I hope you enjoyed playing! Good bye.\n",
        "May the force be with you.\n",
        "Good bye, Mr Anderson.\n",
        "Thank you! Come again!\n",
        "Something better to do?\n",
        "You'll be back...\n"
    ]

    WORDS_FILENAME = "words.txt"

    HRULE = ("-" * 40)

    def __init__(self):
        """Game initialization method."""

        self.word_level = 1
        self.word = None
        self.word_hidden = []

        self.guess = None
        self.guessed = []
        self.ascii_key = 0
        self.guesses_left = 6
        
        self.diff_level = 2
        self.lives = 3
        self.score = 0
        self.score_total = 0

        self.running = True
        self.game_state = self.STATE_SETWORD

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
            self.ascii_key += 1
            self.guesses_left -= 1
            return

        for letter in self.word:
            letter_upper = letter.upper()
            if letter_upper == self.guess[0].upper():
                correct = True

        self.word_hide_set()

        if correct:
            print "\nGood guess! Don't let it go to your head though."
        elif not correct and self.guess.lower() not in self.EXIT_WORDS:
            self.ascii_key += 1
            self.guesses_left -= 1
            if self.guesses_left < 5 and self.score > 0:
                self.score -= 1
            print "\nIncorrect. No one can be right all of the time."

    def check_word_level(self):
        """Checks the level the player is on, and whether the player 
        has solved all of the words in that level. If so, the player 
        is moved up a level.

        """
        if self.word_level == 1:
            if len(self.WORDS_DICT[1]) == 0 and len(self.WORDS_DICT[2]) > 0:
                self.word_level = 2
                print "You've progressed to level 2!\n"
        elif self.word_level == 2:
            if len(self.WORDS_DICT[2]) == 0 and len(self.WORDS_DICT[3]) > 0:
                self.word_level = 3
                print "You've progressed to level 3!\n"

    def file_open_words(self):
        """Opens a file named 'words.txt', if it's present, and uses
        that for the word list.

        """
        with open(self.WORDS_FILENAME, "r") as words_txt:
            words_temp = words_txt.read()
            words_temp = words_temp.splitlines()

            word_keys = self.WORDS_DICT.keys()

            for key in word_keys:
                self.WORDS_DICT[key] = []

            self.sort_words(words_temp)

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
            print "All of your men have been hanged!"
            print "Game over, man! Game over!\n"
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
            print "There are no more words left to solve."
            print "Congratulations on making it to the end!\n"
            if self.score == self.score_total:
                print "You got a perfect score! Truly impressive.\n"
            print score_str
            return True
        else:
            return False

    def play(self):
        """The main game loop."""

        self.print_title(
            "HANGMAN, IN PYTHON", 
            "A Game by Alex Crawford", 
            "v1.0.0"
        )

        self.query_difficulty()
        self.query_load_file()

        self.score_total_set()

        print "\nEnter '/q' as a guess to quit."

        print "\n" + self.HRULE + "\n"

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

                print "\n" + self.HRULE + "\n"

                if self.no_guesses_left() or self.word_solved():
                    self.game_state = self.STATE_END
                    break

            while self.game_state == self.STATE_END:
                self.WORDS_DICT[self.word_level].remove(self.word)
                self.check_word_level()
                self.reset_guess()

                print self.HRULE + "\n"

                if self.no_lives_left() or self.no_words_left():
                    self.running = False
                    break
                else:
                    self.game_state = self.STATE_SETWORD
                    break

            while self.game_state == self.STATE_EXIT:
                self.running = False
                score_str = "Final score: {0}/{1}\n".format(self.score, 
                            self.score_total)
                print choice(self.EXIT_MSGS)
                print score_str
                break

    def print_info(self):
        """Prints the current hangman art, and other relevant information."""

        print "Level: {0}".format(self.word_level)
        print "Score: {0}".format(self.score)
        print "Men left: {0}\n".format(self.lives - 1)
        for line in Game.ASCII_DICT[self.ascii_key]:
            print line
        print
        print "{0}\n".format(" ".join(self.word_hidden))
        print "Guesses: {0}".format(" ".join(sorted(self.guessed)))
        print "Guesses left: {0}\n".format(self.guesses_left)

    def print_title(self, title, subtitle=None, version=None, nl=True):
        """Prints a title, with horizontal rules above and below it. 
        Also prints a subtitle below the title, and/or version, 
        if provided.

        """
        print "\n" + self.HRULE
        print title
        print self.HRULE
        if subtitle is not None:
            print subtitle
        if version is not None:
            print version
        if subtitle is not None or version is not None:
            print self.HRULE
        if nl:
            print

    def query_difficulty(self):
        """Queries the player about what difficulty level they 
        would like to play at. 

        """
        lives_easy = 5
        lives_normal = 3
        lives_hard = 1

        command = raw_input("Difficulty level? (1-3) ")

        if command == "1":
            self.diff_level = 1
            self.lives = lives_easy
        elif command == "2":
            self.diff_level = 2
            self.lives = lives_normal
        elif command == "3":
            self.diff_level = 3
            self.lives = lives_hard

        diff_dict = {1: "easy", 2: "medium", 3: "hard"}
        diff = diff_dict[self.diff_level]

        print "\nDifficulty set to {0} ({1})\n".format(diff, self.diff_level)

    def query_load_file(self):
        """Queries the player about whether or not they'd like to
        load the words from a txt file.

        """
        command = raw_input("Load the word list from a file? (y/n) ")
        
        try:
            if command == "" or command in ['Y', 'y']:
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
                self.game_state = self.STATE_EXIT
                break
            else:
                print "\nInvalid guess. Must be a letter.\n"

    def reset_guess(self):
        """Resets the guesses, and ascii key, and guesses left."""

        self.guessed = []
        self.ascii_key = 0
        self.guesses_left = 6

    def score_total_set(self):
        """Figures the total potential score for the game."""

        for words in self.WORDS_DICT.values():
            for word in words:
                self.score_total += 20

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
            if self.guess is not None and letter_upper in self.guessed:
                temp_hidden.append(letter_upper)
            else:
                temp_hidden.append('_')
        
        self.word_hidden = temp_hidden

    def word_set(self):
        """Gets a random word from the list of words, and sets it 
        as the current word ('self.word').

        """
        if len(self.WORDS_DICT[self.word_level]) > 0:
            self.word = choice(self.WORDS_DICT[self.word_level])
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
        Game().play()
    except:
        print "Oops! Something went wrong. Sorry about that."
