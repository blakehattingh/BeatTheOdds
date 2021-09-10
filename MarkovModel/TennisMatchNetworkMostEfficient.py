# Import the required functions:
from loopybeliefprop import choose
from AdditionalFunctions import combine_recursion, nth_index
import numpy as np

def TennisMatchNetworkMostEfficient(SetScoreDists, ConditionalEvents = {}):
    # Specify the names of the nodes in the Bayesian network
    nodes=['SetScore1','SetScore2','SetScore3','MatchScore']

    # Defining parent nodes:
    parents={}
    parents['MatchScore']=['SetScore1', 'SetScore2', 'SetScore3']

    # Set up the possible outcomes for each node:
    # Possilbe Set Scores: "6-0","6-1","6-2","6-3","6-4","7-5","7-6","0-6","1-6","2-6","3-6","4-6","5-7","6-7"
    outcomes={}
    outcomes['SetScore1']=[1,2,3,4,5,6,7,8,9,10,11,12,13,14]
    outcomes['SetScore2']=[1,2,3,4,5,6,7,8,9,10,11,12,13,14]
    outcomes['SetScore3']=[1,2,3,4,5,6,7,8,9,10,11,12,13,14]
    # Possible Match Scores: "2-0", "2-1", "0-2", "1-2"
    outcomes['MatchScore']=[1,2,3,4]

    # Set up the initial distributions for our parent nodes:
    dist={}
    dist['SetScore1'] = SetScoreDists[0]
    dist['SetScore2'] = SetScoreDists[1]
    dist['SetScore3'] = SetScoreDists[2]

    # MatchScore node distributions:
    dist['MatchScore']={}
    for Score1 in outcomes['SetScore1']:
        for Score2 in outcomes['SetScore2']:
            for Score3 in outcomes['SetScore3']:
                # Find Match winner and Match score:
                if (Score1 < 8):
                    # Player 1 won set 1 (1-0)
                    if (Score2 < 8):
                        # Player 1 won set 2 and hence won the match (2-0)
                        dist['MatchScore'][Score1, Score2, Score3] = [1., 0., 0., 0.]
                    else:
                        # Player 2 won set 2 (1-1)
                        if (Score3 < 8):
                            # Player 1 won set 3 and hence won the match (2-1)
                            dist['MatchScore'][Score1, Score2, Score3] = [0., 1., 0., 0.]
                        else:
                            # Player 2 won set 3 and hence won the match (1-2)
                            dist['MatchScore'][Score1, Score2, Score3] = [0., 0., 0., 1.]
                else:
                    # Player 2 won set 1 (0-1)
                    if (Score2 < 8):
                        # Player 1 won set 2 (1-1)
                        if (Score3 < 8):
                            # Player 1 won set 3 and hence won the match (2-1)
                            dist['MatchScore'][Score1, Score2, Score3] = [0., 1., 0., 0.]
                        else:
                            # Player 2 won set 3 and hence won the match (1-2)
                            dist['MatchScore'][Score1, Score2, Score3] = [0., 0., 0., 1.]
                    else:
                        # Player 2 won set 2 and hence won the match (0-2)
                        dist['MatchScore'][Score1, Score2, Score3] = [0., 0., 1., 0.]

    # Set up initial information:
    info={}
    for i in nodes:
        if (i in ConditionalEvents.keys()):
            # Fix certian nodes identfied by user:
            info[i] = choose(outcomes[i], ConditionalEvents[i])
        else:
            # Otherwise leave them unfixed:
            info[i] = choose(outcomes[i], [])
    return(nodes, dist, parents, outcomes, info)