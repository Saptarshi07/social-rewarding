## Reputation and Social Rewarding

### Overview Content: 

    For the manuscript "Reputation effects drive the joint evolution of cooperation and social rewarding". 

    The repository contains: 
       - the python scripts for generating the results from the model in the manuscript. 
       - demo output files from the script.
       - contains data for the main text figures.
       - The MIT License.

    The two folders contain the python scripts for generating results in the 
      - two-player interaction and 
      - multiplayer interaction (the public goods game)

    In the folder /two-player there are three python scripts: 

      - reward_simuls.py computes the time-series of evolution of strategy distributions in a well mixed population playing the two player donation game. The evolutionary dynamics is govered by the imitation learning. The parameter of the game and the evolutionary dynamics can be adjusted in the scripts. The output is written at two-player/output-files/

      - assortment-timeseries.py computes the time-series of evolution of strategy distributions in an assorted population playing the two-player donation game. The evolutionary dynamics is govered by the imitation learning. The parameter of the game and the evolutionary dynamics can be adjusted in the scripts. The output is written at two-player/output-files/

      - assortment-stationarydist.py computes the stationary distribution of the strategies at the low mutation regime of the evolutionary dynamics when population interactions assortatively. The parameter of the game and the evolutionary dynamics can be adjusted in the scripts. The output is written at two-player/output-files/

    In the folder /public-goods-game there are three python scripts:

      - pgg_reward_simul.py computes the time-series of evolution of strategy distributions in an well mixed population playing the public goods game. The evolutionary dynamics is govered by the imitation learning. The parameter of the game and the evolutionary dynamics can be adjusted in the scripts. The output is written at public-goods-game/output-files/

      - pgg_fixation_probabilities.py computes the fixation probability of a strategy in a resident strategy j when evolution occurs through imitative learning. The script evaluates the 16X16 fixation probability matrix. The output is written in public-goods-game/output-files/

      - fixation-prob-to-stationarydist.py computes the stationary distribution of the strategies at the low mutation regime of the evolutionary
     dynamics for the public goods game. The file requires an input of the fixation probabilities which it reads from /input-files. The output is written at public-goods-game/output-files/
 
### System requirements and dependencies: 

    - All the python scripts run for python version 3.6 and above. The user only needs to install the package - pandas.
    Installation of pandas can be done with the python package installer pip through command line - 
    
        pip install pandas
    
    - Details about the package installer pip can be found in this link: https://pypi.org/project/pip/ 

### Data for the figures:

    - The data for the figures can be found in the zipped folder data-figures.zip
 
### Example output of python scripts for demonstration: 

    - Example outputs of the python scripts can be found in the folders: ../output-files/
    
    For the two-player case the example outputs include: 
    
    a) evolutionary time series of strategies for two-player interactions in the population for assortment and no assortment.
        the other parameters of the example simulation for 10 time steps can be found in the output csv files.
    b) the stationary distribution of strategies in the population (with assortment) at low mutation for the parameter values:
        information transmissibility = 0.5 and degree of assortment = 0.5 and selection strength = 1.
    
    The example files are: 
    
    two-player/output-files/example-assortment-timeseries.csv
    two-player/output-files/example-time-series-two-player.csv
    two-player/output-files/example-assortment-stationarydist.csv
    
    For the public-goods-game case the example outputs include:
    
    a) evolutionary time series of strategies for multiplayer public goods interactions (group size = 4). 
        the other parameters of the example simulation for 10 time steps can be found in the output csv files.       
    b) fixation probability of a mutant strategy in a population of resident strategy.
        only the example of fixation probability of mutant (C,SR) invading a population of (C,NR) is shown.
    c) the stationary distribution of strategies in the population at low mutation for the parameter values:
        information transmissibility = 0.5 and reward value = 0.16 and selection strength = 1.
    
    
    The example files are: 
    
    public-goods-game/output-files/example-pgg-timeseries.csv
    public-goods-game/output-files/example-pgg-fixation.csv
    public-goods-game/output-files/example-stationary_dist.csv
    
    

    

 
 
