# Import the required functions:
import numpy as np
from TennisSetNetwork import TennisSetNetwork
from loopybeliefprop import beliefpropagation
from TennisMatchNetwork1 import TennisMatchNetwork1

def MarkovModelFirstImplementation(P1S, P2S, P1TB, P2TB, FirstToSets, FirstToTBPoints, Viscosity, Iterations = 100, Tol = 0.001):
    
    # Set up the Bayesian Network and run the blief propagation algorithm for each set played:
    # Set 1:
    [nodes, dist, parents, outcomes, info] = TennisSetNetwork(P1S, P2S, P1TB, P2TB)
    [SetDist1, NumGamesDist1, SetScoreDist1] = beliefpropagation(nodes,dist,parents,outcomes,info,Iterations,Tol,
                                                                 ['Set','NumGames','SetScore'], Viscosity)
    # Compute the initial probability distribution for the first server of the next set from the number of games played 
    # in the previous set:
    NumGamesDist1 = np.array(NumGamesDist1)
    InitServerDist = [sum(NumGamesDist1[[0,2,4,5]]), sum(NumGamesDist1[[1,3,6]])]

    # Set 2:
    [nodes, dist, parents, outcomes, info] = TennisSetNetwork(P1S, P2S, P1TB, P2TB, InitServerDist)
    [SetDist2, NumGamesDist2, SetScoreDist2] = beliefpropagation(nodes,dist,parents,outcomes,info,Iterations,Tol,
                                                                 ['Set','NumGames','SetScore'], Viscosity)
    # Compute the initial probability distribution for the first server of the next set from the number of games played 
    # in the previous set:
    NumGamesDist2 = np.array(NumGamesDist2)
    Prob1Serve = InitServerDist[0]*sum(NumGamesDist2[[0,2,4,5]]) + InitServerDist[1]*sum(NumGamesDist2[[1,3,6]])
    Prob2Serve = InitServerDist[1]*sum(NumGamesDist2[[0,2,4,5]]) + InitServerDist[0]*sum(NumGamesDist2[[1,3,6]])
    InitServerDist = [Prob1Serve, Prob2Serve]
    
    # Set 3:
    [nodes, dist, parents, outcomes, info] = TennisSetNetwork(P1S, P2S, P1TB, P2TB, InitServerDist)
    [SetDist3, NumGamesDist3, SetScoreDist3] = beliefpropagation(nodes,dist,parents,outcomes,info,Iterations,Tol,
                                                                 ['Set','NumGames','SetScore'], Viscosity)

    if (FirstToSets == 3):
        # Create a new bayesian network:
        # - The parent nodes as the leaf nodes from above
        # - The leaf nodes of this network are our match nodes

        # Compute the match distributions:
        SetDists = [SetDist1, SetDist2, SetDist3]
        SetScoreDists = [SetScoreDist1, SetScoreDist2, SetScoreDist3]
        NumGamesDists = [NumGamesDist1, NumGamesDist2, NumGamesDist3]
        print(SetDists)
        print(SetScoreDists)
        print(NumGamesDists)
        
        # Set up the new network:
        [nodes, dist, parents, outcomes, info] = TennisMatchNetwork1(SetDists, SetScoreDists, NumGamesDists, 3)
        [MatchDist,NumSetsDist,TotalNumGamesDist,AllSetScoresDist] = beliefpropagation(nodes, dist, parents, outcomes, info, 
        Iterations, Tol, ['Match','NumSets','TotalNumGames','AllSetScores'], Viscosity)
        
        # Return the leaf node distributions:
        return MatchDist, NumSetsDist, TotalNumGamesDist, AllSetScoresDist
                 
    elif (FirstToSets == 5):
        # Compute the initial probability distribution for the first server of the next set from the number of games played 
        # in the previous set:
        NumGamesDist3 = np.array(NumGamesDist3)
        Prob1Serve = InitServerDist[0]*sum(NumGamesDist3[[0,2,4,5]]) + InitServerDist[1]*sum(NumGamesDist3[[1,3,6]])
        Prob2Serve = InitServerDist[1]*sum(NumGamesDist3[[0,2,4,5]]) + InitServerDist[0]*sum(NumGamesDist3[[1,3,6]])
        InitServerDist = [Prob1Serve, Prob2Serve]

        # Set 4:
        [nodes, dist, parents, outcomes, info] = TennisSetNetwork(P1S, P2S, P1TB, P2TB, InitServerDist)
        [SetDist4, NumGamesDist4, SetScoreDist4] = beliefpropagation(nodes, dist, parents, outcomes, info, Iterations, Tol,
                                                                    ['Set','NumGames','SetScore'], Viscosity)

        # Compute the initial probability distribution for the first server of the next set from the number of games played 
        # in the previous set:
        NumGamesDist4 = np.array(NumGamesDist4)
        Prob1Serve = InitServerDist[0]*sum(NumGamesDist4[[0,2,4,5]]) + InitServerDist[1]*sum(NumGamesDist4[[1,3,6]])
        Prob2Serve = InitServerDist[1]*sum(NumGamesDist4[[0,2,4,5]]) + InitServerDist[0]*sum(NumGamesDist4[[1,3,6]])
        InitServerDist = [Prob1Serve, Prob2Serve]

        # Set 5:
        [nodes, dist, parents, outcomes, info] = TennisSetNetwork(P1S, P2S, P1TB, P2TB, InitServerDist)
        [SetDist5, NumGamesDist5, SetScoreDist5] = beliefpropagation(nodes, dist, parents, outcomes, info, Iterations, Tol,
                                                                    ['Set','NumGames','SetScore'], Viscosity)
        
        # Create a new bayesian network:
        # - The parent nodes as the leaf nodes from above
        # - The leaf nodes of this network are our match nodes

        # Compute the match distributions:
        SetDists = [SetDist1, SetDist2, SetDist3, SetDist4, SetDist5]
        SetScoreDists = [SetScoreDist1, SetScoreDist2, SetScoreDist3, SetScoreDist4, SetScoreDist5]
        NumGamesDists = [NumGamesDist1, NumGamesDist2, NumGamesDist3, NumGamesDist4, NumGamesDist5]
        
        # Set up the new network:
        [nodes, dist, parents, outcomes, info] = TennisMatchNetwork1(SetDists, SetScoreDists, NumGamesDists, 5)
        [MatchDist,NumSetsDist,TotalNumGamesDist,AllSetScoresDist] = beliefpropagation(nodes, dist, parents, outcomes, info, 
        Iterations, Tol, ['Match','NumSets','TotalNumGames','AllSetScores'], Viscosity)
        
        # Return the leaf node distributions:
        return MatchDist, NumSetsDist, TotalNumGamesDist, AllSetScoresDist
    else:
        raise ValueError ("First to sets needs to be either 3 or 5")