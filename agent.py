from mesa import Agent

class RandomAgent(Agent):
    """
    Agent that moves randomly.
    Attributes:
        unique_id: Agent's ID 
        direction: Randomly chosen direction chosen from one of eight directions
    """
    def __init__(self, unique_id, model):
        """
        Creates a new random agent.
        Args:
            unique_id: The agent's ID
            model: Model reference for the agent
        """
        super().__init__(unique_id, model)
        self.direction = 4
        self.condition = "Roomba"

    def move(self):
        """ 
        Determines if the agent can move in the direction that was chosen
        """
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True, # Boolean for whether to use Moore neighborhood (including diagonals) or Von Neumann (only up/down/left/right).
            include_center=True) 
        
        # Checks which grid cells are empty
        freeSpaces = list(map(self.model.grid.is_cell_empty, possible_steps))

        #neighborCells = self.model.grid.neighbor_iter(self.pos)


        # If the cell is empty, moves the agent to that cell; otherwise, it stays at the same position
        if freeSpaces[self.direction]:
            self.model.grid.move_agent(self, possible_steps[self.direction])
            print(f"Se mueve de {self.pos} a {possible_steps[self.direction]}; direction {self.direction}")
        elif self.model.grid[possible_steps[self.direction][0]][possible_steps[self.direction][1]].condition == "Dirty": #Checks if the cell in the intended direction is dirty
            self.model.grid[possible_steps[self.direction][0]][possible_steps[self.direction][1]].condition = "Clean"
            self.model.grid.move_agent(self, possible_steps[self.direction])
        else:
            self.direction = self.random.randint(0,8)
            print(f"No se puede mover de {self.pos} en esa direccion.")

    def step(self):
        """ 
        Determines the new direction it will take, and then moves
        """
        #self.direction = self.random.randint(0,8)
        print(f"Agente: {self.unique_id} movimiento {self.direction}")
        self.move()

class ObstacleAgent(Agent):
    """
    Obstacle agent. Just to add obstacles to the grid.
    """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.condition = "Obstacle"

    def step(self):
        pass

class DirtAgent(Agent):
    """
    Dirt agent, a roomba must pass over the cell to "clean" it
    """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.condition = "Dirty"

    def step(self):
        pass