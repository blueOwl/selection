from mesa.batchrunner import BatchRunner
from model import GenModel
import pickle


def compute_ratio(model):
    agent_types = [agent.gen_type for agent in model.schedule.agents]
    return sum(agent_types) / len(agent_types)



fixed_params = {'width':100, 'height':100}

variable_params = {'N': [200]}


batch_run = BatchRunner(
    GenModel,
    variable_params,
    fixed_params,
    iterations=5,
    max_steps=20,
    model_reporters={"two type ratio": compute_ratio}
)
batch_run.run_all()
run_data = batch_run.get_model_vars_dataframe()
pickle.dump(run_data, open('res.pkl','wb'))
