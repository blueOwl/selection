import math

GEN_INFO_SIZE = 50
# gene info list length and mutate number per generation
LIFE_TIME = 5
MAX_GEN_TICK = 2001
ENV_PRESS_PERIOD = 50
MAX_CAPACITY = 1000
IMPECT_R = 10
#generate sus position
#get genetic range
#ENV_R = 10
ENV_STRESS_COF = 1
#mutation settings
'''
MUTATION_VAR = 0.05
MUTATION_THRES = 0.01
MUT_GEN_LENGHT = 2


'''
POPU_MUTA_LOW = -1
POPU_MUTA_HIGH = 1
POPU_MUTA_VAR = 0.1
MUTATION_PRO = 0.01
#beta function settings
T_MAX = 1
T_MIN = -1
T_OPT = 0
ALPHA = math.log(2) / math.log((T_MAX - T_MIN) / (T_OPT - T_MIN))

#global var control env growth rate
'''
VERT_MAX = 200
HORZ_MAX = 200
ALPHA12 = 0.2
ALPHA21 = 0.2
'''
#child position distribution
POS_DIS = [2,1]
#(.15, .3, .3, .15)

TYPE_MAP = {0:'vert',
            1:'horz'}

