from itertools import islice
import os, sys
import numpy as np
import csv
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import time


# Add required folders to the system path:
currentPath = os.path.abspath(os.getcwd())

# Markov Model Files:
sys.path.insert(0, currentPath + '\\BeatTheOdds\\MarkovModel')
from FirstImplementation import *


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

    # run MM:
    start = time.time()
    MarkovModelFirstImplementation(0.62, 0.61, 3)
    end = time.time()
    print('time taken =')
    print(end-start)
    
if __name__ == "__main__":
    main()
