from typing import Sequence
import numpy as np
import math
import statistics as stats
# import matplotlib.pyplot as plt
from loopybeliefprop import beliefpropagation, noinfo, choose
from MarkovSimulations import MarkovChainTieBreaker
from itertools import islice

# Combinatoric Generator:
def combine_recursion(n, k):
    result = []
    combine_dfs(n, k, 1, [], result)
    return result

def combine_dfs(n, k, start, path, result):
    if k == len(path):
        result.append(path)
        return
    for i in range(start, n + 1):
        combine_dfs(n, k, i + 1, path + [i], result)   

def TennisMatch1(SetDists, SetScoreDists, NumGamesDists):
    # Specify the names of the nodes in the Bayesian network
    nodes=['Set1','Set2','Set3','NumGames1','NumGames2','NumGames3','SetScore1','SetScore2','SetScore3','NumSets','Match',
    'TotalNumGames','AllSetScores']

    # Defining parent nodes:
    parents={}
    parents['NumSets']=['Set1', 'Set2', 'Set3']
    parents['Match']=['Set1', 'Set2', 'Set3']
    parents['TotalNumGames']=['NumSets', 'NumGames1', 'NumGames2', 'NumGames3']
    parents['AllSetScores']=['NumSets', 'SetScore1', 'SetScore2', 'SetScore3']

    # Set up the possible outcomes for each node:
    outcomes={}
    outcomes['Set1']=[1, 2]
    outcomes['Set2']=[1, 2]
    outcomes['Set3']=[1, 2]
    outcomes['NumGames1']=[6,7,8,9,10,12,13]
    outcomes['NumGames2']=[6,7,8,9,10,12,13]
    outcomes['NumGames3']=[6,7,8,9,10,12,13]

    # Possilbe Set Scores: "6-0","6-1","6-2","6-3","6-4","7-5","7-6","0-6","1-6","2-6","3-6","4-6","5-7","6-7"
    outcomes['SetScore1']=[1,2,3,4,5,6,7,8,9,10,11,12,13,14]
    outcomes['SetScore2']=[1,2,3,4,5,6,7,8,9,10,11,12,13,14]
    outcomes['SetScore3']=[1,2,3,4,5,6,7,8,9,10,11,12,13,14]
    outcomes['NumSets']=[2,3]
    outcomes['Match']=[1,2]
    outcomes['TotalNumGames']=list(range(12,66))
    outcomes['AllSetScores']=[1,2,3,4,5,6,7,8,9,10,11,12,13,14]

    # Set up the initial distributions for our parent nodes:
    dist={}
    dist['Set1'] = SetDists[0]
    dist['Set2'] = SetDists[1]
    dist['Set3'] = SetDists[2]
    dist['NumGames1'] = NumGamesDists[0]
    dist['NumGames2'] = NumGamesDists[1]
    dist['NumGames3'] = NumGamesDists[2]
    dist['SetScore1'] = SetScoreDists[0]
    dist['SetScore2'] = SetScoreDists[1]
    dist['SetScore3'] = SetScoreDists[2]
    

    # Match node distributions:
    dist['Match']={}
    dist['Match'][1,1,1] = [1.,0.]
    dist['Match'][1,1,2] = [1.,0.]
    dist['Match'][1,2,1] = [1.,0.]
    dist['Match'][1,2,2] = [0.,1.]
    dist['Match'][2,1,1] = [1.,0.]
    dist['Match'][2,1,2] = [0.,1.]
    dist['Match'][2,2,1] = [0.,1.]
    dist['Match'][2,2,2] = [0.,1.]

    # Number of sets distributions:
    dist['NumSets']={}
    dist['NumSets'][1,1,1] = [1.,0.]
    dist['NumSets'][1,1,2] = [1.,0.]
    dist['NumSets'][1,2,1] = [0.,1.]
    dist['NumSets'][1,2,2] = [0.,1.]
    dist['NumSets'][2,1,1] = [0.,1.]
    dist['NumSets'][2,1,2] = [0.,1.]
    dist['NumSets'][2,2,1] = [1.,0.]
    dist['NumSets'][2,2,2] = [1.,0.]

    # Total number of games distributions:
    dist['TotalNumGames']={}
    for Games1 in outcomes['NumGames1']:
        for Games2 in outcomes['NumGames2']:
            for Games3 in outcomes['NumGames3']:
                TotalNumGamesDist2 = [0.] * len(outcomes['TotalNumGames'])
                TotalNumGamesDist3 = [0.] * len(outcomes['TotalNumGames'])

                # If only 2 sets played:
                TotNumGames = Games1 + Games2
                TotalNumGamesDist2[outcomes['TotalNumGames'].index(TotNumGames)] = 1.
                dist['TotalNumGames'][2, Games1, Games2, Games3] = TotalNumGamesDist2

                # If all 3 sets played:
                TotNumGames = Games1 + Games2 + Games3
                TotalNumGamesDist3[outcomes['TotalNumGames'].index(TotNumGames)] = 1.
                dist['TotalNumGames'][3, Games1, Games2, Games3] = TotalNumGamesDist3

    # All Set Scores distributions:
    dist['AllSetScores']={}
    for Set1 in outcomes['SetScore1']:
            for Set2 in outcomes['SetScore2']:
                    for Set3 in outcomes['SetScore3']:
                        AllSetScoresDist = [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.]
                        # Find the index of each set score:
                        indices=[outcomes['SetScore1'].index(Set1),outcomes['SetScore2'].index(Set2),outcomes['SetScore3'].index(Set3)]

                        # Check if the match went to 2 or 3 sets:
                        if ((indices[0] < 7 and indices[1] < 7) or (indices[0] > 6 and indices[1] > 6)):
                            # Player 1 or 2 won in 2 sets:
                            for ind in indices[0:1]:
                                AllSetScoresDist[ind] = AllSetScoresDist[ind] + 1./2.                         
                            dist['AllSetScores'][2, Set1, Set2, Set3] = AllSetScoresDist
                            dist['AllSetScores'][3, Set1, Set2, Set3] = AllSetScoresDist

                        else:
                            for ind in indices:
                                AllSetScoresDist[ind] = AllSetScoresDist[ind] + 1./3.                         
                            dist['AllSetScores'][3, Set1, Set2, Set3] = AllSetScoresDist
                            dist['AllSetScores'][2, Set1, Set2, Set3] = AllSetScoresDist

    # Set up initial information:
    info={}
    for i in nodes:
        info[i] = choose(outcomes[i], "NotSure")
    
    return(nodes, dist, parents, outcomes, info)