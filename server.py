from math import floor
from model import RandomModel, ObstacleAgent, DirtAgent
from mesa.visualization.modules import CanvasGrid, ChartModule, PieChartModule
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter


gridW = 30
gridH = 30
#agentNum = 15
dirtPercentage = 20 #%1 to %100
dirtAmount = floor( ((gridH*gridW)-(gridW*2+gridH*2)) * dirtPercentage/100) #Fills the field with the indicated percantage of dirt
maxSteps = 100

COLORS = {"Dirty": "#B58127", "Clean" : "#9DD0FC"}

def agent_portrayal(agent):
    if agent is None: return
    
    portrayal = {"Shape": "circle",
                 "Filled": "true",
                 "Layer": 2,
                 "Color": "blue",
                 "r": 0.5}

    if (isinstance(agent, ObstacleAgent)):
        portrayal["Color"] = "grey"
        portrayal["Layer"] = 1
        portrayal["r"] = 0.2
    
    if (isinstance(agent, DirtAgent)):
        portrayal["Color"] = COLORS[agent.condition]
        portrayal["Layer"] = 0
        portrayal["Shape"] = "rect"
        portrayal["w"] = 0.2
        portrayal["h"] = 0.2

    return portrayal

dirtChart = ChartModule(
    [{"Label": label, "Color": color} for (label, color) in COLORS.items()]
)
pie_chart = PieChartModule(
    [{"Label": label, "Color": color} for (label, color) in COLORS.items()]
)

model_params = {"N": UserSettableParameter("slider", "Number of roombas", value=1, max_value=floor(((gridH*gridW)-(gridW*2+gridH*2))/2), min_value = 1), #Allows a half of the field to be roombas 
    "width": gridW, 
    "height": gridH, 
    "nDirt": dirtAmount,
    "maxSteps": UserSettableParameter("slider", "Max steps", value=300, max_value=2000, min_value = 1)
}

grid = CanvasGrid(agent_portrayal, gridW, gridH, 500, 500)
server = ModularServer(RandomModel, [grid, dirtChart, pie_chart], "Random Agents", model_params)
                       
server.port = 8521 # The default
server.launch()