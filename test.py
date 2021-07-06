from itertools import islice
from AdditionalFunctions import TieBreakerProbability
from TennisMatchNetwork1 import TennisMatchNetwork1
from loopybeliefprop import beliefpropagation
import numpy as np
import matplotlib.pyplot as plt
import csv

def nth_index(iterable, value, n):
    matches = (idx for idx, val in enumerate(iterable) if val == value)
    return next(islice(matches, n-1, n), None)


def main():
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
    [nodes, dist, parents, outcomes, info] = TennisMatchNetwork1(SetDists, SetScoreDists, NumGamesDists, 5)
    [MatchDist,NumSetsDist,TotalNumGamesDist,AllSetScoresDist] = beliefpropagation(nodes, dist, parents, outcomes, info, 
    Iterations, Tol, ['Match','NumSets','TotalNumGames','AllSetScores'], Viscosity)


if __name__ == "__main__":
    main()
