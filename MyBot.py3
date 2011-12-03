#!/usr/bin/env python3
from ants import *
import random
from collections import defaultdict

# define a class with a do_turn method
# the Ants.run method will parse and update bot input
# it will also run the do_turn method for us
class Kerrigan(object):
    def __init__(self):
        # define class level variables, will be remembered between turns
        self.lings = defaultdict(lambda: None) # stores instances of Ant class
    
    # do_setup is run once at the start of the game
    # after the bot has received the game settings
    # the lings class is created and setup by the Ants.run method
    def do_setup(self, world):
        # initialize data structures after learning the game settings
        self.world = world

        for ling_loc in self.world.my_ants():
            self.lings[ling_loc] = Ling(ling_loc)
    
    # do turn is run once per turn
    # the lings class has the game state and is updated by the Ants.run method
    # it also has several helper methods to use
    def do_turn(self, world):
        # loop through all my lings and try to give them orders
        # the ling_loc is an ling location tuple in (row, col) form
        self.world = world

        for ling_loc in self.world.my_ants():
            # new ant is born
            if self.lings[ling_loc] is None:
                self.lings[ling_loc] = Ling(ling_loc)

            self.execute_move(self.lings[ling_loc])

            # check if we still have time left to calculate more orders
            if self.world.time_remaining() < 10:
                break

    def execute_move(self, ling):
        # move ling state to new square, direction
        move = ling.get_move(self)

        if move:
            new_loc, direction = move
            self.world.issue_order((ling.loc, direction))
            
            self.lings[ling.loc] = None
            self.lings[new_loc] = ling 
            ling.loc = new_loc
    
    def suicide(self, loc):
        return (not self.world.passable(loc) or
                not self.world.unoccupied(loc) or
                self.lings[loc])


DIRECTIONS = ['n','e','s','w']
class Ling(object):
    """ Class to represent each 'ling """
    def __init__(self, loc):
        self.loc = loc
    
    def get_move(self, overlord):
        """ Performs a random move. """
        random.shuffle(DIRECTIONS)

        for direction in DIRECTIONS:
            # the destination method will wrap around the map properly
            # and give us a new (row, col) tuple
            new_loc = overlord.world.destination(self.loc, direction)

            if not overlord.suicide(new_loc):
                # an order is the location of a current ling and a direction
                return (new_loc, direction) 
        

class Baneling(Ling):
    """ Ling that looks for things to attack and then swarms them.  """
    pass

            
if __name__ == '__main__':
    # psyco will speed up python a little, but is not needed
    try:
        import psyco
        psyco.full()
    except ImportError:
        pass
    
    try:
        # if run is passed a class with a do_turn method, it will do the work
        # this is not needed, in which case you will need to write your own
        # parsing function and your own game state class
        Ants.run(Kerrigan())
    except KeyboardInterrupt:
        print('ctrl-c, leaving ...')
