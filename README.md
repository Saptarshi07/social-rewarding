# social-rewarding
For the manuscript "Reputation effects facilitate the joint evolution of cooperation and social rewarding"

The repository contains the python scripts for generating the results from the model in the manuscript and contains data for the figures

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
 
 The data for the figures can be found as data-figures.zip
