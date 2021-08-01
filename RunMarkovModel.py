import random
from typing import Match
from AdditionalFunctions import ComputeTBProbabilities
from FirstImplementation import MarkovModelFirstImplementation
from SecondImplementation import MarkovModelSecondImplementation

def RunMarkovModel(P1S, P2S, FirstToSets, FirstToTBPoints, Method, Viscosity, ConditionalEvents):
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
        [MatchDist, MatchScoreDist, TotalNumGamesDist, AllSetScoresDist] = MarkovModelFirstImplementation(P1S, P2S, 
        FirstToSets, FirstToTBPoints, Viscosity, Iterations, Tol)
        return MatchDist, MatchScoreDist, TotalNumGamesDist, AllSetScoresDist

    elif (Method == 2):
        [MatchDist,MatchScoreDist,TotalNumGamesDist,AllSetScoresDist] = MarkovModelSecondImplementation(P1S,
            P2S, FirstToSets, FirstToTBPoints, Viscosity, ConditionalEvents, Iterations, Tol)
        return MatchDist, MatchScoreDist, TotalNumGamesDist, AllSetScoresDist

def main():
    P1S = 0.7
    P2S = 0.6
    Approach = 2
    Viscosity = 0.5
    ConditionalEvents = {'Set1Server': ['P2Serves'], 'Match': [2], 'MatchScore': [3,4]}

    if (Approach == 1):
        # Run the Markov Model using Implementation 1:
        [MatchDist, MatchScoreDist, TotalNumGamesDist, AllSetScoresDist] = RunMarkovModel(P1S,P2S,3,7,Approach,Viscosity)
        print('Match Distribution: ', end = '')
        print(MatchDist)
        print('Match Score Distribution: ', end = '')
        print(MatchScoreDist)
        print('Number of Games Distribution: ', end = '')
        print(TotalNumGamesDist)
        print('Set Score Distribution: ', end = '')
        print(AllSetScoresDist)
        
    else:
        # Run the Markov Model using the second approach:
        [MatchDist,MatchScoreDist,TotalNumGamesDist,AllSetScoresDist] = RunMarkovModel(P1S,P2S,3,7,Approach,Viscosity,
        ConditionalEvents)
        print('Match Distribution: ', end = '')
        print(MatchDist)
        print('Match Score Distribution: ', end = '')
        print(MatchScoreDist)
        print('Number of Games Distribution: ', end = '')
        print(TotalNumGamesDist)
        print('Set Score Distribution: ', end = '')
        print(AllSetScoresDist)

if __name__ == "__main__":
    main()







