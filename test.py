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
   

if __name__ == "__main__":
    main()
