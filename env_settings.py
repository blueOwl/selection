import numpy as np
from utils import *
from settings import *


sin_fluctuation = (np.sin(np.linspace(0, np.pi * 2 * ENV_PRESS_PERIOD, MAX_GEN_TICK)-0.5*np.pi) +1 ) / 2 * ENV_STRESS_COF#?????
fix_value = [0.5] * MAX_GEN_TICK

increase_env = np.array(fix_value) + np.array(range(len(fix_value))) * 0.005


current_value = fix_value
