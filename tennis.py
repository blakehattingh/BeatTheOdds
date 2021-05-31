from typing import Sequence
import numpy as np
import math
import statistics as stats
# import matplotlib.pyplot as plt
from loopybeliefprop import beliefpropagation, noinfo, choose
from MarkovSimulations import MarkovChainTieBreaker
from itertools import islice
from tennisMatch2 import TennisMatch1, TennisMatch2
# import seaborn as sns

# Find the nth position of a value in an array:
def nth_index(iterable, value, n):
    matches = (idx for idx, val in enumerate(iterable) if val == value)
    return next(islice(matches, n-1, n), None)

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

def TieBreakerProbability(P1S, P2S, Iter, FirstTo):
    # Compute the probability of winning a TB using the MarkovTB Simulation:

    Count1 = 0
    Count2 = 0
    for i in range(Iter):
        # Player 1 Serving first:
        Winner1 = MarkovChainTieBreaker(P1S, P2S, 'i', FirstTo)
        # Player 2 Serving first:
        Winner2 = MarkovChainTieBreaker(P1S, P2S, 'j', FirstTo)
        if (Winner1 == 'i'):
            Count1 = Count1 + 1
        if (Winner2 == 'j'):
            Count2 = Count2 + 1
    
    # Compute their probability of winning when they start the TB serving:
    return [Count1/Iter, Count2/Iter] # Prob Player 1 winning if he serves first, Prob Player 2 winning if he serves first

def TennisSet(P1S, P2S, P1TB, P2TB, InitServerDist = [0.5, 0.5]):
    # Specify the names of the nodes in the Bayesian network
    nodes=['ServerOdd','ServerEven','Set','NumGames','SetScore','G1','G2','G3','G4','G5','G6','G7','G8','G9','G10','G11','G12','TB']

    # Defining parent nodes:
    parents={}
    parents['ServerEven']=['ServerOdd']
    parents['G1']=['ServerOdd']
    parents['G2']=['ServerEven']
    parents['G3']=['ServerOdd']
    parents['G4']=['ServerEven']
    parents['G5']=['ServerOdd']
    parents['G6']=['ServerEven']
    parents['G7']=['ServerOdd']
    parents['G8']=['ServerEven']
    parents['G9']=['ServerOdd']
    parents['G10']=['ServerEven']
    parents['G11']=['ServerOdd']
    parents['G12']=['ServerEven']
    parents['TB']=['ServerOdd']
    parents['Set']=['G1', 'G2', 'G3', 'G4','G5','G6', 'G7', 'G8', 'G9', 'G10', 'G11', 'G12', 'TB']
    parents['NumGames']=['G1', 'G2', 'G3', 'G4','G5','G6', 'G7', 'G8', 'G9', 'G10', 'G11', 'G12', 'TB']
    parents['SetScore']=['G1', 'G2', 'G3', 'G4','G5','G6', 'G7', 'G8', 'G9', 'G10', 'G11', 'G12', 'TB']

    # Set up the possible outcomes for each node:
    outcomes={}
    outcomes['ServerOdd']=["P1Serves","P2Serves"]
    outcomes['ServerEven']=["P1Serves","P2Serves"]
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
    outcomes['Set']=[1,2]
    outcomes['NumGames']=[6,7,8,9,10,12,13]
    outcomes['SetScore']=["6-0","6-1","6-2","6-3","6-4","7-5","7-6","0-6","1-6","2-6","3-6","4-6","5-7","6-7"]

    # Compute the probability of winning a game on serve from the on-serve point probabilities:
    P1G = pow(P1S, 2) / (pow(P1S, 2) + pow((1-P1S), 2))
    P2G = pow(P2S, 2) / (pow(P2S, 2) + pow((1-P2S), 2))

    # Equal chance of each player serving the first game: (Can update if the toss has been done)
    dist={}
    dist['ServerOdd'] = InitServerDist
    dist['ServerEven'] = {}
    dist['ServerEven']["P1Serves"] = [0.,1.]
    dist['ServerEven']["P2Serves"] = [1.,0.]

    # Set up dictionaries for each game:
    dist['G1']={}
    dist['G2']={}
    dist['G3']={}
    dist['G4']={}
    dist['G5']={}
    dist['G6']={}
    dist['G7']={}
    dist['G8']={}
    dist['G9']={}
    dist['G10']={}
    dist['G11']={}
    dist['G12']={}
    dist['TB']={}
    
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

    # Define the possible outcomes of the set, given a sequence of outcomes from all 12 games and the TB:
    dist['Set']={}
    dist['NumGames']={}
    dist['SetScore']={}
    dist['Set'][1,1,1,1,1,1,1,1,1,1,1,1,1] = [1.,0.]
    dist['NumGames'][1,1,1,1,1,1,1,1,1,1,1,1,1] = [1., 0., 0., 0., 0., 0., 0.]
    dist['SetScore'][1,1,1,1,1,1,1,1,1,1,1,1,1] = [1., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.]

    # Possible Set Scores and Number of Games:
    SetScores = [[6,0],[6,1],[6,2],[6,3],[6,4],[7,5],[7,6],[0,6],[1,6],[2,6],[3,6],[4,6],[5,7],[6,7]]
    NumberOfGames = [6,7,8,9,10,12,13]

    for i in range(1,14):
        Seqs = combine_recursion(13,i)

        for j in Seqs:
            # Reset Sequences and distributions:
            InitialSeq = [1,1,1,1,1,1,1,1,1,1,1,1,1]
            SetScoresDist = [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.]
            NumGamesDist = [0., 0., 0., 0., 0., 0., 0.]

            # Place the '2's in each possible combination:
            for games in j:
                InitialSeq[games-1] = 2

            # Assign the correct winner:
            Sequence = tuple(InitialSeq)

            # Set Outcome:

            # Case 1: (i (Player 2 wins) < 6)
            if (i < 6):
                # Player 1 wins:
                dist['Set'][Sequence] = [1.,0.]
            
            # Case 2: (i > 7):
            elif (i > 7):
                # Player 2 wins:
                dist['Set'][Sequence] = [0.,1.]

            # Case 3: (i = 6 or 7)
            else:
                # Check the first 12 games to see if a tie-breaker was required:
                First12 = Sequence[:-1]
                P2Wins = First12.count(2)
                if (P2Wins > 5):
                    # Player 2 wins:
                    dist['Set'][Sequence] = [0.,1.]
                else:
                    # Player 1 wins:
                    dist['Set'][Sequence] = [1.,0.]
                
                # Check if a tie-breaker was needed:
                if (P2Wins == 6):
                    # Check who won the TB:
                    if (Sequence[-1] == 2):
                        # Player 2 won the TB and therefore the set too:
                        dist['Set'][Sequence] = [0.,1.]
                    else:
                        # Player 1 wins:
                        dist['Set'][Sequence] = [1.,0.]  

            # Compute the set score and number of games in the set:
            Game = 0
            iGames = 0
            jGames = 0
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
                NumGames = sum(SetScore)

                # Find the index corresponding to this outcome:
                IndexSS = SetScores.index(SetScore)
                IndexNG = NumberOfGames.index(NumGames)

                # Assign the correct outcome to the respective leaf node:
                SetScoresDist[IndexSS] = 1.
                NumGamesDist[IndexNG] = 1.
                dist['SetScore'][Sequence] = SetScoresDist
                dist['NumGames'][Sequence] = NumGamesDist

            else: # Case 2:
                # Check if the game went beyond 10 games:
                First10Games = InitialSeq[0:10]
                if (First10Games.count(1) == 5):
                    # Set went to 10+ games
                    while (iGames < 7 and jGames < 7):
                        if (InitialSeq[Game] == 1):
                            iGames = iGames + 1
                        else:
                            jGames = jGames + 1
                        Game = Game + 1

                    # Compute score and number of games:
                    SetScore = [iGames, jGames]
                    NumGames = sum(SetScore)

                    # Find the index corresponding to this outcome:
                    IndexSS = SetScores.index(SetScore)
                    IndexNG = NumberOfGames.index(NumGames)

                    # Assign the correct outcome to the respective leaf node:
                    SetScoresDist[IndexSS] = 1.
                    NumGamesDist[IndexNG] = 1.
                    dist['SetScore'][Sequence] = SetScoresDist
                    dist['NumGames'][Sequence] = NumGamesDist          

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
                    NumGames = sum(SetScore)

                    # Find the index corresponding to this outcome:
                    IndexSS = SetScores.index(SetScore)
                    IndexNG = NumberOfGames.index(NumGames)

                    # Assign the correct outcome to the respective leaf node:
                    SetScoresDist[IndexSS] = 1.
                    NumGamesDist[IndexNG] = 1.
                    dist['SetScore'][Sequence] = SetScoresDist
                    dist['NumGames'][Sequence] = NumGamesDist 

    # Set up initial information:
    info={}
    for i in nodes:
        info[i] = choose(outcomes[i], "NotSure")
    
    return(nodes, dist, parents, outcomes, info)

    ######################## USER INPUT STARTS HERE ###########################

def main():
    # Model Parameters:
    P1S = 0.7
    P2S = 0.65
    FirstToSets = 3
    FirstToTBPoints = 7

    # Call TennisMatch:
    TennisMatch(P1S, P2S, FirstToSets, FirstToTBPoints)

def TennisMatch(P1S, P2S, FirstToSets, FirstToTBPoints):

    # Model Parameters:
    # - Max Number of Iterations allowed to reach Steady State.
    # - Tolerance level to check for convergence.
    Iterations = 100
    Tol = 0.001
    
    # Compute the Tie-Breaker probabilities using a simulation approach:
    [P1TB, P2TB] = TieBreakerProbability(P1S, P2S, 100000, FirstToTBPoints)
    
    # Set up the Bayesian Network and run the blief propagation algorithm for each set played:
    # Set 1:
    [nodes, dist, parents, outcomes, info] = TennisSet(P1S, P2S, P1TB, P2TB)
    [SetDist1, NumGamesDist1, SetScoreDist1] = beliefpropagation(nodes,dist,parents,outcomes,info,Iterations,Tol,['Set','NumGames','SetScore'])
    # Compute the initial probability distribution for the first server of the next set from the number of games played in the previous set:
    NumGamesDist1 = np.array(NumGamesDist1)
    InitServerDist = [sum(NumGamesDist1[[0,2,4,5]]), sum(NumGamesDist1[[1,3,6]])]

    # Set 2:
    [nodes, dist, parents, outcomes, info] = TennisSet(P1S, P2S, P1TB, P2TB, InitServerDist)
    [SetDist2, NumGamesDist2, SetScoreDist2] = beliefpropagation(nodes,dist,parents,outcomes,info,Iterations,Tol,['Set','NumGames','SetScore'])
    # Compute the initial probability distribution for the first server of the next set from the number of games played in the previous set:
    NumGamesDist2 = np.array(NumGamesDist2)
    Prob1Serve = InitServerDist[0]*sum(NumGamesDist2[[0,2,4,5]]) + InitServerDist[1]*sum(NumGamesDist2[[1,3,6]])
    Prob2Serve = InitServerDist[1]*sum(NumGamesDist2[[0,2,4,5]]) + InitServerDist[0]*sum(NumGamesDist2[[1,3,6]])
    InitServerDist = [Prob1Serve, Prob2Serve]
    
    # Set 3:
    [nodes, dist, parents, outcomes, info] = TennisSet(P1S, P2S, P1TB, P2TB, InitServerDist)
    [SetDist3, NumGamesDist3, SetScoreDist3] = beliefpropagation(nodes,dist,parents,outcomes,info,Iterations,Tol,['Set','NumGames','SetScore'])

    if (FirstToSets == 3):
        # Create a new bayesian network:
        # - The parent nodes as the leaf nodes from above
        # - The leaf nodes of this network are our match nodes

        # Compute the match distributions:
        SetDists = [SetDist1, SetDist2, SetDist3]
        SetScoreDists = [SetScoreDist1, SetScoreDist2, SetScoreDist3]
        NumGamesDists = [NumGamesDist1, NumGamesDist2, NumGamesDist3]

        # In case match code fails:
        print('SetDists: ',end='')
        print(SetDists)
        print('SetScoreDists: ',end='')
        print(SetScoreDists)
        print('NumGamesDist: ',end='')
        print(NumGamesDists)

        [nodes, dist, parents, outcomes, info] = TennisMatch1(SetDists, SetScoreDists, NumGamesDists)
        [MatchDist,NumSetsDist,TotalNumGamesDist,AllSetScoresDist] = beliefpropagation(nodes, dist, parents, outcomes, info, Iterations, Tol, 
        ['Match','NumSets','TotalNumGames','AllSetScores'])
        print('Match Distribution: ',end='')
        print(MatchDist)
        print('Number of Sets Distribution: ',end='')
        print(NumSetsDist)
        print('Number of Games Distribution: ',end='')
        print(TotalNumGamesDist)
        print('Set Score Distribution: ',end='')
        print(AllSetScoresDist)

        # Plot the distributions:
        TotalGames = list(range(12,66))
        SetScores = ["6-0","6-1","6-2","6-3","6-4","7-5","7-6","0-6","1-6","2-6","3-6","4-6","5-7","6-7"]
        

                   
    elif (FirstToSets == 5):
        # Compute the initial probability distribution for the first server of the next set from the number of games played in the previous set:
        NumGamesDist3 = np.array(NumGamesDist3)
        Prob1Serve = InitServerDist[0]*sum(NumGamesDist3[[0,2,4,5]]) + InitServerDist[1]*sum(NumGamesDist3[[1,3,6]])
        Prob2Serve = InitServerDist[1]*sum(NumGamesDist3[[0,2,4,5]]) + InitServerDist[0]*sum(NumGamesDist3[[1,3,6]])
        InitServerDist = [Prob1Serve, Prob2Serve]

        # Set 4:
        [nodes, dist, parents, outcomes, info] = TennisSet(P1S, P2S, P1TB, P2TB, InitServerDist)
        [SetDist4, NumGamesDist4, SetScoreDist4] = beliefpropagation(nodes, dist, parents, outcomes, info, Iterations, Tol)

        # Compute the initial probability distribution for the first server of the next set from the number of games played in the previous set:
        NumGamesDist4 = np.array(NumGamesDist4)
        Prob1Serve = InitServerDist[0]*sum(NumGamesDist4[[0,2,4,5]]) + InitServerDist[1]*sum(NumGamesDist4[[1,3,6]])
        Prob2Serve = InitServerDist[1]*sum(NumGamesDist4[[0,2,4,5]]) + InitServerDist[0]*sum(NumGamesDist4[[1,3,6]])
        InitServerDist = [Prob1Serve, Prob2Serve]

        # Set 5:
        [nodes, dist, parents, outcomes, info] = TennisSet(P1S, P2S, P1TB, P2TB, InitServerDist)
        [SetDist5, NumGamesDist5, SetScoreDist5] = beliefpropagation(nodes, dist, parents, outcomes, info, Iterations, Tol)
    else:
        raise ValueError ("First to sets needs to be either 3 or 5")


######################### USER INPUT ENDS HERE ############################

if __name__ == "__main__":
    main()
