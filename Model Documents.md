# Model Documents
# Basic Template

## 0. template model


### model level
#### 1. Description:
#### 2. iter and times
#### 3. Model name and agent name:
#### 4. Env setting :
#### 5. Step statistic level data :
#### 6. Mutation method:
#### 7. Initial Way:
#### 8. Initial ratio: 

### Agent level

#### 1. lifetime :
#### 2. genetic info size:
#### 3. generate prob
#### 4. generate method
#### 5. env death method

------------------------------------------------------------

## 1. M_1


### model level
#### 1. Description:
Basic model. Check the correction of our agent base modeling. 

iter: 2000

times: 100 * 9

Based on initial ratio.

#### 2. Model name and agent name: 
basic\_mnodel and basic\_agent
#### 3. Env setting :
Disabled.
#### 4. Step statistic level data :
population size
#### 5. Mutation method:
Disabled.
#### 6. Initial Way:
2000 individuals each.
#### 7. Initial ratio: 
[0.1 - 0.9]

### Agent level

#### 1. lifetime :
Inf.

#### 2. genetic info size:
As default.

#### 3. generate prob

Fixed. 0.3 0.5 0.7
#### 4. generate method
Default.
#### 5. env death method
Fixed 0.1 0.3 0.5  
(0.2对应0.3的出生率，0.3对应0.5的出生率，0.5对应0.7的出生率）

------------------------------------------------------------
## 2. M_2

### model level
#### 1. Description:
Fixed stress, horizontal line, 
Env_pressure=0,0.5,1
iter: 2000

times: 100 * 9

#### 2. Model name and agent name: 
fixed\_mnodel and fixed\_agent
#### 3. Env setting :
Fixed at 0, 0.5, 1
#### 4. Step statistic level data :
population size, population fitness: mean (beta( gene value - enviornment)), population variance, mean gene value
#### 5. Mutation method:
Default, variance=[0.001,0.01] truncated at 2 sd.

#### 6. Initial Way:
Initial variance: 0.1,
#### 7. Initial ratio: 
0.5
### Agent level

#### 1. lifetime :
Inf.

#### 2. genetic info size:
As default.

#### 3. generate prob
As default.

#### 4. generate method
Default.

#### 5. env death method
As default.


------------------------------------------------------------
## 3. M_3

### model level
#### 1. Description:
Linear increasing temperature. 
Various increasing speed, slope [0.001，0.01,0.05,0.1,0.2，0.5] with various mutation.
iter: 2000

times: 100 * 9


#### 2. Model name and agent name: 
linear\_mnodel and linear\_agent
#### 3. Env setting :
Linear increasing, varing slopes
#### 4. Step statistic level data :
population size, population fitness: mean (beta( gene value - enviornment)), population variance, mean gene value
#### 5. Mutation method:
 variance=[0.001,0.01,0.1,0.2], truncated at 2 sd.
slope:[0.001，0.01,0.05,0.1,0.2，0.5]，或者是每一个tick之间温差 

#### 6. Initial Way:
vertical only, horizontal only, both vertical and horizontal presented
#### 7. Initial ratio: 
0.5
### Agent level

#### 1. lifetime :
Inf.

#### 2. genetic info size:
As default.

#### 3. generate prob
As default.

#### 4. generate method
Default.

#### 5. env death method
As default.

???如何控制取点的密度   可能应该改成相邻两个点的差值大小
或者规定一共2000步，决定第2000步的环境压力大小


------------------------------------------------------------
## 4. M_4

### model level
#### 1. Description:
Linear increasing fluctuating temperature. 
x=seq(0,max_tick,1)
coe=rep(c(0,1),50)
y=a*x+0.5+coe*(-b*a)
b>1,b是振幅
a=[0.01] ，b= []
iter: 2000

times: 100 * 9


#### 2. Model name and agent name: 
linear_fluc\_mnodel and linear_fluc\_agent
#### 3. Env setting :
Linear flucutating increasing, varing mean tredn slopes
#### 4. Step statistic level data :
population size, population fitness: mean (beta( gene value - enviornment)), population variance, mean gene value
#### 5. Mutation method:
mutation variance:0.1,0.01,0.001,truncated at 2 sd
#### 6. Initial Way:
Defualt
#### 7. Initial ratio: 
0.5
### Agent level

#### 1. lifetime :
Inf.

#### 2. genetic info size:
As default.

#### 3. generate prob
As default.

#### 4. generate method
Default.

#### 5. env death method
As default.


------------------------------------------------------------

## 5. M_5

### model level
#### 1. Description:
Randomly fluctuating environment. Stress is a random number between [0,1] each step

#### 2. Model name and agent name: 
Random_fluc\_mnodel and Random_fluc\_agent
#### 3. Env setting :
Random number between [0,1]
#### 4. Step statistic level data :
population size, population fitness: mean (beta( gene value - enviornment)), population variance, mean gene value
#### 5. Mutation method:
mutation variance:0.1,0.01,0.001,truncated at 2 sd
#### 6. Initial Way:
Defualt
#### 7. Initial ratio: 
0.5
### Agent level

#### 1. lifetime :
1,5,Inf

#### 2. genetic info size:
As default.

#### 3. generate prob
As default.

#### 4. generate method
Default.

#### 5. env death method
As default.
