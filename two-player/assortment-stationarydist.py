import random
import numpy as np
import pandas as pd 
import math
import sys
import csv

b = 4 #benefit
c = 1 #cost
beta = 3 #reward
gamma = 1 #cost of the reward
pop = 100 #population size
s = 1 #selection strength


filename = "output-files/example-assortment-stationarydist.csv"


def get_payoff(b,c,beta,gamma,lmd):
    
    #computes the 4X4 payoff matrix for the game between donors and recipient

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


all_stgs = []
for i in range(0,4):
    for j in range(0,4):
        all_stgs.append((i,j))


def get_pop_payoff(stg1,stg2,payoff_A, payoff_B,r,strategy_dist):

    #evaluates the population average payoff of a strategy playing donor strategy stg1 and recipient strategy stg2
    #the strategy labels are as follows - donor strategy 0: C, 1: OC, 2: OD, 3: D; 
    #recipient strategy - 0: NR, 1: SR, 2: AR, 3: UR
    #assortment parameter is r

    if r!= 1:
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
    
    elif r ==1:
        payoff = 0
        if strategy_dist[(stg1,stg2)] > 1:
            payoff = payoff_A[stg1][stg2]*0.5 + payoff_B[stg1][stg2]*0.5
        else:
            payoff = 0
            
        return payoff
        


def get_fix_prob_rel(stg1,stg2,lmd,r,s):
    
    #calculates the fixation probability of a mutant stg2 in a homogenous resident population stg1
    
    payoff_A, payoff_B = get_payoff(b,c,beta,gamma,lmd) 
    sum_ = 0
    for m in range(1,pop):
        val = 1
        for nkl in range (1,m+1):
            strategy_dist = {k:0 for k in all_stgs}
            strategy_dist[stg1] += pop-nkl
            strategy_dist[stg2] += nkl
            
            mut_payoff = get_pop_payoff(stg2[0], stg2[1], payoff_A, payoff_B, r, strategy_dist)
            res_payoff = get_pop_payoff(stg1[0], stg1[1], payoff_A, payoff_B, r, strategy_dist) 
            val *= math.exp(-s*(mut_payoff - res_payoff)) 
        sum_ += val
    return 1/(1 + sum_)
    
    
def get_STM(lmd, r, s):
    
    #computes the stationary transition matrix of the population going from 
    #one monomorphic state to another. It is a 16X16 matrix because of 16 strategies.
    
    STM = np.zeros((16,16))
    stgnr_pair = {i: (int(i/4),i%4) for i in range(0,16)}
    for i in range(0,16):
        for j in range(0,16):
            if i!= j:
                stgset1 = stgnr_pair[i]
                stgset2 = stgnr_pair[j]
                STM[i][j] = (1/15)*get_fix_prob_rel(stgset1, stgset2,lmd,r,s)
        row_sum = sum(STM[i])
        STM[i][i] = 1 - row_sum
    print(lmd,r)
    return STM


data = [['lmd', 'r', 's'] + [str(k) for k in range(0,16)]]

#note that r=0 gives stationary distribution for the well mixed population

#the following computes the stationary distribuion for 441 parameter combination of r and lambda -  both ranging from 0 to 1
#this may take some time to compute. To try out for lesser values change the variable range_ below from 21 to less

range_ = 21

for lmd in np.linspace(0,1,range_):
    for r in np.linspace(0,1,range_):
        STM = get_STM(lmd,r,s)
        D, V = np.linalg.eig(STM.T)
        near1_idx = min(D, key=lambda x:abs(x-1))
        vec = list(V[:,list(D).index(near1_idx)].real) #unnormalized std

        std = []
        for val in vec:
            std.append(val/sum(vec))
            
        data.append([lmd,r,s] + std)
        
        

with open(filename,"w") as f:
    writer = csv.writer(f)
    writer.writerows(data)

