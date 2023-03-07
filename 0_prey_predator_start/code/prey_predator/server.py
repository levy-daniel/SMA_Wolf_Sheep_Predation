from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.UserParam import UserSettableParameter

from prey_predator.agents import Wolf, Sheep, GrassPatch
from prey_predator.model import WolfSheep


def wolf_sheep_portrayal(agent):
    if agent is None:
        return

    portrayal = {}

    if type(agent) is Sheep:
        # ... to be completed
        portrayal = {"Shape": "circle",
                 "Filled": "true",
                 "Layer": 0,
                 "Color": "red",
                 "r": 0.5}

    elif type(agent) is Wolf:
        portrayal = {"Shape": "circle",
                 "Filled": "true",
                 "Layer": 0,
                 "Color": "blue",
                 "r": 0.5}        # ... to be completed

    elif type(agent) is GrassPatch:
        if agent.fully_grown:
        # ... to be completed
            portrayal = {"Shape": "rect",
                        "Color": "green",
                        "Filled": "true",
                        "Layer": 0,
                        "w": 1,
                        "h": 1}
        else:
            portrayal = {"Shape": "rect",
                        "Color": "#ffffe0",
                        "Filled": "true",
                        "Layer": 0,
                        "w": 1,
                        "h": 1}
    return portrayal


canvas_element = CanvasGrid(wolf_sheep_portrayal, 20, 20, 500, 500)
chart_element = ChartModule(
    [{"Label": "Wolves", "Color": "#AA0000"}, {"Label": "Sheep", "Color": "#666666"}]
)

height=20
width=20 

model_params = {
    "height" : height,
    "width" : width,
    "initial_sheep" :  UserSettableParameter("slider", "Initial Number of Sheep", value=100, min_value=10, max_value=200, step=1),
    "initial_wolves" :  UserSettableParameter("slider", "Initial Number of Wolf", value=25, min_value=10, max_value=200, step=1),
    "sheep_reproduce" :  UserSettableParameter("slider", "Probability of sheep reproduce", value=0.04, min_value=0.01, max_value=0.2, step=0.05),
    "wolf_reproduce" :  UserSettableParameter("slider", "Probability of wolf reproduce", value=0.05, min_value=0.01, max_value=0.2, step=0.05),
    "wolf_gain_from_food" :  UserSettableParameter("slider", "Energy won when eating 1 sheep", value=20, min_value=1, max_value=30, step=1),
    "grass" :  WolfSheep.grass,
    "grass_regrowth_time" :  UserSettableParameter("slider", "Grass regrowth time", value=30, min_value=10, max_value=100, step=1),
    "sheep_gain_from_food" :  UserSettableParameter("slider", "Energy won when eating grass", value=4, min_value=1, max_value=30, step=1)   
    # ... to be completed  
}

server = ModularServer(
    WolfSheep, [canvas_element, chart_element], "Prey Predator Model", model_params
)
server.port = 8080
