import random
import numpy as np
import math
import sys
import csv
import pandas as pd


#population and evolution parameters
mu = 10**-4
T = 10**2
pop = 100
pops = range(1,101)
s = 10

b = 4 #benefit of cooperation
c = 1 #cost of cooperation
beta = 3 #reward value
gamma = 1 #cost of the reward
lmd, r = 0.5, 0.5 #information transmissibility, assortment

filename = 'output-files/example-assortment-timeseries.csv'



def get_payoff(b,c,beta,gamma,lmd):
    
    #calculates the 4X4 payoff matrix of the game

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


def get_pop_payoff(stg1,stg2,payoff_A, payoff_B,r,strategy_dist):
    
    #evaluates the population average payoff of a strategy playing donor strategy stg1 and recipient strategy stg2
    #the strategy labels are as follows - donor strategy 0: C, 1: OC, 2: OD, 3: D; 
    #recipient strategy - 0: NR, 1: SR, 2: AR, 3: UR
    #assortment parameter is r
    
    x = 1/(1-r)
    payoff = 0
    for (i,j) in strategy_dist:
        if (stg1,stg2) != (i,j):
            payoff += payoff_A[stg1][j]*strategy_dist[(i,j)]*0.5 + payoff_B[i][stg2]*strategy_dist[(i,j)]*0.5
        else:
            if strategy_dist[(i,j)] != 0:
                payoff += payoff_A[stg1][j]*(strategy_dist[(i,j)]-1)*x*0.5 + payoff_B[i][stg2]*(strategy_dist[(i,j)]-1)*x*0.5
            else:
                payoff += 0
    
    urn_pop = (pop - strategy_dist[(stg1,stg2)]) + x*(strategy_dist[(stg1,stg2)] - 1)
    payoff *= 1/(urn_pop)
    return payoff


#some helping functions
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
    #calculates the probability to switching from payoff difference and selection strength
    
    return 1/(1 + math.exp(-s*(payoff1 - payoff2)))

stgs_ = []
for i in range(0,4):
    for j in range(0,4):
        stgs_.append((i,j))

def get_stg_dist(donor_behav,recep_behav):
    stg_dist = {k:0 for k in stgs_}
    for i in donor_behav:
        stg_dist[(donor_behav[i], recep_behav[i])] += 1
    return stg_dist

def get_coop_rate(stgs):
    #calculates the average cooperation rate in the population given
    #a distribution of the 16 strategies in the population and assortment r
    N = pop
    sum_ = 0
    for i in [0,1,2,3]:
        sum_ += stgs[i]*(N-1)
    for i in [4,5,6,7]:
        sum_ += stgs[i]*(N-1)*(1 - lmd)
    
    n_sr = stgs[1] + stgs[5] + stgs[9] + stgs[13]
    n_oc = stgs[4] + stgs[5] + stgs[6] + stgs[7]
    n_od = stgs[8] + stgs[9] + stgs[10] + stgs[11]
    
    sum_ += (n_oc - stgs[5])*n_sr*(1-r)*lmd + r*lmd*stgs[5]*(stgs[5] - 1) + (n_od - stgs[9])*n_sr*(1-r)*lmd + r*lmd*stgs[9]*(stgs[9]-1)
                
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

data = ['lmd', 'r', 'mu', 's', 't'] + [str(k) for k in range(0,16)] + ['coop_rate']
       
with open(filename,'w') as file_:
    wr = csv.writer(file_)
    wr.writerow(data)

donor_vals = [0,0,0,0]
reward_vals = [0,0,0,0]


for t in range(0,T):
    
    donor_dist = get_donor_dist(donor_behav)
    reward_dist = get_recep_dist(recep_behav)
    strategy_dist = get_stg_dist(donor_behav,recep_behav)
    stgs_count = []
    for i in range(0,16):
        stgs_count.append(strategy_dist[(int(i/4),i%4)])
    
    focul,rolemodel = random.sample(pops,2)
    focul_dstg, focul_rstg  = donor_behav[focul], recep_behav[focul]
    stg_removed = set(strategy_set) - set([(focul_dstg,focul_rstg)])
    
    if random.uniform(0,1) < mu: ##mutation
        stg = random.sample(stg_removed,1)[0]
        donor_behav[focul], recep_behav[focul] = stg[0], stg[1]
        
    else: ##pairwise comp and select
        rm_dstg, rm_rstg = donor_behav[rolemodel], recep_behav[rolemodel]
        
        
        payoff_rm = get_pop_payoff(rm_dstg,rm_rstg,payoff_A, payoff_B,r,strategy_dist)
        payoff_focul = get_pop_payoff(focul_dstg,focul_rstg,payoff_A, payoff_B,r,strategy_dist)
        
        if random.uniform(0,1) < fermi(payoff_rm, payoff_focul,s):
            donor_behav[focul], recep_behav[focul] = rm_dstg, rm_rstg
            
    coop_rate = get_coop_rate(stgs_count)
    
    line = [lmd,r,mu,s,t] + stgs_count + [coop_rate]

   

    with open(filename,"a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(line)




        




