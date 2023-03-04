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
        self.random_move()
        self.energy -= 1
        if self.model.grass :
            cellmates = self.model.grid.get_cell_list_contents([self.pos])
            for mates in cellmates:
                if type(mates) is GrassPatch:
                    #Idée : step de fully grown qui rapport plus ou moins d'énergie, if mates.fully_grown != True, ca apporte moins
                    #est ce qu'on remove le carré d'herbe et on en refait pousser random dans les staps de l'agent grass ou juste on attend qu'il repousse au meme endroit
                    #pour remanger
                    if mates.fully_grown:
                        self.energy += self.model.sheep_gain_from_food
                        mates.fully_grown = False
          
         
        #Reproduction step:
        #1. Vérifier que la proba est respectée
        #2. Créer l'agent
        #3. L'ajouter au scheduler 
        #4. Le placer sur la grille
        p = random.random()
        if p < self.model.sheep_reproduce:
            babySheep = Sheep(self.model.next_id(), self.pos, self.model, True, self.energy)
            self.model.schedule.add(babySheep)
            self.model.grid.place_agent(babySheep, babySheep.pos)   
             
        if self.energy < 0:
            self.model.grid.remove_agent(self)
            self.model.schedule.remove(self)
            


class Wolf(RandomWalker):
    """
    A wolf that walks around, reproduces (asexually) and eats sheep.
    """

    energy = None

    def __init__(self, unique_id, pos, model, moore, energy=None):
        super().__init__(unique_id, pos, model, moore=moore)
        self.energy = energy
        self.pos = pos
        self.model = model
        self.moore = moore

    def step(self):
        self.random_move()
        self.energy -=1
        
        p = random.random()
        if p < self.model.wolf_reproduce:
            babyWolf = Wolf(self.model.next_id(), self.pos, self.model, self.moore, self.energy)
            self.model.schedule.add(babyWolf)
            self.model.grid.place_agent(babyWolf, babyWolf.pos)
            
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        for mates in cellmates:
            if type(mates) is Sheep:
                self.energy += self.model.wolf_gain_from_food
                self.model.grid.remove_agent(mates)
                self.model.schedule.remove(mates)
                break
                
        if self.energy < 0:
            self.model.schedule.remove(self)
            self.model.grid.remove_agent(self)
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
        self.pos = pos
        self.model = model
        self.fully_grown = fully_grown
        self.countdown = countdown
        
    def step(self):
        if self.fully_grown == False:
            self.countdown -= 1
            if self.countdown == 0:
                self.fully_grown = True
                self.countdown = self.model.grass_regrowth_time