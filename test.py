from TennisMatchNetwork1Efficient import TennisMatchNetwork1Efficient
from itertools import islice
from AdditionalFunctions import TieBreakerProbability, ComputeTBProbabilities
from TennisMatchNetwork1Efficient import TennisMatchNetwork1Efficient
from loopybeliefprop import beliefpropagation
from OMalleysEqns import TB, Matrices
import numpy as np
import csv
import matplotlib.pyplot as plt

def nth_index(iterable, value, n):
    matches = (idx for idx, val in enumerate(iterable) if val == value)
    return next(islice(matches, n-1, n), None)


def main():
   


    figGames3S, axesGames3S = plt.subplots(1, 1, figsize = [15, 15])
    figGames3S.suptitle('Probability Distributions for Number of Games (first to 3 sets)')

    axesGames3S.bar(range(1,15,1), [1,2,3,4,5,6,7,8,9,10,11,12,13,14], color = 'tab20c')
    plt.show()

if __name__ == "__main__":
    main()
