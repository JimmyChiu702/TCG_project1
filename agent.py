#!/usr/bin/env python3

"""
Basic framework for developing 2048 programs in Python

Author: Hung Guei (moporgic)
        Computer Games and Intelligence (CGI) Lab, NCTU, Taiwan
        http://www.aigames.nctu.edu.tw
"""

from board import board
from action import action
import random


class agent:
    """ base agent """
    
    def __init__(self, options = ""):
        self.info = {}
        options = "name=unknown role=unknown " + options
        for option in options.split():
            data = option.split("=", 1) + [True]
            self.info[data[0]] = data[1]
        return
    
    def open_episode(self, flag = ""):
        return
    
    def close_episode(self, flag = ""):
        return
    
    def take_action(self, state):
        return action()
    
    def check_for_win(self, state):
        return False
    
    def property(self, key):
        return self.info[key] if key in self.info else None
    
    def notify(self, message):
        data = message.split("=", 1) + [True]
        self.info[data[0]] = data[1]
        return
    
    def name(self):
        return self.property("name")
    
    def role(self):
        return self.property("role")


class random_agent(agent):
    """ base agent for agents with random behavior """
    
    def __init__(self, options = ""):
        super().__init__(options)
        seed = self.property("seed")
        if seed is not None:
            random.seed(int(seed))
        self.rstate = random.getstate()
        return
    
    def choice(self, seq):
        random.setstate(self.rstate)
        target = random.choice(seq)
        self.rstate = random.getstate()
        return target
    
    def shuffle(self, seq):
        random.setstate(self.rstate)
        random.shuffle(seq)
        self.rstate = random.getstate()
        return


class rndenv(random_agent):
    """
    random environment
    add a new random tile to an empty cell
    2-tile: 90%
    4-tile: 10%
    """
    
    def __init__(self, options = ""):
        super().__init__("name=random role=environment " + options)
        self.init_tile_bag()
        return

    def open_episode(self, flag = ""):
        self.init_tile_bag()
    
    def take_action(self, state):
        if state.last_move == 0:
            empty = [pos for pos, tile in [(i, state.state[i]) for i in [12, 13, 14, 15]] if not tile]
        elif state.last_move == 1:
            empty = [pos for pos, tile in [(i, state.state[i]) for i in [0, 4, 8, 12]] if not tile]
        elif state.last_move == 2:
            empty = [pos for pos, tile in [(i, state.state[i]) for i in [0, 1, 2, 3]] if not tile]
        elif state.last_move == 3:
            empty = [pos for pos, tile in [(i, state.state[i]) for i in [3, 7, 11, 15]] if not tile]
        else:
            empty = [pos for pos, tile in enumerate(state.state) if not tile]
        if empty:
            pos = self.choice(empty)
            if len(self.tile_bag) == 0:
                self.init_tile_bag()
            tile = self.choice(self.tile_bag)
            self.tile_bag.remove(tile)
            return action.place(pos, tile)
        else:
            return action()
    
    def init_tile_bag(self):
        self.tile_bag = [1, 2, 3]

    
class player(random_agent):
    """
    dummy player
    select a legal action randomly
    """
    
    def __init__(self, options = ""):
        super().__init__("name=dummy role=player " + options)
        return
    
    def take_action(self, state):
        scores = [board(state).slide(op) for op in range(4)]
        max_value = max(scores)
        if max_value != -1:
            max_index = scores.index(max_value)            
            return action.slide(max_index)
        else:
            return action()
    
    
if __name__ == '__main__':
    print('2048 Demo: agent.py\n')
    
    state = board()
    env = rndenv()
    ply = player()
    
    a = env.take_action(state)
    r = a.apply(state)
    print(a)
    print(r)
    print(state)
        
    a = env.take_action(state)
    r = a.apply(state)
    print(a)
    print(r)
    print(state)
    
    print(ply.take_action(state))
    print(ply.take_action(state))
    print(ply.take_action(state))
    print(ply.take_action(state))
    print(ply.take_action(state))
    print(ply.take_action(state))
    print(ply.take_action(state))
    print(ply.take_action(state))
    print(ply.take_action(state))
    
    state = board()
    state[0] = 1
    state[1] = 1
    print(state)
    
    print(ply.take_action(state))
    print(ply.take_action(state))
    print(ply.take_action(state))
    print(ply.take_action(state))
    print(ply.take_action(state))
    print(ply.take_action(state))
    print(ply.take_action(state))
    print(ply.take_action(state))
    print(ply.take_action(state))
    print(state)
    
