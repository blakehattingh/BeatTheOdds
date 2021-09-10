# Import the required functions:
from TennisMatchNetwork1Efficient import TennisMatchNetwork1Efficient
from TennisMatchNetworkCE import TennisMatchNetworkCE
import numpy as np
#from TennisSetNetworkEfficient import TennisSetNetworkEfficient
#from loopybeliefprop import beliefpropagation

def MarkovModelFirstImplementation(P1S, P2S, FirstToSets, FirstToTBPoints, ConditionalEvents= {}, Iterations = 100, Tol = 0.001):
    
    # Set up the Bayesian Network and run the blief propagation algorithm for each set played:
    # Set 1:
    print("Set 1:")
    [nodes, dist, parents, outcomes, info] = TennisSetNetworkEfficient.TennisSetNetworkEfficient(P1S, P2S)
    [SetScoreDist1] = loopybeliefprop.beliefpropagation(nodes,dist,parents,outcomes,info,Iterations,Tol,['SetScore'])

    # Compute the probability distribution of the number of games played in the set:
    NumGamesDist1 = np.zeros(7, dtype = float)
    for i in range(7):
        NumGamesDist1[i] = SetScoreDist1[i] + SetScoreDist1[i+7]
    
    # Construct the initial distribution for the next set, based off the number of games in set 1:
    InitServerDist = [sum(NumGamesDist1[[0,2,4,5]]), sum(NumGamesDist1[[1,3,6]])]

    # Set 2:
    print("Set 2:")
    [nodes, dist, parents, outcomes, info] = TennisSetNetworkEfficient.TennisSetNetworkEfficient(P1S, P2S, InitServerDist)
    [SetScoreDist2] = loopybeliefprop.beliefpropagation(nodes,dist,parents,outcomes,info,Iterations,Tol,['SetScore'])

    # Compute the probability distribution of the number of games played in the set:
    NumGamesDist2 = np.zeros(7, dtype = float)
    for i in range(7):
        NumGamesDist2[i] = SetScoreDist2[i] + SetScoreDist2[i+7]
    
    # Construct the initial distribution for the next set, based off the number of games in set 2 and the initial server:
    P1Serving = (InitServerDist[0]*sum(NumGamesDist2[[0,2,4,5]]) + InitServerDist[1]*sum(NumGamesDist2[[1,3,6]]))
    InitServerDist = [P1Serving, 1. - P1Serving]
    
    # Set 3:
    print("Set 3:")
    [nodes, dist, parents, outcomes, info] = TennisSetNetworkEfficient.TennisSetNetworkEfficient(P1S, P2S, InitServerDist)
    [SetScoreDist3] = loopybeliefprop.beliefpropagation(nodes,dist,parents,outcomes,info,Iterations,Tol,['SetScore'])

    if (FirstToSets == 3):
        # Create a new bayesian network:
        # - The parent nodes as the leaf nodes from above
        # - The leaf nodes of this network are our match nodes

        # Compute the Set Score distributions:
        SetScoreDists = [SetScoreDist1, SetScoreDist2, SetScoreDist3]
        
        # Set up the new network:
        print("Match:")
        [nodes, dist, parents, outcomes, info] = TennisMatchNetworkCE(SetScoreDists, ConditionalEvents)
        [MatchScoreDist,TotalNumGamesDist,AllSetScoresDist] = beliefpropagation(nodes, dist, parents, outcomes, info, 
        Iterations, Tol, ['MatchScore','TotalNumGames','AllSetScores'])

        # Return the leaf node distributions:
        return MatchScoreDist, TotalNumGamesDist, AllSetScoresDist
                 
    elif (FirstToSets == 5):
        # Compute the probability distribution of the number of games played in the set:
        NumGamesDist3 = np.zeros(7, dtype = float)
        for i in range(7):
            NumGamesDist3[i] = SetScoreDist3[i] + SetScoreDist3[i+7]
        
        # Construct the initial distribution for the next set, based off the number of games in set 2 and the initial server:
        P1Serving = (InitServerDist[0]*sum(NumGamesDist3[[0,2,4,5]]) + InitServerDist[1]*sum(NumGamesDist3[[1,3,6]]))
        InitServerDist = [P1Serving, 1. - P1Serving]

        # Set 4:
        print("Set 4:")
        [nodes, dist, parents, outcomes, info] = TennisSetNetworkEfficient.TennisSetNetworkEfficient(P1S, P2S, InitServerDist)
        [SetScoreDist4] = loopybeliefprop.beliefpropagation(nodes, dist, parents, outcomes, info, Iterations, Tol,['SetScore'])

        # Compute the probability distribution of the number of games played in the set:
        NumGamesDist4 = np.zeros(7, dtype = float)
        for i in range(7):
            NumGamesDist4[i] = SetScoreDist4[i] + SetScoreDist4[i+7]
        
        # Construct the initial distribution for the next set, based off the number of games in set 2 and the initial server:
        P1Serving = (InitServerDist[0]*sum(NumGamesDist4[[0,2,4,5]]) + InitServerDist[1]*sum(NumGamesDist4[[1,3,6]]))
        InitServerDist = [P1Serving, 1. - P1Serving]

        # Set 5:
        print("Set 5:")
        [nodes, dist, parents, outcomes, info] = TennisSetNetworkEfficient.TennisSetNetworkEfficient(P1S, P2S, InitServerDist)
        [SetScoreDist5] = loopybeliefprop.beliefpropagation(nodes, dist, parents, outcomes, info, Iterations, Tol,['SetScore'])
        
        # Create a new bayesian network:
        # - The parent nodes as the leaf nodes from above
        # - The leaf nodes of this network are our match nodes

        # Compute the match distributions:
        SetScoreDists = [SetScoreDist1, SetScoreDist2, SetScoreDist3, SetScoreDist4, SetScoreDist5]
        
        # Set up the new network:
        print("Match:")
        [nodes, dist, parents, outcomes, info] = TennisMatchNetwork1Efficient.TennisMatchNetwork1Efficient(SetScoreDists, 5)
        [MatchDist,MatchScoreDist,TotalNumGamesDist,AllSetScoresDist] = loopybeliefprop.beliefpropagation(nodes, dist, parents, outcomes, info, 
        Iterations, Tol, ['Match','MatchScore','TotalNumGames','AllSetScores'])
        
        # Return the leaf node distributions:
        return MatchDist, MatchScoreDist, TotalNumGamesDist, AllSetScoresDist
    else:
        raise ValueError ("First to sets needs to be either 3 or 5")