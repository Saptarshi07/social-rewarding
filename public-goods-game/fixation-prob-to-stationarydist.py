import csv
import pandas as pd
import numpy as np

#this script converts a dataframe of fixation probability to stationary distribution. 
#The input file 'input-files/fixation-probs.csv' of fixation probability for beta = 0.16 lmd = 0.1 is read from input files and #its corresponding stationary distribution is written in output-files/stationary-dist.csv

def get_transition_matrix_from_fixation_df(df):
    mtx = np.zeros((16,16))
    for i in range(0,16):
        for j in range(0,16):
            if i!= j:
                fx = df.loc[df['stg'] == i][str(j)].values[0]
                mtx[i][j] = (1/15)*fx
    for i in range(0,16):
        mtx[i][i] = 1 - sum([mtx[i][j] for j in range(0,16)])
    return mtx

data = [['beta','lmd'] + [str(k) for k in range(0,16)]]

 
    
df = pd.read_csv('input-files/example-fixation-probs.csv')
beta,lmd = df['beta'].drop_duplicates().values[0], df['lmd'].drop_duplicates().values[0]
STM = get_transition_matrix_from_fixation_df(df)

D, V = np.linalg.eig(STM.T)
near1_idx = min(D, key=lambda x:abs(x-1))
vec = list(V[:,list(D).index(near1_idx)].real) #unnormalized std

std = []
for val in vec:
    std.append(val/sum(vec))

data.append([beta, lmd] + std)
    
with open("output-files/example-stationary_dist.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerows(data)

