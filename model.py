# model.py
# gene info list length and mutate number per generation
import random
import math
import numpy as np
from mesa.space import MultiGrid, Grid
from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector

GEN_INFO_SIZE = 10
MUT_GEN_LENGHT = 10
# gene info list length and mutate number per generation
LIFE_TIME = 3
MAX_GEN_TICK = 2001
ENV_PRESS_PERIOD = 500
MAX_CAPACITY = 1000
IMPECT_R = 6
ENV_R = 10
ENV_STRESS_COF = 1
MUTATION_VAR = 0.05

T_MAX, T_MIN, T_OPT = 1, -1, 0
ALPHA = math.log(2) / math.log((T_MAX - T_MIN) / (T_OPT - T_MIN))

#global var control env growth rate
VERT_MAX = 200
HORZ_MAX = 200
ALPHA12 = 0.5
ALPHA21 = 0.5
#child position distribution
POS_DIS = [2,1]
#(.15, .3, .3, .15)

def beta(T, tp):
    #if T < 0: T = -1 * T
    beta_l = {0:1, 1:0.8}
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

def compute_type_ratio(model):
    h_count = np.sum([agent.gen_type for agent in model.schedule.agents])#？？？
    total = model.schedule.get_agent_count()
    return h_count * 1.0 / total

def compute_mean_her_prob(model):
    return np.mean([agent.p for agent in model.schedule.agents if agent.gen_type == 1])

def compute_mean_ver_prob(model):
    return np.mean([agent.p for agent in model.schedule.agents if agent.gen_type == 0])

def compute_her_num(model):
    return len([agent.p for agent in model.schedule.agents if agent.gen_type == 1])

def compute_ver_num(model):
    return len([agent.p for agent in model.schedule.agents if agent.gen_type == 0])

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

class GenModel(Model):
    """A model with some number of agents."""
    def __init__(self, N, width, height):
        self.running = True
        self.num_agents = N
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)
        self.uid = self.num_agents

        #model para
        #self.r1, self.r2 = 1.0, 1.0
        #self.her_max = MAX_CAPACITY
        #self.ver_max = MAX_CAPACITY
        #self.alpha12, self.alpha21 = 0.5, 0.5
        self.env_press = (np.sin(np.linspace(0, np.pi * 2 * ENV_PRESS_PERIOD, MAX_GEN_TICK)) + 1 ) / 2 * ENV_STRESS_COF
        #this is how enviroment values generated
        #all values are chosen from a rescaled sin functions
        #total periods for this sin is ENV_PRESS_PERIOD
        #total values number's are MAX_GEN_TICK

        # Create agents
        for i in range(self.num_agents):
            a = GenAgent(i, self, 0, gen_info=np.random.random(GEN_INFO_SIZE))
            self.schedule.add(a)
            # Add the agent to a random grid cell
            x = random.randrange(self.grid.width)
            y = random.randrange(self.grid.height)
            self.grid.place_agent(a, (x, y))

        #collect data
        self.datacollector = DataCollector(
                model_reporters = {"two type ratio (hor/total)": compute_type_ratio, 
                   "env press": get_cur_press,
                   "horizontal generate mean prob": compute_mean_her_prob,
                   "horizontal num": compute_her_num,
                   "vertical generate mean prob": compute_mean_ver_prob,
                   "vertical num": compute_ver_num,
                   "horizontal gene mean info": compute_mean_her_geneinfo,
                   "vertical gene mean info": compute_mean_ver_geneinfo,
                   "horizontal gene max info": compute_max_her_geneinfo,
                   "vertical gene max info": compute_max_ver_geneinfo,
                   "horizontal gene min info": compute_min_her_geneinfo,
                   "vertical gene min info": compute_min_ver_geneinfo
                    })


   # def get_r(self):
     #   env = self.cur_press
    #    r1, r2 = 1 - two_curve(env), 1 - two_curve(env, 0.8)
      #  return r1, r2

    def get_uid(self):
        uid = self.uid
        self.uid += 1
        return uid

    def get_ver_popu_size(self):
        return self.schedule.get_agent_count() - \
                np.sum([agent.gen_type for agent in self.schedule.agents])

    def get_her_popu_size(self):
        return np.sum([agent.gen_type for agent in self.schedule.agents])

    def get_popu_size(self):
        return self.schedule.get_agent_count()

#    def get_gr_rate(self):
#        cur_popu = self.get_popu_size()
#        her_popu = self.get_her_popu_size()
#        ver_popu = self.get_ver_popu_size()
#        #r1, r2 = self.get_r()
#        #ver_rate = r1 * (self.ver_max - ver_popu - self.alpha21 * her_popu)/self.ver_max
#        #her_rate = r2 * (self.her_max - her_popu - self.alpha12 * ver_popu)/self.her_max
#        ver_rate = (self.ver_max - ver_popu - self.alpha21 * her_popu)/self.ver_max
#        her_rate = (self.her_max - her_popu - self.alpha12 * ver_popu)/self.her_max
#        #print("popu and rate:")
#        #print(ver_popu, ver_rate)
#        #print(her_popu, her_rate)
#        return (ver_rate, her_rate)



    def init_env(self):
        self.cur_press, self.env_press = self.env_press[0], self.env_press[1:]

    def step(self):
        #if (self.schedule.steps + 1) % 3 == 0:
        #    self.press = True
        self.press = True
        self.init_env()
        self.datacollector.collect(self)
        print("population size: ", self.get_popu_size())
        print("env pressure", self.cur_press)
        #self.gr_rate = self.get_gr_rate()
        #if self.press:print("env die")
        self.schedule.step()

class GenAgent(Agent):
    def __init__(self, unique_id, model, generation_num, gen_type = None, gen_info = None):
        super().__init__(unique_id, model)
        self.generation_num = generation_num
        self.lifetime = LIFE_TIME
        self.gen_info = gen_info
        if gen_type != None:
            self.gen_type = gen_type
            #0 is vertical, 1 is herizontal
        else:
            self.gen_type = random.choice(range(2))
        self.p = 0

    def die(self):
        self.model.grid.remove_agent(self)
        self.model.schedule.remove(self)

    @staticmethod
    def mutate_gen_info(info):#？？？mutate before resample
        mu = np.array(list(map(range_filter(-1 * 2 * MUTATION_VAR, 2 * MUTATION_VAR), np.random.normal(0, MUTATION_VAR, MUT_GEN_LENGHT))))
        indexes = np.array(range(GEN_INFO_SIZE))
        info[np.random.choice(indexes, MUT_GEN_LENGHT)] += mu 
        return np.array(list(map(range_filter(0,1), info)))

    def get_gen_info_vetical(self):
        info = np.random.choice(self.gen_info, size=len(self.gen_info),  replace=True)
        return self.mutate_gen_info(info)

    def get_gen_info_heri(self, pos):
        neighbour_info = np.concatenate([i.gen_info for i in self.model.grid.get_neighbors(pos, True, include_center=True, radius=IMPECT_R) if i.gen_type == 1])
        info = np.random.choice(neighbour_info, size=len(self.gen_info),  replace=True)
        return self.mutate_gen_info(info)

    def get_local_env_volume_gr_rate(self):
        neighbours = [agent.gen_type for agent in self.model.grid.get_neighbors(self.pos, True, include_center=False, radius=ENV_R)]
        popu, horz_popu = len(neighbours), np.sum(neighbours)#???
        vert_popu = popu - horz_popu
        vert_rate = (VERT_MAX - vert_popu - ALPHA21 * horz_popu)/VERT_MAX
        horz_rate = (HORZ_MAX - horz_popu - ALPHA12 * vert_popu)/HORZ_MAX
        print(vert_rate, horz_rate)
        return (vert_rate, horz_rate)


    @staticmethod
    def get_pos_dis(l, dis):
        #return a prob list of position distribution
        #the length position list is l and should be even(without center)
        #pos near by center has less dis idx
        partition = len(dis) 
        prob = []
        for i in range(1, l // 2 + 1):
            idx = math.ceil((i * 1.0 / (l//2) * partition)) - 1
            prob.append(dis[idx])
        re_prob = sorted(prob[:], reverse = True)
        probs = re_prob + prob
        return np.array(probs) / (1.0 * sum(probs))

    def gener_sus(self):
    #agent make a child
        next_gen_num = self.generation_num + 1
        neighborhood = self.model.grid.get_neighborhood(self.pos, True, include_center=False, radius=IMPECT_R)
        pos_idx = np.random.choice(range(len(neighborhood)), 1, p=self.get_pos_dis(len(neighborhood), POS_DIS), replace=False)
        pos = neighborhood[int(pos_idx)]
        if self.gen_type == 0:
            gen_info = self.get_gen_info_vetical()
        else:
            gen_info = self.get_gen_info_heri(pos)
        sus = GenAgent(self.model.get_uid(), self.model, next_gen_num, self.gen_type, gen_info)
        self.model.schedule.add(sus)
        self.model.grid.place_agent(sus, pos)

    def get_gener_p(self):
    #total growth prob
    #enviroment size growth rate * genetic infor coef
        env_gr_rate = self.get_local_env_volume_gr_rate()[self.gen_type]
        #self_gen_cof = 0.5 + two_curve(np.mean(self.gen_info)) * 0.5
        self_gen_cof = beta(np.mean(self.gen_info) - self.model.cur_press, self.gen_type)
        #return uni_gr_rate * self_gen_cof
        return env_gr_rate * self_gen_cof

    def check_env_press(self):
        press = self.model.cur_press
        coin = np.random.random()
        if beta_death(np.mean(self.gen_info) - self.model.cur_press)  < coin: 
            self.lifetime = 0

    def check_life(self):
        #check whether agent is alive
        #delete angent if it is dead
        #return true if it is alive
        if self.lifetime <= 0:
            self.die()
            return False
        return True
    
    def step(self):
        #agent behavior 
        # 1. check whether still alive
        # 2. get generate child prob(self.get_gener_p) and decide whether generate child(self.gener_sus)
        self.lifetime -= 1
        if self.model.press:
            self.check_env_press()
        alive = self.check_life()
        if alive:
            coin = np.random.random()
            self.p = self.get_gener_p()
            if coin < self.p:
                self.gener_sus()

