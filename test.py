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
   


    figTime, axesTime = plt.subplots(1, 1, figsize = [15, 12])
    figTime.suptitle('Average runtime: algorithm 1 vs algorithm 2')

    avgTimes = [3, 4]

    axesTime.bar(['Alg 1', 'Alg 2'], avgTimes)

    axesTime.set_ylabel('Time Taken')
    axesTime.set_xlabel('Algorithm')
    axesTime.set_title('Comparing runtimes of different algorithms')
    plt.show()

if __name__ == "__main__":
    main()
