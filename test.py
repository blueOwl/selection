from mesa.batchrunner import BatchRunner, BatchRunnerMP
from mesa.time import RandomActivation
from model import *
import pickle
import numpy as np
import uuid

from customizeTime import *
import env_settings

#M_1 model part
TYPE_MAP = {0:'vert',
            1:'horz'}
class A_1(GenAgent):
        
    def get_gener_p(self):
        #set generate prob at model level
        return self.model.generate_prob
    def muta_genetic_info(self):
        # no need for mutation
        pass
    def check_env_press(self):
        death_prob = self.model.death_prob
        coin = np.random.random()
        if coin < death_prob:
            self.lifetime = 0
        else:
            self.lifetime = 1
        #die with fixed prob, inf lifetime
        
class M_1(GenModel):
    def get_agent_config(self):
        return A_1
    
    def init_env(self):
        #no influence
        return env_settings.increase_env
    
    def get_schedule(self):
        return RandomActivation
    #
    def __init__(self, N, width, height, specific_kargs):
        self.specific_kargs_str = '_'.join([str(i) for i in specific_kargs.values()])
        self.generate_prob = specific_kargs['generate_prob']
        self.death_prob = specific_kargs['death_prob']
        init_ratio = specific_kargs['init_ratio']
        super().__init__(N, width, height, init_ratio)
        #specific_kargs = {'generate_prob':,
        #                  'death_prob':,                  
        #                  'init_ratio':                 
        #                                    }
        

    
    def model_level_record_init(self):
        data_file_name = "./M1_" + self.specific_kargs_str + '_' + str(uuid.uuid1())
        print('data in file ', data_file_name)
        self.data_file = open(data_file_name, 'w', buffering = 1)
        self.data_file.write('#' + '\t'.join((TYPE_MAP[0], TYPE_MAP[1])) + '\n')
        
    def collect_data(self):
        return (self.get_ver_popu_size(), self.get_her_popu_size())
        
        
    def step(self):
        data = self.collect_data()
        print(data)
        self.data_file.write('\t'.join([str(d) for d in data]) + '\n')
        super().step()
        
        
# M1 running part
fixed_params = {'N':2000, 'width':100, 'height':100}

variable_params = {'specific_kargs': [{'generate_prob': 0.6, 'death_prob': 0.5, 'init_ratio':0.5}]}

batch_run = BatchRunnerMP(
    M_1, 5,
    variable_parameters=variable_params,
    fixed_parameters=fixed_params,
    iterations=10,
    max_steps=800,
)
batch_run.run_all()
