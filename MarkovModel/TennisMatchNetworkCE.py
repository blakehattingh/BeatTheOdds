# Import the required functions:
from loopybeliefprop import choose
from AdditionalFunctions import combine_recursion, nth_index
import numpy as np

def TennisMatchNetworkCE(SetScoreDists, ConditionalEvents = {}):
    # Specify the names of the nodes in the Bayesian network
    nodes=['SetScore1','SetScore2','SetScore3','MatchScore','TotalNumGames','AllSetScores']

    # Defining parent nodes:
    parents={}
    parents['MatchScore']=['SetScore1', 'SetScore2', 'SetScore3']
    parents['TotalNumGames']=['MatchScore', 'SetScore1', 'SetScore2', 'SetScore3']
    parents['AllSetScores']=['MatchScore', 'SetScore1', 'SetScore2', 'SetScore3']

    # Set up the possible outcomes for each node:
    # Possilbe Set Scores: "6-0","6-1","6-2","6-3","6-4","7-5","7-6","0-6","1-6","2-6","3-6","4-6","5-7","6-7"
    outcomes={}
    outcomes['SetScore1']=[1,2,3,4,5,6,7,8,9,10,11,12,13,14]
    outcomes['SetScore2']=[1,2,3,4,5,6,7,8,9,10,11,12,13,14]
    outcomes['SetScore3']=[1,2,3,4,5,6,7,8,9,10,11,12,13,14]
    # Possible Match Scores: "2-0", "2-1", "0-2", "1-2"
    outcomes['MatchScore']=[1,2,3,4]
    outcomes['TotalNumGames']=list(range(12,40))
    outcomes['AllSetScores']=[1,2,3,4,5,6,7,8,9,10,11,12,13,14]

    # Set up the initial distributions for our parent nodes:
    dist={}
    dist['SetScore1'] = SetScoreDists[0]
    dist['SetScore2'] = SetScoreDists[1]
    dist['SetScore3'] = SetScoreDists[2]

    # MatchScore, TotalNumGames and AllSetScores node distributions:
    dist['MatchScore']={}
    dist['TotalNumGames']={}
    dist['AllSetScores']={}
    NumberOfGames = [6, 7, 8, 9, 10, 12, 13, 6, 7, 8, 9, 10, 12, 13]
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
                
                # Find the set scores:
                SetScoreDist2 = np.zeros(14, dtype = float)
                SetScoreDist3 = np.zeros(14, dtype = float)

                # 2 set match: (MatchScore outcome = 1 or 3)
                SetScoreDist2[Score1-1] = SetScoreDist2[Score1-1] + 1./2.
                SetScoreDist2[Score2-1] = SetScoreDist2[Score2-1] + 1./2.
                dist['AllSetScores'][1, Score1, Score2, Score3] = SetScoreDist2
                dist['AllSetScores'][3, Score1, Score2, Score3] = SetScoreDist2

                # 3 set match: (MatchScore outcome = 2 or 4)
                SetScoreDist3[Score1-1] = SetScoreDist3[Score1-1] + 1./3.
                SetScoreDist3[Score2-1] = SetScoreDist3[Score2-1] + 1./3.
                SetScoreDist3[Score3-1] = SetScoreDist3[Score3-1] + 1./3.
                dist['AllSetScores'][2, Score1, Score2, Score3] = SetScoreDist3
                dist['AllSetScores'][4, Score1, Score2, Score3] = SetScoreDist3
    
                # Find the number of games played:
                NumGamesDist2 = np.zeros(28, dtype = float)
                NumGamesDist3 = np.zeros(28, dtype = float)
                NumGames1 = NumberOfGames[Score1-1]
                NumGames2 = NumberOfGames[Score2-1]
                NumGames3 = NumberOfGames[Score3-1]

                # 2 set match: (MatchScore outcome = 1 or 3)
                TotalGames = NumGames1 + NumGames2
                NumGamesDist2[TotalGames-12] = 1.
                dist['TotalNumGames'][1, Score1, Score2, Score3] = NumGamesDist2
                dist['TotalNumGames'][3, Score1, Score2, Score3] = NumGamesDist2

                # 3 set match: (MatchScore outcome = 2 or 4)
                TotalGames = NumGames1 + NumGames2 + NumGames3
                NumGamesDist3[TotalGames-12] = 1.
                dist['TotalNumGames'][2, Score1, Score2, Score3] = NumGamesDist3
                dist['TotalNumGames'][4, Score1, Score2, Score3] = NumGamesDist3

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


                    


                    
