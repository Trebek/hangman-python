#===============================================================================
# Hangman, in Python
#-------------------------------------------------------------------------------
# Version: 0.1.6
# Updated: 24-11-2013
# Author: Alex Crawford
# License: MIT
#-------------------------------------------------------------------------------
# http://repl.it/LhR/4
#===============================================================================

"""Overly complex Hangman, in Python (2.7.5)"""

#===============================================================================
# IMPORTS
#===============================================================================

from random import choice

#===============================================================================
# MISC. FORMATTING VARIABLES
#===============================================================================

NL = ('\n')
HR = ('-' * 40)

#===============================================================================
# THE GAME
#===============================================================================

class Game(object):
    """Contains all of the methods the game needs."""
    
    wordlist = [
    "Cup", 
    "Word",
    "Test",
    "Hangman",
    "Python",
    "Snake",
    "Green",
    "Red",
    "Awesome",
    "Chair",
    "Human",
    "Machine",
    "Computer",
    "Keyboard",
    "Cat",
    "Dog",
    "Hand",
    "Foot",
    "Left",
    "Right"
    ]

    def __init__(self):
        """Game initialization method"""

        self.theword = None
        self.hidden = []

        self.guesses = []
        self.gnum = 0
        self.left = 6
        self.men = 3

        self.score = 0

        self.running = True
        self.quitting = False

    def loop(self):
        """The main game loop."""

        playing = True
        playquery = True
        fromfile = False
        
        self.title("HANGMAN, IN PYTHON", "A Game by Alex Crawford\nv0.1.6")
        
        cmd = raw_input("Load the word list from a file? (y/n) ")
        
        if cmd in ['Y', 'y']:
            fromfile = True
            self.getwordfile()
        
        while self.running:
            
            quitmsg = "I hope you enjoyed playing! Good bye."
            
            self.getword()
            self.hideword()
            
            while playing:
                
                self.display()
                self.getguess()
                
                if self.quitting:
                    playquery = False
                    self.running = False
                    print NL + quitmsg
                    break
                
                if self.gnum == len(Ascii.art) - 1:
                    self.display()
                    print "You've run out of guesses... Sorry about that.\n"
                    print "The word was: " + self.theword + NL
                    self.men -= 1
                    self.reset()
                    if self.men == 0:
                        playquery = False
                        self.running = False
                        print "All of your men have been hanged! Game over.\n"
                    print HR
                    break
                elif "".join(self.hidden) == self.theword:
                    self.display(True)
                    print "You solved the word! Exciting, I know.\n"
                    self.wordlist.remove(self.theword)
                    self.score += 10
                    self.reset()
                    print HR
                    break

                if len(self.wordlist) == 0:
                    print "You've solved all of the words in the game!"
                    print "You are the champion (no time for losers)!"
                    print "Game over, man! Game over!"
                    self.running = False
                    break

    def getword(self):
        """Get a random word from the list of words, and set it 
        as the current word.

        """
        self.theword = choice(self.wordlist)

    def getwordfile(self):
        """Opens a file named 'words.txt', if it's present, and uses
        that for the word list.

        """
        self.wordlist = []

        wordtxt = open("words.txt", "r")
        
        for line in wordtxt:
            self.wordlist.append(line.rstrip(NL))
        
        wordtxt.close()

    def hideword(self, guess=None):
        """Generate a hidden version of the chosen word."""
        
        temp = []
        
        for c in self.theword:
            temp.append('_')
                        
        self.hidden = temp

    def getguess(self):
        """Get the player's guess, and compare it to the letters in the 
        chosen word. If player guessed right, the letter is "revealed" 
        in the hidden version of the word. If there is more than one copy 
        of the letter in the word, all are revealed.
        
        """
        temp = []
        right = 0
        wrong = 0
        
        while True:
            guess = raw_input("What's your guess? ")
            if guess == "":
                print "\nInvalid guess.\n"
            else:
                break
        
        if guess.upper() in ["EXIT", "QUIT", "END"]:
            self.quitting = True
            return
        
        if guess.upper() not in self.guesses:
            self.guesses.append(guess[0].upper())            

        for c in self.theword:
            if c.upper() == guess.upper():
                right += 1
                temp.append(c)
            elif c.upper() in self.guesses:
                temp.append(c)
            else:
                wrong += 1
                temp.append('_')

        if right > 0:
            print "\nGood guess! Don't let it go to your head though.\n"
            
        if ((wrong == len(self.theword) or right == 0) and 
            "END" not in self.guesses and "EXIT" not in self.guesses and 
            "QUIT" not in self.guesses):
            self.gnum += 1
            self.left -= 1
            print "\nIncorrect. No one can be right all of the time.\n"
        
        if temp != []:    
            self.hidden = temp
            
        print HR

    def reset(self):
        """Resets the guesses, and number of guesses."""

        self.guesses = []
        self.gnum = 0
        self.left = 6

    def display(self, win=False):
        """Prints the current hangman art, depending on number of guesses. 
        Also prints the hidden word, with any revealed letters.

        """
        tempguessed = []
        
        for guess in sorted(self.guesses):
            tempguessed.append(guess)
        
        print Ascii.art[self.gnum]
        
        if win == False:
            print " ".join(self.hidden) + NL
            print "Guessed letters: " + " ".join(tempguessed)
            print "Guesses left: " + str(self.left) + NL
            print "Score: " + str(self.score)
            print "Men left: " + str(self.men) + NL
        else:
            print "".join(self.hidden) + NL

    def title(self, msg, sub=None, nl=True):
        """Prints a title, with horizontal rules above and below it. 
        Also prints a subtitle below the title, if provided.

        """
        print
        print HR
        print msg
        if sub is not None:
            print sub
        print HR
        if nl:
            print

#===============================================================================
# ASCII ART
#===============================================================================

class Ascii(object):
    """The class containing the ascii hangman "art"."""
    
    art = [
r'''
 +----+ 
 |/   | 
 |      
 |      
 |      
 |      
========
''',
r'''
 +----+ 
 |/   | 
 |    O 
 |      
 |      
 |      
========
''',
r'''
 +----+ 
 |/   | 
 |    O 
 |    | 
 |      
 |      
========
''',
r'''
 +----+ 
 |/   | 
 |    O 
 |    |\
 |      
 |      
========
''',
r'''
 +----+ 
 |/   | 
 |    O 
 |   /|\
 |      
 |      
========
''',
r'''
 +----+ 
 |/   | 
 |    O 
 |   /|\
 |     \
 |      
========
''',
r'''
 +----+
 |/   |
 |    O
 |   /|\
 |   / \
 |      
========
''',
        ]

#===============================================================================
# IF MAIN
#===============================================================================

if __name__ == '__main__':

    game = Game()
    game.loop()
