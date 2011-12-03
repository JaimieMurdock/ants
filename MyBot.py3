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
        self.swarm = defaultdict(lambda: None) # stores instances of Ant class
        self.goals = set()
        self.assigned_goals = set()
        self.unassigned_goals = set()
    
    # do_setup is run once at the start of the game
    # after the bot has received the game settings
    # the lings class is created and setup by the Ants.run method
    def do_setup(self, world):
        # initialize data structures after learning the game settings
        self.world = world

        for ling_loc in self.world.my_ants():
            self.swarm[ling_loc] = Drone(ling_loc)
    
    # do turn is run once per turn
    # the lings class has the game state and is updated by the Ants.run method
    # it also has several helper methods to use
    def do_turn(self, world):
        # loop through all my lings and try to give them orders
        # the ling_loc is an ling location tuple in (row, col) form
        self.world = world

        self.update_goals()

        for ling_loc in self.world.my_ants():
            # new ant is born
            if self.swarm[ling_loc] is None:
                self.swarm[ling_loc] = Drone(ling_loc)

            self.execute_move(self.swarm[ling_loc])

            # check if we still have time left to calculate more orders
            if self.world.time_remaining() < 10:
                break

    def execute_move(self, ling):
        # move ling state to new square, direction
        move = ling.get_move(self)

        if move:
            new_loc, direction = move
            self.world.issue_order((ling.loc, direction))
            
            self.swarm[ling.loc] = None
            self.swarm[new_loc] = ling 
            ling.loc = new_loc
    
    def suicide(self, loc):
        return (not self.world.passable(loc) or
                not self.world.unoccupied(loc) or
                self.swarm[loc])

    def get_goal(self, ling):
        goal = min(self.unassigned_goals,
            key = lambda goal: self.world.distance(ling.loc, goal))
        self.unassigned_goals.remove(goal)
        self.assigned_goals.add(goal)

        return goal

    def update_goals(self):
        self.goals = set(self.world.food())
        self.unassigned_goals = self.goals.difference(self.assigned_goals)

    def moves_from(self, loc):
        moves = [(self.world.destination(loc, direction), direction)
                    for direction in DIRECTIONS]
        moves = [(new_loc, direction) for new_loc, direction in moves 
                    if self.world.passable(new_loc)]
        return moves

        
DIRECTIONS = ['n','e','s','w']
class Ling(object):
    """ Class to represent each 'ling """
    def __init__(self, loc):
        self.loc = loc
    
    def get_move(self, overlord):
        """ Performs a random move. """
        return random.choice(self.valid_moves(overlord))

    def valid_moves(self, overlord):
        moves = [(overlord.world.destination(self.loc, direction), direction)
                    for direction in DIRECTIONS]
        moves = [(new_loc, direction) for new_loc, direction in moves 
                    if not overlord.suicide(new_loc)]
        return moves
        
class Drone(Ling):
    """ Class to represent resource gatherers. Using shortest path for algorithm """
    def __init__(self, loc):
        self.loc = loc
        self.goal = None

    def get_move(self, overlord):
        """ Performs a breadth-first search to all food. """
        if self.goal is None or self.goal not in overlord.goals:
            self.goal = overlord.get_goal(self)
            self.move_queue = self.a_star(overlord, not_dying_but_getting_closer)
        valid_moves = self.valid_moves(overlord) 
        if move_queue[0] in valid_moves
            return move_queue.pop()
        else:
            self.move_queue = self.a_star(overlord, not_dying_but_getting_closer)
            return move_queue.pop() 
             
    @staticmethod
    def not_dying_but_getting_closer(world, loc1, loc2):
        return world.distance(loc1, loc2)

    def a_star(self,overlord,heuristic):
        world = overlord.world
        closedset = set()
        openset = set(self.loc)
        came_from = {} 

        g_score = {self.loc : 0}
        h_score = {self.loc : heuristic(world, self.loc, self.goal)}
        f_score = {self.loc : g_score[self.loc] + h_score[self.loc]}

        while openset:
            move = min(openset, key=lambda loc: f_score[loc])
            if move == self.goal:
                return reconstruct_path(came_from, came_from[self.goal]) 
                
            openset.remove(move)
            closedset.add(move)
            for neighbor in overlord.moves_from(move):
                if neighbor in closedset:
                    continue
                tentative_g_score = g_score[move] + 1 

                if neighbor not in openset:
                    openset.add(neighbor)
                    tentative_is_better = True
                elif tentative_g_score < g_score[neighbor]:
                    tentative_is_better = True
                else:
                    tentative_is_better = False
                
                if tentative_is_better: 
                    came_from[neighbor] = move
                    g_score[neighbor] = tentative_g_score
                    h_score[neighbor] = heuristic(world, neighbor, self.goal)
                    f_score[neighbor] = g_score[neighbor] + h_score[neighbor]

        return None

    @staticmethod
    def reconstruct_path(came_from, loc):
        if came_from[loc]:
            p = reconstruct_path(came_from, came_from[loc])
            p.append(loc)
            return p
        else:
            return [loc]


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


