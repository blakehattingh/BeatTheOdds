# Import the required functions:
from TennisMatchNetwork2Efficient import TennisMatchNetwork2Efficient
from loopybeliefprop import beliefpropagation

def MarkovModelSecondImplementation(P1S,P2S,FirstToSets,FirstToTBPoints,Viscosity,ConditionalEvents,Iterations=100,Tol=0.001):
    # This function utilises the second approach to model a tennis match with a Markov Model.

    # Set up the Bayesain Network:
    [nodes, dist, parents, outcomes, info] = TennisMatchNetwork2Efficient(P1S, P2S, FirstToSets, ConditionalEvents)

    # Run the belief propagation algorithm on this network:
    [MatchDist,MatchScoreDist,TotalNumGamesDist,AllSetScoresDist] = beliefpropagation(nodes,dist,
    parents,outcomes,info,Iterations,Tol,['Match','MatchScore','TotalNumGames','AllSetScores'],
    Viscosity, False)
    return MatchDist,MatchScoreDist,TotalNumGamesDist,AllSetScoresDist
    
