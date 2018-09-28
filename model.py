# model.py
import random
import math
import numpy as np
from mesa.space import MultiGrid, Grid
from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector

GEN_INFO_SIZE = 10
LIFE_TIME = 3
MAX_GEN_TICK = 5000
ENV_PRESS_PERIOD = 100
MAX_CAPACITY = 1000
IMPECT_R = 4
ENV_STRESS_COF = 1
MUTATION_VAR = 0.05

T_MAX, T_MIN, T_OPT = 1, -2, 0
ALPHA = math.log(2) / math.log((T_MAX - T_MIN) / (T_OPT - T_MIN))

def beta(T, tp):
    beta_l = {0:1, 1:0.8}
    #tp is agent type, 0 is vertical, 1 is herizontal
    l = beta_l[tp]
    return l * (2 * (T - T_MIN)**ALPHA * (T_OPT - T_MIN)**(2 * ALPHA)) / (T_OPT - T_MIN)**(2 * ALPHA)

def range_filter(start, end):
    def f(x):
        if x < start: 
            return start
        if x > end:
            return end
        return x
    return f

def two_curve(x, l = 1):
    x = x  * 20 * -1 + 10
    k = 0.4
    return l / (1 + np.exp(1) ** ((-k) * x)) * 0.5

def compute_type_ratio(model):
    h_count = np.sum([agent.gen_type for agent in model.schedule.agents])
    total = model.schedule.get_agent_count()
    return h_count * 1.0 / total

class GenModel(Model):
    """A model with some number of agents."""
    def __init__(self, N, width, height):
        self.running = True
        self.num_agents = N
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)
        self.uid = self.num_agents

        #model para
        self.r1, self.r2 = 1.0, 1.0
        self.her_max = MAX_CAPACITY
        self.ver_max = MAX_CAPACITY
        self.alpha12, self.alpha21 = 0.5, 0.5
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
                model_reporters = {"two type ratio": compute_type_ratio})

    def get_r(self):
        env = self.cur_press
        r1, r2 = 1 - two_curve(env), 1 - two_curve(env, 0.8)
        return r1, r2

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

    def get_gr_rate(self):
        cur_popu = self.get_popu_size()
        her_popu = self.get_her_popu_size()
        ver_popu = self.get_ver_popu_size()
        #r1, r2 = self.get_r()
        #ver_rate = r1 * (self.ver_max - ver_popu - self.alpha21 * her_popu)/self.ver_max
        #her_rate = r2 * (self.her_max - her_popu - self.alpha12 * ver_popu)/self.her_max
        ver_rate = (self.ver_max - ver_popu - self.alpha21 * her_popu)/self.ver_max
        her_rate = (self.her_max - her_popu - self.alpha12 * ver_popu)/self.her_max
        print("popu and rate:")
        print(ver_popu, ver_rate)
        print(her_popu, her_rate)
        return (ver_rate, her_rate)



    def init_env(self):
        self.cur_press, self.env_press = self.env_press[0], self.env_press[1:]

    def step(self):
        self.datacollector.collect(self)
        print("population size: ", self.get_popu_size())
        if (self.schedule.steps + 1) % 3 == 0:
            self.press = True
        else:
            self.press = False
        self.init_env()
        print("env pressure", self.cur_press)
        self.gr_rate = self.get_gr_rate()
        if self.press:print("env die")
        self.schedule.step()

class GenAgent(Agent):
    """ An agent with fixed initial wealth."""
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

    def die(self):
        self.model.grid.remove_agent(self)
        self.model.schedule.remove(self)

    def check_life(self):
        if self.lifetime <= 0:
            self.die()
    @staticmethod
    def mutate_gen_info(info):
        mu = np.array(list(map(range_filter(-1 * 2 * MUTATION_VAR, 2 * MUTATION_VAR), np.random.normal(0, MUTATION_VAR, 10))))
        return np.array(list(map(range_filter(0,1), mu + info)))

    def get_gen_info_vetical(self):
        info = np.random.choice(self.gen_info, size=len(self.gen_info),  replace=True)
        return self.mutate_gen_info(info)

    def get_gen_info_heri(self, pos):
        neighbour_info = np.concatenate([i.gen_info for i in self.model.grid.get_neighbors(pos, True, include_center=False, radius=IMPECT_R)])
        info = np.random.choice(neighbour_info, size=len(self.gen_info),  replace=True)
        return self.mutate_gen_info(info)


    def gener_sus(self):
        next_gen_num = self.generation_num + 1
        pos = random.choice(self.model.grid.get_neighborhood(self.pos, True, include_center=False, radius=IMPECT_R))
        if self.gen_type == 0:
            gen_info = self.get_gen_info_vetical()
        else:
            gen_info = self.get_gen_info_heri(pos)
        sus = GenAgent(self.model.get_uid(), self.model, next_gen_num, self.gen_type, gen_info)
        self.model.schedule.add(sus)
        self.model.grid.place_agent(sus, pos)

    def get_gener_p(self):
        uni_gr_rate = self.model.gr_rate[self.gen_type]
        #self_gen_cof = 0.5 + two_curve(np.mean(self.gen_info)) * 0.5
        self_gen_cof = beta(np.mean(self.gen_info) - self.model.cur_press, self.gen_type)
        return uni_gr_rate * self_gen_cof

    def check_env_press(self):
        press = self.model.cur_press
        coin = np.random.random()
        if press - np.mean(self.gen_info)  > coin:
            self.lifetime = 0

    def step(self):
        self.lifetime -= 1
        coin = np.random.random()
        p = self.get_gener_p()
        #print(coin, p)
        if coin < p:
            self.gener_sus()
        if self.model.press:
            self.check_env_press()
        self.check_life()


'''
class EnvGrid(MultiGrid):
    @staticmethod
    def default_val():
        return []
    def __init__(self, width, height, info_length):
        self.info_length = info_length
        super().__init__(width, height, True)

    def add_info(self, pos, info):
        x, y = pos
        for i in info:
            if len(self.grid[x][y]) <= self.info_length:
                self.grid[x][y].append(i)
            else:
                self.grid[x][y].pop(0)
                self.grid[x][y].append(i)
'''
