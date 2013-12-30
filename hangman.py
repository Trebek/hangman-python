#===============================================================================
# Hangman, in Python
#-------------------------------------------------------------------------------
# Version: 0.1.8
# Updated: 29-12-2013
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

    def __init__(self):
        """Game initialization method."""

        self.wordlist = [
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

        self.easywords = []
        self.normwords = []
        self.hardwords = []

        self.wordhash = {
            1: self.easywords,
            2: self.normwords,
            3: self.hardwords
        }

        self.theword = None
        self.hidden = []

        self.guess = None
        self.gletts = []
        self.gnum = 0
        self.gleft = 6

        self.wordlvl = 1
        self.score = 0
        self.totalscore = 0
        self.men = 3

        self.running = True
        self.quitting = False

        self.quitmsg = "\nI hope you enjoyed playing! Good bye.\n"

        self.exwords = ["exit", "quit", "end"]

    def checkguess(self):
        """Checks the player's guess for a correct letter."""

        temp = []
        right = 0
        wrong = 0

        if self.guess.upper() not in self.gletts:
            self.gletts.append(self.guess[0].upper())
        else:
            self.gnum += 1
            self.gleft -= 1
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
            
        if (wrong == len(self.theword) or right == 0 and             
                self.guess.lower() not in self.exwords):
            self.gnum += 1
            self.gleft -= 1
            if self.gleft < 5 and self.score > 0:
                self.score -= 1
            print "\nIncorrect. No one can be right all of the time."

        if temp != []:    
            self.hidden = temp
            
        print NL + HR + NL

    def checklvl(self):
        """Checks the level the player is on. If the player has solved
        all of the words in that level, the player is moved up a level.

        """
        if len(self.wordhash[self.wordlvl]) > 0:
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
        """Prints the current hangman art, and other relavant information."""

        if not win:
            print "Level: " + str(self.wordlvl)
            print "Score: " + str(self.score)
            print "Men left: " + str(self.men - 1)
            print asciihang[self.gnum]
            print " ".join(self.hidden) + NL
            print "Guesses: " + " ".join(sorted(self.gletts))
            print "Guesses left: " + str(self.gleft) + NL
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
            elif self.guess.lower() in self.exwords:
                self.quitting = True
                break
            else:
                print "\nInvalid guess. Must be a letter.\n"

    def getword(self):
        """Get a random word from the list of words, and set it 
        as the current word.

        """
        if len(self.wordhash[self.wordlvl]) > 0:
            self.theword = choice(self.wordhash[self.wordlvl])
        else:
            print "\nOops! No words to load. Exiting.\n"
            exit()

    def getwordfile(self):
        """Opens a file named 'words.txt', if it's present, and uses
        that for the word list.

        """
        wordtxt = open("words.txt", "r")

        self.wordlist = []
        
        for line in wordtxt:
            self.wordlist.append(line.rstrip(NL))
        
        wordtxt.close()

    def hideword(self):
        """Generate a hidden version of the chosen word."""
        
        temp = []
        
        for c in self.theword:
            temp.append('_')
                        
        self.hidden = temp

    def intro(self):
        """Prints the title, and gets some input from the player,
        including difficulty level and whether or not to load the
        wordlist from a file.

        """

        self.title("HANGMAN, IN PYTHON", "A Game by Alex Crawford", "v0.1.8")

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
            try:
                self.getwordfile()
                print "\nWord file loaded."
            except:
                print "\nCouldn't load file. Loading default."
                pass
        else:
            print "\nDefault word file loaded."

        print "\nEnter 'end', exit', or 'quit' as a guess to quit."

    def mainloop(self):
        """The main game loop."""

        playing = True

        self.intro()
        self.figurescore()
        self.sortwords()

        # del self.wordlist

        print NL + HR + NL

        while self.running:
            
            self.getword()
            self.hideword()
            
            while playing:
                
                self.display()
                self.getguess()

                if self.quitting:
                    self.running = False
                    print NL + HR
                    print self.quitmsg
                    break

                self.checkguess()
                
                if self.gleft == 0:
                    self.display()
                    print "You've run out of guesses... Sorry about that.\n"
                    print "The word was: " + self.theword.upper() + NL
                    self.men -= 1
                    self.reset()
                    self.checklvl()
                    print HR + NL
                    break
                elif "".join(self.hidden) == self.theword:
                    self.display(True)
                    print "You solved the word! Exciting, I know."
                    print "+10 points\n"
                    self.score += 10
                    if self.gleft == 6:
                        print "You didn't make a single wrong guess!"
                        print "+10 bonus points\n"
                        self.score += 10
                    self.checklvl()
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
        self.gleft = 6

    def sortwords(self):
        """Sorts the words in the main wordlist into separate lists,
        for each level, depending on their length. It also deletes
        self.wordlist once the words have been sorted.

        """
        for word in self.wordlist:
            if len(word) in range(1, 5):
                self.easywords.append(word)
            elif len(word) in range(5, 7):
                self.normwords.append(word)
            else:
                self.hardwords.append(word)
        del self.wordlist

    def title(self, msg, sub=None, ver=None, nl=True):
        """Prints a title, with horizontal rules above and below it. 
        Also prints a subtitle below the title, if provided.

        """
        print NL + HR
        print msg
        if sub is not None:
            print sub
        if ver is not None:
            print ver
        print HR
        if nl:
            print

#===============================================================================
# IF MAIN
#===============================================================================

if __name__ == '__main__':
    game = Game()
    game.mainloop()
