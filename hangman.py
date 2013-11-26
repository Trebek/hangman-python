#===============================================================================
# Hangman, in Python
#-------------------------------------------------------------------------------
# Version: 0.1.7
# Updated: 25-11-2013
# Author: Alex Crawford
# License: MIT
#===============================================================================

"""Overly complex object oriented Hangman, in Python (2.7.5)"""

#===============================================================================
# IMPORTS
#===============================================================================

from random import choice

#===============================================================================
# MISC. FORMATTING VARIABLES
#===============================================================================

NL = ("\n")
HR = ("-" * 40)

#===============================================================================
# ASCII HANGMAN
#===============================================================================

asciihang = [
r"""
 +----+ 
 |/   | 
 |      
 |      
 |      
 |      
========
""",
r"""
 +----+ 
 |/   | 
 |    O 
 |      
 |      
 |      
========
""",
r"""
 +----+ 
 |/   | 
 |    O 
 |    | 
 |      
 |      
========
""",
r"""
 +----+ 
 |/   | 
 |    O 
 |   /|
 |      
 |      
========
""",
r"""
 +----+ 
 |/   | 
 |    O 
 |   /|\
 |      
 |      
========
""",
r"""
 +----+ 
 |/   | 
 |    O 
 |   /|\
 |   /
 |      
========
""",
r"""
 +----+
 |/   |
 |    O
 |   /|\
 |   / \
 |      
========
""",
]

#===============================================================================
# THE GAME
#===============================================================================

class Game(object):
    """Contains all of the methods the game needs."""
    
    alpha = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

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

    easywords = []
    normwords = []
    hardwords = []
    worddict = {
        1: easywords,
        2: normwords,
        3: hardwords
    }

    wordlvl = 1
    theword = None
    hidden = []

    guess = None
    gletts = []
    gnum = 0
    left = 6
    men = 3

    score = 0
    totalscore = 0

    running = True
    quitting = False
    quitmsg = "I hope you enjoyed playing! Good bye.\n"

    exwords = ["EXIT", "QUIT", "END"]

    def __init__(self):
        """Game initialization method"""

        self.title("HANGMAN, IN PYTHON", "A Game by Alex Crawford\nv0.1.6")

        cmd = raw_input("Difficulty level? (1-3) ")

        if cmd == "1":
            self.men = 5
        elif cmd == "2":
            self.men = 3
        elif cmd == "3":
            self.men = 1
        else:
            pass
        
        cmd = raw_input("Load the word list from a file? (y/n) ")
        
        if cmd in ['Y', 'y']:
            fromfile = True
            self.getwordfile()
            print "\nWord file loaded."
        else:
            print "\nNo word file loaded."

        print "\nEnter 'end', exit', or 'quit' as a guess to quit."
        
        self.sortwords()

        self.figurescore()

        del Game.wordlist

    def checkguess(self):
        """Checks the player's guess for a correct letter."""

        temp = []
        right = 0
        wrong = 0

        if self.guess.upper() not in self.gletts:
            self.gletts.append(self.guess[0].upper())
        else:
            self.gnum += 1
            self.left -= 1
            return

        for c in self.theword:
            if c.upper() == self.guess.upper():
                right += 1
                temp.append(c)
            elif c.upper() in self.gletts:
                temp.append(c)
            else:
                wrong += 1
                temp.append('_')

        if right > 0:
            print "\nGood guess! Don't let it go to your head though."
            
        if ((wrong == len(self.theword) or right == 0) and             
                self.guess.upper() not in self.exwords):
            self.gnum += 1
            self.left -= 1
            if self.left < 5 and self.score > 0:
                self.score -= 1
            print "\nIncorrect. No one can be right all of the time."

        if temp != []:    
            self.hidden = temp
            
        print NL + HR + NL

    def checkwords(self):
        """Checks the level the player is on, and acts depending on that."""
        if len(self.worddict[self.wordlvl]) > 0:
            if self.wordlvl == 1:
                self.easywords.remove(self.theword)
                if len(self.easywords) == 0 and len(self.normwords) > 0:
                    self.wordlvl = 2
                    print "You've progressed to level 2!\n"
            elif self.wordlvl == 2:
                self.normwords.remove(self.theword)
                if len(self.normwords) == 0 and len(self.hardwords) > 0:
                    self.wordlvl = 3
                    print "You've progressed to level 3!\n"
            elif self.wordlvl == 3:
                self.hardwords.remove(self.theword)

    def display(self, win=False):
        """Prints the current hangman art, and other relevant information."""
        
        if not win:
            print "Level: " + str(self.wordlvl)
            print "Score: " + str(self.score)
            print "Men left: " + str(self.men - 1)
            print asciihang[self.gnum]
            print " ".join(self.hidden) + NL
            # print "Guesses: " + " ".join(tempguessed)
            print "Guesses: " + " ".join(sorted(self.gletts))
            print "Guesses left: " + str(self.left) + NL
        else:
            print "".join(self.hidden).upper() + NL

    def figurescore(self):
        """Figures the total potential score for the game."""

        for word in self.wordlist:
            self.totalscore += 20

    def getguess(self):
        """Get the player's guess."""

        while True:
            self.guess = raw_input("What's your guess? ")
            if self.guess in self.alpha and self.guess is not "":
                break
            elif self.guess.upper() in self.exwords:
                self.quitting = True
                return
            else:
                print "\nInvalid guess. Must be a letter.\n"

    def getword(self):
        """Get a random word from the list of words, and set it 
        as the current word.

        """
        while True:
            if len(self.worddict[self.wordlvl]) > 0:
                self.theword = choice(self.worddict[self.wordlvl])
                break
            else:
                break

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

    def loop(self):
        """The main game loop."""

        playing = True
        fromfile = False

        print NL + HR + NL

        while self.running:
            
            self.getword()
            self.hideword()
            
            while playing:
                
                self.display()
                self.getguess()
                self.checkguess()
                
                if self.quitting:
                    self.running = False
                    print self.quitmsg
                    break
                
                # if self.gnum == len(asciihang) - 1:
                if self.left == 0:
                    self.display()
                    print "You've run out of guesses... Sorry about that.\n"
                    print "The word was: " + self.theword.upper() + NL
                    self.men -= 1
                    self.reset()
                    self.checkwords()
                    print HR + NL
                    break
                elif "".join(self.hidden) == self.theword:
                    self.display(True)
                    print "You solved the word! Exciting, I know."
                    print "+10 points\n"
                    self.score += 10
                    if self.left == 6:
                        print "You didn't make a single wrong guess!"
                        print "+10 bonus points\n"
                        self.score += 10
                    self.checkwords()
                    self.reset()
                    print HR + NL
                    break

            self.scorestr = "{0} {1} {2} {3}{4}".format("Final score:", 
                self.score, "/", self.totalscore, NL)

            if self.men == 0:
                print "All of your men have been hanged!"
                print "Game over, man! Game over!\n"
                print self.scorestr
                break

            if (len(self.easywords) == 0 and len(self.normwords) == 0 and 
                    len(self.hardwords) == 0):
                print "There are no more words left to solve."
                print "Congratulations on making it to the end!\n"
                if self.score == self.totalscore:
                    print "You got a perfect score! Truly impressive.\n"
                print self.scorestr
                break

    def reset(self):
        """Resets the guesses, and number of guesses."""

        self.gletts = []
        self.gnum = 0
        self.left = 6

    def sortwords(self):
        """Sorts the words in the main wordlist into separate lists,
        depending on their length

        """
        for word in self.wordlist:
            if len(word) in range(1, 4):
                self.easywords.append(word)
            elif len(word) in range(5, 6):
                self.normwords.append(word)
            else:
                self.hardwords.append(word)

    def title(self, msg, sub=None, nl=True):
        """Prints a title, with horizontal rules above and below it. 
        Also prints a subtitle below the title, if provided.

        """
        print NL + HR
        print msg
        if sub is not None:
            print sub
        print HR
        if nl:
            print

#===============================================================================
# IF MAIN
#===============================================================================

if __name__ == '__main__':

    game = Game()
    game.loop()
