# Import the required functions:
from TennisMatchNetwork2 import TennisMatchNetwork2
from loopybeliefprop import beliefpropagation

def MarkovModelSecondImplementation(P1S, P2S, P1TB, P2TB, FirstToSets, FirstToTBPoints,Viscosity,Iterations=100,Tol=0.001):
    # This function utilises the second approach to model a tennis match with a Markov Model.

    # Set up the Bayesain Network:
    [nodes, dist, parents, outcomes, info] = TennisMatchNetwork2(P1S, P2S, P1TB, P2TB, FirstToSets)

    # Run the belief propagation algorithm on this network:
    [MatchDist,Set1Dist,Set2Dist,Set3Dist,NumSetsDist,TotalNumGamesDist,AllSetScoresDist] = beliefpropagation(nodes,dist,
    parents,outcomes,info,Iterations,Tol,['Match','Set1','Set2','Set3','NumSets','TotalNumGames','AllSetScores'],Viscosity, True)
    return MatchDist,Set1Dist,Set2Dist,Set3Dist,NumSetsDist,TotalNumGamesDist,AllSetScoresDist
    
