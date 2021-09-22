# Import the required functions:
from loopybeliefprop import choose
from AdditionalFunctions import combine_recursion, nth_index
import numpy as np

def TennisMatchNetworkMostEfficient(SetScoreDists, FirstToSets, ConditionalEvents = {}):
    if (FirstToSets == 3):
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
    elif (FirstToSets == 5):
        # Specify the names of the nodes in the Bayesian network
        nodes=['SetScore1','SetScore2','SetScore3','SetScore4','SetScore5','MatchScore']

        # Defining parent nodes:
        parents={}
        parents['MatchScore']=['SetScore1', 'SetScore2', 'SetScore3', 'SetScore4', 'SetScore5']

        # Set up the possible outcomes for each node:
        # Possilbe Set Scores: "6-0","6-1","6-2","6-3","6-4","7-5","7-6","0-6","1-6","2-6","3-6","4-6","5-7","6-7"
        outcomes={}
        outcomes['SetScore1']=[1,2,3,4,5,6,7,8,9,10,11,12,13,14]
        outcomes['SetScore2']=[1,2,3,4,5,6,7,8,9,10,11,12,13,14]
        outcomes['SetScore3']=[1,2,3,4,5,6,7,8,9,10,11,12,13,14]
        outcomes['SetScore4']=[1,2,3,4,5,6,7,8,9,10,11,12,13,14]
        outcomes['SetScore5']=[1,2,3,4,5,6,7,8,9,10,11,12,13,14]
        # Possible Match Scores: "3-0", "3-1", "3-2", "0-3", "1-3", "2-3"
        outcomes['MatchScore']=[1,2,3,4,5,6]

        # Set up the initial distributions for our parent nodes:
        dist={}
        dist['SetScore1'] = SetScoreDists[0]
        dist['SetScore2'] = SetScoreDists[1]
        dist['SetScore3'] = SetScoreDists[2]
        dist['SetScore4'] = SetScoreDists[3]
        dist['SetScore5'] = SetScoreDists[4]

        # Match, MatchScore, TotalNumGames and AllSetScores node distributions:
        dist['MatchScore']={}
        for Score1 in outcomes['SetScore1']:
            for Score2 in outcomes['SetScore2']:
                for Score3 in outcomes['SetScore3']:
                    for Score4 in outcomes['SetScore4']:
                        for Score5 in outcomes['SetScore5']:
                            # Find Match winner and Match score:
                            ScoreDist = np.zeros(6, dtype = float)
                            if (Score1 < 8):
                                Set1 = 1
                            else:
                                Set1 = 2
                            if (Score2 < 8):
                                Set2 = 1
                            else:
                                Set2 = 2
                            if (Score3 < 8):
                                Set3 = 1
                            else:
                                Set3 = 2
                            if (Score4 < 8):
                                Set4 = 1
                            else:
                                Set4 = 2
                            if (Score5 < 8):
                                Set5 = 1
                            else:
                                Set5 = 2
                            
                            # Create the sequence of sets:
                            Sequence = [Set1, Set2, Set3, Set4, Set5]

                            # See who won the match:
                            if (sum(Sequence) < 8):
                                # Find the occurence of the 3rd win for player 1:
                                Set = nth_index(Sequence, 1, 3)
                                ScoreDist[Set-2] = 1.
                                dist['MatchScore'][Score1, Score2, Score3, Score4, Score5] = ScoreDist
                            else:
                                # Find the occurence of the 3rd win for player 2:
                                Set = nth_index(Sequence, 2, 3)
                                ScoreDist[Set+1] = 1.
                                dist['MatchScore'][Score1, Score2, Score3, Score4, Score5] = ScoreDist
                        
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