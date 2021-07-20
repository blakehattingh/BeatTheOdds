from TennisMatchNetwork1Efficient import TennisMatchNetwork1Efficient
from itertools import islice
from AdditionalFunctions import TieBreakerProbability, ComputeTBProbabilities
from TennisMatchNetwork1Efficient import TennisMatchNetwork1Efficient
from loopybeliefprop import beliefpropagation
from OMalleysEqns import TB, Matrices
import numpy as np
import csv

def nth_index(iterable, value, n):
    matches = (idx for idx, val in enumerate(iterable) if val == value)
    return next(islice(matches, n-1, n), None)


def main():
    P = 0.6
    P2S = 0.7
    Q = 1. - P2S 
    [A, B] = Matrices()
    TBServeA = TB(P, Q, A)
    TBServeB = TB(Q, P, A)
    # [P1TB, P2TB] = ComputeTBProbabilities(P, P2S)
    print(TBServeA)
    print(TBServeB)


    '''
    Viscosity = 0.5
    Iterations = 100
    Tol = 0.01
    SetDists = [[0.8,0.2],[0.6,0.4],[0.7,0.3],[0.45,0.55],[0.8,0.2]]
    SetScoreDists = [[0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.,0.,0.,0.],[0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.,0.,0.,0.],
    [0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.,0.,0.,0.],[0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.,0.,0.,0.],[0.1,0.1,0.1,0.1,
    0.1,0.1,0.1,0.1,0.1,0.1,0.,0.,0.,0.]]
    NumGamesDist = [0.] * 7
    for i in range(len(NumGamesDist)):
        NumGamesDist[i] = 1. / len(NumGamesDist)
    NumGamesDists = [NumGamesDist, NumGamesDist, NumGamesDist, NumGamesDist, NumGamesDist]

    # Set up the new network:
    [nodes, dist, parents, outcomes, info] = TennisMatchNetwork1Efficient(SetScoreDists, 5)
    [MatchDist,NumSetsDist,TotalNumGamesDist,AllSetScoresDist] = beliefpropagation(nodes, dist, parents, outcomes, info, 
    Iterations, Tol, ['Match','MatchScore','TotalNumGames','AllSetScores'], Viscosity)
    
    print('Match Distribution: ', end = '')
    print(MatchDist)
    print('Number of Sets Distribution: ', end = '')
    print(NumSetsDist)
    print('Number of Games Distribution: ', end = '')
    print(TotalNumGamesDist)
    print('Set Score Distribution: ', end = '')
    print(AllSetScoresDist)
    '''

if __name__ == "__main__":
    main()
