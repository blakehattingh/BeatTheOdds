from itertools import islice
import os, sys
relativePath = os.path.abspath('')
sys.path.append(relativePath + '\\MarkovModel')
sys.path.append(relativePath + '\\OptimisationModel')
from RunMarkovModel import RunMarkovModel
from TennisMatchNetwork1Efficient import TennisMatchNetwork1Efficient
from TennisSetNetworkEfficient import TennisSetNetworkEfficient
from AdditionalFunctions import RemainingOdds, TieBreakerProbability, ComputeTBProbabilities, OddsComputer, RemainingOdds
from loopybeliefprop import beliefpropagation, choose
from OMalleysEqns import TB, Matrices, Match3, Set
from CVaRModel import CVaRModel
import numpy as np
import csv
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

def nth_index(iterable, value, n):
    matches = (idx for idx, val in enumerate(iterable) if val == value)
    return next(islice(matches, n-1, n), None)

def main():

    # Comparing our model and O'Malley's Equations:
    P1S = 0.60
    P2S = 0.55
    Viscosity = 0.5
    '''
    # Implementation 1:
    [MatchDist, MatchScoreDist, TotalNumGamesDist, AllSetScoresDist] = RunMarkovModel(P1S,P2S,3,7,1,Viscosity)
    print('Match Distribution: ', end = '')
    print(MatchDist)
    
    # Implementation 2:
    [MatchDist, MatchScoreDist, TotalNumGamesDist, AllSetScoresDist] = RunMarkovModel(P1S,P2S,3,7,2,Viscosity)
    print('Match Distribution: ', end = '')
    print(MatchDist)
    '''
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
    #[A, B] = Matrices()
    #print(Set(P1S, 1. - P2S, A, B))

    x = [[2,3,9],[4,5,6]]
    y =[]
    y = y+x[0]
    y = y+x[1]
    print(y)

if __name__ == "__main__":
    main()
