# Import the required functions:
from TennisMatchNetwork2 import TennisMatchNetwork2
from loopybeliefprop import beliefpropagation

def MarkovModelSecondImplementation(P1S, P2S, P1TB, P2TB, FirstToSets, FirstToTBPoints, Mode,Viscosity,Iterations=100,Tol=0.001):
    # This function utilises the second approach to model a tennis match with a Markov Model.

    if (Mode == 'Simple'):
        # Set up the Bayesain Network:
        [nodes, dist, parents, outcomes, info] = TennisMatchNetwork2(P1S, P2S, P1TB, P2TB, FirstToSets, Mode)

        # Run the belief propagation algorithm on this network:
        [MatchDist] = beliefpropagation(nodes,dist,parents,outcomes,info,Iterations,Tol,['Match'],Viscosity, True)
        return MatchDist
    else:
        # Set up the Bayesain Network:
        [nodes, dist, parents, outcomes, info] = TennisMatchNetwork2(P1S, P2S, P1TB, P2TB, FirstToSets, Mode)
        print("Doing complex version of second implementation")

        # Run the belief propagation algorithm on this network:
        [MatchDist,Set1Dist,Set2Dist,Set3Dist,NumSetsDist,TotalNumGamesDist,AllSetScoresDist] = beliefpropagation(nodes,dist,
        parents,outcomes,info,Iterations,Tol,['Match','Set1','Set2','Set3','NumSets','TotalNumGames','AllSetScores'],Viscosity, True)
        return MatchDist,Set1Dist,Set2Dist,Set3Dist,NumSetsDist,TotalNumGamesDist,AllSetScoresDist
    
