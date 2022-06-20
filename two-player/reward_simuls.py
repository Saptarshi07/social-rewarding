import random
import numpy as np
import math
import sys
import csv

#game parameters

lmd = 0.5 #information transmissibility
b = 4 #benefit
c = 1 #cost
beta = 3 #reward
gamma = 1 #cost of the reward

#evolution parameters
pop = 100 #population size
pops = range(1,pop+1)
s = 1 #selection strength
mu = 10**-1 #mutation rate
T = 10**2 #number of timesteps


filename = 'output-files/example-times-series-two-player.csv'


#Strategies are labeled from 0 to 15. 
# 0: C,NR   1: C,SR   2: C,AR    3: C,UR
# 4: OC,NR  5: OC,SR  6: OC,AR   7: OC,UR
# 8: OD,NR  9: OD,SR  10: OD,AR  11: OD,UR
# 12: D,NR 13: D,SR   14: D,AR   15: D,UR


def get_payoff(b,c,beta,gamma,lmd):
    
    #computes the 4 X 4 payoff matrix
    
    payoff_A = np.zeros((4,4))
    payoff_B = np.zeros((4,4))

    payoff_A[0][0], payoff_B[0][0] = (-c), (b)
    payoff_A[0][1], payoff_B[0][1] = (-c + beta), (b - gamma)
    payoff_A[0][2], payoff_B[0][2] = (-c),  (b)
    payoff_A[0][3], payoff_B[0][3] = (-c + beta), (b - gamma)
    payoff_A[1][0], payoff_B[1][0] = (-(1-lmd)*c),  ((1-lmd)*b)
    payoff_A[1][1], payoff_B[1][1] = (-c + beta), (b - gamma)
    payoff_A[1][2], payoff_B[1][2] = (lmd*beta - (1 - lmd)*c), ((1- lmd)*b - lmd*gamma)
    payoff_A[1][3], payoff_B[1][3] = (beta - (1 - lmd)*c), ((1- lmd)*b - gamma)
    payoff_A[2][0], payoff_B[2][0] = (0), (0)
    payoff_A[2][1], payoff_B[2][1] = (-lmd*c + lmd*beta), (lmd*b - lmd*gamma)
    payoff_A[2][2], payoff_B[2][2] = (beta), (-gamma)
    payoff_A[2][3], payoff_B[2][3] = (beta),  (-gamma)
    payoff_A[3][0], payoff_B[3][0] = (0), (0)
    payoff_A[3][1], payoff_B[3][1] = (0), (0)
    payoff_A[3][2], payoff_B[3][2] = (beta), (-gamma)
    payoff_A[3][3], payoff_B[3][3] = (beta), (-gamma)
    return payoff_A, payoff_B

def get_avg_payoff(stg1,stg2,payoff_A, payoff_B,donor_dist,reward_dist):
    #evaluates the population average payoff of a strategy playing donor strategy stg1 and recipient strategy stg2
    #the strategy labels are as follows - donor strategy 0: C, 1: OC, 2: OD, 3: D; 
    #recipient strategy - 0: NR, 1: SR, 2: AR, 3: UR
    
    eval_doner = 0 
    eval_recep = 0
    eval_same = 0.5*(payoff_A[stg1][stg2] + payoff_B[stg1][stg2])
    for j in range(0,4):
        eval_doner += payoff_A[stg1][j]*reward_dist[j]*0.5
        eval_recep += payoff_B[j][stg2]*donor_dist[j]*0.5
    return (1/(pop - 1))*(eval_doner + eval_recep - eval_same)
    
def get_donor_dist(donor_behav):
    res = {0:0,1:0,2:0,3:0}
    for i in donor_behav:
        res[donor_behav[i]] += 1
    return res
    
def get_recep_dist(recep_behav):
    res = {0:0,1:0,2:0,3:0}
    for i in recep_behav:
        res[recep_behav[i]] += 1
    return res
    
def fermi(payoff1,payoff2,s):
    return 1/(1 + math.exp(-s*(payoff1 - payoff2)))


def get_stg_dist(donor_behav,recep_behav):
    stgs = {k:0 for k in range(0,16)}
    for k in donor_behav:
        i = donor_behav[k]
        j = recep_behav[k]
        stgs[i*4 + j] += 1
    return stgs


def get_coop_rate(stgs):
    #calculates the average cooperation rate in the population given
    #a distribution of the 16 strategies in the population
    N = pop
    sum_ = 0
    for i in [0,1,2,3]:
        sum_ += stgs[i]*(N-1)
    for i in [4,5,6,7]:
        sum_ += stgs[i]*(N-1)*(1 - lmd)
    for i in [4,5,6,7]:
        for j in [1,5,9,13]:
            if i!=j:
                sum_ += stgs[i]*stgs[j]*lmd
            else:
                sum_ += stgs[i]*(stgs[j] - 1)*lmd
                
    for i in [8,9,10,11]:
        for j in [1,5,9,13]:
            if i!=j:
                sum_ += stgs[i]*stgs[j]*lmd
            else:
                sum_ += stgs[i]*(stgs[j] - 1)*lmd
                
    sum_ = sum_/(N*(N-1))
    return sum_
    


## equal initialization 

payoff_A, payoff_B = get_payoff(b,c,beta,gamma,lmd)
donor_behav = {i:0 for i in range(1,pop+1)}
recep_behav = {i:0 for i in range(1,pop+1)}

D = [0]*int(pop/4) + [1]*int(pop/4) + [2]*int(pop/4) + [3]*int(pop/4)
R = [0]*int(pop/4) + [1]*int(pop/4) + [2]*int(pop/4) + [3]*int(pop/4)
random.shuffle(D)
random.shuffle(R)

for i in range(1,101):
    donor_behav[i] = D.pop()
    recep_behav[i] = R.pop()


    
strategy_set = []
for i in range(0,4):
    for j in range(0,4):
        strategy_set.append((i,j))



dres_book = {i:[] for i in range(0,4)}
rres_book = {i:[] for i in range(0,4)}



#setting up the data-file for writing the time series output

data = ['gamma','lmd','mu', 's', 't'] + [str(k) for k in range(0,16)] + ['coop_rate']



with open(filename,'w') as file_:
    wr = csv.writer(file_)
    wr.writerow(data)

donor_vals = [0,0,0,0]
reward_vals = [0,0,0,0]


for t in range(0,T):

    donor_dist = get_donor_dist(donor_behav)
    reward_dist = get_recep_dist(recep_behav)
    
    stgs = get_stg_dist(donor_behav,recep_behav)
    print(stgs)
        
        
    coop_rate = get_coop_rate(stgs)

            
    focul,rolemodel = random.sample(pops,2)
    focul_dstg, focul_rstg  = donor_behav[focul], recep_behav[focul]
    stg_removed = set(strategy_set) - set([(focul_dstg,focul_rstg)])
    
    ##mutation
    
    if random.uniform(0,1) < mu: 
        stg = random.sample(stg_removed,1)[0]
        donor_behav[focul], recep_behav[focul] = stg[0], stg[1]
        
    ##pairwise comp and select
    
    else:
        rm_dstg, rm_rstg = donor_behav[rolemodel], recep_behav[rolemodel]
        payoff_rm = get_avg_payoff(rm_dstg,rm_rstg,payoff_A, payoff_B,donor_dist,reward_dist)
        payoff_focul = get_avg_payoff(focul_dstg,focul_rstg,payoff_A, payoff_B, donor_dist,reward_dist)

        if random.uniform(0,1) < fermi(payoff_rm, payoff_focul,s):
            donor_behav[focul], recep_behav[focul] = rm_dstg, rm_rstg
            


    data = [gamma,lmd,mu,s,t] + [stgs[k] for k in stgs] + [coop_rate]



    with open(filename,'a') as file_:
        wr = csv.writer(file_)
        wr.writerow(data)



        




