import numpy as np
import random
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_context('poster')
sns.set_style("whitegrid", {'axes.grid' : False})

#Generic Environment Class
class Environment:

    def __init__(self, grid=None, shape=None, coverage=None):
        self.agents = {}
        self.a2i = {}
        self.i2a = {}
        self.time_step = 0
        if grid is None:
            if len(shape) != 2 or type(shape[0]) is not int or type(shape[1]) is not int:
                raise TypeError('Expected shape to be tuple of ints')
            elif coverage > 1.0 or coverage < 0:
                raise ValueError('Expected coverage to be [0, 1]')

            self.shape = shape
            self.grid = np.zeros(shape)
            self.agent_grid = np.zeros(shape)

            N = int(shape[0] * shape[1] * coverage)
            n = 0
            while n < N:
                x_rand = random.randint(0, shape[0]-1)
                y_rand = random.randint(0, shape[1]-1)
                if self.grid[x_rand, y_rand] == 0:
                    self.grid[x_rand, y_rand] = -1
                    self.agent_grid[x_rand, y_rand] = -1
                    n += 1
        else:
            self.shape = grid.shape
            self.grid = grid
            self.agent_grid = grid

    def update(self, time_steps=1):
        for t in range(time_steps):
            for agent in self.agents:
                self.agents[agent].transition(self.grid)

            for agent in self.agents:
                self.agents[agent].resolve(self.agents)

            self.time_step += 1

        self.update_agent_grid()

    def update_agent_grid(self):
        self.agent_grid = self.grid.copy()
        for name, agent in self.agents.items():
            self.agent_grid[agent.pos[0], agent.pos[1]] = self.a2i[name] #Deal with this later

    def add_agent(self, agent):
        self.agents[agent.name] = agent
        self.a2i[agent.name] = len(self.agents)
        self.i2a[self.a2i[agent.name]] = agent.name

        for agent in self.agents:
            self.agents[agent].resolve(self.agents)

        self.update_agent_grid()
    # def pretty_print(self):
    #
    #     for y in range(self.shape[1]):
    #
    #         print('\t'.join(s))

    def dump(self):
        print()
    def show_image(self):
        im = np.zeros((self.shape[0], self.shape[1], 3))
        for y in range(self.shape[1]):
            for x in range(self.shape[0]):
                if self.agent_grid[x, y] == 0:
                    im[x, y, :] = np.ones(3)
                elif self.agent_grid[x, y] == -1:
                    im[x, y, :] = np.zeros(3)
                else:
                    im[x, y, :] = self.agents[self.i2a[self.agent_grid[x, y]]].color
        plt.title('Time Step: %d'%self.time_step)
        plt.imshow(im)
        plt.show()
        return im


# Generic Agent Class
class Agent:
    def __init__(self, name, pos=(0,0), color=np.array([0, 0, 1])):
        self.name = name
        self.pos = pos
        self.past_pos = None
        self.color = color

    def transition(self, grid):
        pass

    def resolve(self, agents):
        pass







