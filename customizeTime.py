from mesa.time import BaseScheduler
import numpy as random

class RandomActivationWithMutation(BaseScheduler):
    def mutate(self, keys, prob):
        """
	mutate steps:
	1. get all agents number
	2. random choose keys from #agents * gene length with prob
	3. generate random perturbations with same length as keys
	4. convert keys to agent key and gene number
	5. add perturbation to certain gene
	"""
        keys_length = len(keys) * GEN_INFO_SIZE
         
    def step(self):
        """ 
	First do mutation steps. Then,
	Executes the step of all agents, one at a time, in
        random order.

        """
        agent_keys = list(self._agents.keys())
	mutate(agent_keys, MUTATION_PRO)
        random.shuffle(agent_keys)

        for agent_key in agent_keys:
            self._agents[agent_key].step()
        self.steps += 1
        self.time += 1
