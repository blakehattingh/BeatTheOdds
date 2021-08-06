from TennisMatchNetwork1Efficient import TennisMatchNetwork1Efficient
from TennisSetNetworkEfficient import TennisSetNetworkEfficient
from itertools import islice
from AdditionalFunctions import RemainingOdds, TieBreakerProbability, ComputeTBProbabilities, OddsComputer, RemainingOdds
from loopybeliefprop import beliefpropagation, choose
from OMalleysEqns import TB, Matrices, Match3, Set
from CVaRModel import CVaRModel
from RunMarkovModel import RunMarkovModel
import numpy as np
import csv
import matplotlib.pyplot as plt

def nth_index(iterable, value, n):
    matches = (idx for idx, val in enumerate(iterable) if val == value)
    return next(islice(matches, n-1, n), None)


def main():
    '''
    Bets = ['AWins', 'BWins', '3-0', '3-1', '3-2', '0-3', '1-3', '2-3']
    Probabilities = [0.04470312, 0.10620195, 0.09589186, 0.10717187, 0.3687957, 0.37723549]
    Z = [[1.80,0,4.5,0,0,0,0,0],[1.80,0,0,3.2,0,0,0,0],[1.80,0,0,0,3.8,0,0,0],
    [0,2.06,0,0,0,12.0,0,0],[0,2.06,0,0,0,0,10.0,0],[0,2.06,0,0,0,0,0,9.0]]
    lam = 4.
    beta = 0.2
    CVaRModel(Probabilities, Z, lam, beta, Bets)
    '''

    # Comparing our model and O'Malley's Equations:
    P1S = 0.60
    P2S = 0.55
    Viscosity = 0.5
    '''
    # Implementation 1:
    [MatchDist, MatchScoreDist, TotalNumGamesDist, AllSetScoresDist] = RunMarkovModel(P1S,P2S,3,7,1,Viscosity)
    print('Match Distribution: ', end = '')
    print(MatchDist)
    '''
    # Implementation 2:
    [MatchDist, MatchScoreDist, TotalNumGamesDist, AllSetScoresDist] = RunMarkovModel(P1S,P2S,3,7,2,Viscosity)
    print('Match Distribution: ', end = '')
    print(MatchDist)
    
    '''
    # Run a single set and compare to O'Malley:
    [nodes,dist,parents,outcomes,info] = TennisSetNetworkEfficient(P1S, P2S, InitServerDist = [1., 0.])
    [SetScoreDist1] = beliefpropagation(nodes,dist,parents,outcomes,info,100,0.001,['SetScore'])
    AWins = sum(SetScoreDist1[0:7])
    BWins = sum(SetScoreDist1[7:14])
    print(AWins, BWins)

    TwoNil = AWins * AWins
    TwoOne = AWins * BWins * AWins * 2
    print(TwoOne + TwoNil)
    '''

    # O'Malley's:
    [A, B] = Matrices()
    print(Match3(P1S, 1. - P2S, A, B))

if __name__ == "__main__":
    main()
