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

chart1 = ChartModule([{"Label": "two type ratio (ver/total)",
                      "Color": "Black"}, 
		      {"Label": "env press", "Color": "Red"}],
                      data_collector_name='datacollector')

chart2 = ChartModule([{"Label": "horizontal generate mean prob",
                      "Color": "Red"}, 
		      {"Label": "vertical generate mean prob", "Color": "Blue"}],
                      data_collector_name='datacollector')

chart3 = ChartModule([{"Label": "horizontal generate mean info",
                      "Color": "Red"}, 
		      {"Label": "vertical generate mean info", "Color": "Blue"}],
                      data_collector_name='datacollector')



server = ModularServer(GenModel,
                       [grid, chart1, chart2, chart3],
                       "Gen Model",
                       {"N": 200  , 'width':100, 'height':100})

