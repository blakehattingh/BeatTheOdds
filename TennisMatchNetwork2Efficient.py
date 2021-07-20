# Import the required functions:
from typing import Set
from loopybeliefprop import choose
from AdditionalFunctions import combine_recursion, nth_index
import numpy as np
from OMalleysEqns import TB
 
def TennisMatchNetwork2Efficient(P1S, P2S, FirstToSets):
    if (FirstToSets == 3):
        # Specify the names of the nodes in the Bayesian network
        nodes=['Set1Server','SetScore1','G1','G2','G3','G4','G5','G6','G7','G8','G9','G10','G11','G12','TB','Set2Server',
        'SetScore2','S2G1','S2G2','S2G3','S2G4','S2G5','S2G6','S2G7','S2G8','S2G9','S2G10','S2G11', 'S2G12','S2TB',
        'Set3Server','SetScore3','S3G1','S3G2','S3G3','S3G4','S3G5','S3G6','S3G7','S3G8','S3G9','S3G10','S3G11','S3G12',
        'S3TB','Match','TotalNumGames','AllSetScores','MatchScore']

        # Defining parent nodes:
        parents={}
        GameNodes1 = ['G1','G2','G3','G4','G5','G6','G7','G8','G9','G10','G11','G12','TB']
        GameNodes2 = ['S2G1','S2G2','S2G3','S2G4','S2G5','S2G6','S2G7','S2G8','S2G9','S2G10','S2G11','S2G12','S2TB']
        GameNodes3 = ['S3G1','S3G2','S3G3','S3G4','S3G5','S3G6','S3G7','S3G8','S3G9','S3G10','S3G11','S3G12','S3TB']
        for set in range(3):
            for node in range(13):
                if (set == 0):
                    parents[GameNodes1[node]] = ['Set1Server']
                elif (set == 1):
                    parents[GameNodes2[node]] = ['Set2Server']
                else:
                    parents[GameNodes3[node]] = ['Set3Server']

        parents['SetScore1']=['G1', 'G2', 'G3', 'G4','G5','G6', 'G7', 'G8', 'G9', 'G10', 'G11', 'G12', 'TB']
        parents['SetScore2']=['S2G1','S2G2','S2G3','S2G4','S2G5','S2G6','S2G7','S2G8','S2G9','S2G10','S2G11','S2G12','S2TB']
        parents['SetScore3']=['S3G1','S3G2','S3G3','S3G4','S3G5','S3G6','S3G7','S3G8','S3G9','S3G10','S3G11','S3G12','S3TB']
    
        # Set up links between sets:
        parents['Set2Server'] = ['Set1Server','SetScore1']
        parents['Set3Server'] = ['Set2Server','SetScore2']

        # Set up the links to the output nodes:
        parents['Match'] = ['SetScore1', 'SetScore2', 'SetScore3']
        parents['TotalNumGames'] = ['MatchScore', 'SetScore1', 'SetScore2', 'SetScore3']
        parents['AllSetScores'] = ['MatchScore', 'SetScore1', 'SetScore2', 'SetScore3']
        parents['MatchScore'] = ['SetScore1', 'SetScore2', 'SetScore3']

        # Set up the possible outcomes for each node:
        outcomes={}
        outcomes['Set1Server']=["P1Serves","P2Serves"]
        outcomes['G1']=[1,2]
        outcomes['G2']=[1,2]
        outcomes['G3']=[1,2]
        outcomes['G4']=[1,2]
        outcomes['G5']=[1,2]
        outcomes['G6']=[1,2]
        outcomes['G7']=[1,2]
        outcomes['G8']=[1,2]
        outcomes['G9']=[1,2]
        outcomes['G10']=[1,2]
        outcomes['G11']=[1,2]
        outcomes['G12']=[1,2]
        outcomes['TB']=[1,2]
        outcomes['SetScore1']=[1,2,3,4,5,6,7,8,9,10,11,12,13,14]
        outcomes['SetScore2']=[1,2,3,4,5,6,7,8,9,10,11,12,13,14]
        outcomes['SetScore3']=[1,2,3,4,5,6,7,8,9,10,11,12,13,14]
        outcomes['Set2Server']=["P1Serves","P2Serves"]
        outcomes['S2G1']=[1,2]
        outcomes['S2G2']=[1,2]
        outcomes['S2G3']=[1,2]
        outcomes['S2G4']=[1,2]
        outcomes['S2G5']=[1,2]
        outcomes['S2G6']=[1,2]
        outcomes['S2G7']=[1,2]
        outcomes['S2G8']=[1,2]
        outcomes['S2G9']=[1,2]
        outcomes['S2G10']=[1,2]
        outcomes['S2G11']=[1,2]
        outcomes['S2G12']=[1,2]
        outcomes['S2TB']=[1,2]
        outcomes['Set3Server']=["P1Serves","P2Serves"]
        outcomes['S3G1']=[1,2]
        outcomes['S3G2']=[1,2]
        outcomes['S3G3']=[1,2]
        outcomes['S3G4']=[1,2]
        outcomes['S3G5']=[1,2]
        outcomes['S3G6']=[1,2]
        outcomes['S3G7']=[1,2]
        outcomes['S3G8']=[1,2]
        outcomes['S3G9']=[1,2]
        outcomes['S3G10']=[1,2]
        outcomes['S3G11']=[1,2]
        outcomes['S3G12']=[1,2]
        outcomes['S3TB']=[1,2]

        # outcomes for output nodes:
        outcomes['Match'] = [1,2]
        outcomes['TotalNumGames'] = list(range(12, 40))
        outcomes['AllSetScores'] = [1,2,3,4,5,6,7,8,9,10,11,12,13,14]
        outcomes['MatchScore'] = [1,2,3,4]

        # Compute the probability of winning a game on serve from the on-serve point probabilities:
        P1G = pow(P1S, 4) * (15 - 4 * P1S - (10 * pow(P1S, 2) / (1 - 2 * P1S * (1 - P1S))))
        P2G = pow(P2S, 4) * (15 - 4 * P2S - (10 * pow(P2S, 2) / (1 - 2 * P2S * (1 - P2S))))
        print(P1G)
        print(P2G)

        # Compute the probability of winning a TB starting with service:
        P1TB = TB(P1S, 1 - P2S)
        P2TB = TB(P2S, 1 - P1S)

        # Set up distribution dictionaries for all nodes in network:
        dist={}
        for node in nodes:
            dist[node] = {}

        # Equal chance of each player serving the first game: (Can update if the toss has been done)
        dist['Set1Server'] = [0.5,0.5]

        # Create the conditional distributions for the starting server of each set, given the previous sets first server and the
        # number of games played in the last set:
        for i in outcomes["SetScore1"]:
            # Odd Number of games: (i = 2, 4, 7, 9, 11, 14)
            if (i in [2,4,7,9,11,14]):
                dist['Set2Server']["P1Serves",i] = [0., 1.]
                dist['Set3Server']["P1Serves",i] = [0., 1.]
                dist['Set2Server']["P2Serves",i] = [1., 0.]
                dist['Set3Server']["P2Serves",i] = [1., 0.]
            else:
                dist['Set2Server']["P1Serves",i] = [1., 0.]
                dist['Set3Server']["P1Serves",i] = [1., 0.]
                dist['Set2Server']["P2Serves",i] = [0., 1.]
                dist['Set3Server']["P2Serves",i] = [0., 1.]

        # Define the probabilities for each game, given the server:
        # Player 1 serving:
        dist['G1']["P1Serves"]=[P1G,1.-P1G]
        dist['G2']["P1Serves"]=[P1G,1.-P1G]
        dist['G3']["P1Serves"]=[P1G,1.-P1G]
        dist['G4']["P1Serves"]=[P1G,1.-P1G]
        dist['G5']["P1Serves"]=[P1G,1.-P1G]
        dist['G6']["P1Serves"]=[P1G,1.-P1G]
        dist['G7']["P1Serves"]=[P1G,1.-P1G]
        dist['G8']["P1Serves"]=[P1G,1.-P1G]
        dist['G9']["P1Serves"]=[P1G,1.-P1G]
        dist['G10']["P1Serves"]=[P1G,1.-P1G]
        dist['G11']["P1Serves"]=[P1G,1.-P1G]
        dist['G12']["P1Serves"]=[P1G,1.-P1G]
        dist['TB']["P1Serves"]=[P1TB,1.-P1TB]

        # Player 2 serving:
        dist['G1']["P2Serves"]=[1.-P2G,P2G]
        dist['G2']["P2Serves"]=[1.-P2G,P2G]
        dist['G3']["P2Serves"]=[1.-P2G,P2G]
        dist['G4']["P2Serves"]=[1.-P2G,P2G]
        dist['G5']["P2Serves"]=[1.-P2G,P2G]
        dist['G6']["P2Serves"]=[1.-P2G,P2G]
        dist['G7']["P2Serves"]=[1.-P2G,P2G]
        dist['G8']["P2Serves"]=[1.-P2G,P2G]
        dist['G9']["P2Serves"]=[1.-P2G,P2G]
        dist['G10']["P2Serves"]=[1.-P2G,P2G]
        dist['G11']["P2Serves"]=[1.-P2G,P2G]
        dist['G12']["P2Serves"]=[1.-P2G,P2G]
        dist['TB']["P2Serves"]=[1.-P2TB,P2TB]

        print(dist['G1']["P1Serves"])
        print(dist['G1']["P2Serves"])

        # Player 1 serving:
        dist['S2G1']["P1Serves"]=[P1G,1.-P1G]
        dist['S2G2']["P1Serves"]=[P1G,1.-P1G]
        dist['S2G3']["P1Serves"]=[P1G,1.-P1G]
        dist['S2G4']["P1Serves"]=[P1G,1.-P1G]
        dist['S2G5']["P1Serves"]=[P1G,1.-P1G]
        dist['S2G6']["P1Serves"]=[P1G,1.-P1G]
        dist['S2G7']["P1Serves"]=[P1G,1.-P1G]
        dist['S2G8']["P1Serves"]=[P1G,1.-P1G]
        dist['S2G9']["P1Serves"]=[P1G,1.-P1G]
        dist['S2G10']["P1Serves"]=[P1G,1.-P1G]
        dist['S2G11']["P1Serves"]=[P1G,1.-P1G]
        dist['S2G12']["P1Serves"]=[P1G,1.-P1G]
        dist['S2TB']["P1Serves"]=[P1TB,1.-P1TB]

        # Player 2 serving:
        dist['S2G1']["P2Serves"]=[1.-P2G,P2G]
        dist['S2G2']["P2Serves"]=[1.-P2G,P2G]
        dist['S2G3']["P2Serves"]=[1.-P2G,P2G]
        dist['S2G4']["P2Serves"]=[1.-P2G,P2G]
        dist['S2G5']["P2Serves"]=[1.-P2G,P2G]
        dist['S2G6']["P2Serves"]=[1.-P2G,P2G]
        dist['S2G7']["P2Serves"]=[1.-P2G,P2G]
        dist['S2G8']["P2Serves"]=[1.-P2G,P2G]
        dist['S2G9']["P2Serves"]=[1.-P2G,P2G]
        dist['S2G10']["P2Serves"]=[1.-P2G,P2G]
        dist['S2G11']["P2Serves"]=[1.-P2G,P2G]
        dist['S2G12']["P2Serves"]=[1.-P2G,P2G]
        dist['S2TB']["P2Serves"]=[1.-P2TB,P2TB]

        # Player 1 serving:
        dist['S3G1']["P1Serves"]=[P1G,1.-P1G]
        dist['S3G2']["P1Serves"]=[P1G,1.-P1G]
        dist['S3G3']["P1Serves"]=[P1G,1.-P1G]
        dist['S3G4']["P1Serves"]=[P1G,1.-P1G]
        dist['S3G5']["P1Serves"]=[P1G,1.-P1G]
        dist['S3G6']["P1Serves"]=[P1G,1.-P1G]
        dist['S3G7']["P1Serves"]=[P1G,1.-P1G]
        dist['S3G8']["P1Serves"]=[P1G,1.-P1G]
        dist['S3G9']["P1Serves"]=[P1G,1.-P1G]
        dist['S3G10']["P1Serves"]=[P1G,1.-P1G]
        dist['S3G11']["P1Serves"]=[P1G,1.-P1G]
        dist['S3G12']["P1Serves"]=[P1G,1.-P1G]
        dist['S3TB']["P1Serves"]=[P1TB,1.-P1TB]

        # Player 2 serving:
        dist['S3G1']["P2Serves"]=[1.-P2G,P2G]
        dist['S3G2']["P2Serves"]=[1.-P2G,P2G]
        dist['S3G3']["P2Serves"]=[1.-P2G,P2G]
        dist['S3G4']["P2Serves"]=[1.-P2G,P2G]
        dist['S3G5']["P2Serves"]=[1.-P2G,P2G]
        dist['S3G6']["P2Serves"]=[1.-P2G,P2G]
        dist['S3G7']["P2Serves"]=[1.-P2G,P2G]
        dist['S3G8']["P2Serves"]=[1.-P2G,P2G]
        dist['S3G9']["P2Serves"]=[1.-P2G,P2G]
        dist['S3G10']["P2Serves"]=[1.-P2G,P2G]
        dist['S3G11']["P2Serves"]=[1.-P2G,P2G]
        dist['S3G12']["P2Serves"]=[1.-P2G,P2G]
        dist['S3TB']["P2Serves"]=[1.-P2TB,P2TB]

        # Define the possible outcomes of the set, given a sequence of outcomes from all 12 games and the TB:   
        dist['SetScore1'][1,1,1,1,1,1,1,1,1,1,1,1,1] = [1., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.]
        dist['SetScore2'][1,1,1,1,1,1,1,1,1,1,1,1,1] = [1., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.]
        dist['SetScore3'][1,1,1,1,1,1,1,1,1,1,1,1,1] = [1., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.]

        # Possible Set Scores and Number of Games:
        SetScores = [[6,0],[6,1],[6,2],[6,3],[6,4],[7,5],[7,6],[0,6],[1,6],[2,6],[3,6],[4,6],[5,7],[6,7]]

        # Go through each possible sequence of games for each set and assign the correct outcome:
        for i in range(1,14):
            Seqs = combine_recursion(13,i)

            for j in Seqs:
                # Reset Sequences and distributions:
                InitialSeq = [1,1,1,1,1,1,1,1,1,1,1,1,1]
                SetScoresDist = [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.]

                # Place the '2's in each possible combination:
                for games in j:
                    InitialSeq[games-1] = 2
                Sequence = tuple(InitialSeq)
        
                # Compute the set score:
                Game = 0
                iGames = 0
                jGames = 0

                # Tally score:
                while (iGames < 6 and jGames < 6):
                    if (Sequence[Game] == 1):
                        iGames += 1
                    else:
                        jGames += 1
                    Game += 1
                
                # Check if the winner has a margin of at least 2:
                if ((iGames > jGames + 1) or (jGames > iGames + 1)):
                    SetScore = [iGames, jGames]
                    IndexSS = SetScores.index(SetScore)
                    SetScoresDist[IndexSS] = 1.
                    dist['SetScore1'][Sequence] = SetScoresDist
                    dist['SetScore2'][Sequence] = SetScoresDist
                    dist['SetScore3'][Sequence] = SetScoresDist
                else:
                    # Set went beyond 11 games: (current score = 6-5 or 5-6)
                    if (iGames > jGames):
                        if (Sequence[Game] == 1):
                            # 7-5:
                            SetScoresDist[5] = 1.
                            dist['SetScore1'][Sequence] = SetScoresDist
                            dist['SetScore2'][Sequence] = SetScoresDist
                            dist['SetScore3'][Sequence] = SetScoresDist
                        else:
                            # Check TB:
                            if (Sequence[12] == 1):
                                # 7-6
                                SetScoresDist[6] = 1.
                                dist['SetScore1'][Sequence] = SetScoresDist
                                dist['SetScore2'][Sequence] = SetScoresDist
                                dist['SetScore3'][Sequence] = SetScoresDist
                            else:
                                # 6-7
                                SetScoresDist[13] = 1.
                                dist['SetScore1'][Sequence] = SetScoresDist
                                dist['SetScore2'][Sequence] = SetScoresDist
                                dist['SetScore3'][Sequence] = SetScoresDist 
                    else:
                        if (Sequence[Game] == 2):
                            # 5-7:
                            SetScoresDist[12] = 1.
                            dist['SetScore1'][Sequence] = SetScoresDist
                            dist['SetScore2'][Sequence] = SetScoresDist
                            dist['SetScore3'][Sequence] = SetScoresDist
                        else:
                            # Check TB:
                            if (Sequence[12] == 1):
                                # 6-7
                                SetScoresDist[13] = 1.
                                dist['SetScore1'][Sequence] = SetScoresDist
                                dist['SetScore2'][Sequence] = SetScoresDist
                                dist['SetScore3'][Sequence] = SetScoresDist
                            else:
                                # 7-6
                                SetScoresDist[6] = 1.
                                dist['SetScore1'][Sequence] = SetScoresDist
                                dist['SetScore2'][Sequence] = SetScoresDist
                                dist['SetScore3'][Sequence] = SetScoresDist                             

                '''
                # Case 1: Set did not go beyond 10 games
                if (i <= 4 or i > 8):
                    while (iGames < 6 and jGames < 6):
                        if (InitialSeq[Game] == 1):
                            iGames = iGames + 1
                        else:
                            jGames = jGames + 1
                        Game = Game + 1
                    
                    # Compute score and number of games:
                    SetScore = [iGames, jGames]

                    # Find the index corresponding to this outcome:
                    IndexSS = SetScores.index(SetScore)

                    # Assign the correct outcome to the respective leaf node:
                    SetScoresDist[IndexSS] = 1.
                    dist['SetScore1'][Sequence] = SetScoresDist
                    dist['SetScore2'][Sequence] = SetScoresDist
                    dist['SetScore3'][Sequence] = SetScoresDist 

                else: # Case 2:
                    # Check if the game went beyond 10 games:
                    First10Games = InitialSeq[0:10]
                    if (First10Games.count(1) == 5):
                        # Set went to 10+ games (score = 5-5)
                        while (iGames < 7 and jGames < 7):
                            if (InitialSeq[Game] == 1):
                                iGames = iGames + 1
                            else:
                                jGames = jGames + 1
                            Game = Game + 1

                        # Compute score and number of games:
                        SetScore = [iGames, jGames]

                        # Find the index corresponding to this outcome:
                        IndexSS = SetScores.index(SetScore)

                        # Assign the correct outcome to the respective leaf node:
                        SetScoresDist[IndexSS] = 1.
                        dist['SetScore1'][Sequence] = SetScoresDist
                        dist['SetScore2'][Sequence] = SetScoresDist
                        dist['SetScore3'][Sequence] = SetScoresDist

                    else: 
                        # Set went to 10- games
                        while (iGames < 6 and jGames < 6):
                            if (InitialSeq[Game] == 1):
                                iGames = iGames + 1
                            else:
                                jGames = jGames + 1
                            Game = Game + 1

                        # Compute score and number of games:
                        SetScore = [iGames, jGames]

                        # Find the index corresponding to this outcome:
                        IndexSS = SetScores.index(SetScore)

                        # Assign the correct outcome to the respective leaf node:
                        SetScoresDist[IndexSS] = 1.
                        dist['SetScore1'][Sequence] = SetScoresDist
                        dist['SetScore2'][Sequence] = SetScoresDist
                        dist['SetScore3'][Sequence] = SetScoresDist
                        '''
        # Leaf node distributions:
        NumberOfGames = [6,7,8,9,10,12,13,6,7,8,9,10,12,13]
        for SS1 in outcomes['SetScore1']:
            for SS2 in outcomes['SetScore2']:
                for SS3 in outcomes['SetScore3']:
                    # Match outcome:
                    if ((SS1 < 8 and SS2 < 8) or (SS1 < 8 and SS3 < 8) or (SS2 < 8 and SS3 < 8)):
                        dist['Match'][SS1, SS2, SS3] = [1., 0.]
                    else:
                        dist['Match'][SS1, SS2, SS3] = [0., 1.]
                        
                    # Match Score:
                    if (SS1 < 8 and SS2 < 8):
                        dist['MatchScore'][SS1, SS2, SS3] = [1., 0., 0., 0.]
                    elif ((SS1 < 8 and SS2 > 7 and SS3 < 8) or (SS1 > 7 and SS2 < 8 and SS3 < 8)):
                        dist['MatchScore'][SS1, SS2, SS3] = [0., 1., 0., 0.]
                    elif (SS1 > 7 and SS2 > 7):
                        dist['MatchScore'][SS1, SS2, SS3] = [0., 0., 1., 0.]
                    else:
                        dist['MatchScore'][SS1, SS2, SS3] = [0., 0., 0., 1.]

                    # Total Number of Games:
                    Games1 = NumberOfGames[SS1-1]
                    Games2 = NumberOfGames[SS2-1]
                    Games3 = NumberOfGames[SS3-1]
                    TotalGamesDist2 = np.zeros(28, dtype = float)
                    TotalGamesDist3 = np.zeros(28, dtype = float)
                    # 2 Sets:
                    TotalGames = Games1 + Games2
                    TotalGamesDist2[TotalGames-12] = 1.
                    dist['TotalNumGames'][1, SS1, SS2, SS3] = TotalGamesDist2
                    dist['TotalNumGames'][3, SS1, SS2, SS3] = TotalGamesDist2
                    # 3 Sets:
                    TotalGames = Games1 + Games2 + Games3
                    TotalGamesDist3[TotalGames-12] = 1.
                    dist['TotalNumGames'][2, SS1, SS2, SS3] = TotalGamesDist3
                    dist['TotalNumGames'][4, SS1, SS2, SS3] = TotalGamesDist3

                    # All Set Score distributions:
                    # 2 Sets:
                    SetScoresDist = np.zeros(14, dtype = float)
                    SetScoresDist[SS1-1] = SetScoresDist[SS1-1] + 1./2.
                    SetScoresDist[SS2-1] = SetScoresDist[SS2-1] + 1./2.
                    dist['AllSetScores'][1, SS1, SS2, SS3] = SetScoresDist
                    dist['AllSetScores'][3, SS1, SS2, SS3] = SetScoresDist

                    # 3 Sets:
                    SetScoresDist = np.zeros(14, dtype = float)
                    SetScoresDist[SS1-1] = SetScoresDist[SS1-1] + 1./3.
                    SetScoresDist[SS2-1] = SetScoresDist[SS2-1] + 1./3.
                    SetScoresDist[SS3-1] = SetScoresDist[SS3-1] + 1./3.
                    dist['AllSetScores'][2, SS1, SS2, SS3] = SetScoresDist                           
                    dist['AllSetScores'][4, SS1, SS2, SS3] = SetScoresDist 
              
    # Set up initial information:
    info={}
    for i in nodes:
        info[i] = choose(outcomes[i], "NotSure")
    
    return(nodes, dist, parents, outcomes, info)