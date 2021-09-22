def RunMarkovModel(P1S, P2S, FirstToSets, FirstToTBPoints, Method, Viscosity, ConditionalEvents = {}):
    # This function runs the Markov Model using one of the approaches implemented.

    # Model Parameters:
    # Max Number of Iterations until Steady State reached:
    Iterations = 100
    # Tolerance level on Steady States:
    Tol = 0.001

    # Compute the TB Probabilities:
    [P1TB, P2TB] = ComputeTBProbabilities(P1S, P2S)
    
    # Run the Markov Model using the method specified by the user:
    if (Method == 1):
        [MatchScoreDist, TotalNumGames,AllSetScoresDist] = MarkovModelFirstImplementation(P1S, P2S, 
        FirstToSets, FirstToTBPoints, ConditionalEvents, Iterations, Tol)
        return MatchScoreDist, TotalNumGames, AllSetScoresDist

    elif (Method == 2):
        [MatchDist,MatchScoreDist,TotalNumGamesDist,AllSetScoresDist] = MarkovModelSecondImplementation(P1S,
            P2S, FirstToSets, FirstToTBPoints, Viscosity, ConditionalEvents, Iterations, Tol)
        return MatchDist, MatchScoreDist, TotalNumGamesDist, AllSetScoresDist

def MarkovModelFirstImplementation(P1S, P2S, FirstToSets, ConditionalEvents= {}, Iterations = 100, Tol = 0.001):
    # Set up the Bayesian Network and run the blief propagation algorithm for each set played:
    # Set 1:
    print("Set 1:")
    [nodes, dist, parents, outcomes, info] = TennisSetNetworkEfficient(P1S, P2S)
    [SetScoreDist1] = beliefpropagation(nodes,dist,parents,outcomes,info,Iterations,Tol,['SetScore'])

    # Compute the probability distribution of the number of games played in the set:
    NumGamesDist1 = np.zeros(7, dtype = float)
    for i in range(7):
        NumGamesDist1[i] = SetScoreDist1[i] + SetScoreDist1[i+7]
    
    # Construct the initial distribution for the next set, based off the number of games in set 1:
    InitServerDist = [sum(NumGamesDist1[[0,2,4,5]]), sum(NumGamesDist1[[1,3,6]])]

    # Set 2:
    print("Set 2:")
    [nodes, dist, parents, outcomes, info] = TennisSetNetworkEfficient(P1S, P2S, InitServerDist)
    [SetScoreDist2] = beliefpropagation(nodes,dist,parents,outcomes,info,Iterations,Tol,['SetScore'])

    # Compute the probability distribution of the number of games played in the set:
    NumGamesDist2 = np.zeros(7, dtype = float)
    for i in range(7):
        NumGamesDist2[i] = SetScoreDist2[i] + SetScoreDist2[i+7]
    
    # Construct the initial distribution for the next set, based off the number of games in set 2 and the initial server:
    P1Serving = (InitServerDist[0]*sum(NumGamesDist2[[0,2,4,5]]) + InitServerDist[1]*sum(NumGamesDist2[[1,3,6]]))
    InitServerDist = [P1Serving, 1. - P1Serving]
    
    # Set 3:
    print("Set 3:")
    [nodes, dist, parents, outcomes, info] = TennisSetNetworkEfficient(P1S, P2S, InitServerDist)
    [SetScoreDist3] = beliefpropagation(nodes,dist,parents,outcomes,info,Iterations,Tol,['SetScore'])

    if (FirstToSets == 3):
        # Create a new bayesian network:
        # - The parent nodes as the leaf nodes from above
        # - The leaf nodes of this network are our match nodes

        # Compute the Set Score distributions:
        SetScoreDists = [SetScoreDist1, SetScoreDist2, SetScoreDist3]
        
        # Set up the new network:
        print("Match:")
        [nodes, dist, parents, outcomes, info] = TennisMatchNetworkMostEfficient(SetScoreDists, 3, ConditionalEvents)
        [MatchScoreDist] = beliefpropagation(nodes, dist, parents, outcomes, info, 
        Iterations, Tol, ['MatchScore'])

        print(MatchScoreDist)
        # Return the leaf node distributions:
        return MatchScoreDist
                 
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
        [nodes, dist, parents, outcomes, info] = TennisSetNetworkEfficient(P1S, P2S, InitServerDist)
        [SetScoreDist4] = beliefpropagation(nodes, dist, parents, outcomes, info, Iterations, Tol,['SetScore'])

        # Compute the probability distribution of the number of games played in the set:
        NumGamesDist4 = np.zeros(7, dtype = float)
        for i in range(7):
            NumGamesDist4[i] = SetScoreDist4[i] + SetScoreDist4[i+7]
        
        # Construct the initial distribution for the next set, based off the number of games in set 2 and the initial server:
        P1Serving = (InitServerDist[0]*sum(NumGamesDist4[[0,2,4,5]]) + InitServerDist[1]*sum(NumGamesDist4[[1,3,6]]))
        InitServerDist = [P1Serving, 1. - P1Serving]

        # Set 5:
        print("Set 5:")
        [nodes, dist, parents, outcomes, info] = TennisSetNetworkEfficient(P1S, P2S, InitServerDist)
        [SetScoreDist5] = beliefpropagation(nodes, dist, parents, outcomes, info, Iterations, Tol,['SetScore'])
        
        # Create a new bayesian network:
        # - The parent nodes as the leaf nodes from above
        # - The leaf nodes of this network are our match nodes

        # Compute the match distributions:
        SetScoreDists = [SetScoreDist1, SetScoreDist2, SetScoreDist3, SetScoreDist4, SetScoreDist5]
        
        # Set up the new network:
        print("Match:")
        [nodes, dist, parents, outcomes, info] = TennisMatchNetworkMostEfficient(SetScoreDists, 5)
        MatchScoreDist = beliefpropagation(nodes, dist, parents, outcomes, info, 
        Iterations, Tol, ['MatchScore'])
        
        # Return the leaf node distributions:
        return MatchScoreDist
    else:
        raise ValueError ("First to sets needs to be either 3 or 5")

def MarkovModelSecondImplementation(P1S,P2S,FirstToSets,FirstToTBPoints,Viscosity,ConditionalEvents,Iterations=100,Tol=0.001):
    # This function utilises the second approach to model a tennis match with a Markov Model.

    # Set up the Bayesain Network:
    [nodes, dist, parents, outcomes, info] = TennisMatchNetwork2NoLinks(P1S, P2S, ConditionalEvents)

    # Run the belief propagation algorithm on this network:
    [MatchDist,MatchScoreDist,TotalNumGamesDist,AllSetScoresDist] = beliefpropagation(nodes,dist,
    parents,outcomes,info,Iterations,Tol,['Match','MatchScore','TotalNumGames','AllSetScores'],
    Viscosity, False)
    return MatchDist,MatchScoreDist,TotalNumGamesDist,AllSetScoresDist
    