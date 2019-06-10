from mesa.time import BaseScheduler
from settings import *
import numpy as np
import random

def v_in_intv(v, interval):
    #value in intrval
    if v > interval[1]: return interval[1]
    if v < interval[0]: return interval[0]
    return v

class RandomActivationWithMutation(BaseScheduler):
    def pertub_gene(self, agent_key, gene_key):
        agent_key, gene_key = int(agent_key), int(gene_key)
        #print(agent_key, gene_key)
        v = self._agents[agent_key].gen_info[gene_key]
        v += v_in_intv(np.random.normal(0, POPU_MUTA_VAR), (POPU_MUTA_LOW, POPU_MUTA_HIGH))
        self._agents[agent_key].gen_info[gene_key] = v_in_intv(v, (0, 1))
        
    def mutate(self, prob):
        """
	mutate steps:
	1. get all agents number
	2. generate indeicators from bernouli distribution, convert it to its index as keys
	3. generate random perturbations with same length as keys
	4. convert keys to agent key and gene index
	5. add perturbation to certain gene
	"""
        keys = list(self._agents.keys())
        keys_length = len(keys) * GEN_INFO_SIZE
        indicators = np.random.binomial(size=keys_length, n=1, p=prob)
        samples = np.where(indicators)[0]
        #samples = np.random.choice(np.arange(keys_length), int(np.floor(prob * keys_length)))
        #get n random samples where n = floor(prob * total_length)
        (agent_key_idxs, gene_keys) = np.divmod(samples,  GEN_INFO_SIZE)
        for i in range(len(agent_key_idxs)):
            self.pertub_gene(keys[agent_key_idxs[i]], gene_keys[i])

    def step(self):
        """ 
	First do mutation steps. Then,
	Executes the step of all agents, one at a time, in
        random order.

        """
	#version 0.8.5
        self.mutate(MUTATION_PRO)
        for agent in self.agent_buffer(shuffled=True):
            agent.step()
        self.steps += 1
        self.time += 1
        '''
        self.mutate(MUTATION_PRO)
        agent_keys = list(self._agents.keys())
        random.shuffle(agent_keys)

        for agent_key in agent_keys:
            self._agents[agent_key].step()
        self.steps += 1
        self.time += 1
        '''
