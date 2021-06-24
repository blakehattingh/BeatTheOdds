import random
from AdditionalFunctions import TieBreakerProbability
from FirstImplementation import MarkovModelFirstImplementation
from SecondImplementation import MarkovModelSecondImplementation

def RunMarkovModel(P1S, P2S, FirstToSets, FirstToTBPoints, Method, Viscosity, Mode = 'Simple'):
    # This function runs the Markov Model using one of the approaches implemented.

    # Model Parameters:
    # Max Number of Iterations until Steady State reached:
    Iterations = 100
    # Tolerance level on Steady States:
    Tol = 0.0001

    # Compute the tie-breaker probabilities using the simulation:
    random.seed(14)
    [P1TB, P2TB] = [0.31866, 0.68287]# TieBreakerProbability(P1S, P2S, 100000, FirstToTBPoints)
    print(P1TB, P2TB)

    # Run the Markov Model using the method specified by the user:
    if (Method == 1):
        [MatchDist, NumSetsDist, TotalNumGamesDist, AllSetScoresDist] = MarkovModelFirstImplementation(P1S, P2S, P1TB, P2TB, 
        FirstToSets, FirstToTBPoints, Viscosity, Iterations, Tol)
        return MatchDist, NumSetsDist, TotalNumGamesDist, AllSetScoresDist

    elif (Method == 2):
        if (Mode == 'Simple'):
            MatchDist = MarkovModelSecondImplementation(P1S, P2S, P1TB,P2TB,FirstToSets,FirstToTBPoints,Mode,Viscosity,Iterations,Tol)
            return MatchDist

        elif (Mode == 'Complex'):
            [MatchDist,NumSetsDist,TotalNumGamesDist,AllSetScoresDist] = MarkovModelSecondImplementation(P1S, P2S, P1TB, P2TB, 
            FirstToSets, FirstToTBPoints, Mode, Viscosity, Iterations, Tol)
            return MatchDist, NumSetsDist, TotalNumGamesDist, AllSetScoresDist


def main():
    P1S = 0.70
    P2S = 0.80
    Approach = 2
    Viscosity = 0.5

    if (Approach == 1):
        # Run the Markov Model using the first approach:
        [MatchDist, NumSetsDist, TotalNumGamesDist, AllSetScoresDist] = RunMarkovModel(P1S,P2S,3,7,1,Viscosity)
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
        [MatchDist, NumSetsDist, TotalNumGamesDist, AllSetScoresDist] = RunMarkovModel(P1S,P2S,3,7,2,Viscosity,'Complex')
        print('Match Distribution: ', end = '')
        print(MatchDist)
        print('Number of Sets Distribution: ', end = '')
        print(NumSetsDist)
        print('Number of Games Distribution: ', end = '')
        print(TotalNumGamesDist)
        print('Set Score Distribution: ', end = '')
        print(AllSetScoresDist)

if __name__ == "__main__":
    main()







