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


## 1. M_1


### model level
#### 1. Description:
Basic model. Check the correction of our agent base modeling. 

iter: 2000

times: 400 * 9

Based on initial ration.

#### 2. Model name and agent name: 
basic\_mnodel and basic\_agent
#### 3. Env setting :
Disabled.
#### 4. Step statistic level data :
population size
#### 5. Mutation method:
Disabled.
#### 6. Initial Way:
As default.
#### 7. Initial ratio: 
[0.1 - 0.9]

### Agent level

#### 1. lifetime :
Inf.

#### 2. genetic info size:
As default.

#### 3. generate prob

* ? Initial ration 0.5 : gen_prob in [0.2-0.8]

Fixed. 0.5
#### 4. generate method
Default.
#### 5. env death method
* ? Initial ration 0.5 : gen_prob in [0.2-0.8]
Fixed 0.5