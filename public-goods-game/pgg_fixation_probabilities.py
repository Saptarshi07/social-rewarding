import random
import numpy as np
import math
import collections
import itertools
import sys
import csv

r = 2 #productivity of the public goods
c = 1 #cost of cooperation, contribution to the public goods
Z = 100 #population size
s = 1 #selection strength
beta = 0.4
gamma = 0.1
lmd = 0.5

filename = 'output-files/example-pgg-fixation.csv'

def get_nr_RS_RA_AR(player_set):
    #returns the number of social rewarders, antisocial rewarders and unconditional rewarders from a list of players 
    #list of players is a list of integers between 0 and 15.
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
        #returns the number of unconditional cooperators, opportunistic cooperators and opportunistic defectors from a list of players 
    #list of players is a list of integers between 0 and 15.
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
    #returns the payoff of every strategy in the public goods game. The composition of the group is the list player set. 
    
    N = len(player_set)
    payoff_dict = {ppl:0 for ppl in player_set}
    
    #frequency of strategies in the group
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
            
    
    return payoff_dict
    
           
all_configs = list(itertools.combinations_with_replacement(range(0,16),4))

config_to_player_dict = {k:{} for k in all_configs}

for config in all_configs:
    config_to_player_dict[config] = get_payoff(config,c,r,beta,gamma,lmd)
 

def check_config_presence(config,list_):
    #returns a certain composition of the group - config - iff it is present in a list of possible compositions - list_
    for perm in list(itertools.permutations(config)):
        if perm in list_:
            return perm
        
def nCr(n,r):
    #calculates the binomial coefficient - choose r from n. 
    if n<r:
        return 0 #this is defined because we dont want to count groups that cannot be formed while evaluating
                 #payoff of strategies
    else:
        f = math.factorial
        return f(n) / f(r) / f(n-r)
    

def get_population_payoff(stg,composition,precomp_payoff,Z):
    #calculates payoff of strategy stg in a population composition is described by
    #dictionary 'composition'. The dictionary 'precomp_payoff' is the dictionary of 
    #the payoff of strategies in any group composition. These are precomputed. 
    if composition[stg] == 0:
        return 0
    
    N = len(list(precomp_payoff.keys())[0])
    all_possible_configs = list(itertools.combinations_with_replacement(range(0,16),N-1))
    
    
    denom = nCr(Z-1,N-1)
    sum_ = 0
    
    for config in all_possible_configs:

        counter=collections.Counter(config)
        prod = 1
        for key in list(counter.keys()):
            comp = composition[key]
            
            if key == stg:
                prod *= nCr(comp-1,counter[key])
            else:
                prod *= nCr(comp,counter[key])
                
        list_ = list(config)
        list_.append(stg)
        
        
        pgg_table = check_config_presence(list_,list(precomp_payoff.keys()))
        

        payoffs_comp = precomp_payoff[pgg_table]

        sum_ += (prod*payoffs_comp[stg])/denom
        
    return sum_
    
            
        
    
def get_fixation_prob(stg_res,stg_mut,s,beta=beta,gamma=gamma,lmd=lmd,c=c,r=r,Z=Z):
    
    #calculates the fixation probability of the strategy stg_mut in the resident population of stg_res
    #under the the imitation dynamics with selection strength s. 
    
    sum_ = 1
    res_payoff = {k:0 for k in range(1,Z)}
    mut_payoff = {k:0 for k in range(1,Z)}
    for k in res_payoff:
        composition = {k:0 for k in range(0,16)}
        composition[stg_res] = k
        composition[stg_mut] = Z-k
            
        pi_mut = get_population_payoff(stg_mut,composition,config_to_player_dict,Z)
        pi_res = get_population_payoff(stg_res,composition,config_to_player_dict,Z)
        res_payoff[k] = pi_res
        mut_payoff[Z - k] = pi_mut
    
    for m in range(1,Z):
        prod = 1
        for n_k in range(1,m+1):
            pi_mut = mut_payoff[n_k]
            pi_res = res_payoff[Z - n_k]
            prod *= math.exp(-s*(pi_mut - pi_res))
        sum_ += prod
    
    return 1/sum_

data = [['stg_res', 'stg_mut', 'beta', 'gamma', 'lmd', 'fix-prob']]




for i in range(0,16):
    for j in range(0,16):
        open_ = [i,j,beta,gamma,lmd]
        if i != j:
            open_.append(get_fixation_prob(i,j,s,beta,gamma,lmd,c,r,Z))
        else:
            open_.append(0)
    data.append(open_)
    


with open(filename, "w") as f:
  writer = csv.writer(f)
  writer.writerows(data)
    
