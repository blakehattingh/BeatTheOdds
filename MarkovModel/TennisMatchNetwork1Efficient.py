# Import the required functions:
from loopybeliefprop import choose
from OtherFunctions.AdditionalFunctions import combine_recursion, nth_index
import numpy as np

def TennisMatchNetwork1Efficient(SetScoreDists, FirstToSets, ConditionalEvents = {}):
    if (FirstToSets == 3):
        # Specify the names of the nodes in the Bayesian network
        nodes=['SetScore1','SetScore2','SetScore3','Match','MatchScore','TotalNumGames','AllSetScores']

        # Defining parent nodes:
        parents={}
        parents['Match']=['SetScore1', 'SetScore2', 'SetScore3']
        parents['MatchScore']=['SetScore1', 'SetScore2', 'SetScore3']
        parents['TotalNumGames']=['MatchScore', 'SetScore1', 'SetScore2', 'SetScore3']
        parents['AllSetScores']=['MatchScore', 'SetScore1', 'SetScore2', 'SetScore3']

        # Set up the possible outcomes for each node:
        # Possilbe Set Scores: "6-0","6-1","6-2","6-3","6-4","7-5","7-6","0-6","1-6","2-6","3-6","4-6","5-7","6-7"
        outcomes={}
        outcomes['SetScore1']=[1,2,3,4,5,6,7,8,9,10,11,12,13,14]
        outcomes['SetScore2']=[1,2,3,4,5,6,7,8,9,10,11,12,13,14]
        outcomes['SetScore3']=[1,2,3,4,5,6,7,8,9,10,11,12,13,14]
        outcomes['Match']=[1,2]
        # Possible Match Scores: "2-0", "2-1", "0-2", "1-2"
        outcomes['MatchScore']=[1,2,3,4]
        outcomes['TotalNumGames']=list(range(12,40))
        outcomes['AllSetScores']=[1,2,3,4,5,6,7,8,9,10,11,12,13,14]

        # Set up the initial distributions for our parent nodes:
        dist={}
        dist['SetScore1'] = SetScoreDists[0]
        dist['SetScore2'] = SetScoreDists[1]
        dist['SetScore3'] = SetScoreDists[2]

        # Match, MatchScore, TotalNumGames and AllSetScores node distributions:
        dist['Match']={}
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
                            dist['Match'][Score1, Score2, Score3] = [1., 0.]
                            dist['MatchScore'][Score1, Score2, Score3] = [1., 0., 0., 0.]
                        else:
                            # Player 2 won set 2 (1-1)
                            if (Score3 < 8):
                                # Player 1 won set 3 and hence won the match (2-1)
                                dist['Match'][Score1, Score2, Score3] = [1.0, 0.]
                                dist['MatchScore'][Score1, Score2, Score3] = [0., 1., 0., 0.]
                            else:
                                # Player 2 won set 3 and hence won the match (1-2)
                                dist['Match'][Score1, Score2, Score3] = [0., 1.]
                                dist['MatchScore'][Score1, Score2, Score3] = [0., 0., 0., 1.]
                    else:
                        # Player 2 won set 1 (0-1)
                        if (Score2 < 8):
                            # Player 1 won set 2 (1-1)
                            if (Score3 < 8):
                                # Player 1 won set 3 and hence won the match (2-1)
                                dist['Match'][Score1, Score2, Score3] = [1.0, 0.]
                                dist['MatchScore'][Score1, Score2, Score3] = [0., 1., 0., 0.]
                            else:
                                # Player 2 won set 3 and hence won the match (1-2)
                                dist['Match'][Score1, Score2, Score3] = [0., 1.0]
                                dist['MatchScore'][Score1, Score2, Score3] = [0., 0., 0., 1.]
                        else:
                            # Player 2 won set 2 and hence won the match (0-2)
                            dist['Match'][Score1, Score2, Score3] = [0., 1.0]
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
        
    elif (FirstToSets == 5):
        # Specify the names of the nodes in the Bayesian network
        nodes=['SetScore1','SetScore2','SetScore3','SetScore4','SetScore5','Match','MatchScore','TotalNumGames','AllSetScores']

        # Defining parent nodes:
        parents={}
        parents['Match']=['SetScore1', 'SetScore2', 'SetScore3', 'SetScore4', 'SetScore5']
        parents['MatchScore']=['SetScore1', 'SetScore2', 'SetScore3', 'SetScore4', 'SetScore5']
        parents['TotalNumGames']=['MatchScore', 'SetScore1', 'SetScore2', 'SetScore3', 'SetScore4', 'SetScore5']
        parents['AllSetScores']=['MatchScore', 'SetScore1', 'SetScore2', 'SetScore3', 'SetScore4', 'SetScore5']

        # Set up the possible outcomes for each node:
        # Possilbe Set Scores: "6-0","6-1","6-2","6-3","6-4","7-5","7-6","0-6","1-6","2-6","3-6","4-6","5-7","6-7"
        outcomes={}
        outcomes['SetScore1']=[1,2,3,4,5,6,7,8,9,10,11,12,13,14]
        outcomes['SetScore2']=[1,2,3,4,5,6,7,8,9,10,11,12,13,14]
        outcomes['SetScore3']=[1,2,3,4,5,6,7,8,9,10,11,12,13,14]
        outcomes['SetScore4']=[1,2,3,4,5,6,7,8,9,10,11,12,13,14]
        outcomes['SetScore5']=[1,2,3,4,5,6,7,8,9,10,11,12,13,14]
        outcomes['Match']=[1,2]
        # Possible Match Scores: "3-0", "3-1", "3-2", "0-3", "1-3", "2-3"
        outcomes['MatchScore']=[1,2,3,4,5,6]
        outcomes['TotalNumGames']=list(range(18,66))
        outcomes['AllSetScores']=[1,2,3,4,5,6,7,8,9,10,11,12,13,14]

        # Set up the initial distributions for our parent nodes:
        dist={}
        dist['SetScore1'] = SetScoreDists[0]
        dist['SetScore2'] = SetScoreDists[1]
        dist['SetScore3'] = SetScoreDists[2]
        dist['SetScore4'] = SetScoreDists[3]
        dist['SetScore5'] = SetScoreDists[4]

        # Match, MatchScore, TotalNumGames and AllSetScores node distributions:
        dist['Match']={}
        dist['MatchScore']={}
        dist['TotalNumGames']={}
        dist['AllSetScores']={}
        NumberOfGames = [6, 7, 8, 9, 10, 12, 13, 6, 7, 8, 9, 10, 12, 13]
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
                                # Player 1 won
                                dist['Match'][Score1, Score2, Score3, Score4, Score5] = [1., 0.]
                                # Find the occurence of the 3rd win for player 1:
                                Set = nth_index(Sequence, 1, 3)
                                ScoreDist[Set-2] = 1.
                                dist['MatchScore'][Score1, Score2, Score3, Score4, Score5] = ScoreDist
                            else:
                                # Player 2 won
                                dist['Match'][Score1, Score2, Score3, Score4, Score5] = [0., 1.]
                                # Find the occurence of the 3rd win for player 2:
                                Set = nth_index(Sequence, 2, 3)
                                ScoreDist[Set+1] = 1.
                                dist['MatchScore'][Score1, Score2, Score3, Score4, Score5] = ScoreDist
                            
                            # Find the set scores:
                            SetScoreDist3 = np.zeros(14, dtype = float)
                            SetScoreDist4 = np.zeros(14, dtype = float)
                            SetScoreDist5 = np.zeros(14, dtype = float)

                            # 3 set match: (MatchScore outcome = 1 or 4)
                            SetScoreDist3[Score1-1] = SetScoreDist3[Score1-1] + 1./3.
                            SetScoreDist3[Score2-1] = SetScoreDist3[Score2-1] + 1./3.
                            SetScoreDist3[Score3-1] = SetScoreDist3[Score3-1] + 1./3.
                            dist['AllSetScores'][1, Score1, Score2, Score3, Score4, Score5] = SetScoreDist3
                            dist['AllSetScores'][4, Score1, Score2, Score3, Score4, Score5] = SetScoreDist3

                            # 4 set match: (MatchScore outcome = 2 or 5)
                            SetScoreDist4[Score1-1] = SetScoreDist4[Score1-1] + 1./4.
                            SetScoreDist4[Score2-1] = SetScoreDist4[Score2-1] + 1./4.
                            SetScoreDist4[Score3-1] = SetScoreDist4[Score3-1] + 1./4.
                            SetScoreDist4[Score4-1] = SetScoreDist4[Score4-1] + 1./4.
                            dist['AllSetScores'][2, Score1, Score2, Score3, Score4, Score5] = SetScoreDist4
                            dist['AllSetScores'][5, Score1, Score2, Score3, Score4, Score5] = SetScoreDist4

                            # 5 set match: (MatchScore outcome = 3 or 6)
                            SetScoreDist5[Score1-1] = SetScoreDist5[Score1-1] + 1./5.
                            SetScoreDist5[Score2-1] = SetScoreDist5[Score2-1] + 1./5.
                            SetScoreDist5[Score3-1] = SetScoreDist5[Score3-1] + 1./5.
                            SetScoreDist5[Score4-1] = SetScoreDist5[Score4-1] + 1./5.
                            SetScoreDist5[Score5-1] = SetScoreDist5[Score5-1] + 1./5.
                            dist['AllSetScores'][3, Score1, Score2, Score3, Score4, Score5] = SetScoreDist5
                            dist['AllSetScores'][6, Score1, Score2, Score3, Score4, Score5] = SetScoreDist5

                            # Find the number of games played:
                            NumGamesDist3 = np.zeros(48, dtype = float)
                            NumGamesDist4 = np.zeros(48, dtype = float)
                            NumGamesDist5 = np.zeros(48, dtype = float)
                            NumGames1 = NumberOfGames[Score1-1]
                            NumGames2 = NumberOfGames[Score2-1]
                            NumGames3 = NumberOfGames[Score3-1]
                            NumGames4 = NumberOfGames[Score4-1]
                            NumGames5 = NumberOfGames[Score5-1]

                            # 3 set match: (MatchScore outcome = 1 or 4)
                            TotalGames = NumGames1 + NumGames2 + NumGames3
                            NumGamesDist3[TotalGames-18] = 1.
                            dist['TotalNumGames'][1, Score1, Score2, Score3, Score4, Score5] = NumGamesDist3
                            dist['TotalNumGames'][4, Score1, Score2, Score3, Score4, Score5] = NumGamesDist3

                            # 4 set match: (MatchScore outcome = 2 or 5)
                            TotalGames = NumGames1 + NumGames2 + NumGames3 + NumGames4
                            NumGamesDist4[TotalGames-18] = 1.
                            dist['TotalNumGames'][2, Score1, Score2, Score3, Score4, Score5] = NumGamesDist4
                            dist['TotalNumGames'][5, Score1, Score2, Score3, Score4, Score5] = NumGamesDist4

                            # 4 set match: (MatchScore outcome = 3 or 6)
                            TotalGames = NumGames1 + NumGames2 + NumGames3 + NumGames4 + NumGames5
                            NumGamesDist5[TotalGames-18] = 1.
                            dist['TotalNumGames'][3, Score1, Score2, Score3, Score4, Score5] = NumGamesDist5
                            dist['TotalNumGames'][6, Score1, Score2, Score3, Score4, Score5] = NumGamesDist5

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


                    


                    
