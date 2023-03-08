from mesa import Agent
from prey_predator.random_walk import RandomWalker
import random

class Sheep(RandomWalker):
    """
    A sheep that walks around, reproduces (asexually) and gets eaten.

    The init is the same as the RandomWalker.
    """

    energy = None

    def __init__(self, unique_id, pos, model, moore, energy=None):
        super().__init__(unique_id, pos, model, moore=moore)
        self.energy = energy
        self.pos = pos
        self.model = model
        self.moore = moore

    def step(self):
        """
        A model step. Move, then eat grass and reproduce.
        """
        
        # Decrement energy by 1 at each step
        self.energy -= 1 
        
        # Death
        if self.energy <= 0:
            # If energy is less than or equal to 0, remove agent from the grid and the scheduler
            self.model.grid.remove_agent(self)
            self.model.schedule.remove(self)
            return  
        
        # If energy is greater than 0, move randomly
        self.random_move()  # Move randomly in the neighboring cells (Moore)

        # If grass has grown
        if self.model.grass:
            cellmates = self.model.grid.get_cell_list_contents([self.pos])
            for mates in cellmates:
                # If cell contains grass
                if type(mates) is GrassPatch:
                    # If grass is fully grown, eat it and increment energy by the gain from food
                    if mates.fully_grown:
                        self.energy += self.model.sheep_gain_from_food
                        mates.fully_grown = False
          
        # Reproduction step:
        # 1. Check if probability is met
        # 2. Create a new sheep agent
        # 3. Add the new sheep agent to the scheduler
        # 4. Place the new sheep agent on the grid

        # 1. Check if probability is met
        p = random.random()
        if p < self.model.sheep_reproduce:
            # 2. Create a new sheep agent
            self.energy //= 2  # The energy is divided between the parent and the child
            babySheep = Sheep(self.model.next_id(), self.pos, self.model, self.moore, self.energy)
            # 3. Add the new sheep agent to the scheduler
            self.model.schedule.add(babySheep)
            # 4. Place the new sheep agent on the grid
            self.model.grid.place_agent(babySheep, self.pos)   

            


class Wolf(RandomWalker):
    """
    A wolf that walks around, reproduces (asexually) and eats sheep.
    """

    energy = None

    def __init__(self, unique_id, pos, model, moore, energy=None):
        super().__init__(unique_id, pos, model, moore=moore)
        self.energy = energy  # set initial energy
        self.pos = pos  # set initial position
        self.model = model  # set model
        self.moore = moore  # set type of movement

    def step(self):
        self.energy -= 1  # decrease energy

        # Death
        if self.energy <= 0:  # if the wolf's energy is depleted
            self.model.schedule.remove(self)  # remove the wolf from the schedule
            self.model.grid.remove_agent(self)  # remove the wolf from the grid
            return

        self.random_move()  # move randomly
        # Reproduction
        p = random.random()  # generate a random number
        if p < self.model.wolf_reproduce:  # if the number is less than the wolf's reproduction rate
            self.energy //= 2  # reduce the energy of the parent wolf by half
            babyWolf = Wolf(self.model.next_id(), self.pos, self.model, self.moore, self.energy)  # create a baby wolf
            self.model.schedule.add(babyWolf)  # add the baby wolf to the schedule
            self.model.grid.place_agent(babyWolf, self.pos)  # place the baby wolf in the grid

        # Eating
        cellmates = self.model.grid.get_cell_list_contents([self.pos])  # get the agents in the wolf's current cell
        for mate in cellmates:
            if isinstance(mate, Sheep) and self.energy < 15:  # if the wolf is hungry and there is a sheep in the cell
                self.energy += self.model.wolf_gain_from_food  # increase the wolf's energy
                self.model.grid.remove_agent(mate)  # remove the sheep from the grid
                self.model.schedule.remove(mate)  # remove the sheep from the schedule
                break  # stop eating after eating one sheep



class GrassPatch(Agent):
    """
    A patch of grass that grows at a fixed rate and it is eaten by sheep
    """

    def __init__(self, unique_id, pos, model, fully_grown, countdown):
        """
        Creates a new patch of grass

        Args:
            grown: (boolean) Whether the patch of grass is fully grown or not
            countdown: Time for the patch of grass to be fully grown again
        """
        super().__init__(unique_id, model)
        self.pos = pos
        self.model = model
        self.fully_grown = fully_grown
        self.countdown = countdown
        
    def step(self):
        """
        Update the state of the patch of grass at each step
        """
        # Check if the patch of grass is not fully grown
        if self.fully_grown == False:
            self.countdown -= 1
            # Check if the countdown has reached zero
            if self.countdown == 0:
                # Regrow the grass
                self.fully_grown = True
                self.countdown = self.model.grass_regrowth_time



