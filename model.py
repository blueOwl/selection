# model.py
# gene info list length and mutate number per generation
import random
import math
import numpy as np
from mesa.space import MultiGrid, Grid
from mesa import Agent, Model
from mesa.time import RandomActivation
from customizeTime import RandomActivationWithMutation, RandomActivationMutationNoConstrain
from mesa.datacollection import DataCollector
from utils import *
import settings 
import env_settings

#for env settings see env_settings.py
class GenModel(Model):
    """setting the agent for model"""
    def get_agent_config(self):
        return GenAgent
    def init_env(self):
        return env_settings.current_value
    def model_level_data_collect(self):pass

    def model_level_record_init(self):pass
    
    def model_level_report(self):pass

    def get_schedule(self):
        return RandomActivationWithMutation
    
    def get_gene_init(self, gene_size):
        #return [0] * gene_size
        return np.clip(np.random.normal(loc=settings.INIT_MEAN, scale=settings.INIT_SD, size=gene_size), settings.INIT_LOW, settings.INIT_HIGH)
    
    def __init__(self, N, width, height, init_ratio=0.5):
        self.env_idx = 0
        self.running = True
        self.num_agents = N
        self.grid = MultiGrid(width, height, True)
        self.schedule = self.get_schedule()(self)
        self.uid = self.num_agents
        self.agent = self.get_agent_config()
        self.model_level_record_init()

        #pre-generate enviroment values
        

        self.env_press = self.init_env()
        

        # Create agents
        coins = np.random.random(self.num_agents)
        used = []
        pos = ()
        # for decide agent type
        for i in range(self.num_agents):
            if coins[i] < init_ratio: 
                agent_type = 0
            else:
                agent_type = 1
            a = self.agent(i, self, 0, gen_info=self.get_gene_init(GEN_INFO_SIZE), gen_type=agent_type)
            self.schedule.add(a)
            # Add the agent to a random grid cell
            while True:
            # make sure initial uniq position
                x = random.randrange(self.grid.width)
                y = random.randrange(self.grid.height)
                if not (x, y) in used:
                    pos = (x, y)
                    used.append(pos)
                    break
            self.grid.place_agent(a, (x, y))

        #collect data
        '''
        self.datacollector = DataCollector(
                model_reporters = {"two type ratio (hor/total)": compute_type_ratio, 
                   #"env press": get_cur_press,
                   #"vertical generate env prob": compute_mean_ver_env_prob,
                   #"vertical generate self prob": compute_mean_ver_self_prob,
                   #"horizontal generate env prob": compute_mean_her_env_prob,
                   #"horizontal generate self prob": compute_mean_her_self_prob,
                   #"horizontal generate mean prob": compute_mean_her_prob,
                   "horizontal num": compute_her_num,
                   #"vertical generate mean prob": compute_mean_ver_prob,
                   "vertical num": compute_ver_num,
                   "horizontal gene mean info": compute_mean_her_geneinfo,
                   "vertical gene mean info": compute_mean_ver_geneinfo,
                   "horizontal gene max info": compute_max_her_geneinfo,
                   "vertical gene max info": compute_max_ver_geneinfo,
                   "horizontal gene min info": compute_min_her_geneinfo,
                   "vertical gene min info": compute_min_ver_geneinfo
                    })
         '''


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



    def get_env(self):
        self.cur_press = self.env_press[self.env_idx]
        self.env_idx += 1
    def write_model_level_record(self):
        pass
    
    def step(self):
        #if (self.schedule.steps + 1) % 3 == 0:
         #   self.press = True
        #else:
         #   self.press = False##selection every step, but can explore selection every k step
        self.press = True
        self.get_env()
        '''self.datacollector.collect(self)'''
        print(self.schedule.steps ,"population size: ", self.get_popu_size())
        #print("env pressure", self.cur_press)
        #self.gr_rate = self.get_gr_rate()
        #if self.press:print("env die")
        self.schedule.step()
        self.write_model_level_record()

class GenAgent(Agent):
    def __init__(self, unique_id, model, generation_num, gen_type = None, gen_info = None):
        super().__init__(unique_id, model)
        self.generation_num = generation_num
        self.lifetime = settings.LIFE_TIME
        self.gen_info = gen_info
        if gen_type != None:
            self.gen_type = gen_type
            #0 is vertical, 1 is herizontal
        else:
            self.gen_type = random.choice(range(2))
        self.p = 0
        self.env_gr_rate = 0
        self.self_gen_cof = 0
        self.set_beta()
    
    def set_beta(self):
        self.beta = beta
        self.beta_death = beta_death
        
    def die(self):
        self.model.grid.remove_agent(self)
        self.model.schedule.remove(self)

    @staticmethod
    def mutate_gen_info(info):
        #mutate before resample
        return info

    def get_gen_info_vetical(self):
        info = np.random.choice(self.gen_info, size=len(self.gen_info),  replace=True)
        return self.mutate_gen_info(info)

    def get_gen_info_heri(self):
        pos = self.pos
        neighbour_info = np.concatenate([i.gen_info for i in self.model.grid.get_neighbors(pos, True, include_center=True, radius=settings.IMPECT_R) if i.gen_type == 1])
        info = np.random.choice(neighbour_info, size=len(self.gen_info),  replace=True)
        return self.mutate_gen_info(info)


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
        if not self.model.grid.is_cell_empty(pos): 
            return#if cell is occupied, no reproduction
        if self.gen_type == 0:
            gen_info = self.get_gen_info_vetical()
        else:
            gen_info = self.get_gen_info_heri()
        sus = self.__class__(self.model.get_uid(), self.model, next_gen_num, self.gen_type, gen_info)
        self.model.schedule.add(sus)
        self.model.grid.place_agent(sus, pos)
    
    def get_gener_p(self):
    #total growth prob
        self.self_gen_cof = 1 * self.beta(np.mean(self.gen_info) - self.model.cur_press, self.gen_type)
        return self.self_gen_cof

    def check_env_press(self):
        press = self.model.cur_press
        coin = np.random.random()
        if self.beta_death(np.mean(self.gen_info) - self.model.cur_press)  < coin: 
            self.lifetime = 0

    def check_life(self):
        #check whether agent is alive
        #delete angent if it is dead
        #return true if it is alive
        if self.lifetime <= 0:
            self.die()
            return False
        return True
    
    def muta_genetic_info(self):
        pass
        '''
        individual mutate
        1. mutate with prob MUTATION_THRES
        2. mutate with fixed length MUT_GEN_LENGHT
        3. mutate with truncated normal (0, MUTATION_VAR)
        
        coin = np.random.random()
        if coin < MUTATION_THRES:
            mu = np.array(list(map(range_filter(-1 * 2 * MUTATION_VAR, 2 * MUTATION_VAR), np.random.normal(0, MUTATION_VAR, MUT_GEN_LENGHT))))
            indexes = np.array(range(GEN_INFO_SIZE))
            self.gen_info[np.random.choice(indexes, MUT_GEN_LENGHT, replace=False)] += mu 
            '''
    def step(self):
        #agent behavior 
        # 1. check whether still alive
        # 2. do mutation step
        # 3. get generate child prob(self.get_gener_p) and decide whether generate child(self.gener_sus)
        self.lifetime -= 1

        #indiviual mutation
        self.muta_genetic_info()

        #generate offspring
        coin = np.random.random()
        self.p = self.get_gener_p()
        if coin < self.p:
            self.gener_sus()
   
        #check env 
        if self.model.press:
            self.check_env_press()

        #check alife
        self.check_life()

