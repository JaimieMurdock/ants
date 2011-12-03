#!/usr/bin/env python3
from ants import *
import random
from collections import defaultdict

DIRECTIONS = ['n','e','s','w']
# define a class with a do_turn method
# the Ants.run method will parse and update bot input
# it will also run the do_turn method for us
class MyBot:
    def __init__(self):
        # define class level variables, will be remembered between turns
        self.ants = None
        self.world = defaultdict(lambda: None)
    
    # do_setup is run once at the start of the game
    # after the bot has received the game settings
    # the ants class is created and setup by the Ants.run method
    def do_setup(self, ants):
        # initialize data structures after learning the game settings
        pass
    
    # do turn is run once per turn
    # the ants class has the game state and is updated by the Ants.run method
    # it also has several helper methods to use
    def do_turn(self, ants):
        # loop through all my ants and try to give them orders
        # the ant_loc is an ant location tuple in (row, col) form
        self.ants = ants

        for ant_loc in ants.my_ants():
            self.ant_action(ant_loc)

            # check if we still have time left to calculate more orders
            if ants.time_remaining() < 10:
                break

    def ant_action(self, ant_loc):
        """ Function for each ant movement """
        # TODO: construct world map construction
        self._world_map(ant_loc)
        
        self._random_move(ant_loc)

    def _world_map(self, ant_loc):
        """ Build up research. """
        for direction in DIRECTIONS:
            loc = self.ants.destination(ant_loc, direction)

            if self.ants.passable(loc) and self.ants.unoccupied(loc):
                self.world[loc] = True

    def _move_away(self, ant_loc):
        raise NotImplementedError

    def _random_move(self, ant_loc):
        random.shuffle(DIRECTIONS)

        for direction in DIRECTIONS:
            # the destination method will wrap around the map properly
            # and give us a new (row, col) tuple
            new_loc = self.ants.destination(ant_loc, direction)

            if (self.ants.passable(new_loc) and self.ants.unoccupied(new_loc)
                and self.world[new_loc]):
                # an order is the location of a current ant and a direction
                self.world[ant_loc] = True
                self.world[new_loc] = False
                self.ants.issue_order((ant_loc, direction))

                # stop now, don't give 1 ant multiple orders
                break
            
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
        Ants.run(MyBot())
    except KeyboardInterrupt:
        print('ctrl-c, leaving ...')
