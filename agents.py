import numpy as np
from numpy.random import choice
from numpy.random import dirichlet

from gridworld import Environment, Agent

class RandomAgent(Agent):

    def __init__(self, name, pos=(0,0), color=np.array([0,1,0]), alpha=5e-3):
        super(RandomAgent, self).__init__(name=name, pos=pos, color=color)

        self.actions = {'stay':(0,0),
                        'north':(0,1),
                        'south':(0,-1),
                        'east':(1,0),
                        'west':(-1, 0)}

        self.action2index = {a:i for i, a in enumerate(self.actions)}
        self.index2action = {self.action2index[a]:a for a in self.actions}
        self.alpha = alpha
        self.last_action = None
        self.distribution = dirichlet(alpha=(alpha,)*len(self.actions)) #dample a random dirichlet distribution

    def transition(self, grid):
        self.last_action = self.action2index['stay']
        x_edge, y_edge = grid.shape
        self.past_pos = self.pos
        move_index = choice(list(range(len(self.actions))), p=self.distribution)
        move = self.actions[self.index2action[move_index]]
        x, y = (self.pos[0] + move[0], self.pos[1] + move[1])
        if x < x_edge and y < y_edge and x >= 0 and y >= 0:
            if grid[x, y] == 0:
                self.pos = (self.pos[0] + move[0], self.pos[1] + move[1])
                self.last_action = move_index

    def state_observe(self):
        state_vec = np.zeros((len(self.pos),))
        for i, p in enumerate(self.pos):
            state_vec[i] = p
        return state_vec

    def action_observe(self):
        action_vec = np.zeros(shape=(len(self.actions)))
        action_vec[self.last_action] = 1.0
        return action_vec
