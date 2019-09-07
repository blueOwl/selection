import numpy as np
import os
from settings import * 

def check_path(path):
    if not os.path.exists(path): 
        try:os.mkdir(path)
        except:pass
    return path

def compute_type_ratio(model):
    h_count = np.sum([agent.gen_type for agent in model.schedule.agents])#？？？
    total = model.schedule.get_agent_count()
    return h_count * 1.0 / total

def compute_mean_her_env_prob(model):
    data = [agent.env_gr_rate for agent in model.schedule.agents if agent.gen_type == 1 and agent.env_gr_rate != 0]
    return np.mean(data)
def compute_mean_her_self_prob(model):
    return np.mean([agent.self_gen_cof for agent in model.schedule.agents if agent.gen_type == 1 and agent.self_gen_cof != 0])
def compute_mean_ver_env_prob(model):
    return np.mean([agent.env_gr_rate for agent in model.schedule.agents if agent.gen_type == 0 and agent.env_gr_rate != 0])
def compute_mean_ver_self_prob(model):
    return np.mean([agent.self_gen_cof for agent in model.schedule.agents if agent.gen_type == 0 and agent.self_gen_cof != 0])
#self.env_gr_rate * self.self_gen_cof

def compute_mean_her_prob(model):
    return np.mean([agent.p for agent in model.schedule.agents if agent.gen_type == 1 and agent.p != 0])

def compute_mean_ver_prob(model):
    return np.mean([agent.p for agent in model.schedule.agents if agent.gen_type == 0 and agent.p != 0])

def compute_her_num(model):
    return len([agent for agent in model.schedule.agents if agent.gen_type == 1])

def compute_ver_num(model):
    return len([agent for agent in model.schedule.agents if agent.gen_type == 0])

def compute_mean_her_geneinfo(model):
    return np.mean([np.mean(agent.gen_info) for agent in model.schedule.agents if agent.gen_type == 1])

def compute_mean_ver_geneinfo(model):
    return np.mean([np.mean(agent.gen_info) for agent in model.schedule.agents if agent.gen_type == 0])

def compute_max_her_geneinfo(model):
    return np.mean([np.max(agent.gen_info) for agent in model.schedule.agents if agent.gen_type == 1])

def compute_max_ver_geneinfo(model):
    return np.mean([np.max(agent.gen_info) for agent in model.schedule.agents if agent.gen_type == 0])

def compute_min_her_geneinfo(model):
    return np.mean([np.min(agent.gen_info) for agent in model.schedule.agents if agent.gen_type == 1])

def compute_min_ver_geneinfo(model):
    return np.mean([np.min(agent.gen_info) for agent in model.schedule.agents if agent.gen_type == 0])

def beta(T, tp):
    #if T < 0: T = -1 * T
    tp = TYPE_MAP[tp]
    beta_l = {	'vert':1, 
		'horz':1.0}
    #tp is agent type, 0 is vertical, 1 is horizontal
    l = beta_l[tp]
    return l * ((2 * (T - T_MIN)**ALPHA *(T_OPT-T_MIN)** ALPHA) - (T - T_MIN) ** (2 * ALPHA)) / ((T_OPT - T_MIN)**(2 * ALPHA))

def beta_death(T):
    return ((2 * (T - T_MIN)**ALPHA *(T_OPT-T_MIN)** ALPHA) - (T - T_MIN) ** (2 * ALPHA)) / ((T_OPT - T_MIN)**(2 * ALPHA))


def range_filter(start, end):
    def f(x):
        if x < start: 
            return start
        if x > end:
            return end
        return x
    return f

#def two_curve(x, l = 1):
 #   x = x  * 20 * -1 + 10
  #  k = 0.4
   # return l / (1 + np.exp(1) ** ((-k) * x)) * 0.5


def get_cur_press(model):
    return model.cur_press

def compute_ratio(model):
    agent_types = [agent.gen_type for agent in model.schedule.agents]
    return 1 - (sum(agent_types) / len(agent_types))
