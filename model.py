from mesa import Model
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
from mesa.space import Grid
from agent import RandomAgent, ObstacleAgent, DirtAgent

class RandomModel(Model):
    """ 
    Creates a new model with random agents.
    Args:
        N: Number of agents in the simulation
        height, width: The size of the grid to model
    """
    def __init__(self, N, nDirt, width, height, maxSteps):
        self.num_agents = N
        self.dirtAmount = nDirt
        self.grid = Grid(width,height,torus = False) 
        self.schedule = RandomActivation(self)
        self.running = True
        self.steps = 0
        self.maxSteps = maxSteps

        self.datacollector = DataCollector(
            {
                "Dirty": lambda m: self.countType(m, "Dirty"),
                "Clean": lambda m: self.countType(m, "Clean"),
            }
        )
        
        # Creates the border of the grid
        border = [(x,y) for y in range(height) for x in range(width) if y in [0, height-1] or x in [0, width - 1]]

        for pos in border:
            obs = ObstacleAgent(pos, self)
            self.schedule.add(obs)
            self.grid.place_agent(obs, pos)

        # Add the roomba at the 1,1 coords
        for i in range(self.num_agents):
            a = RandomAgent(i+1000, self) 
            self.schedule.add(a)

            pos = (1,1)
            self.grid.place_agent(a, pos)
        
        #Adds dirt cells
        for i in range(self.dirtAmount):
            a = DirtAgent(i+2000, self) 
            self.schedule.add(a)

            pos_gen = lambda w, h: (self.random.randrange(w), self.random.randrange(h))
            pos = pos_gen(self.grid.width, self.grid.height)
            while (not self.grid.is_cell_empty(pos)):
                pos = pos_gen(self.grid.width, self.grid.height)
            self.grid.place_agent(a, pos)

    
        self.running = True
        self.datacollector.collect(self)

    def step(self):
        '''Advance the model by one step.'''
        self.schedule.step()
        self.datacollector.collect(self)
        stepCount = self.schedule.steps

        # Halt if there's no dirty cells
        if self.countType(self, "Dirty") == 0 or stepCount == self.maxSteps:
            self.running = False

    #Helps count cells of a given tupe
    @staticmethod
    def countType(model, cellCondition):
        count = 0
        for cell in model.schedule.agents:
            if cell.condition == cellCondition:
                count += 1

        return count