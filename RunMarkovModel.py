import random
from AdditionalFunctions import ComputeTBProbabilities
from FirstImplementation import MarkovModelFirstImplementation
from SecondImplementation import MarkovModelSecondImplementation

def RunMarkovModel(P1S, P2S, FirstToSets, FirstToTBPoints, Method, Viscosity, Mode = 'Simple'):
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
        [MatchDist, NumSetsDist, TotalNumGamesDist, AllSetScoresDist] = MarkovModelFirstImplementation(P1S, P2S, P1TB, P2TB, 
        FirstToSets, FirstToTBPoints, Viscosity, Iterations, Tol)
        return MatchDist, NumSetsDist, TotalNumGamesDist, AllSetScoresDist

    elif (Method == 2):
        [MatchDist,Set1Dist,Set2Dist,Set3Dist,NumSetsDist,TotalNumGamesDist,AllSetScoresDist] = MarkovModelSecondImplementation(P1S,
            P2S, P1TB, P2TB, FirstToSets, FirstToTBPoints, Viscosity, Iterations, Tol)
        return MatchDist, Set1Dist, Set2Dist, Set3Dist, NumSetsDist, TotalNumGamesDist, AllSetScoresDist


def main():
    P1S = 0.6
    P2S = 0.55
    Approach = 2
    Viscosity = 0.5

    if (Approach == 1):
        '''
        # Run the Markov Model using the first approach:
        [MatchDist, NumSetsDist, TotalNumGamesDist, AllSetScoresDist] = RunMarkovModel(P1S,P2S,5,7,Approach,Viscosity)
        print('Match Distribution: ', end = '')
        print(MatchDist)
        print('Number of Sets Distribution: ', end = '')
        print(NumSetsDist)
        print('Number of Games Distribution: ', end = '')
        print(TotalNumGamesDist)
        print('Set Score Distribution: ', end = '')
        print(AllSetScoresDist)
        '''
        [MatchDist, NumSetsDist, TotalNumGamesDist, AllSetScoresDist] = RunMarkovModel(P1S,P2S,3,7,Approach,Viscosity)
        print('Match Distribution: ', end = '')
        print(MatchDist)
        print('Number of Sets Distribution: ', end = '')
        print(NumSetsDist)
        print('Number of Games Distribution: ', end = '')
        print(TotalNumGamesDist)
        print('Set Score Distribution: ', end = '')
        print(AllSetScoresDist)
        

    else:
        # Run the Markov Model using the second approach:
        [MatchDist, Set1Dist, Set2Dist, Set3Dist, NumSetsDist, TotalNumGamesDist, AllSetScoresDist] = RunMarkovModel(P1S,P2S,5,7,
        Approach,Viscosity)
        print('Match Distribution: ', end = '')
        print(MatchDist)
        print('Set 1 Distribution: ', end = '')
        print(Set1Dist)
        print('Set 2 Distribution: ', end = '')
        print(Set2Dist)
        print('Set 3 Distribution: ', end = '')
        print(Set3Dist)
        print('Number of Sets Distribution: ', end = '')
        print(NumSetsDist)
        print('Number of Games Distribution: ', end = '')
        print(TotalNumGamesDist)
        print('Set Score Distribution: ', end = '')
        print(AllSetScoresDist)

        [MatchDist, Set1Dist, Set2Dist, Set3Dist, NumSetsDist, TotalNumGamesDist, AllSetScoresDist] = RunMarkovModel(P1S,P2S,3,7,
        Approach,Viscosity)
        print('Match Distribution: ', end = '')
        print(MatchDist)
        print('Set 1 Distribution: ', end = '')
        print(Set1Dist)
        print('Set 2 Distribution: ', end = '')
        print(Set2Dist)
        print('Set 3 Distribution: ', end = '')
        print(Set3Dist)
        print('Number of Sets Distribution: ', end = '')
        print(NumSetsDist)
        print('Number of Games Distribution: ', end = '')
        print(TotalNumGamesDist)
        print('Set Score Distribution: ', end = '')
        print(AllSetScoresDist)

if __name__ == "__main__":
    main()







