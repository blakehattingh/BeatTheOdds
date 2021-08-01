from TennisMatchNetwork1Efficient import TennisMatchNetwork1Efficient
from itertools import islice
from AdditionalFunctions import RemainingOdds, TieBreakerProbability, ComputeTBProbabilities, OddsComputer, RemainingOdds
from TennisMatchNetwork1Efficient import TennisMatchNetwork1Efficient
from loopybeliefprop import beliefpropagation, choose
from OMalleysEqns import TB, Matrices
from CVaRModel import CVaRModel
import numpy as np
import csv
import matplotlib.pyplot as plt

def nth_index(iterable, value, n):
    matches = (idx for idx, val in enumerate(iterable) if val == value)
    return next(islice(matches, n-1, n), None)


def main():
    Bets = ['AWins', 'BWins', '3-0', '3-1', '3-2', '0-3', '1-3', '2-3']
    Probabilities = [0.04470312, 0.10620195, 0.09589186, 0.10717187, 0.3687957, 0.37723549]
    Z = [[1.80,0,4.5,0,0,0,0,0],[1.80,0,0,3.2,0,0,0,0],[1.80,0,0,0,3.8,0,0,0],
    [0,2.06,0,0,0,12.0,0,0],[0,2.06,0,0,0,0,10.0,0],[0,2.06,0,0,0,0,0,9.0]]
    lam = 0.
    beta = 0.5
    CVaRModel(Probabilities, Z, lam, beta, Bets)

if __name__ == "__main__":
    main()
