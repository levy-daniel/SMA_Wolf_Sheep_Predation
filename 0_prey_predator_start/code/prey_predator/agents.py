from mesa import Agent
from prey_predator.random_walk import RandomWalker


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
        self.random_move()
        self.energy -= 1
        if self.model.grass :
            temp = 0
          
         
        #Reproduction step:
        #1. Vérifier que la proba est respectée
        #2. Créer l'agent
        #3. L'ajouter au scheduler et à la grille
        #4. Le placer sur la grille
        self.model.initial_sheep += self.model.initial_sheep * self.model.sheep_reproduce
        
        if self.energy < 0:
            self.model.grid.remove_agent(self)
            self.model.schedule.remove(self)
            
            
        # ... to be completed


class Wolf(RandomWalker):
    """
    A wolf that walks around, reproduces (asexually) and eats sheep.
    """

    energy = None

    def __init__(self, unique_id, pos, model, moore, energy=None):
        super().__init__(unique_id, pos, model, moore=moore)
        self.energy = energy

    def step(self):
        self.random_move()
        # ... to be completed


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
        # ... to be completed

    def step(self):
        # ... to be completed