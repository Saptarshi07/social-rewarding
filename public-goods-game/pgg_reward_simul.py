import random
import numpy as np
import pandas as pd 
import math
import collections
import csv
import itertools
import sys


#Parameters---

r = 2 #productivity
c = 1 #contribution to pgg
Z = 100 #population size
s = 10 #selection strength
N = 4 #size of pgg group
mu = 10**-2 #mutation rate
T = 10**2 #number of time steps for simulation
beta = 0.4 #reward value
gamma = 0.1 #cost of reward
lmd = 0.5 #information transmissibility

#end of parameters----

filename = "output-files/example-pgg-timeseries.csv"

#random_initialization

random_vect = [random.randint(0,100) for i in range(0,16)]
random_vect = [ int(i*100/sum(random_vect)) for i in random_vect]
random_vect[-1] = random_vect[-1] + (100-sum(random_vect))

composition = {k:random_vect[k] for k in range(0,16)}
pop_s = []
for k in composition:
    pop_s.extend([k]*composition[k])
   
random.shuffle(pop_s)
#print(pop_s)
pop_strategy = {k:pop_s[k] for k in range(0,Z)}
#print(pop_s)


#helpful functions

def get_nr_RS_RA_AR(player_set):
    #from a set of players it evaluates the number of SR (nr_RS),AR (nr_RA) and UR (nr_AR)players
    nr_RS = 0
    nr_RA = 0
    nr_AR = 0
    for ppl in player_set:
        if(ppl%4 == 1):
            nr_RS+=1
        elif(ppl%4 == 2):
            nr_RA+=1
        elif(ppl%4 == 3):
            nr_AR+=1
    return (nr_RS,nr_RA,nr_AR)

def get_nr_C_OC_OD(player_set):
    #from a set of players it evaluates the number of C,OC and OD players
    nr_C = 0
    nr_OC = 0
    nr_OD = 0
    for ppl in player_set:
        if(int(ppl/4) == 0):
            nr_C+=1
        elif(int(ppl/4) == 1):
            nr_OC+=1
        elif(int(ppl/4) == 2):
            nr_OD+=1
    return (nr_C,nr_OC,nr_OD)
    
def get_payoff(player_set,c=c,r=r,beta=beta,gamma=gamma,lmd=lmd):
    
    #function for evaluating the payoff of each strategy in a pgg group. 
    #the list player_set defines the composition of the group where strategies are labeled from 0 to 15
    
    #the strategy labels are as follows - donor strategy 0: C, 1: OC, 2: OD, 3: D; 
    #recipient strategy - 0: NR, 1: SR, 2: AR, 3: UR
    
    #the function returns two dictionaries 
    #- payoff dict returns the payoff of each strategy in the group
    #- coop_dict returns the cooperation rate of each strategy in the group
    
    N = len(player_set)
    payoff_dict = {ppl:0 for ppl in player_set}
    
    #frequency of strategies
    freq = {k:0 for k in range(0,16)}
    for i in player_set:
        freq[i] += 1
    
    #donation to PGG
    pot = 0
    for idx in range(0,len(player_set)):
        ppl = player_set[idx]
        others = player_set[:idx] + player_set[idx+1 :]
        n_ppl_rs, n_ppl_ra, n_ppl_ar = get_nr_RS_RA_AR(others)
        
        if(int(ppl/4) == 0):
            pot += c
        elif(int(ppl/4) == 1):
            if beta*(n_ppl_rs - n_ppl_ra) > c*(1 - r/N):
                pot += c
            else:
                pot += (1 - lmd)*c
        elif(int(ppl/4) == 2):
            if beta*(n_ppl_rs - n_ppl_ra) > c*(1 - r/N):
                pot += lmd*c
            else:
                pot += 0
            
        elif(int(ppl/4) == 3):
            pot += 0
            
    coop_rate = pot/(len(player_set)*c)
    pot = pot*r
    
    #pool-sharing, getting reward:
    
    cont_dict = {k:0 for k in range(0,len(player_set))} #makes note of who contributed what
    
    for idx in range(0,len(player_set)):
        
        ppl = player_set[idx]
        #number of rewarders from perspective of player
        others = player_set[:idx] + player_set[idx+1 :]
        n_ppl_rs, n_ppl_ra, n_ppl_ar = get_nr_RS_RA_AR(others)
        
        if(int(ppl/4) == 0):
            payoff_dict[ppl] += pot/N + (n_ppl_rs + n_ppl_ar)*beta - c
            cont_dict[idx] = 1
            
        elif(int(ppl/4) == 1):
            if beta*(n_ppl_rs - n_ppl_ra) > c*(1 - r/N):
                payoff_dict[ppl] += pot/N + (n_ppl_rs + n_ppl_ar)*beta - c
                cont_dict[idx] = 1
            else:
                payoff_dict[ppl] += pot/N + (lmd*n_ppl_ra + (1 - lmd)*n_ppl_rs + n_ppl_ar)*beta - (1-lmd)*c
                cont_dict[idx] = (1-lmd)
                
        elif(int(ppl/4) == 2):
            if beta*(n_ppl_rs - n_ppl_ra) > c*(1 - r/N):
                payoff_dict[ppl] += pot/N + (lmd*n_ppl_rs + (1 - lmd)*n_ppl_ra + n_ppl_ar)*beta - lmd*c
                cont_dict[idx] = lmd
            else:
                payoff_dict[ppl] += pot/N + (n_ppl_ra + n_ppl_ar)*beta
                cont_dict[idx] = 0
            
        elif(int(ppl/4) == 3):
            payoff_dict[ppl] += pot/N + (n_ppl_ar+n_ppl_ra)*beta
            cont_dict[idx] = 0
    
    
    
    for ppl in payoff_dict: 
        payoff_dict[ppl] = payoff_dict[ppl]/freq[ppl]
    
    #giving reward:
    
    for idx in range(0,len(player_set)):
        ppl = player_set[idx]
    
        if(ppl%4 == 1):
            payoff_dict[ppl] -= (sum(cont_dict.values()) - cont_dict[idx])*gamma/freq[ppl] 
                
        elif(ppl%4 == 2):
            payoff_dict[ppl] -= (N-1-(sum(cont_dict.values()) - cont_dict[idx]))*gamma/freq[ppl] 
            
        elif(ppl%4 == 3):
            payoff_dict[ppl] -= (N-1)*gamma/freq[ppl] 
            
    
    return payoff_dict,coop_rate


#precomputing of payoffs:
    #for every possible group configuration in the population, the payoff of strategies in those groups are pre-computed.

all_configs = list(itertools.combinations_with_replacement(range(0,16),N))

config_to_player_dict = {k:{} for k in all_configs}
config_to_cooperation_dict = {k:{} for k in all_configs}

for config in all_configs:
    payoff_cooperation = get_payoff(config)
    config_to_player_dict[config] = payoff_cooperation[0]
    config_to_cooperation_dict[config] = payoff_cooperation[1]
    
#end of precomputing of payoffs    
    
def check_config_presence(config,list_):
    #if the configuration (or any of its permutations) being searched is in the list_ of configurations, 
    #this function returns that configuration
    
    for perm in list(itertools.permutations(config)):
        if perm in list_:
            return perm
        
def nCr(n,r):
    #calculates the binomial coefficient nCr 
    if n<r:
        return 0 #this is defined because we dont want to count groups that cannot be formed while evaluating
                 #payoff of strategies
    else:
        f = math.factorial
        return f(n) / f(r) / f(n-r)
    
    
def get_population_payoff(stg,composition,precomp,Z):
    
    #calculates payoff of strategy stg in a population composition dictionary 'composition' based on pre computed PGG
    #payoff of any table configuration.
    
    if composition[stg] == 0:
        return 0
    
    N = len(list(precomp[0].keys())[0])
    all_possible_configs = list(itertools.combinations_with_replacement(range(0,16),N-1))
    
    
    denom = nCr(Z-1,N-1)
    sum_ = 0
    
    for config in all_possible_configs:
        #print(config)
        counter=collections.Counter(config)
        prod = 1
        for key in list(counter.keys()):
            comp = composition[key]
            #print(comp,key)
            if key == stg:
                prod *= nCr(comp-1,counter[key])
            else:
                prod *= nCr(comp,counter[key])
                
        list_ = list(config)
        list_.append(stg)
        
        #print(list_)
        pgg_table = check_config_presence(list_,list(precomp[0].keys()))
        
        #print(pgg_table)
        payoffs_comp = precomp[0][pgg_table]
        #print(payoffs_comp[stg])
        #print(prod/denom)
        sum_ += (prod*payoffs_comp[stg])/denom
        
    return sum_


def get_population_cooperation(composition,coop_precomp):
    #gets the cooperation rate of the population considering groups are forming randomly in a well mixed population
    #with composition given by the dictionary composition
    coop = 0
    list_ = [] 
    for i in composition:
        if composition[i] != 0:
            list_ += [i]*composition[i]
    combinations = list(itertools.combinations(list_, 4))
    coop = 0
    for i in combinations:
        coop += coop_precomp[i]
    return coop/(len(combinations))    
    
def fermi(payoff1,payoff2,s):
    return 1/(1 + math.exp(-s*(payoff1 - payoff2)))

def choose_from_without(list_,without):
    temp = list_
    temp.remove(without)
    return random.choice(temp)



#data

data = [['t','s','beta', 'gamma', 'lmd', 'mu','coop'] + [str(k) for k in list(composition.keys())]]

with open(filename, "w") as f:
    writer = csv.writer(f)
    writer.writerows(data)
    
#simulation:

for t in range(0,T):
    coop = get_population_cooperation(composition,config_to_cooperation_dict)
    
    results = [[t,s,beta,gamma,lmd,mu,coop] + [composition[k] for k in range(0,len(composition))]]
    
    with open(filename, "a") as f:
        writer = csv.writer(f)
        writer.writerows(results)
    
    focul = random.randint(0,Z-1)
    focul_stg = pop_strategy[focul]
    if random.uniform(0,1) < mu:
        random_stg = choose_from_without(list(range(0,16)),focul_stg)
        pop_strategy[focul] = random_stg
    else:
        
        rm = choose_from_without(list(range(0,Z)),focul)
        rm_stg = pop_strategy[rm]
        
        payoff_rm_stg = get_population_payoff(rm_stg,composition,(config_to_player_dict,config_to_cooperation_dict),Z)
        payoff_focul_stg = get_population_payoff(focul_stg,composition,(config_to_player_dict,config_to_cooperation_dict),Z)
        
        if random.uniform(0,1) < fermi(payoff_rm_stg,payoff_focul_stg,s):
            pop_strategy[focul] = rm_stg
            
    comp = collections.Counter(list(pop_strategy.values()))
    composition = {k:0 for k in range(0,16)}
    for i in comp:
        composition[i] = comp[i]




    
       