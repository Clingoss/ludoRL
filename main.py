import sys
import src.ludo as game
from src.RNDbot import RNDbot
from src.RL import RL
import pandas as pd
import numpy as np

from tqdm import tqdm

def most_frequent(List):
    counter = 0
    num = List[0]
     
    for i in List:
        curr_frequency = List.count(i)
        if(curr_frequency> counter):
            counter = curr_frequency
            num = i
 
    return num

if __name__ == "__main__":
    RED = RL(gamma=0.0,alpha=0.0,epsilon=0.0,eps=0)
    RED.Q = np.load("QQ.npy")
    BLUE = RL(gamma=0.0,alpha=0.0,epsilon=0.0)
    BLUE.Qsq = np.load("QsQ.npy")
    GREEN = RL(gamma=0.0,alpha=0.0,epsilon=0.0,eps=0)
    GREEN.Q = np.load("QSARSA.npy")
    YELLOW = RNDbot()
    
    tornament = { "game0": [0,0,0,0]}
    for i in tqdm(range(100), unit="tornaments"):
        games = []
        for _ in range(30):
            games.append(game.Ludo(RED,BLUE,YELLOW,GREEN).winner)
        name = "game" + str(i)
        tornament.update({name:games})

    df = pd.DataFrame(tornament) 
    df.to_csv('exp/smallrun.csv')

    #np.save('QSARSA.npy',GREEN.Q)
    #print(GREEN.Q)
    #np.save('QsQ.npy',BLUE.Qsq)
    #print(BLUE.Qsq)
    #np.save('QQ.npy',RED.Q)
    #print(RED.Q)


    # tornament = { "game0": [0,0,0,0]}
    # for i in tqdm(range(10), unit="tornaments"):
    #     games = []
    #     BLUE = RL(alpha=((i+1)/10))
    #     for j in range(30):
    #         games.append(game.Ludo(RED,BLUE,YELLOW,GREEN).winner)
    #     name = "game" + str(i)
    #     tornament.update({name:games})

    # df = pd.DataFrame(tornament) 
    # df.to_csv('exp/learningRateTestQ.csv')


    # tornament = { "game0": [0,0,0,0]}
    # for i in tqdm(range(10), unit="tornaments"):
    #     games = []
    #     BLUE = RL(epsilon=(i/10))
    #     for _ in range(30):
    #         games.append(game.Ludo(RED,BLUE,YELLOW,GREEN).winner)
    #     name = "game" + str(i)
    #     tornament.update({name:games})
    
    # df = pd.DataFrame(tornament) 
    # df.to_csv('exp/explorationFactorTestQ.csv')