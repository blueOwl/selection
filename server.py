# server.py
import math
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import ChartModule
from model import GenModel

def agent_portrayal(agent):
    portrayal = {"Shape": "circle",
                 "Filled": "true",
                 "Layer":1,
                 "r": 0.8}
                 #"text":agent.generation_num,
                 #"text_color":'black',

    if agent.gen_type == 0:
        portrayal["Color"] = "red"
    else:
        portrayal["Color"] = "blue"
    return portrayal

grid = CanvasGrid(agent_portrayal, 100, 100, 500, 500)

chart = ChartModule([{"Label": "two type ratio",
                      "Color": "Black"}],
                      data_collector_name='datacollector')


server = ModularServer(GenModel,
                       [grid, chart],
                       "Gen Model",
                       {"N": 200  , 'width':100, 'height':100})

