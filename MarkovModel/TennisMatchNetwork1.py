# Import the required functions:
from loopybeliefprop import choose
from AdditionalFunctions import combine_recursion, nth_index
import numpy as np

def TennisMatchNetwork1(SetDists, SetScoreDists, NumGamesDists, FirstToSets):
    if (FirstToSets == 3):
        # Specify the names of the nodes in the Bayesian network
        nodes=['Set1','Set2','Set3','NumGames1','NumGames2','NumGames3','SetScore1','SetScore2','SetScore3','Match','NumSets',
        'TotalNumGames','AllSetScores']

        # Defining parent nodes:
        parents={}
        parents['Match']=['Set1', 'Set2', 'Set3']
        parents['NumSets']=['Set1', 'Set2', 'Set3']
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
        outcomes['TotalNumGames']=list(range(12,40))
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
                    TotalNumGamesDist2 = np.zeros(28, dtype = float)
                    TotalNumGamesDist3 = np.zeros(28, dtype = float)

                    # If only 2 sets played:
                    TotNumGames = Games1 + Games2
                    TotalNumGamesDist2[TotNumGames - 12] = 1.
                    dist['TotalNumGames'][2, Games1, Games2, Games3] = TotalNumGamesDist2

                    # If all 3 sets played:
                    TotNumGames = Games1 + Games2 + Games3
                    TotalNumGamesDist3[TotNumGames - 12] = 1.
                    dist['TotalNumGames'][3, Games1, Games2, Games3] = TotalNumGamesDist3

        # All Set Scores distributions:
        dist['AllSetScores']={}
        for Set1 in outcomes['SetScore1']:
                for Set2 in outcomes['SetScore2']:
                        for Set3 in outcomes['SetScore3']:
                            # Update distribution for both cases, 2 and 3 set matches:
                            # 2 Sets:
                            AllSetScoresDist = np.zeros(14, dtype = float)
                            AllSetScoresDist[Set1-1] = AllSetScoresDist[Set1-1] + 1./2.
                            AllSetScoresDist[Set2-1] = AllSetScoresDist[Set2-1] + 1./2.
                            dist['AllSetScores'][2, Set1, Set2, Set3] = AllSetScoresDist

                            # 3 Sets:
                            AllSetScoresDist = np.zeros(14, dtype = float)
                            AllSetScoresDist[Set1-1] = AllSetScoresDist[Set1-1] + 1./3.
                            AllSetScoresDist[Set2-1] = AllSetScoresDist[Set2-1] + 1./3.
                            AllSetScoresDist[Set3-1] = AllSetScoresDist[Set3-1] + 1./3.
                            dist['AllSetScores'][3, Set1, Set2, Set3] = AllSetScoresDist

    elif (FirstToSets == 5):
        # Specify the names of the nodes in the Bayesian network
        nodes=['Set1','Set2','Set3','Set4','Set5','NumGames1','NumGames2','NumGames3','NumGames4','NumGames5','SetScore1','SetScore2',
        'SetScore3','SetScore4','SetScore5','NumSets','Match','TotalNumGames','AllSetScores']

        # Defining parent nodes:
        parents={}
        parents['NumSets']=['Set1', 'Set2', 'Set3', 'Set4', 'Set5']
        parents['Match']=['Set1', 'Set2', 'Set3', 'Set4', 'Set5']
        parents['TotalNumGames']=['NumSets', 'NumGames1', 'NumGames2', 'NumGames3', 'NumGames4', 'NumGames5']
        parents['AllSetScores']=['NumSets', 'SetScore1', 'SetScore2', 'SetScore3', 'SetScore4', 'SetScore5']

        # Set up the possible outcomes for each node:
        outcomes={}
        outcomes['Set1']=[1, 2]
        outcomes['Set2']=[1, 2]
        outcomes['Set3']=[1, 2]
        outcomes['Set4']=[1, 2]
        outcomes['Set5']=[1, 2]
        outcomes['NumGames1']=[6,7,8,9,10,12,13]
        outcomes['NumGames2']=[6,7,8,9,10,12,13]
        outcomes['NumGames3']=[6,7,8,9,10,12,13]
        outcomes['NumGames4']=[6,7,8,9,10,12,13]
        outcomes['NumGames5']=[6,7,8,9,10,12,13]

        # Possilbe Set Scores: "6-0","6-1","6-2","6-3","6-4","7-5","7-6","0-6","1-6","2-6","3-6","4-6","5-7","6-7"
        outcomes['SetScore1']=[1,2,3,4,5,6,7,8,9,10,11,12,13,14]
        outcomes['SetScore2']=[1,2,3,4,5,6,7,8,9,10,11,12,13,14]
        outcomes['SetScore3']=[1,2,3,4,5,6,7,8,9,10,11,12,13,14]
        outcomes['SetScore4']=[1,2,3,4,5,6,7,8,9,10,11,12,13,14]
        outcomes['SetScore5']=[1,2,3,4,5,6,7,8,9,10,11,12,13,14]
        outcomes['NumSets']=[3,4,5]
        outcomes['Match']=[1,2]
        outcomes['TotalNumGames']=list(range(18,66))
        outcomes['AllSetScores']=[1,2,3,4,5,6,7,8,9,10,11,12,13,14]

        # Set up the initial distributions for our parent nodes:
        dist={}
        dist['Set1'] = SetDists[0]
        dist['Set2'] = SetDists[1]
        dist['Set3'] = SetDists[2]
        dist['Set4'] = SetDists[3]
        dist['Set5'] = SetDists[4]
        dist['NumGames1'] = NumGamesDists[0]
        dist['NumGames2'] = NumGamesDists[1]
        dist['NumGames3'] = NumGamesDists[2]
        dist['NumGames4'] = NumGamesDists[3]
        dist['NumGames5'] = NumGamesDists[4]
        dist['SetScore1'] = SetScoreDists[0]
        dist['SetScore2'] = SetScoreDists[1]
        dist['SetScore3'] = SetScoreDists[2]
        dist['SetScore4'] = SetScoreDists[3]
        dist['SetScore5'] = SetScoreDists[4]

        # Match node distributions: (Number of sets = 5) 
        # Number of sets distributions:
        dist['NumSets']={} 
        dist['Match'] = {}
        dist['NumSets'][1,1,1,1,1] = [1., 0., 0.]
        dist['Match'][1,1,1,1,1] = [1.,0.]     
        for i in range(1,6):
            Seqs = combine_recursion(5,i)

            for j in Seqs:
                # Reset Sequences and distributions:
                InitialSeq = [1,1,1,1,1]
                NumSetDist = [0., 0., 0.]

                # Place the '2's in each possible combination:
                for games in j:
                    InitialSeq[games-1] = 2
                Sequence = tuple(InitialSeq)

                # Assign the correct winner and number of sets:
                if (i < 3):
                    # Player 1 won:
                    dist['Match'][Sequence] = [1.,0.]
                    # Find occurence of 3rd set win for player 1:
                    Set = nth_index(Sequence, 1, 3)
                    NumSetDist[Set-2] = 1.
                    dist['NumSets'][Sequence] = NumSetDist
                else:
                    # Player 2 won:
                    dist['Match'][Sequence] = [0.,1.]
                    # Find occurence of 3rd set win for player 2:
                    Set = nth_index(Sequence, 2, 3)
                    NumSetDist[Set-2] = 1.
                    dist['NumSets'][Sequence] = NumSetDist

        # Total number of games distributions:
        dist['TotalNumGames']={}
        for Games1 in outcomes['NumGames1']:
            for Games2 in outcomes['NumGames2']:
                for Games3 in outcomes['NumGames3']:
                    for Games4 in outcomes['NumGames4']:
                        for Games5 in outcomes['NumGames5']:
                            TotalNumGamesDist3 = np.zeros(48, dtype = float)
                            TotalNumGamesDist4 = np.zeros(48, dtype = float)
                            TotalNumGamesDist5 = np.zeros(48, dtype = float)

                            # If only 3 sets played:
                            TotNumGames = Games1 + Games2 + Games3
                            TotalNumGamesDist3[outcomes['TotalNumGames'].index(TotNumGames)] = 1.
                            dist['TotalNumGames'][3, Games1, Games2, Games3, Games4, Games5] = TotalNumGamesDist3

                            # If 4 sets played:
                            TotNumGames = Games1 + Games2 + Games3 + Games4
                            TotalNumGamesDist4[outcomes['TotalNumGames'].index(TotNumGames)] = 1.
                            dist['TotalNumGames'][4, Games1, Games2, Games3, Games4, Games5] = TotalNumGamesDist4

                            # If all 5 sets played:
                            TotNumGames = Games1 + Games2 + Games3 + Games4 + Games5
                            TotalNumGamesDist5[outcomes['TotalNumGames'].index(TotNumGames)] = 1.
                            dist['TotalNumGames'][5, Games1, Games2, Games3, Games4, Games5] = TotalNumGamesDist5

        # All Set Scores distributions:
        dist['AllSetScores']={}
        for Set1 in outcomes['SetScore1']:
            for Set2 in outcomes['SetScore2']:
                for Set3 in outcomes['SetScore3']:
                    for Set4 in outcomes['SetScore4']:
                        for Set5 in outcomes['SetScore5']:                       
                            # Update distribution for all cases; 3, 4 and 5 set matches:
                            AllSetScoresDist3 = np.zeros(14, dtype = float)
                            AllSetScoresDist4 = np.zeros(14, dtype = float)
                            AllSetScoresDist5 = np.zeros(14, dtype = float)

                            # 3 Sets:
                            AllSetScoresDist3[Set1-1] = AllSetScoresDist3[Set1-1] + 1./3.
                            AllSetScoresDist3[Set2-1] = AllSetScoresDist3[Set2-1] + 1./3.
                            AllSetScoresDist3[Set3-1] = AllSetScoresDist3[Set3-1] + 1./3.
                            dist['AllSetScores'][3, Set1, Set2, Set3, Set4, Set5] = AllSetScoresDist3
                        
                            # 4 Sets:
                            AllSetScoresDist4[Set1-1] = AllSetScoresDist4[Set1-1] + 1./4.
                            AllSetScoresDist4[Set2-1] = AllSetScoresDist4[Set2-1] + 1./4.
                            AllSetScoresDist4[Set3-1] = AllSetScoresDist4[Set3-1] + 1./4.
                            AllSetScoresDist4[Set4-1] = AllSetScoresDist4[Set4-1] + 1./4.
                            dist['AllSetScores'][4, Set1, Set2, Set3, Set4, Set5] = AllSetScoresDist4

                            # 5 Sets:
                            AllSetScoresDist5[Set1-1] = AllSetScoresDist5[Set1-1] + 1./5.
                            AllSetScoresDist5[Set2-1] = AllSetScoresDist5[Set2-1] + 1./5.
                            AllSetScoresDist5[Set3-1] = AllSetScoresDist5[Set3-1] + 1./5.
                            AllSetScoresDist5[Set4-1] = AllSetScoresDist5[Set4-1] + 1./5.
                            AllSetScoresDist5[Set5-1] = AllSetScoresDist5[Set5-1] + 1./5.
                            dist['AllSetScores'][5, Set1, Set2, Set3, Set4, Set5] = AllSetScoresDist5

    # Set up initial information:
    info={}
    for i in nodes:
        info[i] = choose(outcomes[i], "NotSure")
    
    return(nodes, dist, parents, outcomes, info)