from model import *

model = GenModel(200, 50, 50)
for i in range(100):
        model.step()

print(model.datacollector.get_model_vars_dataframe())
